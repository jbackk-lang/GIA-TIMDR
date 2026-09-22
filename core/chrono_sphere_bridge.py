# core/chrono_sphere_bridge.py
"""
chrono_sphere_bridge.py -- implementacja PRE-REJESTROWANEJ (patrz
docs/geometry/PREREG_CHRONO_SPHERE_BRIDGE_v0.1.md) konstrukcji
"chrono_sphere_bridge": piata iteracja watku M/S<->G przez Chronoproces
(po chrono_cone_ratio v0.1, chrono_pendulum_ratio/net_turn v0.2,
chrono_centrifugal_ratio v0.3 -- wszystkie odrzucone na kontroli --
oraz chrono_membrane_bridge v0.1/v0.2 -- potwierdzony).

RDZEN POMYSLU: formalizacja Chronoprocesu Xi=(T,x,Gamma,phi) jako
przeksztalcenie T_G miedzy dwiema przestrzeniami stanow galezi G:

    S_G  = {Gamma:T×C->R | C >= 3 kanaly, niezaleznosc sprawdzona liczbowo}
    S_G' = {(u(t), r(t)) | u(t) in S^2, r(t) >= 0}

Dla trzech jednoczesnie probkowanych kanalow (c_x,c_y,c_z):

    v(t) = (|x_cx(t)|, |x_cy(t)|, |x_cz(t)|)
    r(t) = ||v(t)||
    u(t) = v(t)/r(t)  (kierunek na sferze; u_0=(1,1,1)/sqrt(3) gdy r(t)=0)

Metryka: wazona predkosc katowa Omega_win = suma(r(t)*omega(t)) /
suma(r(t)), omega(t) = arccos(u(t).u(t+dt)), liczona tylko tam gdzie
r(t) i r(t+dt) przechodza próg (percentyl 20% w oknie).

ZASTRZEZENIE (patrz PREREG SS3.2): rektyfikacja |x| NIE stabilizuje
r(t) -- r(t)=sqrt(sum x_i^2) jest identyczne ze znakiem czy bez niego,
bo podniesienie do kwadratu usuwa znak. Rektyfikacja robi cos innego:
ogranicza u(t) do DODATNIEGO OKTANTU sfery (kazda wspolrzedna >=0), wiec
maksymalny mozliwy kat miedzy dwoma punktami to pi/2, nie pi. To
swiadoma decyzja interpretacyjna (u(t) = wzgledna dominacja kanalow),
nie mechanizm stabilizujacy. Stabilizacje r(t) zapewnia WYLACZNIE prog+
maska (SS3.3 PREREG).

Bramka niezaleznosci kanalow (SS3.1 PREREG) reuzywa
timdr_geometry.spectral_family (channel_correlation_matrix,
spectrum_from_correlation) -- ten sam kod co chrono_membrane_bridge,
nie nowa implementacja.

Nic w tym pliku nie zostalo zmienione PO zobaczeniu wynikow kontroli
syntetycznych ani realnych danych -- wszystkie stale sa przeniesione
1:1 z zamrozonej pre-rejestracji.
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
# Stale zamrozone w PREREG_CHRONO_SPHERE_BRIDGE_v0.1.md
# ---------------------------------------------------------------------

INDEPENDENCE_ALPHA = 0.9      # próg bramki: lambda_1/sum(lambda) < 0.9 -> wejscie do S_G
R_PERCENTILE = 20.0           # percentyl progu r_min w oknie
U0_FALLBACK = np.array([1.0, 1.0, 1.0]) / np.sqrt(3.0)  # kierunek bazowy gdy r(t)=0

# ---------------------------------------------------------------------
# SS3.1 Bramka niezaleznosci kanalow (liczbowa, nie opisowa)
# ---------------------------------------------------------------------


def independence_gate(channels: Sequence[np.ndarray], alpha: float = INDEPENDENCE_ALPHA) -> Tuple[bool, float]:
    """Zwraca (czy_okno_kwalifikuje_sie, lambda_1/sum(lambda)).
    Reuzywa channel_correlation_matrix/spectrum_from_correlation z
    spectral_family -- ten sam mechanizm co bramka membrany."""
    C = channel_correlation_matrix(channels)
    eig = spectrum_from_correlation(C)
    conc = spectral_concentration(eig)
    if np.isnan(conc):
        return False, conc
    return conc < alpha, conc


# ---------------------------------------------------------------------
# SS3.2 Transformacja T_G: S_G -> S_G'
# ---------------------------------------------------------------------


def compute_v_r_u(cx: np.ndarray, cy: np.ndarray, cz: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """v(t) = (|cx|,|cy|,|cz|), r(t)=||v(t)||, u(t)=v(t)/r(t) (u_0 gdy
    r(t)=0). Rektyfikacja ogranicza u(t) do dodatniego oktantu S^2 --
    patrz zastrzezenie w docstringu modulu, NIE stabilizuje r(t)."""
    v = np.stack([np.abs(cx), np.abs(cy), np.abs(cz)], axis=1)  # (n,3)
    r = np.linalg.norm(v, axis=1)  # (n,)
    u = np.empty_like(v)
    nonzero = r > 0
    u[nonzero] = v[nonzero] / r[nonzero, None]
    u[~nonzero] = U0_FALLBACK
    return v, r, u


def r_mask(r: np.ndarray, percentile: float = R_PERCENTILE) -> np.ndarray:
    """M(t) = 1 jesli r(t) >= percentyl `percentile` rozkladu r(t) W TYM
    OKNIE, inaczej 0. Jedyny mechanizm stabilizujacy kierunek u(t)
    (SS3.3 PREREG)."""
    if len(r) == 0:
        return np.zeros(0, dtype=bool)
    r_min = np.percentile(r, percentile)
    return r >= r_min


# ---------------------------------------------------------------------
# SS4 Metryka: Omega_win, wazona predkosc katowa
# ---------------------------------------------------------------------


def angular_velocity_window(u: np.ndarray, r: np.ndarray, mask: np.ndarray, dt_samples: int) -> float:
    """Omega_win = sum(r(t)*omega(t)) / sum(r(t)) dla t z mask(t)=1 I
    mask(t+dt)=1, omega(t)=arccos(u(t).u(t+dt)). NaN jesli brak ważnych
    par."""
    n = len(u)
    if dt_samples <= 0 or dt_samples >= n:
        return float("nan")
    u1 = u[: n - dt_samples]
    u2 = u[dt_samples:]
    r1 = r[: n - dt_samples]
    m1 = mask[: n - dt_samples]
    m2 = mask[dt_samples:]
    valid = m1 & m2
    if not np.any(valid):
        return float("nan")
    dot = np.clip(np.sum(u1[valid] * u2[valid], axis=1), -1.0, 1.0)
    omega = np.arccos(dot)
    weights = r1[valid]
    total_w = np.sum(weights)
    if total_w < 1e-12:
        return float("nan")
    return float(np.sum(weights * omega) / total_w)


def sphere_window_metrics(
    cx: np.ndarray, cy: np.ndarray, cz: np.ndarray, dt_values: Sequence[int], alpha: float = INDEPENDENCE_ALPHA
) -> Optional[Dict[str, float]]:
    """Petla jednego okna: bramka niezaleznosci -> T_G -> maska r(t) ->
    Omega_win dla kazdego dt w dt_values. Zwraca None jesli okno
    odrzucone przez bramke (nie liczone dalej, SS3.1)."""
    ok, conc = independence_gate([cx, cy, cz], alpha=alpha)
    if not ok:
        return None
    v, r, u = compute_v_r_u(cx, cy, cz)
    mask = r_mask(r)
    out = {"gate_concentration": conc}
    for dt in dt_values:
        out[f"omega_win_dt{dt}"] = angular_velocity_window(u, r, mask, dt)
    return out


# ---------------------------------------------------------------------
# SS5 Generatory syntetyczne (zamrozone PRZED implementacja)
# ---------------------------------------------------------------------

SYN_N_CHANNELS = 3
SYN_NOISE_STD = 1.0
SYN_JUMP_K = 8.0          # (v0.1, ODRZUCONY) wielkosc skoku wzgledem sigma w kontroli pozytywnej
SYN_GATE_NOISE_EPS = 0.05  # znikomy szum w kontroli bramki (c)

# v0.2 (PREREG_CHRONO_SPHERE_BRIDGE_v0.2.md SS1) -- cykliczne "kopniecia"
SYN_N_KICKS = 8            # liczba kopniec w oknie, niezaleznie od window_size
SYN_KICK_K = 8.0           # amplituda szczytowa kopniecia (ta sama stala co v0.1 SYN_JUMP_K)
SYN_KICK_WIDTH_FRACTION = 0.2  # kick_width = kick_period // 5


def make_direction_jump(window_size: int, seed: Optional[int]) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(a) v0.1, ODRZUCONY na kontroli -- patrz
    RESULT_CHRONO_SPHERE_BRIDGE_v0.1.md. Zachowane w kodzie jako
    udokumentowany, odrzucony wariant, NIE kasowane. Trzy niezalezne
    kanaly szumu + wstrzykniety nagly skok kierunku w polowie okna
    (jeden kanal dostaje trwaly offset w drugiej polowie) -- dawal
    Omega_win NIZSZE niz czysty szum (r=-1.000), bo po skoku sygnal
    "zamarza" (dlugi odcinek bliski-zerowej predkosci katowej, wysoko
    wazony przez podniesione r(t))."""
    rng = np.random.default_rng(seed)
    half = window_size // 2
    cx = rng.normal(0.0, SYN_NOISE_STD, window_size)
    cy = rng.normal(0.0, SYN_NOISE_STD, window_size)
    cz = rng.normal(0.0, SYN_NOISE_STD, window_size)
    cx[half:] += SYN_JUMP_K
    return cx, cy, cz


def make_periodic_kicks(window_size: int, seed: Optional[int]) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(a) v0.2 -- PREREG_CHRONO_SPHERE_BRIDGE_v0.2.md SS1. Tlo
    identyczne z (b) (niezalezny szum na wszystkich trzech kanalach),
    PLUS N_KICKS periodycznych, KROTKICH, TROJKATNYCH impulsow
    dodanych do c_x (ten sam kanal za kazdym razem -- uzasadnienie
    fizyczne: uderzenie od uszkodzenia konsekwentnie najsilniej
    pobudza czujnik najblizszy miejscu uszkodzenia). Trojkat (nie
    prostokat) celowo -- brak plaskiego szczytu, kierunek zmienia sie
    CIAGLE przez caly czas trwania kazdego impulsu."""
    rng = np.random.default_rng(seed)
    cx = rng.normal(0.0, SYN_NOISE_STD, window_size)
    cy = rng.normal(0.0, SYN_NOISE_STD, window_size)
    cz = rng.normal(0.0, SYN_NOISE_STD, window_size)

    kick_period = window_size // SYN_N_KICKS
    kick_width = max(2, kick_period // 5)
    half_width = kick_width / 2.0

    for i in range(SYN_N_KICKS):
        center = i * kick_period + kick_period // 2
        lo = max(0, int(center - half_width))
        hi = min(window_size, int(center + half_width) + 1)
        for t in range(lo, hi):
            dist = abs(t - center)
            contrib = SYN_KICK_K * (1.0 - dist / half_width)
            if contrib > 0:
                cx[t] += contrib

    return cx, cy, cz


def make_independent_noise_3(window_size: int, seed: Optional[int]) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(b) NEGATYWNA -- trzy niezalezne kanaly szumu, bez skoku, bez
    wspolnego skladnika, przez caly czas."""
    rng = np.random.default_rng(seed)
    cx = rng.normal(0.0, SYN_NOISE_STD, window_size)
    cy = rng.normal(0.0, SYN_NOISE_STD, window_size)
    cz = rng.normal(0.0, SYN_NOISE_STD, window_size)
    return cx, cy, cz


def make_gate_should_reject(window_size: int, seed: Optional[int]) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(c) BRAMKA -- trzy kopie tego samego sygnalu + znikomy szum.
    Test sanity samej bramki niezaleznosci (SS3.1): powinna to
    odrzucic (lambda_1/sum(lambda) ~ 1)."""
    rng = np.random.default_rng(seed)
    s = rng.normal(0.0, SYN_NOISE_STD, window_size)
    eps = SYN_GATE_NOISE_EPS
    cx = s + rng.normal(0.0, eps, window_size)
    cy = s + rng.normal(0.0, eps, window_size)
    cz = s + rng.normal(0.0, eps, window_size)
    return cx, cy, cz


# ---------------------------------------------------------------------
# Bramka kontrolna (SS5 PREREG)
# ---------------------------------------------------------------------

SYN_WINDOW_SIZES = (500, 1000, 2000)
SYN_N_WINDOWS = 30
SYN_SEED = 0
SYN_ALPHA = 0.05
SYN_DT = 1  # kontrole syntetyczne uzywaja jednego dt -- stabilnosc miedzy dt sprawdzana dopiero na danych realnych (SS4/SS6 PREREG)


@dataclass
class GateSanityResult:
    n_windows: int
    n_rejected: int
    reject_fraction: float
    passed: bool


def run_gate_sanity(window_size: int, n_windows: int = SYN_N_WINDOWS, seed: int = SYN_SEED) -> GateSanityResult:
    """(c) Test sanity bramki: PRZED (a) vs (b) sprawdzamy, ze bramka
    faktycznie odrzuca prawie wszystkie okna z trzema kopiami tego
    samego sygnalu (SS5 PREREG, 'jesli bramka NIE odrzuci (c),
    zatrzymanie')."""
    rng = np.random.default_rng(seed)
    seeds = rng.integers(0, 2**31 - 1, size=n_windows)
    n_rejected = 0
    for s in seeds:
        cx, cy, cz = make_gate_should_reject(window_size, int(s))
        ok, _conc = independence_gate([cx, cy, cz])
        if not ok:
            n_rejected += 1
    frac = n_rejected / n_windows
    return GateSanityResult(
        n_windows=n_windows,
        n_rejected=n_rejected,
        reject_fraction=frac,
        passed=frac >= 0.9,  # prawie wszystkie -- próg zamrozony razem z kodem (nie po zobaczeniu wyniku)
    )


@dataclass
class SphereControlResult:
    __test__ = False
    gate_sanity: GateSanityResult
    omega_test: Optional[TestResult]
    n_valid_pos: int
    n_valid_neg: int
    n_total: int
    passed: bool
    inconclusive: bool
    reason: str


MIN_VALID_FRAC = 0.5


def run_sphere_controls(
    window_size: int, n_windows: int = SYN_N_WINDOWS, seed: int = SYN_SEED, alpha: float = SYN_ALPHA, dt: int = SYN_DT
) -> SphereControlResult:
    gate_result = run_gate_sanity(window_size, n_windows=n_windows, seed=seed)
    if not gate_result.passed:
        return SphereControlResult(
            gate_sanity=gate_result,
            omega_test=None,
            n_valid_pos=0,
            n_valid_neg=0,
            n_total=n_windows,
            passed=False,
            inconclusive=False,
            reason=(
                f"Bramka sanity (c) NIE odrzucila wystarczajaco okien z trzema "
                f"kopiami tego samego sygnalu: odrzucono {gate_result.n_rejected}/"
                f"{gate_result.n_windows} (< 90%). Sama bramka wadliwa -- "
                f"zatrzymanie przed testem (a) vs (b), zgodnie z PREREG SS5."
            ),
        )

    rng = np.random.default_rng(seed)
    seeds_pos = rng.integers(0, 2**31 - 1, size=n_windows)
    seeds_neg = rng.integers(0, 2**31 - 1, size=n_windows)

    pos_vals = []
    for s in seeds_pos:
        cx, cy, cz = make_periodic_kicks(window_size, int(s))
        m = sphere_window_metrics(cx, cy, cz, dt_values=[dt])
        pos_vals.append(m[f"omega_win_dt{dt}"] if m is not None else float("nan"))
    neg_vals = []
    for s in seeds_neg:
        cx, cy, cz = make_independent_noise_3(window_size, int(s))
        m = sphere_window_metrics(cx, cy, cz, dt_values=[dt])
        neg_vals.append(m[f"omega_win_dt{dt}"] if m is not None else float("nan"))

    pos_arr = np.array(pos_vals)
    neg_arr = np.array(neg_vals)
    pos_valid = pos_arr[~np.isnan(pos_arr)]
    neg_valid = neg_arr[~np.isnan(neg_arr)]

    min_needed = max(2, int(np.ceil(MIN_VALID_FRAC * n_windows)))
    if len(pos_valid) < min_needed or len(neg_valid) < min_needed:
        return SphereControlResult(
            gate_sanity=gate_result,
            omega_test=None,
            n_valid_pos=len(pos_valid),
            n_valid_neg=len(neg_valid),
            n_total=n_windows,
            passed=False,
            inconclusive=True,
            reason=(
                f"Za duzo NaN/odrzuconych okien w Omega_win: "
                f"pos={len(pos_valid)}/{n_windows}, neg={len(neg_valid)}/{n_windows}, "
                f"prog={min_needed}."
            ),
        )

    omega_test = mann_whitney_test(pos_valid, neg_valid)
    pos_ok = omega_test.pvalue < alpha and abs(omega_test.effect_size_r) >= 0.3
    direction_ok = omega_test.median_test > omega_test.median_background
    passed = pos_ok and direction_ok

    if passed:
        reason = (
            "Kontrola pozytywna (wstrzykniety skok kierunku vs niezalezny "
            "szum) wykryla istotnie WYZSZE Omega_win w oczekiwanym kierunku."
        )
    elif not pos_ok:
        reason = "Brak istotnej roznicy (lub za maly efekt) miedzy skokiem kierunku a szumem -- metryka za malo czula."
    else:
        reason = "Istotna roznica, ale w NIEoczekiwanym kierunku (szum > skok) -- mechanika podejrzana."

    return SphereControlResult(
        gate_sanity=gate_result,
        omega_test=omega_test,
        n_valid_pos=len(pos_valid),
        n_valid_neg=len(neg_valid),
        n_total=n_windows,
        passed=passed,
        inconclusive=False,
        reason=reason,
    )


def run_synthetic_controls() -> List[Dict]:
    rows = []
    for window_size in SYN_WINDOW_SIZES:
        result = run_sphere_controls(window_size=window_size)
        rows.append({"window_size": window_size, "result": result})
    return rows


def format_synthetic_report(rows: List[Dict]) -> str:
    lines = ["## Kontrole syntetyczne chrono_sphere_bridge v0.1", ""]
    for row in rows:
        w = row["window_size"]
        r: SphereControlResult = row["result"]
        lines.append(f"### window_size={w}")
        g = r.gate_sanity
        lines.append(
            f"bramka sanity (c): odrzucono {g.n_rejected}/{g.n_windows} "
            f"({g.reject_fraction:.1%}) -- {'PASSED' if g.passed else 'FAILED'}"
        )
        if r.inconclusive:
            lines.append(f"INCONCLUSIVE: {r.reason}")
        elif r.omega_test is None:
            lines.append(f"ZATRZYMANE NA BRAMCE: {r.reason}")
        else:
            t = r.omega_test
            lines.append(
                f"n_valid: pos={r.n_valid_pos}/{r.n_total}, neg={r.n_valid_neg}/{r.n_total}"
            )
            lines.append(
                f"Omega_win (a vs b): p={t.pvalue:.4g} r={t.effect_size_r:.3f} "
                f"({effect_size_label(t.effect_size_r)}) "
                f"mediana(a)={t.median_test:.4g} mediana(b)={t.median_background:.4g}"
            )
            lines.append(f"PASSED={r.passed} -- {r.reason}")
        lines.append("")
    return "\n".join(lines)


__all__ = [
    "INDEPENDENCE_ALPHA",
    "R_PERCENTILE",
    "independence_gate",
    "compute_v_r_u",
    "r_mask",
    "angular_velocity_window",
    "sphere_window_metrics",
    "make_direction_jump",
    "make_independent_noise_3",
    "make_gate_should_reject",
    "run_gate_sanity",
    "run_sphere_controls",
    "SYN_WINDOW_SIZES",
    "SYN_N_WINDOWS",
    "SYN_SEED",
    "SYN_ALPHA",
    "SYN_DT",
    "run_synthetic_controls",
    "format_synthetic_report",
]


if __name__ == "__main__":
    t0 = time.time()
    rows = run_synthetic_controls()
    print(format_synthetic_report(rows))
    print(f"Czas: {time.time()-t0:.2f}s")
