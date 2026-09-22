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

REFAKTORYZACJA (bez zmiany logiki/zachowania): rdzen matematyczny
(macierz korelacji, widmo, metryki, generatory syntetyczne, bramka
kontrolna, raportowanie) zostal wydzielony do reuzywalnego,
domenowo-agnostycznego modulu `timdr_geometry.spectral_family` w
sister-repo TIMDR-Geometry-Formalism (scalonym jako podkatalog tego
repo), zeby latwiej bylo go dopasowac/reuzyc w innych konstrukcjach
(np. core/chrono_trumpet_spectrum.py juz go uzywa bezposrednio). Ten
plik zostaje jako cienki wrapper/punkt wejscia specyficzny dla tej
konkretnej historii badawczej (lozyska CWRU, PREREG v0.1) -- importuje
wszystko z nowej lokalizacji i zachowuje dokladnie to samo API
(core/real_chrono_membrane_bridge*.py oraz core/chrono_trumpet_spectrum.py
nadal importuja stad bez zadnych zmian).
"""
from __future__ import annotations

import os
import sys
import time

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_THIS_DIR)
_GEOMETRY_FORMALISM = os.path.join(_REPO_ROOT, "TIMDR-Geometry-Formalism")
for _p in (_REPO_ROOT, _GEOMETRY_FORMALISM):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from timdr_geometry.spectral_family import (  # noqa: E402
    EDGE_FRACTION,
    OMEGA_SHARED,
    channel_correlation_matrix,
    spectrum_from_correlation,
    spectral_concentration,
    participation_ratio,
    membrane_window_metrics,
    GROWTH_RATE,
    NOISE_STD,
    SHARED_K_CONST,
    make_growing_shared,
    make_independent_noise,
    make_constant_shared,
    MembraneControlResult,
    MIN_VALID_FRAC,
    run_membrane_controls,
    SYN_WINDOW_SIZES,
    SYN_N_WINDOWS,
    SYN_SEED,
    SYN_ALPHA,
    SYN_N_CHANNELS,
    run_synthetic_controls,
    format_synthetic_report,
)

__all__ = [
    "EDGE_FRACTION",
    "OMEGA_SHARED",
    "channel_correlation_matrix",
    "spectrum_from_correlation",
    "spectral_concentration",
    "participation_ratio",
    "membrane_window_metrics",
    "GROWTH_RATE",
    "NOISE_STD",
    "SHARED_K_CONST",
    "make_growing_shared",
    "make_independent_noise",
    "make_constant_shared",
    "MembraneControlResult",
    "MIN_VALID_FRAC",
    "run_membrane_controls",
    "SYN_WINDOW_SIZES",
    "SYN_N_WINDOWS",
    "SYN_SEED",
    "SYN_ALPHA",
    "SYN_N_CHANNELS",
    "run_synthetic_controls",
    "format_synthetic_report",
]


if __name__ == "__main__":
    t0 = time.time()
    rows = run_synthetic_controls()
    print(format_synthetic_report(rows))
    print(f"Czas: {time.time()-t0:.2f}s")
