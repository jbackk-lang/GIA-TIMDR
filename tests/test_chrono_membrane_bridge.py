# tests/test_chrono_membrane_bridge.py
"""Smoke test dla core/chrono_membrane_bridge.py PO refaktoryzacji.

Rdzen matematyczny (macierz korelacji, widmo, metryki, generatory
syntetyczne, bramka kontrolna) zostal wydzielony do
timdr_geometry.spectral_family w TIMDR-Geometry-Formalism -- pelne
testy jednostkowe tych funkcji sa teraz w
TIMDR-Geometry-Formalism/tests/test_spectral_family.py.

Ten plik sprawdza WYLACZNIE, ze core/chrono_membrane_bridge.py
(cienki wrapper, punkt wejscia specyficzny dla PREREG lozysk CWRU)
nadal poprawnie importuje sie i re-eksportuje wszystkie nazwy, na
ktorych zaleznych sa core/real_chrono_membrane_bridge*.py oraz
core/chrono_trumpet_spectrum.py -- czyli ze refaktoryzacja nie
zlamala wstecznej kompatybilnosci API.
"""
import os
import sys

import numpy as np

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_THIS_DIR)
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from core.chrono_membrane_bridge import (  # noqa: E402
    channel_correlation_matrix,
    spectrum_from_correlation,
    spectral_concentration,
    participation_ratio,
    membrane_window_metrics,
    make_growing_shared,
    make_independent_noise,
    make_constant_shared,
    MembraneControlResult,
    run_membrane_controls,
    run_synthetic_controls,
    format_synthetic_report,
)


def test_wrapper_exports_are_importable_and_callable():
    # dokladnie te nazwy, ktorych uzywaja core/real_chrono_membrane_bridge*.py
    # (membrane_window_metrics) i core/chrono_trumpet_spectrum.py
    # (channel_correlation_matrix, spectrum_from_correlation) -- import
    # powyzej juz by sie wywalil, gdyby ktoregos brakowalo.
    rng = np.random.default_rng(0)
    chans = [rng.normal(0, 1, 64) for _ in range(2)]
    m = membrane_window_metrics(chans)
    assert set(m.keys()) == {"spectral_concentration", "participation_ratio", "membrane_spectral_ratio"}


def test_wrapper_run_synthetic_controls_end_to_end_smoke():
    # mala, szybka wersja (nie pelna PREREG siatka) -- tylko sprawdza,
    # ze bramka kontrolna dziala end-to-end przez wrapper.
    result = run_membrane_controls(n_channels=2, n_windows=10, window_size=128, seed=0)
    assert isinstance(result, MembraneControlResult)
    assert result.n_total == 10
