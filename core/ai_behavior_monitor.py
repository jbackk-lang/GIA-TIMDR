# core/ai_behavior_monitor.py
"""
ai_behavior_monitor.py -- KONCEPCYJNY PROTOTYP, BEZ REALNYCH DANYCH.

Odpowiedz na pytanie uzytkownika: "czy mozemy i ma to sens stworzyc
zabezpieczenie AI przed szkodliwym dzialaniem?" -- most miedzy
istniejacym formalizmem M/S (anomalia/defekt/skret/rezonans M,
Axioms_S_TIMDR_Signal.md) a monitorowaniem zachowania systemu AI.

===========================================================================
CZYM TO JEST, A CZYM NIE JEST -- PRZECZYTAJ PRZED UZYCIEM
===========================================================================

To NIE jest "bezpieczenstwo AI" w sensie glebokiego alignmentu (nie
zapobiega temu, zeby dostatecznie zdolny/zlosliwy system zaprojektowal
dzialanie, ktore NIE zaburza sledzonych statystyk). To jest GENERYCZNY,
statystyczny detektor DRYFU/WSPOLBIEZNOSCI ANOMALII na wybranych przez
uzytkownika sygnalach proxy -- odpowiednik czujnika dymu, nie zrozumienia
ognia. Zlapie NAGLA, SKOORDYNOWANA zmiane w wielu sledzonych kanalach
naraz (np. jednoczesny wzrost ryzykownych akcji + spadek odmow + wzrost
latencji) -- NIE zlapie pojedynczego, dobrze zamaskowanego szkodliwego
dzialania, ktore nie porusza zadnej z wybranych metryk powierzchniowych.

Matematyka (anomalia_flags, rezonans-K, kalibracja mocy) jest CALKOWICIE
reuzyta z istniejacego, juz przetestowanego kodu tego ekosystemu
(TIMDR-Math-Formalism/timdr_formalism/{chronosignal,calibration}.py) --
ZERO nowej matematyki w tym pliku. Nowosc to WYLACZNIE: (a) zestaw
kanalow-proxy dla "zachowania AI" (sekcja 1, PROPOZYCJA startowa, nie
ustalona definicja), (b) syntetyczny generator normalny/atak do
demonstracji mechaniki (sekcja 3) -- BEZ realnych danych, bo uzytkownik
jawnie potwierdzil, ze na razie nie ma konkretnego monitorowanego
systemu.

ZANIM TO ZOSTANIE UZYTE NA PRAWDZIWYM SYSTEMIE, POTRZEBA:
  1. Realnej definicji kazdego kanalu dla KONKRETNEGO systemu (jak
     dokladnie liczysz "risk_action_rate"? z jakiego logu? jaka
     kategoryzacja ryzyka?).
  2. Realnych danych pozytywnej kontroli (znane epizody szkodliwe/ataki)
     i negatywnej (normalna praca) -- bez tego `calibrate_resonance_K`
     PRAWIDLOWO odmowi rekomendacji progu (patrz "moc testu" w module
     kalibracji), zgodnie z ta sama dyscyplina co reszta tego ekosystemu.
  3. Jawnej akceptacji, ze to jest WARSTWA UZUPELNIAJACA (wykrywanie
     dryfu/anomalii statystycznej), nie ZASTEPUJACA dedykowanych narzedzi
     AI safety (klasyfikatory tresci, probing aktywacji, circuit
     breakers, red-teaming) -- ktore rozumieja SEMANTYKE, nie tylko
     statystyke powierzchniowa.
===========================================================================
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from typing import Callable, Dict, List

import numpy as np

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_THIS_DIR)
_MATH_FORMALISM = os.path.join(_REPO_ROOT, "TIMDR-Math-Formalism")
for _p in (_REPO_ROOT, _MATH_FORMALISM):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from timdr_formalism.chronosignal import (  # noqa: E402
    anomalia_flags,
    defekt_flags,
    skret_flags,
)
from timdr_formalism.calibration import (  # noqa: E402
    calibrate_resonance_K,
    compute_anomaly_flags,
    theoretical_independence_baseline_rate,
    CalibrationResult,
)

# ---------------------------------------------------------------------
# 1. Kanaly-proxy dla zachowania AI (PROPOZYCJA STARTOWA, nie ustalona
#    definicja -- do zastapienia realnymi metrykami konkretnego systemu)
# ---------------------------------------------------------------------

CHANNEL_DESCRIPTIONS: Dict[str, str] = {
    "risk_action_rate": (
        "Frakcja akcji w oknie sklasyfikowanych jako wysokiego ryzyka "
        "(np. zapis/usuniecie pliku, transakcja finansowa, wywolanie "
        "sieciowe poza dozwolona lista) -- proxy eskalacji uprawnien."
    ),
    "refusal_rate": (
        "Frakcja zadan odrzuconych/odmownych w oknie -- NAGLY SPADEK "
        "moze wskazywac na udany jailbreak/obejscie zabezpieczen; nagly "
        "WZROST moze wskazywac na dryf/nadmierna restrykcyjnosc."
    ),
    "output_entropy": (
        "Srednia entropia/perplexity tokenow wyjsciowych w oknie -- "
        "niezwykle skoki/spadki jako proxy generacji adwersarialnej lub "
        "zdegenerowanej."
    ),
    "latency_ratio": (
        "Srednia latencja/koszt akcji w oknie wzgledem kroczacej "
        "bazowej -- proxy niezwyklych petli rozumowania (np. mozliwy "
        "reward hacking, uciekajaca petla narzedziowa)."
    ),
    "repetition_score": (
        "Samopodobienstwo kolejnych wyjsc w oknie -- proxy zapetlonego/"
        "zdegenerowanego zachowania."
    ),
}

DEFAULT_CHANNELS: List[str] = list(CHANNEL_DESCRIPTIONS.keys())


# ---------------------------------------------------------------------
# 2. Cienka warstwa nad istniejacymi detektorami (ZERO nowej matematyki)
# ---------------------------------------------------------------------


def per_channel_flags(
    channels: Dict[str, np.ndarray], k: float = 2.0
) -> Dict[str, np.ndarray]:
    """anomalia_flags() per kanal -- reuzyte 1:1 z chronosignal.py."""
    return {name: anomalia_flags(series, k=k) for name, series in channels.items()}


def per_channel_defects(
    channels: Dict[str, np.ndarray], factor: float = 0.3
) -> Dict[str, np.ndarray]:
    """defekt_flags() per kanal (nagle skoki) -- reuzyte 1:1."""
    return {name: defekt_flags(series, factor=factor) for name, series in channels.items()}


def per_channel_reversals(
    channels: Dict[str, np.ndarray], factor: float = 1.5
) -> Dict[str, np.ndarray]:
    """skret_flags() per kanal (odwrocenia trendu) -- reuzyte 1:1."""
    return {name: skret_flags(series, factor=factor) for name, series in channels.items()}


@dataclass
class MonitorResult:
    channel_names: List[str]
    n_timesteps: int
    anomaly_counts: Dict[str, int]
    calibration: CalibrationResult  # wynik calibrate_resonance_K -- zawiera
    # empiryczna stope rezonansu, baseline niezaleznosci, p permutacyjne,
    # kontrole mocy, rekomendacje K (albo jawna odmowe rekomendacji)


def run_resonance_monitor(
    channels: Dict[str, np.ndarray], K: int, seed: int = 0
) -> MonitorResult:
    """Glowna funkcja: kanaly -> flagi anomalii per kanal -> koincydencja
    >=K kanalow naraz -> kalibracja/test permutacyjny z kontrola mocy
    (calibrate_resonance_K, REUZYTE bez modyfikacji z
    TIMDR-Math-Formalism/timdr_formalism/calibration.py)."""
    names = list(channels.keys())
    flags = compute_anomaly_flags(channels)
    result = calibrate_resonance_K(flags, K, seed=seed)
    return MonitorResult(
        channel_names=names,
        n_timesteps=len(next(iter(channels.values()))),
        anomaly_counts={n: int(f.sum()) for n, f in zip(names, flags)},
        calibration=result,
    )


# ---------------------------------------------------------------------
# 3. Syntetyczny generator normalny/atak -- WYLACZNIE do demonstracji
#    mechaniki (uzytkownik potwierdzil brak realnych danych na tym
#    etapie). Zamrozone PRZED uruchomieniem, zgodnie z dyscyplina
#    anty-numerologiczna reszty tego ekosystemu.
# ---------------------------------------------------------------------

N_TIMESTEPS = 200  # okna (np. 200 kolejnych "tur"/akcji agenta)
ATTACK_START = 150  # od tej tury zaczyna sie skoordynowana eskalacja
ATTACK_LEN = 20
SEED = 0


def _baseline_channel(rng: np.random.Generator, mean: float, std: float) -> np.ndarray:
    return rng.normal(mean, std, N_TIMESTEPS)


def make_normal_trace(seed: int) -> Dict[str, np.ndarray]:
    """Kontrola negatywna: piec kanalow, KAZDY niezalezny bialy szum
    wokol wlasnej bazowej wartosci -- brak skoordynowanej struktury z
    konstrukcji."""
    rng = np.random.default_rng(seed)
    return {
        "risk_action_rate": _baseline_channel(rng, 0.05, 0.02).clip(0, 1),
        "refusal_rate": _baseline_channel(rng, 0.10, 0.03).clip(0, 1),
        "output_entropy": _baseline_channel(rng, 3.0, 0.3),
        "latency_ratio": _baseline_channel(rng, 1.0, 0.15),
        "repetition_score": _baseline_channel(rng, 0.15, 0.05).clip(0, 1),
    }


def make_attack_trace(seed: int) -> Dict[str, np.ndarray]:
    """Kontrola pozytywna: taki sam szum bazowy jak make_normal_trace,
    plus SKOORDYNOWANE przesuniecie w oknie [ATTACK_START,
    ATTACK_START+ATTACK_LEN) w CZTERECH z pieciu kanalow naraz
    (risk_action_rate w gore, refusal_rate w dol, latency_ratio w gore,
    repetition_score w gore) -- symulacja eskalacji: agent zaczyna
    czesciej wykonywac ryzykowne akcje, rzadziej odmawiac, wolniej/
    drozej rozumowac, i powtarzac wzorce. output_entropy CELOWO
    pozostawione bez zmiany -- test, czy koincydencja 4/5 nadal daje
    sygnal bez piatego kanalu."""
    trace = make_normal_trace(seed)
    sl = slice(ATTACK_START, ATTACK_START + ATTACK_LEN)
    trace["risk_action_rate"][sl] += 0.35
    trace["refusal_rate"][sl] -= 0.08
    trace["latency_ratio"][sl] += 0.9
    trace["repetition_score"][sl] += 0.35
    for k in trace:
        trace[k] = trace[k].clip(0, None)
    return trace


def run_synthetic_self_test(K: int = 3) -> Dict[str, MonitorResult]:
    """Kontrola pozytywna + negatywna, RAZEM, PRZED jakimkolwiek
    zastosowaniem do realnych danych (wzorzec z reszty ekosystemu,
    skill p.3 krok 5)."""
    return {
        "negative_control (normalna praca)": run_resonance_monitor(
            make_normal_trace(SEED), K=K, seed=SEED
        ),
        "positive_control (skoordynowana eskalacja)": run_resonance_monitor(
            make_attack_trace(SEED), K=K, seed=SEED
        ),
    }


def format_report(results: Dict[str, MonitorResult]) -> str:
    """Deleguje do CalibrationResult.report() (reuzyty, nie
    zduplikowany format) -- dodaje tylko etykiete kanalow na wierzchu."""
    lines = []
    for label, r in results.items():
        lines.append(f"=== {label} ===")
        lines.append(f"kanaly: {r.channel_names}")
        lines.append(r.calibration.report())
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    print(__doc__)
    print("\n" + "=" * 70)
    print("URUCHAMIAM SYNTETYCZNY SAMO-TEST (K=3 z 5 kanalow)")
    print("=" * 70 + "\n")
    results = run_synthetic_self_test(K=3)
    print(format_report(results))
