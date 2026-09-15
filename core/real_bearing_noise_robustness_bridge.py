# core/real_bearing_noise_robustness_bridge.py
"""
real_bearing_noise_robustness_bridge.py -- test odpornosci piatki metryk
M/S<->topologia/K (torsja, winding, crossing, homologia perzystentna,
winding fazy OAM) zbudowanych 2026-09-15, na propozycje uzytkownika:
"jesli znamy dobre dane to mozna zaszumic nimi i obserwowac czy sie
dubluja czy cos innego".

KOLEJNOSC DOKUMENTACJI (jawnie odwrocona na wyrazna prosbe uzytkownika,
2026-09-15): normalnie ten ekosystem pisze PREREG_*.md PRZED implementacja
i uruchomieniem (patrz wszystkie poprzednie mosty w tym repo). Tym razem
uzytkownik poprosil wprost: "zrobmy odwrotnie przygotujemy na koniec
zbuduj teraz". SUBSTANCJA dyscypliny anty-numerologicznej jest mimo to
zachowana: wszystkie parametry ponizej (WINDOW_SIZES, SIGMAS, wybor
plikow, definicja generatorow, N_WINDOWS, SEED, ALPHA) sa zamrozone W TYM
PLIKU PRZED jego uruchomieniem, jednym commitem razem z wynikiem -- zaden
parametr nie zostal zmieniony PO zobaczeniu wyniku. Towarzyszacy
PREREG_REAL_BEARING_NOISE_ROBUSTNESS.md, napisany PO fakcie (na wyrazna
prosbe uzytkownika co do kolejnosci), opisuje dokladnie to, co ponizej
zostalo zamrozone -- nie zaden inny, "wygladzony po fakcie" wariant.

RDZEN POMYSLU: piec poprzednich mostow (PREREG_TREFOIL_*, PREREG_WINDING_
CROSSING_*, PREREG_PERSISTENT_HOMOLOGY_*, PREREG_PHASE_WINDING_OAM_*)
testowalo WYLACZNIE na SYNTETYCZNYM sygnale (dwie niewspolmierne
czestotliwosci + szum). Ten most zamienia SYNTETYCZNA kontrole pozytywna
na REALNE dane -- prawdziwe nagrania przyspieszeniomierza lozysk CWRU
(znany, oznakowany defekt vs znany, oznakowany stan zdrowy), z syntetycznym
szumem DODANYM NA WIERZCH realnego sygnalu, rosnaca moca. Pytanie
uzytkownika "czy sie dubluja" operacjonalizowane jako: przy jakim poziomie
szumu (jesli w ogole) traci sie zdolnosc odroznienia realnego defektu od
realnego stanu zdrowego -- i czy krzywa degradacji przypomina te z
syntetycznej serii (nagle zalamanie przy niskim sigma) czy jest inna
(np. stopniowa, albo defekt trzyma sie dluzej niz syntetyczny sygnal).

ZRODLO DANYCH: TIMDR-Industrial-Predict/data/cwru_bearing/*.csv -- realne
nagrania Case Western Reserve University bearing dataset, kazdy plik to
1536 probek przyspieszenia (jeden wiersz, bez naglowka), predkosc obrotowa
1797 RPM, uszkodzenie 0.021" (srednica):
  - normal_1797_de_first1536.csv  -- lozysko zdrowe (KLASA NEGATYWNA)
  - ir_0021_1797_de_first1536.csv -- defekt biezni wewnetrznej
  - or6_0021_1797_de_first1536.csv -- defekt biezni zewnetrznej
  - b_0021_1797_de_first1536.csv  -- defekt kulki
(trzy pliki defektu = trzy niezalezne uruchomienia mostu, kazde zdrowe
vs jeden typ defektu, nie mieszane).
"""
from __future__ import annotations

import os
import sys
import time
from typing import Callable, Dict, List

import numpy as np

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_THIS_DIR)
_MATH_FORMALISM = os.path.join(_REPO_ROOT, "TIMDR-Math-Formalism")
_DATA_DIR = os.path.join(
    os.path.dirname(_REPO_ROOT), "TIMDR-Industrial-Predict", "data", "cwru_bearing"
)
for _p in (_REPO_ROOT, _MATH_FORMALISM):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from timdr_formalism.pipeline import (  # noqa: E402
    run_controls,
    ControlResult,
    effect_size_label,
)

from core.trefoil_ms_bridge import metric_fn as torsion_metric  # noqa: E402
from core.winding_crossing_ms_bridge import (  # noqa: E402
    winding_metric_fn,
    crossing_metric_fn,
)
from core.persistent_homology_ms_bridge import h1_total_persistence_fn  # noqa: E402
from core.phase_winding_oam_ms_bridge import phase_winding_fn  # noqa: E402

METRICS: Dict[str, Callable[[np.ndarray], float]] = {
    "torsion_max|tau|": torsion_metric,
    "winding_number": winding_metric_fn,
    "crossing_number": crossing_metric_fn,
    "h1_persistence": h1_total_persistence_fn,
    "phase_winding": phase_winding_fn,
}

# ---------------------------------------------------------------------
# 1. Wczytanie realnych danych (zamrozone -- te 4 pliki, nic innego)
# ---------------------------------------------------------------------

NORMAL_FILE = "normal_1797_de_first1536.csv"
DEFECT_FILES = {
    "ir_0021": "ir_0021_1797_de_first1536.csv",
    "or6_0021": "or6_0021_1797_de_first1536.csv",
    "b_0021": "b_0021_1797_de_first1536.csv",
}


def _load_row_csv(path: str) -> np.ndarray:
    with open(path, "r") as f:
        line = f.read().strip()
    return np.array([float(v) for v in line.split(",") if v != ""], dtype=float)


def load_real_signals() -> Dict[str, np.ndarray]:
    out = {"normal": _load_row_csv(os.path.join(_DATA_DIR, NORMAL_FILE))}
    for name, fname in DEFECT_FILES.items():
        out[name] = _load_row_csv(os.path.join(_DATA_DIR, fname))
    return out


# ---------------------------------------------------------------------
# 2. Generatory: okno realnego sygnalu (niezachodzace segmenty) + szum
#    addytywny skalowany do odchylenia standardowego TEGO okna (zamrozone)
# ---------------------------------------------------------------------


def make_real_window_injector(
    real_signal: np.ndarray, sigma_frac: float, window_size: int
) -> Callable[[int, "int | None"], np.ndarray]:
    """Zwraca generator(window_size, seed) -- window_size ignorowany
    (musi zgadzac sie z zamknieciem `window_size` powyzej, taka sama
    konwencja podpisu jak w make_positive_injector innych mostow, zeby
    pasowal do run_controls bez zmian w pipeline). Segment wybierany
    deterministycznie z `seed` (modulo liczba dostepnych niezachodzacych
    segmentow), szum gaussowski o odchyleniu `sigma_frac * std(segment)`
    dodany PO wyborze segmentu, wlasnym rng zaseedowanym tym samym
    `seed` -- wiec ten sam seed zawsze daje ten sam segment + ten sam
    szum (odtwarzalnosc), rozne seedy daja rozne (segment, szum).
    Przy sigma_frac=0.0 zwraca CZYSTY realny segment bez modyfikacji --
    W ODROZNIENIU od poprzednich mostow (gdzie sigma=0 bylo zdegenerowane
    dla kontroli negatywnej = czysty szum = stala zerowa), tu sigma=0 jest
    NAJCZYSTSZYM, najbardziej informacyjnym wierszem siatki: to pytanie
    "czy metryka w ogole odroznia realny defekt od realnego zdrowia BEZ
    zadnego dodatkowego szumu" -- zaznaczone wprost w raporcie, nie
    oznaczone jako degenerate."""
    n_avail = len(real_signal) // window_size
    if n_avail < 1:
        raise ValueError(
            f"window_size={window_size} > dlugosc sygnalu={len(real_signal)}"
        )
    segments = [
        real_signal[i * window_size : (i + 1) * window_size] for i in range(n_avail)
    ]

    def _gen(_window_size_ignored: int, seed) -> np.ndarray:
        s = int(seed) if seed is not None else 0
        idx = s % n_avail
        seg = segments[idx].copy()
        if sigma_frac > 0:
            rng = np.random.default_rng(s)
            noise_std = sigma_frac * float(seg.std())
            seg = seg + rng.normal(0.0, noise_std, window_size)
        return seg

    return _gen


# ---------------------------------------------------------------------
# 3. Siatka (zamrozona)
# ---------------------------------------------------------------------

WINDOW_SIZES = (32, 64)  # 1536/32=48 segmentow (> N_WINDOWS=30, brak potrzeby
# reuzycia), 1536/64=24 segmentow (< 30, reuzycie z roznym szumem
# nieuniknione i jawnie odnotowane w wynikach)
SIGMAS = (0.0, 0.1, 0.3, 0.5, 1.0)  # ulamek wlasnego std okna, identyczna
# siatka nominalna co w poprzednich pieciu mostach dla porownywalnosci
N_WINDOWS = 30
SEED = 0
ALPHA = 0.05


def run_grid_for_defect(
    real_signals: Dict[str, np.ndarray], defect_name: str
) -> List[Dict]:
    normal_sig = real_signals["normal"]
    defect_sig = real_signals[defect_name]
    rows: List[Dict] = []
    for window_size in WINDOW_SIZES:
        n_avail_normal = len(normal_sig) // window_size
        n_avail_defect = len(defect_sig) // window_size
        for sigma in SIGMAS:
            for metric_name, metric in METRICS.items():
                result: ControlResult = run_controls(
                    metric_fn=metric,
                    positive_injector=make_real_window_injector(
                        defect_sig, sigma, window_size
                    ),
                    negative_generator_a=make_real_window_injector(
                        normal_sig, sigma, window_size
                    ),
                    negative_generator_b=make_real_window_injector(
                        normal_sig, sigma, window_size
                    ),
                    n_windows=N_WINDOWS,
                    window_size=window_size,
                    seed=SEED,
                    alpha=ALPHA,
                )
                rows.append({
                    "defect": defect_name,
                    "metric": metric_name,
                    "window_size": window_size,
                    "sigma": sigma,
                    "n_avail_normal": n_avail_normal,
                    "n_avail_defect": n_avail_defect,
                    "reuse_needed": N_WINDOWS > min(n_avail_normal, n_avail_defect),
                    "passed": result.passed,
                    "reason": result.reason,
                    "pos_p": result.positive.pvalue,
                    "pos_r": result.positive.effect_size_r,
                    "pos_r_label": effect_size_label(result.positive.effect_size_r),
                    "neg_p": result.negative.pvalue,
                    "neg_r": result.negative.effect_size_r,
                })
    return rows


def format_report(rows: List[Dict]) -> str:
    lines = []
    lines.append(
        f"{'defekt':>9} {'metryka':>18} {'okno':>5} {'sigma':>6} {'passed':>7} "
        f"{'pos_p':>10} {'pos_r':>8} {'pos_r_lbl':>10} {'neg_p':>10} {'neg_r':>8} {'reuse':>6}"
    )
    for r in rows:
        lines.append(
            f"{r['defect']:>9} {r['metric']:>18} {r['window_size']:>5} "
            f"{r['sigma']:>6.2f} {str(r['passed']):>7} {r['pos_p']:>10.4g} "
            f"{r['pos_r']:>8.3f} {r['pos_r_label']:>10} {r['neg_p']:>10.4g} "
            f"{r['neg_r']:>8.3f} {('TAK' if r['reuse_needed'] else ''):>6}"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    t0 = time.time()
    signals = load_real_signals()
    all_rows: List[Dict] = []
    for defect_name in DEFECT_FILES:
        all_rows.extend(run_grid_for_defect(signals, defect_name))
    dt = time.time() - t0

    print(format_report(all_rows))
    n_pass = sum(1 for r in all_rows if r["passed"])
    print(
        f"\nPRZESZLO: {n_pass}/{len(all_rows)} komorek siatki "
        f"({len(DEFECT_FILES)} defekty x {len(METRICS)} metryk x "
        f"{len(WINDOW_SIZES)} okna x {len(SIGMAS)} poziomow szumu). "
        f"Czas: {dt:.1f}s"
    )
