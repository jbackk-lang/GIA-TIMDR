# core/trefoil_frenet_torsion.py
"""
trefoil_frenet_torsion.py -- torsja Freneta-Serreta wzdluz trojwezla
(trefoil knot) jako kandydat na piate, formalnie odrebne znaczenie
slowa "skret" w ekosystemie TIMDR.

KONTEKST (patrz docs/geometry/TIMDR_Trefoil_FrenetTorsion.md dla pelnego
opisu i uzasadnienia): uzytkownik zaproponowal model, w ktorym "os
wzdluz figury [trojwezla helikalnego] reprezentuje skret, odstepstwa
[deformacje] pierwszego wezla to defekty, calosc [powinna byc]
rewidowana rezonansem". Dokladnie ta figura -- "trojwezel helikalny"
jako czesc "Potrojnego Tourosomobius" -- juz istnieje w
docs/geometry/tourosomobius.md, ale WYLACZNIE jako notacja pojeciowa:
brak dziedziny/przeciwdziedziny, brak dowodu, brak kodu, brak testow.

WAZNE ROZROZNIENIE (docs/theory/TIMDR_Twists.md): "skret" ma juz w tym
ekosystemie CZTERY formalnie odrebne znaczenia, z ktorych jedno --
"skret topologiczny (tau)" z Operators_N_TIMDR.md -- zostalo JAWNIE
SPRAWDZONE I ODRZUCONE jako tozsame z torsja Freneta-Serreta krzywej
(timdr-signal-framework SS20). Ten modul NIE nazywa niczego tutaj
"skretem TIMDR" -- liczy wprost, jednoznacznie nazwana "torsje
Freneta-Serreta wzdluz osi trojwezla" jako PIATY, oddzielny obiekt.

MATEMATYKA (identyczna z THE_TIMDR_Hyperflow_Engine/the_geo_pro_4d.py,
tam juz zwalidowana: blad <0.001% wzgledem analitycznej helisy dla
gestego probkowania):
    v  = p_t  - p_t1
    v1 = p_t1 - p_t2
    a  = v - v1
    a1 = v1 - (p_t2 - p_t3)
    j  = a - a1
    kappa = |v x a| / |v|^3
    tau   = det(v, a, j) / |v x a|^2
Bramkowanie szumu na malej krzywiznie identyczne jak w zrodle: jesli
kappa < min_curvature, tau=0 (nie na cross_norm==0 wprost -- patrz
docstring the_geo_pro_4d.py, "Poprawka wzgledem pseudokodu
uzytkownika").

Progi anomalia/defekt sa CELOWO identyczne z
synoptyk-v2.0/analyzer/adaptive_thresholds.py (mean+-2*std dla
anomalii, 0.3*(p90-p10) dla defektu skoku) -- zeby test byl
odtwarzalny tym samym, juz uzywanym w ekosystemie wzorcem, nie nowa,
niezaleznie wymyslona metryka.
"""
from __future__ import annotations

import math
from typing import Dict, List, Tuple

import numpy as np

Point3 = Tuple[float, float, float]

# Domyslne parametry -- takie same jak the_geo_pro_4d.DEFAULT_MIN_CURVATURE
DEFAULT_MIN_SPEED = 1e-6
DEFAULT_MIN_CURVATURE = 1e-4


def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _norm(v):
    return math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)


def _cross(a, b):
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def curvature_torsion_at(
    p_t: Point3, p_t1: Point3, p_t2: Point3, p_t3: Point3,
    min_speed: float = DEFAULT_MIN_SPEED,
    min_curvature: float = DEFAULT_MIN_CURVATURE,
) -> Dict[str, float]:
    """Jeden punkt: krzywizna kappa i torsja Freneta-Serreta tau, liczone
    z 4 kolejnych probek trajektorii (v/a/j roznicami skonczonymi).
    Identyczne matematycznie z THE_GEO_PRO_4D() w
    THE_TIMDR_Hyperflow_Engine/the_geo_pro_4d.py -- powielone tu (nie
    zaimportowane), bo GIA-TIMDR i THE_TIMDR_Hyperflow_Engine sa
    osobnymi repo bez wspolnej zaleznosci pakietowej; ten sam wzorzec
    co the_geo_pro_4d.py samo stosuje wobec FLIGHT-TRACKING-TIMDR
    (matematycznie identyczne, zweryfikowane numerycznie, osobna kopia
    kodu z jawnym odnosnikiem)."""
    v = _sub(p_t, p_t1)
    v1 = _sub(p_t1, p_t2)
    a = _sub(v, v1)
    a1 = _sub(v1, _sub(p_t2, p_t3))
    j = _sub(a, a1)

    speed = _norm(v)
    if speed < min_speed:
        return {"gated": True, "curvature": 0.0, "torsion": 0.0}

    cross_va = _cross(v, a)
    cross_norm = _norm(cross_va)
    kappa = cross_norm / speed ** 3

    if kappa < min_curvature:
        tau = 0.0
    else:
        tau = _dot(cross_va, j) / cross_norm ** 2

    return {"gated": False, "curvature": kappa, "torsion": tau}


def trefoil_points(n: int = 300) -> Tuple[np.ndarray, np.ndarray]:
    """Klasyczny trojwezel (trefoil knot), probkowany rownomiernie po
    parametrze t w [0, 2*pi). Ma naturalna symetrie 3-krotna -- trzy
    "wezly"/loby przy t = 0, 2*pi/3, 4*pi/3.

    Zwraca (t, pts) gdzie pts.shape == (n, 3).
    """
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    x = np.sin(t) + 2 * np.sin(2 * t)
    y = np.cos(t) - 2 * np.cos(2 * t)
    z = -np.sin(3 * t)
    return t, np.stack([x, y, z], axis=1)


def inject_node_deformation(
    pts: np.ndarray, t: np.ndarray, t0: float, amp: float, width: float,
) -> np.ndarray:
    """Lokalne odksztalcenie (gaussowski 'bump' w osi z, poprzecznie do
    plaszczyzny xy) w okolicy parametru t0 -- model "deformacji wezla"
    z hipotezy uzytkownika. Odleglosc liczona CYKLICZNIE (min(|t-t0|,
    2*pi-|t-t0|)), bo trojwezel jest zamknieta krzywa -- odksztalcenie
    przy t0=0 poprawnie obejmuje probki blisko obu koncow tablicy, nie
    tylko jeden brzeg."""
    pts2 = pts.copy()
    d = np.minimum(np.abs(t - t0), 2 * np.pi - np.abs(t - t0))
    bump = amp * np.exp(-(d ** 2) / (2 * width ** 2))
    pts2[:, 2] += bump
    return pts2


def compute_kappa_tau(
    pts: np.ndarray,
    min_speed: float = DEFAULT_MIN_SPEED,
    min_curvature: float = DEFAULT_MIN_CURVATURE,
) -> Tuple[np.ndarray, np.ndarray]:
    """Krzywizna i torsja dla calej trajektorii (pierwsze 3 probki maja
    NaN -- brak 4 kolejnych punktow potrzebnych do liczenia v/a/j)."""
    n = len(pts)
    kappas = np.full(n, np.nan)
    taus = np.full(n, np.nan)
    for i in range(3, n):
        r = curvature_torsion_at(
            tuple(pts[i]), tuple(pts[i - 1]), tuple(pts[i - 2]), tuple(pts[i - 3]),
            min_speed=min_speed, min_curvature=min_curvature,
        )
        kappas[i] = r["curvature"]
        taus[i] = r["torsion"]
    return kappas, taus


def _is_anomaly(series: np.ndarray, mean: float, std: float) -> np.ndarray:
    """Identyczny wzor jak AdaptiveThresholds.is_anomaly() w
    synoptyk-v2.0/analyzer/adaptive_thresholds.py: poza mean +- 2*std."""
    return (series > mean + 2 * std) | (series < mean - 2 * std)


def _is_defect(series: np.ndarray, p10: float, p90: float) -> np.ndarray:
    """Identyczny wzor jak AdaptiveThresholds.is_defect(): skok miedzy
    kolejnymi probkami > 0.3*(p90-p10)."""
    thr = 0.3 * (p90 - p10) if (p90 - p10) > 0 else 1.0
    d = np.abs(np.diff(series, prepend=series[0]))
    return d > thr


def detect_channels(pts: np.ndarray, t: np.ndarray) -> Dict[str, np.ndarray]:
    """Liczy 3 kanaly (krzywizna, torsja, odchylenie pozycji od
    centroidu) i dla kazdego zwraca boolowska flage anomalia-LUB-defekt
    (ta sama logika progowa co adaptive_thresholds.py). Punkty z NaN
    (pierwsze 3 probki) sa traktowane jako "brak wykrycia", nie
    propagowane jako fałszywe alarmy."""
    kappa, tau = compute_kappa_tau(pts)
    pos_dev = np.linalg.norm(pts - pts.mean(axis=0), axis=1)

    flags: Dict[str, np.ndarray] = {}
    for name, series in (("curvature", kappa), ("torsion", tau), ("pos_dev", pos_dev)):
        valid = ~np.isnan(series)
        f = np.zeros(len(series), dtype=bool)
        s = series[valid]
        mean, std = float(np.mean(s)), float(np.std(s))
        p10, p90 = float(np.percentile(s, 10)), float(np.percentile(s, 90))
        f[valid] = _is_anomaly(s, mean, std) | _is_defect(s, p10, p90)
        flags[name] = f
    return flags


def rezonans(flags: Dict[str, np.ndarray], k: int = 2) -> np.ndarray:
    """Koincydencja >= k z len(flags) kanalow jednoczesnie -- ta sama
    logika K-z-N co rezonans-M w synoptyk-v2.0 (DEFAULT_RESONANCE_K=3
    z 5 parametrow pogodowych tam; tu K=2 z 3 kanalow geometrycznych,
    bo tylko 3 kanaly sa w ogole zdefiniowane dla tego modelu)."""
    coincidence = sum(v.astype(int) for v in flags.values())
    return coincidence >= k


def nearest_sample_to_t0(t: np.ndarray, t0: float) -> int:
    """Indeks probki najblizszej parametrowi t0 (pomocnicze do testow
    lokalizacji)."""
    return int(np.argmin(np.abs(t - t0)))
