# core/trefoil_weather_embedding_validation.py
"""
trefoil_weather_embedding_validation.py -- uczciwa, kontrolowana
walidacja pomyslu "zanurzyc 3 realne parametry pogodowe jako (x,y,z)
'trajektorii' i liczyc kappa/tau tak jak dla trojwezla" na REALNYCH
danych Krakow_Centrum (synoptyk-v2.0/krakow_forecast_snapshots.csv).

KONTEKST: wstepny test (rozmowa, nie w kodzie) na 24 punktach serii
prognoz (lead_days=1) znalazl 2 dni oznaczone jako "anomalia
geometryczna" (2026-08-27/28), NIE pokrywajace sie z plaska detekcja
per-parametr. Zanim uznano to za realny wynik, przetestowano to
protokolem timdr-signal-framework SS2 (kontrola pozytywna + negatywna,
NIE akceptuj wyniku bez sprawdzenia mocy testu) -- WYNIK: hipoteza
NIE PRZESZLA obu kontroli. Ten modul jest kodem tej walidacji, nie
tylko proza -- patrz docs/geometry/TIMDR_Trefoil_RealDataValidation.md
dla pelnego opisu i interpretacji.

TRZY NIEZALEZNE PROBLEMY ZNALEZIONE (wszystkie potwierdzone tutaj):

1. ARTEFAKT LUK W PROBKOWANIU: na series z realnymi lukami do 4 dni
   (seria prognoz), probka TUZ PO duzej luce (>=2 dni) ma P(falszywa
   flaga geometryczna) = 4.1x wyzsze niz probka regularna -- na CZYSTYM
   SZUMIE, bez zadnej prawdziwej anomalii. Korekta na rzeczywisty
   uplyw czasu (dt-aware roznice skonczone) NIE usuwa tego efektu
   (przetestowano oddzielnie, patrz rozmowa) -- wyzsze pochodne
   (przyspieszenie, szarpniecie) pozostaja niestabilne numerycznie przy
   nierownym kroku, niezaleznie od poprawnego skalowania przez dt.

2. NIEROZROZNIALNOSC OD SZUMU: na series prawie codziennej (tylko 1
   luka 2-dniowa, seria realnych OBSERWACJI, nie prognoz) -- 3 flagi
   znalezione w realnych danych (2026-08-31, 09-03, 09-05, z dala od
   jedynej luki) sa STATYSTYCZNIE NIEODROZNIALNE od czystego szumu:
   P(>=3 falszywe flagi w jednej realizacji BEZ zadnej anomalii) = 0.60
   (3000 syntetycznych realizacji skorelowanego spaceru losowego o tej
   samej dlugosci i wzorcu probkowania).

3. MASKOWANIE PRZEZ MALA PROBKE (glowna przyczyna niskiego recall):
   prog mean+-2*std liczony z TEJ SAMEJ, malej probki (n~24-27), ktora
   jest testowana -- pojedynczy realny outlier (nawet bardzo duzy, do
   20 odchylen standardowych wstrzykniete jednoczesnie we wszystkich 3
   znormalizowanych parametrach) SAM zawyza wlasny prog wykrywania.
   Wynik: recall NIE rosnie z amplituda anomalii (9.2% przy amp=3,
   4.6% przy amp=20 -- MALEJE, bo wiekszy outlier bardziej zawyza wlasny
   prog). Prog odporny (mediana/MAD) czesciowo naprawia recall (~20-25%,
   teraz rosnie z amplituda), ale kosztem falszywych alarmow
   eksplodujacych do P(>=1 falszywa flaga)=0.997 na czystym szumie --
   sama dystrybucja kappa/tau z potrojnego roznicowania krotkiego,
   nie-gladkiego (podobnego do spaceru losowego) szeregu jest zbyt
   ciezko-ogonowa/niestabilna dla jakiegokolwiek prostego progu.

WNIOSEK: w przeciwienstwie do syntetycznego trojwezla
(core/trefoil_frenet_torsion.py -- gladka krzywa C^2, gesto probkowana,
N=300), ta sama matematyka zastosowana do KROTKIEGO (N~24-27),
NIEGLADKIEGO (losowo-podobnego) realnego szeregu pogodowego nie dziala.
To NIE jest problem kalibracji progu -- to fundamentalny problem
numerycznego roznicowania (trzykrotnego!) krotkiego, zaszumionego
szeregu: kazde kolejne roznicowanie (v->a->j) wzmacnia szum, a przy
n~25 probek nie ma zapasu danych, zeby to uśrednic.
"""
from __future__ import annotations

from typing import Callable, Tuple

import numpy as np


def kappa_tau_time_aware(pts: np.ndarray, t: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Krzywizna/torsja z roznic skonczonych UWZGLEDNIAJACYCH rzeczywisty
    uplyw czasu miedzy probkami (nie zaklada jednostkowego kroku, w
    przeciwienstwie do compute_kappa_tau() w
    trefoil_frenet_torsion.py -- tam bylo to bezpieczne zalozenie,
    poniewaz syntetyczny trojwezel jest probkowany rownomiernie po
    parametrze; realne dane pogodowe NIE sa rownomiernie probkowane)."""
    n = len(pts)
    kappas = np.full(n, np.nan)
    taus = np.full(n, np.nan)
    for i in range(3, n):
        dt1, dt2, dt3 = t[i] - t[i-1], t[i-1] - t[i-2], t[i-2] - t[i-3]
        v = (pts[i] - pts[i-1]) / dt1
        v1 = (pts[i-1] - pts[i-2]) / dt2
        v2 = (pts[i-2] - pts[i-3]) / dt3
        a = (v - v1) / ((dt1 + dt2) / 2)
        a1 = (v1 - v2) / ((dt2 + dt3) / 2)
        j = (a - a1) / ((dt1 + dt2 + dt3) / 3)
        speed = np.linalg.norm(v)
        if speed < 1e-9:
            continue
        cross = np.cross(v, a)
        cn = np.linalg.norm(cross)
        kappa = cn / speed ** 3
        kappas[i] = kappa
        taus[i] = np.dot(cross, j) / cn ** 2 if kappa > 1e-4 else 0.0
    return kappas, taus


def is_anomaly_meanstd(series: np.ndarray, k: float = 2.0) -> np.ndarray:
    """Oryginalny prog (identyczny z adaptive_thresholds.py w
    synoptyk-v2.0): mean +- k*std, liczone z TEJ SAMEJ probki."""
    mean, std = series.mean(), series.std()
    return (series > mean + k * std) | (series < mean - k * std)


def is_anomaly_median_mad(series: np.ndarray, k: float = 3.5) -> np.ndarray:
    """Prog odporny (mediana/MAD) -- test hipotezy maskowania (#3
    w docstring modulu)."""
    med = np.median(series)
    mad = np.median(np.abs(series - med)) * 1.4826
    if mad == 0:
        mad = 1e-9
    return np.abs(series - med) > k * mad


def flags_for(pts: np.ndarray, t: np.ndarray, anomaly_fn: Callable = is_anomaly_meanstd) -> np.ndarray:
    """Boolowska flaga anomalii geometrycznej (kappa LUB tau) dla calej
    serii, danym detektorem progowym."""
    n = len(pts)
    kappa, tau = kappa_tau_time_aware(pts, t)
    valid = ~np.isnan(kappa)
    flagged = np.zeros(n, dtype=bool)
    idxv = np.where(valid)[0]
    if len(idxv) == 0:
        return flagged
    flagged[idxv] = anomaly_fn(kappa[valid]) | anomaly_fn(tau[valid])
    return flagged


def gen_correlated_walk(n: int, rng: np.random.Generator, corr: float = 0.7) -> np.ndarray:
    """Syntetyczny, skorelowany spacer losowy 3 'parametrow' -- model
    null BEZ zadnej wstrzknietej anomalii, imitujacy trwalosc pogody
    (kolejne dni skorelowane) na potrzeby kontroli negatywnej/mocy
    testu. Zwraca zestandaryzowane (z-score) wspolrzedne."""
    base = np.cumsum(rng.normal(0, 1, n))
    p1 = base + rng.normal(0, 1, n) * np.sqrt(1 - corr)
    p2 = -0.5 * base + rng.normal(0, 1, n) * np.sqrt(1 - corr) * 2 + np.cumsum(rng.normal(0, 0.3, n))
    p3 = 0.3 * base + np.cumsum(rng.normal(0, 0.5, n))
    pts = np.stack([p1, p2, p3], axis=1)
    return (pts - pts.mean(axis=0)) / pts.std(axis=0)
