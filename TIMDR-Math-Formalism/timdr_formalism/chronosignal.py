"""
timdr_formalism/chronosignal.py

Czas jako sygnal: instancja generycznego obiektu x:T->R z gale
zi sygnalowej TIMDR (Axioms_S_TIMDR_Signal.md) na konkretny przypadek
"T = kolejne znaczniki czasu (timestamps)".

Nie wprowadza nowej matematyki ani nowych aksjomatow -- to jest wpisanie
sie w istniejaca definicje sygnalu z Chronoprocesu Xi=(T,x,Gamma,phi)
(pelny opis: GIA-TIMDR/docs/theory/TIMDR_Chronoprocess.md, sekcja 2;
skrot: GIA-TIMDR/SKILL_timdr-signal-framework.md, sekcja 5), z dwiema
rozdzielonymi seriami:

    tempo(t)  = t[i+1] - t[i]                        -- proces odstepow
    drift(t)  = tempo_zmierzone(t) - tempo_nominalne  -- wymaga zegara
                                                          referencyjnego

Detektory anomalia/defekt/skret ponizej sa samodzielna implementacja
definicji z sekcji 1 skilla timdr-signal-framework (ten konkretny kod
detektorow NIE istnial dotad w tym repo -- pipeline.py to warstwa
PROTOKOLU testowania numerologii/formalizmu, nie warstwa detektorow),
zastosowana tu do sygnalu tempa/driftu.

Konwencje (`m, s = series.mean(), series.std()` dla anomalii; p90-p10
jako skala dla defektu) sa dokladnie tymi samymi, ktorych uzywa
examples/real_weather_resonance_validation.py (anomaly_flags) i skill
paragraf 1 -- nie nowy wybor progu.

Walidacja wejścia jest częścią kontraktu modułu: znaczniki i serie muszą
być jednowymiarowe i skończone, a progi oraz nominalny odstęp muszą mieć
dopuszczalne wartości. Aktualny zestaw formalizmów M/S przeszedł w
GitHub Actions dla commitu `ec28c9bb`; testy automatyczne potwierdzają
zachowanie kodu w sprawdzonym zakresie, nie empiryczną skuteczność
detektorów na dowolnej domenie danych. Przykład
`examples/chronosignal_demo.py` pozostaje osobnym skryptem demonstracyjnym
i nie jest objęty tym wynikiem CI.
"""
from __future__ import annotations

from typing import Optional, Sequence

import numpy as np


def _finite_series(values: Sequence[float], name: str) -> np.ndarray:
    arr = np.asarray(values, dtype=float)
    if arr.ndim != 1 or arr.size == 0:
        raise ValueError(f"{name} musi byc niepusta seria 1D")
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"{name} musi zawierac wylacznie skonczone wartosci")
    return arr


# ---------------------------------------------------------------------
# Instancja sygnalu: tempo i drift
# ---------------------------------------------------------------------

def tempo(timestamps: Sequence[float]) -> np.ndarray:
    """tempo(t) = t[i+1] - t[i] -- seria odstepow miedzy kolejnymi
    znacznikami czasu. Dlugosc n-1 dla n znacznikow.

    Wymaga SCISLE rosnacych znacznikow -- nie sortuje ani nie
    deduplikuje sam, zeby blad kolejnosci zdarzen (dane wejsciowe nie w
    kolejnosci chronologicznej, albo zdublowany znacznik) nie zostal po
    cichu zamaskowany posortowaniem w srodku funkcji.
    """
    ts = _finite_series(timestamps, "timestamps")
    if ts.size < 2:
        raise ValueError("tempo() wymaga >= 2 znacznikow czasu")
    with np.errstate(over="ignore", invalid="ignore"):
        intervals = np.diff(ts)
    if not np.all(np.isfinite(intervals)):
        raise ValueError("odstepy czasu musza byc skonczone i reprezentowalne")
    if np.any(intervals <= 0):
        raise ValueError(
            "timestamps musza byc scisle rosnace -- posortuj/odduplikuj "
            "wejscie PRZED wywolaniem tempo(), nie w srodku"
        )
    return intervals


def drift(timestamps: Sequence[float], nominal_interval: float) -> np.ndarray:
    """drift(t) = tempo_zmierzone(t) - tempo_nominalne.

    Wymaga JAWNEGO zewnetrznego zegara referencyjnego
    (`nominal_interval`) -- bez niego drift jest formalnie
    niezdefiniowany (patrz dyskusja "naprawa M/S": tempo i drift to dwie
    OSOBNE wielkosci, tempo nie wymaga referencji, drift wymaga).
    """
    if not np.isfinite(nominal_interval) or nominal_interval <= 0:
        raise ValueError("nominal_interval musi byc skonczone i > 0")
    return tempo(timestamps) - nominal_interval


# ---------------------------------------------------------------------
# Detektory na dowolnym skalarnym sygnale x:T->R (tu: tempo()/drift())
# ---------------------------------------------------------------------

def anomalia_flags(
    series: Sequence[float],
    k: float = 2.0,
    reference_series: Optional[Sequence[float]] = None,
) -> np.ndarray:
    """Wykrywa |x - mean(reference)| > k*std(reference).

    Gdy reference_series=None, zachowuje historyczny tryb in-sample:
    srednia i odchylenie sa liczone z tego samego wektora. Ten tryb ma
    ograniczenie samowplywu: dla n<=5 i k=2 zaden element nie moze
    przekroczyc progu (max |z_i| <= sqrt(n-1)). Dla krotkich okien
    zalecany jest oddzielny reference_series, niezalezny od ocenianych
    probek. Gdy odchylenie referencji wynosi zero, kazda niezerowa
    roznica od stalej referencji jest flaga (scisly prog > 0).
    """
    s = _finite_series(series, "series")
    if s.size < 2:
        raise ValueError("anomalia_flags() wymaga >= 2 elementow")
    if not np.isfinite(k) or k < 0:
        raise ValueError("k musi byc skonczone i >= 0")
    if reference_series is None:
        reference = s
    else:
        reference = _finite_series(reference_series, "reference_series")
        if reference.size < 2:
            raise ValueError("reference_series wymaga >= 2 elementow")
    m, sd = reference.mean(), reference.std()
    return np.abs(s - m) > k * sd


def defekt_flags(series: Sequence[float], factor: float = 0.3) -> np.ndarray:
    """Skok |diff(series)_i| > factor*(p90-p10) -- maska dlugosci
    len(series)-1; flags[i] mowi o skoku miedzy series[i] i series[i+1].
    """
    s = _finite_series(series, "series")
    if s.size < 2:
        raise ValueError("defekt_flags() wymaga >= 2 elementow")
    if not np.isfinite(factor) or factor < 0:
        raise ValueError("factor musi byc skonczone i >= 0")
    p10, p90 = np.percentile(s, [10, 90])
    spread = p90 - p10
    # Nie zwracamy automatycznie samych False przy spread==0:
    # dla serii prawie stalej z rzadkim skokiem p10==p90, a literalny
    # prog wynosi zero i kazdy niezerowy skok powinien zostac wykryty.
    # Dla serii idealnie stalej diff==0, wiec scisle >0 nadal daje False.
    return np.abs(np.diff(s)) > factor * spread


def skret_flags(series: Sequence[float], factor: float = 1.5) -> np.ndarray:
    """Punkt zwrotny: znak lokalnego nachylenia (diff) zmienia sie miedzy
    dwoma kolejnymi krokami I wielkosc zmiany (|d[i+1]-d[i]|) przekracza
    factor*std(d), gdzie d=diff(series). Maska dlugosci len(series)-2;
    flags[i] odpowiada zwrotowi na styku d[i]/d[i+1] (czyli series[i+2]).

    Wymaga OBU sasiadujacych nachylen niezerowych, zeby plaski odcinek
    (d=0) nastepnie ruszajacy w dowolna strone nie liczyl sie jako
    "zwrot" -- to nie jest w oryginalnej definicji z sekcji 1 skilla,
    ale jest jawnym, udokumentowanym wyborem tej implementacji.
    """
    s = _finite_series(series, "series")
    if s.size < 3:
        raise ValueError("skret_flags() wymaga >= 3 elementow")
    if not np.isfinite(factor) or factor < 0:
        raise ValueError("factor musi byc skonczone i >= 0")
    d = np.diff(s)
    sign_d = np.sign(d)
    sign_flip = (sign_d[:-1] != sign_d[1:]) & (sign_d[:-1] != 0) & (sign_d[1:] != 0)
    magnitude = np.abs(d[1:] - d[:-1])
    sd = d.std()
    if sd == 0.0:
        return np.zeros(d.size - 1, dtype=bool)
    return sign_flip & (magnitude > factor * sd)
