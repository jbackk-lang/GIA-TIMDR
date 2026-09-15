# core/trefoil_ms_bridge.py
"""
trefoil_ms_bridge.py -- implementacja PRE-REJESTROWANEJ (patrz
docs/geometry/PREREG_TREFOIL_MS_BRIDGE.md) syntetycznej kontroli
pozytywnej/negatywnej dla mostu "sygnal 1D (M/S) -> embedding opozniajacy
3D -> torsja Freneta-Serreta -> pojedynczy skalar -> pipeline
anty-numerologiczny".

WAZNE ZASTRZEZENIE A PRIORI (sekcja 1 pre-rejestracji): dwie niezalezne
wczesniejsze proby w tym ekosystemie (core/trefoil_weather_embedding_
validation.py -- realne dane pogodowe; estymator DMD w
GS_Matrix_Helical_Coupling_DRAFT.md sekcja 6) juz zawiodly z tego samego
powodu -- wzmacnianie szumu przez wielokrotne roznicowanie krotkiego
szeregu. Oczekiwanie a priori jest PESYMISTYCZNE, nie optymistyczne.

Nic w tym pliku nie zostalo zmienione PO zobaczeniu wynikow -- wszystkie
wybory (lag, w1/w2, rozmiary okien, siatka szumu, metryka redukcji) sa
przeniesione 1:1 z zamrozonej pre-rejestracji. Odstepstwa/uzupelnienia
decyzji NIE w pelni doprecyzowanych w pre-rejestracji (np. losowa faza w
kontroli negatywnej B) sa oznaczone w kodzie jako takie, zdecydowane
PRZED uruchomieniem, nie po.
"""
from __future__ import annotations

import os
import sys
from typing import Callable, Dict, List, Tuple

import numpy as np

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_THIS_DIR)
_MATH_FORMALISM = os.path.join(_REPO_ROOT, "TIMDR-Math-Formalism")
for _p in (_REPO_ROOT, _MATH_FORMALISM):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from timdr_formalism.pipeline import (  # noqa: E402
    run_controls,
    ControlResult,
    effect_size_label,
)
from core.trefoil_weather_embedding_validation import kappa_tau_time_aware  # noqa: E402

# ---------------------------------------------------------------------
# 3.1-3.3 Embedding + metryka skalarna (zamrozone, sekcja 3 pre-rejestracji)
# ---------------------------------------------------------------------

LAG = 1  # zamrozone -- NIE strojone po wyniku


def metric_fn(signal_1d: np.ndarray, lag: int = LAG) -> float:
    """3.1-3.3: sygnal 1D -> embedding opozniajacy 3D -> kappa_tau_time_aware
    (reuzyta BEZ MODYFIKACJI z core/trefoil_weather_embedding_validation.py,
    wlacznie z jej wewnetrznymi, niekonfigurowalnymi progami speed<1e-9 i
    kappa>1e-4 -- patrz zastrzezenie w towarzyszacym dokumencie wynikow:
    to NIE jest DEFAULT_MIN_SPEED=1e-6 z trefoil_frenet_torsion.py, bo
    kappa_tau_time_aware ma te progi zaszyte na sztywno, nie jako
    parametry) -> max(|tau|) po probkach niezbramkowanych.

    Sygnal normalizowany (x-mean)/std PRZED embeddingiem (amendment
    identyczny jak przy estymatorze ksztaltu helikalnego -- rozne domeny
    maja rozne skale amplitudy)."""
    x = np.asarray(signal_1d, dtype=float)
    std = float(x.std())
    if std < 1e-12:
        return 0.0
    xn = (x - float(x.mean())) / std

    n = len(xn) - 2 * lag
    if n < 4:
        return 0.0

    pts = np.stack([xn[:n], xn[lag:lag + n], xn[2 * lag:2 * lag + n]], axis=1)
    t = np.arange(n, dtype=float)  # indeks probki jako "czas" trajektorii embeddingu

    _kappa, tau = kappa_tau_time_aware(pts, t)
    valid = ~np.isnan(tau)
    if not np.any(valid):
        return 0.0
    # max(|tau|) po probkach niezbramkowanych: gated points maja tau=0.0
    # (nie NaN) wewnatrz kappa_tau_time_aware, wiec max naturalnie je
    # ignoruje o ile istnieje choc jedna niezbramkowana probka -- zgodne
    # z sekcja 3.3 pre-rejestracji bez dodatkowego filtrowania.
    return float(np.max(np.abs(tau[valid])))


# ---------------------------------------------------------------------
# 4-5 Generatory: pozytywny + dwie kontrole negatywne (zamrozone, sekcje 4-5)
# ---------------------------------------------------------------------

W1 = 1.0
W2 = 2.7  # zamrozone, stosunek niewspolmierny do W1


def make_positive_injector(sigma: float) -> Callable[[int, "int | None"], np.ndarray]:
    """4: suma dwoch niewspolmiernych czestotliwosci + szum -- genuine
    nieplanarna trajektoria w embeddingu opozniajacym."""
    def _gen(window_size: int, seed) -> np.ndarray:
        rng = np.random.default_rng(seed)
        t = np.arange(window_size, dtype=float)
        phi = rng.uniform(0, 2 * np.pi)
        x = np.sin(W1 * t) + 0.5 * np.sin(W2 * t + phi)
        if sigma > 0:
            x = x + rng.normal(0.0, sigma, window_size)
        return x
    return _gen


def make_negative_a(sigma: float) -> Callable[[int, "int | None"], np.ndarray]:
    """5A: czysty szum bialy. UWAGA: przy sigma=0.0 daje staly (zerowy)
    sygnal -- zdegenerowany, ale NIE modyfikowany po fakcie; opisany
    wprost w raporcie jako nieinformatywny wiersz siatki, nie ukryty."""
    def _gen(window_size: int, seed) -> np.ndarray:
        rng = np.random.default_rng(seed)
        return rng.normal(0.0, sigma, window_size)
    return _gen


def make_negative_b(sigma: float) -> Callable[[int, "int | None"], np.ndarray]:
    """5B: pojedyncza czestotliwosc (planarna w embeddingu opozniajacym,
    genuine torsja=0 z definicji) + szum -- test SPECYFICZNOSCI, nie
    ogolnego szumu. Losowa faza dodana dla symetrii z kontrola pozytywna
    (decyzja podjeta PRZED uruchomieniem, wypelnia luke niedoprecyzowana
    w sekcji 5 pre-rejestracji -- tam nie bylo jawnie powiedziane, czy
    faza ma byc losowana; robimy to tak samo jak w kontroli pozytywnej,
    zeby jedyna roznica miedzy pozytywna a B byla DRUGA czestotliwosc,
    nie obecnosc/brak losowej fazy)."""
    def _gen(window_size: int, seed) -> np.ndarray:
        rng = np.random.default_rng(seed)
        t = np.arange(window_size, dtype=float)
        phi = rng.uniform(0, 2 * np.pi)
        x = np.sin(W1 * t + phi)
        if sigma > 0:
            x = x + rng.normal(0.0, sigma, window_size)
        return x
    return _gen


# ---------------------------------------------------------------------
# 6-7 Siatka + uruchomienie (zamrozone, sekcje 6-7)
# ---------------------------------------------------------------------

WINDOW_SIZES = (300, 64)  # reżim A (gesty), reżim B (rzadki/realistyczny)
SIGMAS = (0.0, 0.1, 0.3, 0.5, 1.0)
N_WINDOWS = 30
SEED = 0
ALPHA = 0.05


def run_grid() -> List[Dict]:
    rows: List[Dict] = []
    for window_size in WINDOW_SIZES:
        for sigma in SIGMAS:
            result: ControlResult = run_controls(
                metric_fn=metric_fn,
                positive_injector=make_positive_injector(sigma),
                negative_generator_a=make_negative_a(sigma),
                negative_generator_b=make_negative_b(sigma),
                n_windows=N_WINDOWS,
                window_size=window_size,
                seed=SEED,
                alpha=ALPHA,
            )
            degenerate = sigma == 0.0  # neg_a stala zerowa przy sigma=0
            rows.append({
                "window_size": window_size,
                "sigma": sigma,
                "degenerate_neg_a": degenerate,
                "passed": result.passed,
                "reason": result.reason,
                "pos_p": result.positive.pvalue,
                "pos_r": result.positive.effect_size_r,
                "pos_r_label": effect_size_label(result.positive.effect_size_r),
                "pos_median_test": result.positive.median_test,
                "pos_median_bg": result.positive.median_background,
                "neg_p": result.negative.pvalue,
                "neg_r": result.negative.effect_size_r,
                "neg_median_a": result.negative.median_test,
                "neg_median_b": result.negative.median_background,
            })
    return rows


def format_report(rows: List[Dict]) -> str:
    lines = []
    lines.append(
        f"{'okno':>5} {'sigma':>6} {'passed':>7} {'pos_p':>10} {'pos_r':>8} "
        f"{'pos_r_lbl':>10} {'neg_p':>10} {'neg_r':>8} {'degen':>6}"
    )
    for r in rows:
        lines.append(
            f"{r['window_size']:>5} {r['sigma']:>6.2f} {str(r['passed']):>7} "
            f"{r['pos_p']:>10.4g} {r['pos_r']:>8.3f} {r['pos_r_label']:>10} "
            f"{r['neg_p']:>10.4g} {r['neg_r']:>8.3f} "
            f"{'TAK' if r['degenerate_neg_a'] else '':>6}"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    rows = run_grid()
    print(format_report(rows))
    n_pass = sum(1 for r in rows if r["passed"])
    print(f"\nPRZESZLO: {n_pass}/{len(rows)} komorek siatki "
          f"({len(WINDOW_SIZES)} okna x {len(SIGMAS)} poziomow szumu).")
