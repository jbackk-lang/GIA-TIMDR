# tests/test_real_chrono_membrane_bridge_independent.py
"""Testy jednostkowe dla core/real_chrono_membrane_bridge_independent.py.

Sprawdzaja WYLACZNIE mechanike pomocnicza (segmentacja, próbkowanie,
klasyfikacja grupowa) -- IDENTYCZNA logika co
tests/test_real_chrono_membrane_bridge_v0_2.py, bo funkcje pomocnicze sa
1:1 przeniesione. NIE powtarzaja calego testu na realnych danych CWRU
(dane zrodlowe -- CWRU_Bearing_NumPy_4LUM-main.zip -- zyja WYLACZNIE w
/tmp poza tym repo, wg instrukcji zadania; pelny wynik na realnych
danych jest w docs/geometry/RESULT_CHRONO_MEMBRANE_BEARING_
INDEPENDENT_CONFIRMATION.md, wygenerowany jednorazowo skryptem
`python core/real_chrono_membrane_bridge_independent.py`)."""
import os
import sys

import numpy as np
import pytest

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_THIS_DIR)
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from core.real_chrono_membrane_bridge_independent import (  # noqa: E402
    _segment_pool,
    _sample_windows,
    run_group_test,
    NORMAL_FILES,
    FAULT_FILES,
    WINDOW_SIZES,
)


def test_segment_pool_no_overlap_and_correct_count():
    signals = {"DE": np.arange(500, dtype=float), "FE": np.arange(500, dtype=float)}
    pool = _segment_pool(signals, ["DE", "FE"], window_size=100)
    assert len(pool) == 5
    assert pool[0][0][0] == 0
    assert pool[1][0][0] == 100
    assert pool[-1][0][-1] == 499


def test_sample_windows_no_replacement_when_enough_available():
    pool = [[np.array([float(i)])] for i in range(50)]
    sampled = _sample_windows(pool, n_windows=30, seed=0)
    assert len(sampled) == 30
    values = [s[0][0] for s in sampled]
    assert len(set(values)) == 30  # bez powtorzen


def test_sample_windows_reuses_when_not_enough_available():
    pool = [[np.array([float(i)])] for i in range(5)]
    sampled = _sample_windows(pool, n_windows=30, seed=0)
    assert len(sampled) == 30


def test_run_group_test_detects_normal_greater_than_fault():
    rng = np.random.default_rng(0)

    def corrated_pair(n):
        base = rng.normal(0, 1, n)
        return [base + rng.normal(0, 0.01, n), base + rng.normal(0, 0.01, n)]

    def independent_pair(n):
        return [rng.normal(0, 1, n), rng.normal(0, 1, n)]

    pos_pool = [corrated_pair(128) for _ in range(40)]
    neg_pool = [independent_pair(128) for _ in range(40)]

    row = run_group_test(pos_pool, neg_pool, "spectral_concentration", seed_pos=0, seed_neg=1)
    assert row["status"] == "SUPPORTED"
    assert row["r"] > 0
    assert row["p"] < 0.05


def test_run_group_test_inconclusive_when_too_few_valid():
    pool_small = [[np.array([1.0, 2.0]), np.array([1.0, 2.0])] for _ in range(3)]
    row = run_group_test(pool_small, pool_small, "spectral_concentration", n_windows=3, seed_pos=0, seed_neg=1)
    assert row["status"] == "INCONCLUSIVE"


def test_selected_file_lists_are_disjoint_and_span_both_new_rpms():
    """Audyt wyboru plikow (PREREG-owy, decyzja podjeta PRZED wynikiem):
    2 pliki normal (1730/1750), 6 plikow fault obejmujacych oba RPM,
    >=3 rozne typy uszkodzenia, >=3 rozne rozmiary."""
    assert len(NORMAL_FILES) == 2
    assert any("1730" in f for f in NORMAL_FILES)
    assert any("1750" in f for f in NORMAL_FILES)
    assert len(FAULT_FILES) == 6
    assert set(NORMAL_FILES).isdisjoint(set(FAULT_FILES.values()))
    fault_types = {name.split("_")[1] for name in FAULT_FILES}
    assert fault_types.issuperset({"IR", "B", "OR6", "OR3"})
    assert any("1730" in f for f in FAULT_FILES.values())
    assert any("1750" in f for f in FAULT_FILES.values())


def test_window_sizes_match_frozen_methodology():
    assert WINDOW_SIZES == (128, 256, 512)


@pytest.mark.skipif(
    not all(os.path.exists(f) for f in list(NORMAL_FILES) + list(FAULT_FILES.values())),
    reason="dane zrodlowe CWRU_Bearing_NumPy_4LUM zyja w /tmp/cwru_fresh, poza tym repo",
)
def test_real_data_loadable_and_has_de_fe_channels():
    from core.real_chrono_membrane_bridge_independent import load_pools
    normal_pool, fault_pool_combined, fault_pool_per_type, _, _ = load_pools(window_size=512)
    assert len(normal_pool) > 30
    assert len(fault_pool_combined) > 30
    assert len(fault_pool_per_type) == 6
    for seg in normal_pool[0]:
        assert len(seg) == 512
