# tests/test_real_chrono_membrane_bridge_v0_2.py
"""Testy jednostkowe dla core/real_chrono_membrane_bridge_v0_2.py --
patrz docs/geometry/PREREG_CHRONO_MEMBRANE_BEARING_v0.2.md. Sprawdzaja
WYLACZNIE mechanike podzialu na polowy i klasyfikacji (funkcje
pomocnicze), NIE powtarzaja calego testu na realnych danych CWRU
(ten jest uruchamiany jako skrypt, wyniki w RESULT_..._v0.2.md).
"""
import os
import sys

import numpy as np
import pytest

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_THIS_DIR)
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from core.real_chrono_membrane_bridge_v0_2 import (  # noqa: E402
    split_signals_in_half,
    _segment_pool,
    _sample_windows,
    run_group_test,
)


def test_split_signals_in_half_covers_full_length_without_overlap():
    signals = {"DE": np.arange(101, dtype=float), "FE": np.arange(101, dtype=float) * 2}
    first, second = split_signals_in_half(signals)
    for ch in ("DE", "FE"):
        assert len(first[ch]) + len(second[ch]) == 101 or len(first[ch]) + len(second[ch]) == 100
        # n // 2 split: first half floor(n/2), second half the remainder
        assert len(first[ch]) == 50
        assert len(second[ch]) == 51
        combined = np.concatenate([first[ch], second[ch]])
        assert np.array_equal(combined, signals[ch])


def test_split_signals_in_half_even_length():
    signals = {"DE": np.arange(200, dtype=float), "FE": np.arange(200, dtype=float)}
    first, second = split_signals_in_half(signals)
    assert len(first["DE"]) == 100
    assert len(second["DE"]) == 100
    # non-overlapping: first is strictly the first 100, second the last 100
    assert first["DE"][-1] == 99
    assert second["DE"][0] == 100


def test_split_signals_in_half_rejects_mismatched_lengths():
    signals = {"DE": np.zeros(10), "FE": np.zeros(11)}
    with pytest.raises(ValueError):
        split_signals_in_half(signals)


def test_segment_pool_no_overlap_and_correct_count():
    signals = {"DE": np.arange(500, dtype=float), "FE": np.arange(500, dtype=float)}
    pool = _segment_pool(signals, ["DE", "FE"], window_size=100)
    assert len(pool) == 5
    # windows in order, non-overlapping
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
    # pos (normal) ma wyzsza korelacje miedzy kanalami niz neg (fault):
    # symulujemy przez konstrukcje sygnalow wprost, nie przez membrane_window_metrics
    # (uzywamy dw ch szeregow bardzo skorelowanych dla "normal" i niezaleznych dla "fault")
    def corrated_pair(n):
        base = rng.normal(0, 1, n)
        return [base + rng.normal(0, 0.01, n), base + rng.normal(0, 0.01, n)]

    def independent_pair(n):
        return [rng.normal(0, 1, n), rng.normal(0, 1, n)]

    pos_pool = [corrated_pair(128) for _ in range(40)]
    neg_pool = [independent_pair(128) for _ in range(40)]

    row = run_group_test(pos_pool, neg_pool, "spectral_concentration", seed=0)
    assert row["status"] == "SUPPORTED"
    assert row["r"] > 0
    assert row["p"] < 0.05


def test_run_group_test_inconclusive_when_too_few_valid():
    pool_small = [[np.array([1.0, 2.0]), np.array([1.0, 2.0])] for _ in range(3)]
    row = run_group_test(pool_small, pool_small, "spectral_concentration", n_windows=3, seed=0)
    assert row["status"] == "INCONCLUSIVE"
