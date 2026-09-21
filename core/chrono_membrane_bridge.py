# core/chrono_membrane_bridge.py
"""
chrono_membrane_bridge.py -- implementacja PRE-REJESTROWANEJ (patrz
docs/geometry/PREREG_CHRONO_MEMBRANE_BEARING_v0.1.md) konstrukcji
"chrono_membrane_bridge": czwarta iteracja tego samego watku badawczego
(po chrono_cone_ratio v0.1, chrono_pendulum_ratio/net_turn v0.2,
chrono_centrifugal_ratio v0.3 -- core/chrono_cone_bridge{,_v2,_v3}.py),
ale ISTOTNA zmiana kierunku, NIE v0.4 tej samej konstrukcji.

RDZEN POMYSLU: v0.1-v0.3 probowaly zbudowac obiekt galezi G z JEDNEGO
sygnalu skalarnego, embedowanego sztucznie w 2D/3D -- rodzina
trajektorii Chronoprocesu Gamma:TxI->R^3 (docs/theory/
TIMDR_Chronoprocess.md SS3) byla we wszystkich trzech JAWNIE
jednoelementowa {gamma}, czyli nie byla prawdziwa rodzina wcale. Tu `s`
(indeks rodziny) indeksuje KANAL (DE/FE/BA lozyska CWRU, jednoczesnie
dostepne w tym samym pliku NPZ), `t` indeksuje probke czasu -- to jest
PRAWDZIWA rodzina {gamma_s}_{s in I}, I = zbior kanalow.

Dla przesuwnego okna: macierz korelacji Pearsona N x N (N = liczba
jednoczesnie dostepnych kanalow) miedzy kanalami WEWNATRZ okna, widmo
tej macierzy (eigvalsh, rzeczywiste i nieujemne z konstrukcji -- macierz
korelacji jest symetryczna PSD). To jest "membrana" tej sesji -- jej
ksztalt (widmo) to "kotara": rozpieta (widmo rownomierne) vs zapadnieta
w jeden kierunek (jeden dominujacy lambda_1).

Metryki (PREREG SS4): `spectral_concentration` = lambda_1/sum(lambda),
`participation_ratio` = (sum lambda)^2 / sum(lambda^2) (standardowa
miara z fizyki/statystyki, IPR odwrocone), `membrane_spectral_ratio` =
koncentracja na koncu okna / koncentracja na poczatku okna (brzeg/brzeg,
analogicznie do chrono_cone_ratio, ale na widmie, nie na promieniu
jednego kanalu).

Nic w tym pliku nie zostalo zmienione PO zobaczeniu wynikow kontroli
syntetycznych ani realnych danych -- wszystkie stale sa przeniesione 1:1
z zamrozonej pre-rejestracji.
"""
from __future__ import annotations

import os
import sys
import time
from typing import Callable, Dict, List, Optional, Sequence

import numpy as np

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_THIS_DIR)
_MATH_FORMALISM = os.path.join(_REPO_ROOT, "TIMDR-Math-Formalism")
for _p in (_REPO_ROOT, _MATH_FORMALISM):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from timdr_formalism.pipeline import (  # noqa: E402
    mann_whitney_test,
    effect_size_label,
    TestResult,
)

# ---------------------------------------------------------------------
# Stale zamrozone w PREREG SS3-6
# ---------------------------------------------------------------------

EDGE_FRACTION = 0.2          # SS4.3 -- ten sam wzorzec co cala rodzina v0.1-v0.3
OMEGA_SHARED = 2 * np.pi / 15.0  # SS5 -- okres wspoldzielonego skladnika kontroli syntetycznych

# ---------------------------------------------------------------------
# SS3. Macierz korelacji i widmo
# ---------------------------------------------------------------------


def channel_correlation_matrix(channels: Sequence[np.ndarray]) -> np.ndarray:
    """C(t) = corrcoef(x_1, ..., x_N) -- N x N, symetryczna, C_ii=1.
    PREREG SS3.1 -- korelacja (Pearson), NIE kowariancja (uzasadnienie:
    kanaly DE/FE/BA maja rozne bezwzgledne skale/czulosci, kowariancja
    bylaby zdominowana przez kanal o najwiekszej wariancji niezaleznie
    od struktury sprzezenia)."""
    stack = np.stack([np.asarray(c, dtype=float) for c in channels], axis=0)
    return np.corrcoef(stack)


def spectrum_from_correlation(C: np.ndarray) -> np.ndarray:
    """lambda_1 >= ... >= lambda_N >= 0 -- eigvalsh (dedykowany dla
    macierzy symetrycznych), posortowane malejaco. Ujemne wartosci rzedu
    bledu numerycznego (macierz jest teoretycznie PSD) sa przyciete do 0
    -- czysto numeryczna korekta, PREREG SS3.2."""
    eigvals = np.linalg.eigvalsh(C)  # rosnaco
    eigvals = np.clip(eigvals, 0.0, None)
    return eigvals[::-1]  # malejaco: lambda_1 pierwszy


def spectral_concentration(eigvals: np.ndarray) -> float:
    """PREREG SS4.1 -- lambda_1 / sum(lambda_i). NaN jesli suma ~ 0
    (wszystkie wartosci wlasne numerycznie zerowe -- zdegenerowany
    przypadek, np. stale kanaly)."""
    total = float(np.sum(eigvals))
    if total < 1e-12:
        return float("nan")
    return float(eigvals[0]) / total


def participation_ratio(eigvals: np.ndarray) -> float:
    """PREREG SS4.2 -- (sum lambda)^2 / sum(lambda^2). Zakres [1, N].
    NaN jesli suma kwadratow ~ 0."""
    sq_sum = float(np.sum(eigvals ** 2))
    if sq_sum < 1e-12:
        return float("nan")
    total = float(np.sum(eigvals))
    return (total ** 2) / sq_sum


# ---------------------------------------------------------------------
# SS4.3. membrane_spectral_ratio -- brzeg/brzeg, analogiczne do rodziny
# v0.1-v0.3
# ---------------------------------------------------------------------


def _n_edge(n: int, n_channels: int, edge_fraction: float) -> int:
    """PREREG SS4.3 -- prog N+3 (nie goly 2 jak w v0.1-v0.3), bo kazdy
    brzeg wymaga policzenia osobnej macierzy korelacji N x N."""
    return max(n_channels + 3, round(edge_fraction * n))


def membrane_window_metrics(
    channels: Sequence[np.ndarray], edge_fraction: float = EDGE_FRACTION
) -> Dict[str, float]:
    """Zwraca `spectral_concentration`, `participation_ratio` (liczone
    na CALYM oknie) oraz `membrane_spectral_ratio` (brzeg/brzeg,
    PREREG SS4.3). NaN dla ktorejkolwiek wielkosci jesli dane sa
    zdegenerowane (np. za krotkie okno wzgledem liczby kanalow)."""
    n_channels = len(channels)
    n = len(channels[0])
    for c in channels:
        if len(c) != n:
            raise ValueError("wszystkie kanaly musza miec identyczna dlugosc (wspolna os czasu)")

    C_full = channel_correlation_matrix(channels)
    eig_full = spectrum_from_correlation(C_full)
    conc_full = spectral_concentration(eig_full)
    pr_full = participation_ratio(eig_full)

    n_edge = _n_edge(n, n_channels, edge_fraction)
    if n_edge >= n // 2 + 1 or n_edge < n_channels + 1:
        # okno za krotkie zeby sensownie rozdzielic brzegi -- NaN, nie
        # falszywa wartosc (PREREG SS4.3, analogicznie do NaN w v0.1-v0.3)
        ratio = float("nan")
    else:
        start_ch = [c[:n_edge] for c in channels]
        end_ch = [c[-n_edge:] for c in channels]
        eig_start = spectrum_from_correlation(channel_correlation_matrix(start_ch))
        eig_end = spectrum_from_correlation(channel_correlation_matrix(end_ch))
        conc_start = spectral_concentration(eig_start)
        conc_end = spectral_concentration(eig_end)
        if np.isnan(conc_start) or np.isnan(conc_end) or conc_start < 1e-9:
            ratio = float("nan")
        else:
            ratio = conc_end / conc_start

    return {
        "spectral_concentration": conc_full,
        "participation_ratio": pr_full,
        "membrane_spectral_ratio": ratio,
    }


# ---------------------------------------------------------------------
# PREREG SS5. Generatory kontrolne syntetyczne (zamrozone)
# ---------------------------------------------------------------------

GROWTH_RATE = 0.05     # (a) tempo narastania wspoldzielonego skladnika
NOISE_STD = 1.0        # wspolne dla (a)/(b)/(c) -- poziom niezaleznego szumu na kanal
SHARED_K_CONST = 1.5   # (c) stala amplituda wspoldzielonego skladnika


def make_growing_shared(n_channels: int, window_size: int, seed: Optional[int]) -> List[np.ndarray]:
    """(a) POZYTYWNA -- niezalezny szum + STOPNIOWO rosnacy
    wspoldzielony skladnik, PREREG SS5a."""
    rng = np.random.default_rng(seed)
    t = np.arange(window_size, dtype=float)
    shared = np.sin(OMEGA_SHARED * t)
    growth = GROWTH_RATE * t
    channels = []
    for _ in range(n_channels):
        indep = rng.normal(0.0, NOISE_STD, window_size)
        channels.append(indep + growth * shared)
    return channels


def make_independent_noise(n_channels: int, window_size: int, seed: Optional[int]) -> List[np.ndarray]:
    """(b) NEGATYWNA A -- calkowicie niezalezny bialy szum, bez trendu,
    bez wspolnego skladnika, PREREG SS5b."""
    rng = np.random.default_rng(seed)
    return [rng.normal(0.0, NOISE_STD, window_size) for _ in range(n_channels)]


def make_constant_shared(n_channels: int, window_size: int, seed: Optional[int]) -> List[np.ndarray]:
    """(c) DODATKOWA -- niezalezny szum + STALY wspoldzielony skladnik
    (ta sama amplituda przez caly czas), PREREG SS5c."""
    rng = np.random.default_rng(seed)
    t = np.arange(window_size, dtype=float)
    shared = np.sin(OMEGA_SHARED * t)
    channels = []
    for _ in range(n_channels):
        indep = rng.normal(0.0, NOISE_STD, window_size)
        channels.append(indep + SHARED_K_CONST * shared)
    return channels


# ---------------------------------------------------------------------
# Bramka kontrolna z obsluga NaN (wzorem chrono_cone_bridge.py)
# ---------------------------------------------------------------------


class MembraneControlResult:
    __test__ = False

    def __init__(
        self,
        positive: Optional[TestResult],
        negative: Optional[TestResult],
        conc_b_median: float,
        conc_c_median: float,
        n_valid_pos: int,
        n_valid_neg_a: int,
        n_valid_neg_b: int,
        n_total: int,
        passed: bool,
        inconclusive: bool,
        reason: str,
    ):
        self.positive = positive
        self.negative = negative
        self.conc_b_median = conc_b_median
        self.conc_c_median = conc_c_median
        self.n_valid_pos = n_valid_pos
        self.n_valid_neg_a = n_valid_neg_a
        self.n_valid_neg_b = n_valid_neg_b
        self.n_total = n_total
        self.passed = passed
        self.inconclusive = inconclusive
        self.reason = reason


MIN_VALID_FRAC = 0.5


def run_membrane_controls(
    n_channels: int,
    n_windows: int,
    window_size: int,
    seed: int = 0,
    alpha: float = 0.05,
    edge_fraction: float = EDGE_FRACTION,
) -> MembraneControlResult:
    rng = np.random.default_rng(seed)
    seeds = rng.integers(0, 2**31 - 1, size=n_windows)

    def _metrics(gen, seed_offset=0):
        ratios = []
        concs = []
        for s in seeds:
            channels = gen(n_channels, window_size, int(s) + seed_offset)
            m = membrane_window_metrics(channels, edge_fraction=edge_fraction)
            ratios.append(m["membrane_spectral_ratio"])
            concs.append(m["spectral_concentration"])
        return np.array(ratios), np.array(concs)

    pos_ratio, _pos_conc = _metrics(make_growing_shared)
    neg_a_ratio, neg_a_conc = _metrics(make_independent_noise, seed_offset=1)
    neg_b_ratio, neg_b_conc = _metrics(make_constant_shared, seed_offset=2)

    pos_valid = pos_ratio[~np.isnan(pos_ratio)]
    neg_a_valid = neg_a_ratio[~np.isnan(neg_a_ratio)]
    neg_b_valid = neg_b_ratio[~np.isnan(neg_b_ratio)]

    n_total = n_windows
    min_needed = max(2, int(np.ceil(MIN_VALID_FRAC * n_total)))

    conc_b_median = float(np.nanmedian(neg_a_conc))
    conc_c_median = float(np.nanmedian(neg_b_conc))

    if (
        len(pos_valid) < min_needed
        or len(neg_a_valid) < min_needed
        or len(neg_b_valid) < min_needed
    ):
        return MembraneControlResult(
            positive=None,
            negative=None,
            conc_b_median=conc_b_median,
            conc_c_median=conc_c_median,
            n_valid_pos=len(pos_valid),
            n_valid_neg_a=len(neg_a_valid),
            n_valid_neg_b=len(neg_b_valid),
            n_total=n_total,
            passed=False,
            inconclusive=True,
            reason=(
                f"Za duzo NaN w membrane_spectral_ratio (okno za krotkie "
                f"wzgledem N={n_channels} kanalow) w co najmniej jednej "
                f"grupie: pos={len(pos_valid)}/{n_total}, "
                f"neg_a={len(neg_a_valid)}/{n_total}, "
                f"neg_b={len(neg_b_valid)}/{n_total}, prog={min_needed}."
            ),
        )

    positive = mann_whitney_test(pos_valid, neg_a_valid)
    negative = mann_whitney_test(neg_a_valid, neg_b_valid)

    pos_ok = positive.pvalue < alpha
    neg_ok = negative.pvalue >= alpha
    passed = pos_ok and neg_ok

    if passed:
        reason = (
            "Kontrola pozytywna (rosnacy wspoldzielony skladnik vs "
            "niezalezny szum) wykryla istotna roznice na "
            "membrane_spectral_ratio, kontrola negatywna (niezalezny "
            "szum vs staly wspoldzielony skladnik) nie dala falszywego "
            "alarmu (obie plaskie w czasie, mimo roznego poziomu "
            "koncentracji)."
        )
    elif not pos_ok and not neg_ok:
        reason = "Kontrola pozytywna NIE wykryla efektu I kontrola negatywna dala falszywy alarm -- mechanika zepsuta."
    elif not pos_ok:
        reason = "Kontrola pozytywna nie wykryla rosnacego sprzezenia -- metryka za malo czula."
    else:
        reason = "Kontrola negatywna dala istotna roznice -- stala korelacja generuje falszywy trend rangowy wzgledem braku korelacji, odnotowane wprost."

    return MembraneControlResult(
        positive=positive,
        negative=negative,
        conc_b_median=conc_b_median,
        conc_c_median=conc_c_median,
        n_valid_pos=len(pos_valid),
        n_valid_neg_a=len(neg_a_valid),
        n_valid_neg_b=len(neg_b_valid),
        n_total=n_total,
        passed=passed,
        inconclusive=False,
        reason=reason,
    )


# ---------------------------------------------------------------------
# PREREG SS5. Siatka syntetyczna (zamrozona)
# ---------------------------------------------------------------------

SYN_WINDOW_SIZES = (128, 256, 512)
SYN_N_WINDOWS = 30
SYN_SEED = 0
SYN_ALPHA = 0.05
SYN_N_CHANNELS = (2, 3)  # N=2 primarny test, N=3 sekundarny (PREREG SS2)


def run_synthetic_controls() -> List[Dict]:
    rows = []
    for n_channels in SYN_N_CHANNELS:
        for window_size in SYN_WINDOW_SIZES:
            result = run_membrane_controls(
                n_channels=n_channels,
                n_windows=SYN_N_WINDOWS,
                window_size=window_size,
                seed=SYN_SEED,
                alpha=SYN_ALPHA,
            )
            rows.append({"n_channels": n_channels, "window_size": window_size, "result": result})
    return rows


def format_synthetic_report(rows: List[Dict]) -> str:
    lines = ["## Kontrole syntetyczne chrono_membrane_bridge", ""]
    for row in rows:
        n_ch = row["n_channels"]
        w = row["window_size"]
        r: MembraneControlResult = row["result"]
        lines.append(f"### N={n_ch} kanaly, window_size={w}")
        lines.append(
            f"n_valid: pos={r.n_valid_pos}/{r.n_total}, "
            f"neg_a={r.n_valid_neg_a}/{r.n_total}, neg_b={r.n_valid_neg_b}/{r.n_total}"
        )
        lines.append(
            f"median spectral_concentration: (b) niezalezny={r.conc_b_median:.4g} "
            f"(c) staly wspoldzielony={r.conc_c_median:.4g} "
            f"(1/N={1.0/n_ch:.4g})"
        )
        if r.inconclusive:
            lines.append(f"INCONCLUSIVE: {r.reason}")
        else:
            lines.append(
                f"pozytywna (a vs b, membrane_spectral_ratio): p={r.positive.pvalue:.4g} "
                f"r={r.positive.effect_size_r:.3f} ({effect_size_label(r.positive.effect_size_r)}) "
                f"mediana(a)={r.positive.median_test:.4g} mediana(b)={r.positive.median_background:.4g}"
            )
            lines.append(
                f"negatywna (b vs c, membrane_spectral_ratio): p={r.negative.pvalue:.4g} "
                f"r={r.negative.effect_size_r:.3f} "
                f"mediana(b)={r.negative.median_test:.4g} mediana(c)={r.negative.median_background:.4g}"
            )
            lines.append(f"PASSED={r.passed} -- {r.reason}")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    t0 = time.time()
    rows = run_synthetic_controls()
    print(format_synthetic_report(rows))
    print(f"Czas: {time.time()-t0:.2f}s")
