# core/chrono_modal_geometry_bridge.py
"""
chrono_modal_geometry_bridge.py -- implementacja PRE-REJESTROWANEJ
(patrz docs/geometry/PREREG_CHRONO_MODAL_GEOMETRY_BRIDGE_v0.1.md)
konstrukcji mostu K->G: widmo jednego kanalu M/S -> trzy obwiednie
rezonansow charakterystycznych lozyska (BPFO/BPFI/BSF) -> trajektoria
Gamma(t,s)=A_s(t)*e_s w R^3 -> krzywizna/skret Freneta-Serreta.

NIE reuzywa chrono_sphere_bridge (odrzucony v0.1/v0.2) -- inny obiekt
geometryczny (krzywizna/skret krzywej w R^3, nie kierunek+promien na
S^2 z wazona predkoscia katowa) -- ale dzieli z nim TEN SAM
zdiagnozowany typ ryzyka (saturacja przy dominacji jednego wymiaru),
sprawdzany tu jawnie jako DWUSTRONNA kontrola (SS5.2 PREREG), nie
zakladany za bezpieczny z powodu innego wzoru.

Bramka niezaleznosci (SS3.3 PREREG) reuzywa timdr_geometry.spectral_family
-- ten sam kod co chrono_sphere_bridge i chrono_membrane_bridge.

Nic w tym pliku nie zostalo zmienione PO zobaczeniu wynikow kontroli
syntetycznych -- wszystkie stale sa przeniesione 1:1 z zamrozonej
pre-rejestracji.
"""
from __future__ import annotations

import os
import sys
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_THIS_DIR)
_GEOMETRY_FORMALISM = os.path.join(_REPO_ROOT, "TIMDR-Geometry-Formalism")
_MATH_FORMALISM = os.path.join(_REPO_ROOT, "TIMDR-Math-Formalism")
for _p in (_REPO_ROOT, _GEOMETRY_FORMALISM, _MATH_FORMALISM):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from timdr_geometry.spectral_family import (  # noqa: E402
    channel_correlation_matrix,
    spectrum_from_correlation,
    spectral_concentration,
)
from timdr_formalism.pipeline import (  # noqa: E402
    mann_whitney_test,
    effect_size_label,
    TestResult,
)

# ---------------------------------------------------------------------
# SS2 PREREG: geometria lozyska CWRU (drive-end SKF 6205-2RS JEM),
# zweryfikowana wyszukiwaniem 2026-09-22, nie z pamieci.
# ---------------------------------------------------------------------

BEARING_N_BALLS = 9
BEARING_BALL_DIAM_MM = 7.94
BEARING_PITCH_DIAM_MM = 39.04
BEARING_CONTACT_ANGLE_RAD = 0.0
CWRU_RPM = 1797
FR_HZ = CWRU_RPM / 60.0  # 29.95 Hz


def _characteristic_frequencies(fr: float) -> Dict[str, float]:
    ratio = (BEARING_BALL_DIAM_MM / BEARING_PITCH_DIAM_MM) * np.cos(BEARING_CONTACT_ANGLE_RAD)
    bpfo = (BEARING_N_BALLS / 2.0) * fr * (1 - ratio)
    bpfi = (BEARING_N_BALLS / 2.0) * fr * (1 + ratio)
    bsf_1x = (BEARING_PITCH_DIAM_MM / (2 * BEARING_BALL_DIAM_MM)) * fr * (1 - ratio ** 2)
    bsf_2x = 2 * bsf_1x  # konwencja "2x", patrz PREREG SS2
    ftf = (fr / 2.0) * (1 - ratio)  # nieuzywane w v0.1, patrz PREREG SS0
    return {"BPFO": bpfo, "BPFI": bpfi, "BSF": bsf_2x, "FTF": ftf}


CHAR_FREQS = _characteristic_frequencies(FR_HZ)  # BPFO=107.364, BPFI=162.186, BSF=141.169 Hz
BAND_NAMES = ("BPFO", "BPFI", "BSF")  # kolejnosc = kolejnosc osi e_1,e_2,e_3 (SS3.4 PREREG)
BAND_RELATIVE_WIDTH = 0.15  # +-15% czestotliwosci srodkowej (SS3.1 PREREG)

FS_RAW_HZ = 12000.0
FS_ENV_HZ = 500.0
DECIMATION_FACTOR = int(round(FS_RAW_HZ / FS_ENV_HZ))  # 24

EPS_1 = 1e-6  # floor na ||gamma'|| (SS3.4 PREREG)
EPS_2 = 1e-9  # floor na ||gamma' x gamma''||

INDEPENDENCE_ALPHA = 0.9  # ta sama stala co chrono_sphere_bridge


def band_edges(center_hz: float, relative_width: float = BAND_RELATIVE_WIDTH) -> Tuple[float, float]:
    return center_hz * (1 - relative_width), center_hz * (1 + relative_width)


# ---------------------------------------------------------------------
# SS3.2 PREREG: filtr pasmowy (FFT-domenowy) + obwiednia Hilberta
# ---------------------------------------------------------------------


# bandpass_fft/hilbert_envelope/decimate_simple: WYDZIELONE do
# timdr_formalism.envelope_demodulation (2026-09-22, po potwierdzonym
# wyniku modal_band_energy_bridge v0.2) jako domenowo-agnostyczny rdzen
# M/S->K, reuzywany rowniez przez core/modal_band_energy_bridge.py.
# Importowane ponizej, NIE redefiniowane -- zachowuje identyczne API.
from timdr_formalism.envelope_demodulation import (  # noqa: E402
    bandpass_fft,
    hilbert_envelope,
    decimate_simple,
)


def channel_to_envelope(x_de: np.ndarray, fs: float, center_hz: float) -> np.ndarray:
    f_lo, f_hi = band_edges(center_hz)
    filtered = bandpass_fft(x_de, fs, f_lo, f_hi)
    env = hilbert_envelope(filtered)
    return decimate_simple(env, DECIMATION_FACTOR)


# ---------------------------------------------------------------------
# SS3.3 PREREG: bramka niezaleznosci (reuzyta ze spectral_family)
# ---------------------------------------------------------------------


def independence_gate(envelopes: Sequence[np.ndarray], alpha: float = INDEPENDENCE_ALPHA) -> Tuple[bool, float]:
    C = channel_correlation_matrix(envelopes)
    eig = spectrum_from_correlation(C)
    conc = spectral_concentration(eig)
    if np.isnan(conc):
        return False, conc
    return conc < alpha, conc


# ---------------------------------------------------------------------
# SS3.4 PREREG: geometria Freneta-Serreta na trajektorii zdecymowanej
# ---------------------------------------------------------------------


def frenet_curvature_torsion(gamma: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """gamma: (n,3). Zwraca (kappa, tau), dlugosc n-4 (potrzebne 2
    probki zapasu z kazdej strony dla gamma'''). Degeneracja
    obslugiwana wg SS3.4 PREREG: kappa=0 (nie NaN) gdy trajektoria
    lokalnie nieruchoma/prosta; tau=NaN w tych punktach (wykluczone z
    agregacji)."""
    n = len(gamma)
    if n < 5:
        return np.zeros(0), np.zeros(0)

    # Wszystkie trzy pochodne liczone na WSPOLNYM zakresie indeksow
    # i=2..n-3 (0-indeksowane), dlugosc n-4, jawnie wyrownane (patrz
    # wyprowadzenie w komentarzu commitu -- kazda z trzech tablic
    # ponizej ma dlugosc n-4 z konstrukcji, bez potrzeby docinania po
    # fakcie, co bylo zrodlem bledu przesuniecia w pierwszej wersji).
    gp = (gamma[3 : n - 1] - gamma[1 : n - 3]) / 2.0
    gpp = gamma[3 : n - 1] - 2 * gamma[2 : n - 2] + gamma[1 : n - 3]
    gppp = (gamma[4:n] - 2 * gamma[3 : n - 1] + 2 * gamma[1 : n - 3] - gamma[0 : n - 4]) / 2.0
    m = len(gp)
    assert len(gpp) == m and len(gppp) == m, "niezgodnosc dlugosci pochodnych -- blad implementacji"

    cross = np.cross(gp, gpp)
    norm_cross = np.linalg.norm(cross, axis=1)
    norm_gp = np.linalg.norm(gp, axis=1)

    kappa = np.zeros(m)
    tau = np.full(m, np.nan)

    degenerate = (norm_gp < EPS_1) | (norm_cross < EPS_2)
    ok = ~degenerate

    kappa[ok] = norm_cross[ok] / (norm_gp[ok] ** 3)
    # kappa[degenerate] pozostaje 0.0 z konwencji (SS3.4 PREREG)

    numer_tau = np.sum(cross[ok] * gppp[ok], axis=1)
    tau[ok] = numer_tau / (norm_cross[ok] ** 2)
    # tau[degenerate] pozostaje NaN -- wykluczone z agregacji

    return kappa, tau


def window_metrics(gamma: np.ndarray) -> Dict[str, float]:
    kappa, tau = frenet_curvature_torsion(gamma)
    if len(kappa) == 0:
        return {"kappa_win": float("nan"), "tau_win": float("nan"), "n_tau_valid": 0}
    tau_valid = tau[~np.isnan(tau)]
    return {
        "kappa_win": float(np.median(kappa)),
        "tau_win": float(np.median(tau_valid)) if len(tau_valid) > 0 else float("nan"),
        "n_tau_valid": len(tau_valid),
    }


def modal_geometry_window_metrics(
    envelopes: Sequence[np.ndarray], alpha: float = INDEPENDENCE_ALPHA
) -> Optional[Dict[str, float]]:
    """Petla jednego okna: bramka niezaleznosci -> Gamma(t,s) -> kappa/tau."""
    ok, conc = independence_gate(envelopes, alpha=alpha)
    if not ok:
        return None
    gamma = np.stack(envelopes, axis=1)  # (n,3)
    metrics = window_metrics(gamma)
    metrics["gate_concentration"] = conc
    return metrics


# ---------------------------------------------------------------------
# SS5 PREREG: generatory syntetyczne (zamrozone PRZED implementacja)
# ---------------------------------------------------------------------

SYN_BASELINE_MU = 5.0
SYN_BASELINE_SIGMA = 1.0
SYN_DOMINANT_K = 5.0       # amplituda oscylacji dominujacego pasma (5x sigma tla)
SYN_DOMINANT_CYCLES = 3    # liczba cykli oscylacji w oknie
SYN_GATE_NOISE_EPS = 0.05


def make_envelope_background(window_size: int, seed: Optional[int]) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(b) NEGATYWNA -- trzy niezalezne obwiednie o podobnej, stalej
    sredniej amplitudzie i niezaleznym szumem wokol niej (SS5.2
    PREREG)."""
    rng = np.random.default_rng(seed)
    a0 = rng.normal(SYN_BASELINE_MU, SYN_BASELINE_SIGMA, window_size)
    a1 = rng.normal(SYN_BASELINE_MU, SYN_BASELINE_SIGMA, window_size)
    a2 = rng.normal(SYN_BASELINE_MU, SYN_BASELINE_SIGMA, window_size)
    return a0, a1, a2


def make_dominant_resonance(window_size: int, seed: Optional[int]) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(a) POZYTYWNA -- jedna obwiednia (indeks 0, BPFO) dostaje
    istotnie podwyzszona, zmienna w czasie amplitude wzgledem
    pozostalych dwoch (SS5.2 PREREG), ktore pozostaja niezmienione
    wzgledem (b)."""
    rng = np.random.default_rng(seed)
    t = np.arange(window_size, dtype=float)
    omega = 2 * np.pi * SYN_DOMINANT_CYCLES / window_size
    a0 = SYN_BASELINE_MU + SYN_DOMINANT_K * np.sin(omega * t) + rng.normal(0.0, SYN_BASELINE_SIGMA, window_size)
    a1 = rng.normal(SYN_BASELINE_MU, SYN_BASELINE_SIGMA, window_size)
    a2 = rng.normal(SYN_BASELINE_MU, SYN_BASELINE_SIGMA, window_size)
    return a0, a1, a2


def make_gate_should_reject(window_size: int, seed: Optional[int]) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(c) BRAMKA -- trzy niemal identyczne obwiednie + znikomy szum."""
    rng = np.random.default_rng(seed)
    s = rng.normal(SYN_BASELINE_MU, SYN_BASELINE_SIGMA, window_size)
    eps = SYN_GATE_NOISE_EPS
    a0 = s + rng.normal(0.0, eps, window_size)
    a1 = s + rng.normal(0.0, eps, window_size)
    a2 = s + rng.normal(0.0, eps, window_size)
    return a0, a1, a2


# ---------------------------------------------------------------------
# Bramka kontrolna (SS5 PREREG)
# ---------------------------------------------------------------------

SYN_WINDOW_SIZES = (250, 500, 1000)
SYN_N_WINDOWS = 30
SYN_SEED = 0
SYN_ALPHA = 0.05
MIN_VALID_FRAC = 0.5


@dataclass
class GateSanityResult:
    n_windows: int
    n_rejected: int
    reject_fraction: float
    passed: bool


def run_gate_sanity(window_size: int, n_windows: int = SYN_N_WINDOWS, seed: int = SYN_SEED) -> GateSanityResult:
    rng = np.random.default_rng(seed)
    seeds = rng.integers(0, 2**31 - 1, size=n_windows)
    n_rejected = 0
    for s in seeds:
        a0, a1, a2 = make_gate_should_reject(window_size, int(s))
        ok, _conc = independence_gate([a0, a1, a2])
        if not ok:
            n_rejected += 1
    frac = n_rejected / n_windows
    return GateSanityResult(n_windows=n_windows, n_rejected=n_rejected, reject_fraction=frac, passed=frac >= 0.9)


@dataclass
class ModalGeometryControlResult:
    __test__ = False
    gate_sanity: GateSanityResult
    kappa_test: Optional[TestResult]
    tau_test: Optional[TestResult]
    n_valid_pos_kappa: int
    n_valid_neg_kappa: int
    n_valid_pos_tau: int
    n_valid_neg_tau: int
    n_total: int
    kappa_direction: str  # "wzbogacenie" | "saturacja" | "brak_efektu" | "inconclusive"
    reason: str


def run_modal_geometry_controls(
    window_size: int, n_windows: int = SYN_N_WINDOWS, seed: int = SYN_SEED, alpha: float = SYN_ALPHA
) -> ModalGeometryControlResult:
    gate_result = run_gate_sanity(window_size, n_windows=n_windows, seed=seed)
    if not gate_result.passed:
        return ModalGeometryControlResult(
            gate_sanity=gate_result,
            kappa_test=None,
            tau_test=None,
            n_valid_pos_kappa=0,
            n_valid_neg_kappa=0,
            n_valid_pos_tau=0,
            n_valid_neg_tau=0,
            n_total=n_windows,
            kappa_direction="inconclusive",
            reason=(
                f"Bramka sanity (c) NIE odrzucila wystarczajaco okien: "
                f"{gate_result.n_rejected}/{gate_result.n_windows} (<90%). "
                f"Zatrzymanie przed testem glownym, zgodnie z PREREG SS5.1."
            ),
        )

    rng = np.random.default_rng(seed)
    seeds_pos = rng.integers(0, 2**31 - 1, size=n_windows)
    seeds_neg = rng.integers(0, 2**31 - 1, size=n_windows)

    pos_kappa, pos_tau = [], []
    for s in seeds_pos:
        a0, a1, a2 = make_dominant_resonance(window_size, int(s))
        m = modal_geometry_window_metrics([a0, a1, a2])
        pos_kappa.append(m["kappa_win"] if m is not None else float("nan"))
        pos_tau.append(m["tau_win"] if m is not None else float("nan"))
    neg_kappa, neg_tau = [], []
    for s in seeds_neg:
        a0, a1, a2 = make_envelope_background(window_size, int(s))
        m = modal_geometry_window_metrics([a0, a1, a2])
        neg_kappa.append(m["kappa_win"] if m is not None else float("nan"))
        neg_tau.append(m["tau_win"] if m is not None else float("nan"))

    pos_kappa, neg_kappa = np.array(pos_kappa), np.array(neg_kappa)
    pos_tau, neg_tau = np.array(pos_tau), np.array(neg_tau)

    pos_kappa_v = pos_kappa[~np.isnan(pos_kappa)]
    neg_kappa_v = neg_kappa[~np.isnan(neg_kappa)]
    pos_tau_v = pos_tau[~np.isnan(pos_tau)]
    neg_tau_v = neg_tau[~np.isnan(neg_tau)]

    min_needed = max(2, int(np.ceil(MIN_VALID_FRAC * n_windows)))
    if len(pos_kappa_v) < min_needed or len(neg_kappa_v) < min_needed:
        return ModalGeometryControlResult(
            gate_sanity=gate_result,
            kappa_test=None,
            tau_test=None,
            n_valid_pos_kappa=len(pos_kappa_v),
            n_valid_neg_kappa=len(neg_kappa_v),
            n_valid_pos_tau=len(pos_tau_v),
            n_valid_neg_tau=len(neg_tau_v),
            n_total=n_windows,
            kappa_direction="inconclusive",
            reason=f"Za duzo NaN/odrzuconych okien w kappa_win: pos={len(pos_kappa_v)}, neg={len(neg_kappa_v)}, prog={min_needed}.",
        )

    kappa_test = mann_whitney_test(pos_kappa_v, neg_kappa_v, alternative="two-sided")
    tau_test = None
    if len(pos_tau_v) >= min_needed and len(neg_tau_v) >= min_needed:
        tau_test = mann_whitney_test(pos_tau_v, neg_tau_v, alternative="two-sided")

    significant = kappa_test.pvalue < alpha and abs(kappa_test.effect_size_r) >= 0.3
    if not significant:
        direction = "brak_efektu"
        reason = "Brak istotnej roznicy (lub za maly efekt) miedzy dominujacym rezonansem a tlem na kappa_win."
    elif kappa_test.median_test > kappa_test.median_background:
        direction = "wzbogacenie"
        reason = "kappa_win ISTOTNIE WYZSZE przy dominujacym rezonansie -- most K->G dziala w kierunku przeciwnym do porazki sfery."
    else:
        direction = "saturacja"
        reason = "kappa_win ISTOTNIE NIZSZE przy dominujacym rezonansie -- TEN SAM mechanizm saturacji co chrono_sphere_bridge, drugi niezalezny dowod."

    return ModalGeometryControlResult(
        gate_sanity=gate_result,
        kappa_test=kappa_test,
        tau_test=tau_test,
        n_valid_pos_kappa=len(pos_kappa_v),
        n_valid_neg_kappa=len(neg_kappa_v),
        n_valid_pos_tau=len(pos_tau_v),
        n_valid_neg_tau=len(neg_tau_v),
        n_total=n_windows,
        kappa_direction=direction,
        reason=reason,
    )


def run_synthetic_controls() -> List[Dict]:
    rows = []
    for window_size in SYN_WINDOW_SIZES:
        result = run_modal_geometry_controls(window_size=window_size)
        rows.append({"window_size": window_size, "result": result})
    return rows


def format_synthetic_report(rows: List[Dict]) -> str:
    lines = ["## Kontrole syntetyczne chrono_modal_geometry_bridge v0.1", ""]
    lines.append(f"Czestotliwosci charakterystyczne (1797 RPM): {CHAR_FREQS}")
    lines.append("")
    for row in rows:
        w = row["window_size"]
        r: ModalGeometryControlResult = row["result"]
        lines.append(f"### window_size={w}")
        g = r.gate_sanity
        lines.append(
            f"bramka sanity (c): odrzucono {g.n_rejected}/{g.n_windows} ({g.reject_fraction:.1%}) "
            f"-- {'PASSED' if g.passed else 'FAILED'}"
        )
        if r.kappa_test is None:
            lines.append(f"ZATRZYMANE: {r.reason}")
        else:
            kt = r.kappa_test
            lines.append(
                f"n_valid kappa: pos={r.n_valid_pos_kappa}/{r.n_total}, neg={r.n_valid_neg_kappa}/{r.n_total}"
            )
            lines.append(
                f"kappa_win (a vs b): p={kt.pvalue:.4g} r={kt.effect_size_r:.3f} ({effect_size_label(kt.effect_size_r)}) "
                f"mediana(a)={kt.median_test:.4g} mediana(b)={kt.median_background:.4g}"
            )
            if r.tau_test is not None:
                tt = r.tau_test
                lines.append(
                    f"tau_win (a vs b): p={tt.pvalue:.4g} r={tt.effect_size_r:.3f} "
                    f"mediana(a)={tt.median_test:.4g} mediana(b)={tt.median_background:.4g} "
                    f"(n_tau: pos={r.n_valid_pos_tau}, neg={r.n_valid_neg_tau})"
                )
            else:
                lines.append("tau_win: za mało ważnych wartości do testu")
            lines.append(f"KIERUNEK: {r.kappa_direction} -- {r.reason}")
        lines.append("")
    return "\n".join(lines)


__all__ = [
    "CHAR_FREQS",
    "BAND_NAMES",
    "band_edges",
    "bandpass_fft",
    "hilbert_envelope",
    "decimate_simple",
    "channel_to_envelope",
    "independence_gate",
    "frenet_curvature_torsion",
    "window_metrics",
    "modal_geometry_window_metrics",
    "make_envelope_background",
    "make_dominant_resonance",
    "make_gate_should_reject",
    "run_gate_sanity",
    "run_modal_geometry_controls",
    "run_synthetic_controls",
    "format_synthetic_report",
]


if __name__ == "__main__":
    t0 = time.time()
    rows = run_synthetic_controls()
    print(format_synthetic_report(rows))
    print(f"Czas: {time.time()-t0:.2f}s")
