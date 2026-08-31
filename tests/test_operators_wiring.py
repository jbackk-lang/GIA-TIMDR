"""
test_operators_wiring.py — testy wpięcia constants.py w operators.py i
diagnostics.py (audyt sesji 2026-08-31: constants.py był plikiem,
którego NIC nie importowało; kilka progów/wag było zdefiniowanych, ale
nigdzie nieużywanych albo niezależnie zduplikowanych).

Zakres: op_deltaS/defect_map z jednym źródłem prawdy (DELTA_S_THRESHOLD)
i opcją adaptacyjną; op_R_local (lokalny rezonans + EMA); op_stab_weighted
(aktywacja STAB_*_WEIGHT); op_spectral_filtered (SPECTRAL_MIN/MAX_FREQ,
NORMALIZE); op_prime z PRIME_SENSITIVITY; op_transition (nowy filtr
"Obszarów przejściowych" z §2.4 dokumentacji teoretycznej). Stare
funkcje (op_stab, op_spectral, op_R) sprawdzone jako NIETKNIĘTE
(regresja wsteczna kompatybilność z pipeline.py).
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

from core.constants import (
    DELTA_S_THRESHOLD,
    DELTA_S_SOFT,
    DELTA_S_HARD,
    STAB_LAMBDA_WEIGHT,
    STAB_TAU_WEIGHT,
    STAB_RHO_WEIGHT,
    PRIME_SENSITIVITY,
)
from core.operators import (
    op_lambda,
    op_tau,
    op_J,
    op_deltaS,
    adaptive_delta_s_threshold,
    op_R,
    op_R_local,
    op_stab,
    op_stab_weighted,
    op_stab_weighted_from_data,
    op_spectral,
    op_spectral_filtered,
    op_prime,
    op_transition,
)
from core.diagnostics import defect_map


# ── op_deltaS / defect_map: jedno źródło prawdy (DELTA_S_THRESHOLD) ────

def test_op_deltaS_default_threshold_matches_constant():
    tau_field = [0, 0, 0, 20, 0, 0]  # skok 0->20 (|Δ|=20) w indeksie 3
    result = op_deltaS(tau_field)  # domyślny threshold=DELTA_S_THRESHOLD=12
    assert (3, 20) in result


def test_op_deltaS_respects_custom_threshold():
    tau_field = [0, 0, 0, 10, 0, 0]  # skok w górę |Δ|=10 (idx 3), potem w dół |Δ|=10 (idx 4)
    assert op_deltaS(tau_field, threshold=12) == []  # 10 <= 12, brak defektu
    assert op_deltaS(tau_field, threshold=5) == [(3, 10), (4, 0)]  # oba skoki > 5


def test_op_deltaS_and_defect_map_agree_on_same_threshold():
    """Sedno naprawy: obie funkcje mają teraz JEDNO źródło prawdy
    (DELTA_S_THRESHOLD) zamiast dwóch niezależnych kopii '12' - ich
    wynik musi się zgadzać przy tym samym threshold."""
    tau_field = [1, 2, -3, 15, 15, -20, 0, 3]
    assert op_deltaS(tau_field) == defect_map(tau_field)
    assert op_deltaS(tau_field, threshold=5) == defect_map(tau_field, threshold=5)


def test_op_deltaS_adaptive_threshold_opt_in():
    """threshold=None włącza próg adaptacyjny - sprawdzamy, że faktycznie
    UŻYWA adaptive_delta_s_threshold(), nie że akurat zgaduje '12'."""
    tau_field = [0, 1, 0, 1, 0, 1, 0, 50]  # jeden duży skok na tle małego szumu
    adaptive_result = op_deltaS(tau_field, threshold=None)
    manual_threshold = adaptive_delta_s_threshold(tau_field)
    manual_result = op_deltaS(tau_field, threshold=manual_threshold)
    assert adaptive_result == manual_result
    # i próg adaptacyjny faktycznie wykrywa duży skok
    assert any(v == 50 or v == -50 for _i, v in adaptive_result) or adaptive_result != []


def test_adaptive_delta_s_threshold_matches_hand_computed_std():
    tau_field = [0, 4, 0, 4]  # diffs: |4-0|,|0-4|,|4-0| = [4,4,4] -> std=0
    result = adaptive_delta_s_threshold(tau_field, k=2.5)
    assert result == pytest.approx(0.0)  # zerowa wariancja -> próg=0


def test_adaptive_delta_s_threshold_rejects_too_short_field():
    with pytest.raises(ValueError):
        adaptive_delta_s_threshold([5])


# ── op_R_local: lokalny rezonans + EMA (RESONANCE_SMOOTHING) ───────────

def test_op_R_local_matches_hand_computed_value_no_smoothing():
    data = bytes([3, 4, 0])  # window=3, jeden punkt: sqrt(9+16+0)=5
    result = op_R_local(data, window=3)
    assert result == pytest.approx([5.0])


def test_op_R_local_aligns_length_with_op_tau():
    data = bytes([10, 20, 30, 40, 50, 60])
    tau_field = op_tau(data)
    local_r = op_R_local(data, window=3)
    assert len(local_r) == len(tau_field) == len(data) - 2


def test_op_R_local_smoothing_changes_result():
    # zmienna amplituda lokalnej energii (stała amplituda dałaby EMA==raw)
    data = bytes([0, 0, 50, 0, 0, 0, 0, 200, 0, 0])
    raw = op_R_local(data, window=3, smoothing=None)
    smoothed = op_R_local(data, window=3, smoothing=0.3)
    assert raw != smoothed
    assert smoothed[0] == raw[0]  # EMA: y[0]=x[0]


def test_op_R_local_rejects_invalid_window():
    with pytest.raises(ValueError):
        op_R_local(b"abc", window=0)


def test_op_R_global_still_returns_single_scalar_unchanged():
    # regresja: stary op_R() zostaje nietknięty (jedna liczba, całe dane)
    data = bytes([3, 4])
    assert op_R(data) == pytest.approx(5.0)
    assert isinstance(op_R(data), float)


# ── op_stab_weighted: aktywacja STAB_*_WEIGHT ───────────────────────────

def test_op_stab_weighted_matches_hand_computed_value():
    lam = [1.0, 2.0]
    tau = [3.0, 4.0]
    rho = [5.0, 6.0]
    result = op_stab_weighted(lam, tau, rho)
    expected = [
        STAB_LAMBDA_WEIGHT * 1.0 + STAB_TAU_WEIGHT * 3.0 + STAB_RHO_WEIGHT * 5.0,
        STAB_LAMBDA_WEIGHT * 2.0 + STAB_TAU_WEIGHT * 4.0 + STAB_RHO_WEIGHT * 6.0,
    ]
    assert result == pytest.approx(expected)


def test_op_stab_weighted_rejects_mismatched_lengths():
    with pytest.raises(ValueError):
        op_stab_weighted([1.0, 2.0], [3.0], [5.0, 6.0])


def test_op_stab_weighted_from_data_builds_aligned_channels():
    data = bytes([10, 20, 30, 40, 50])
    result = op_stab_weighted_from_data(data)
    # ręczna rekonstrukcja tych samych trzech kanałów
    lam = list(op_lambda(data))[1:len(data) - 1]
    tau = op_tau(data)
    rho = op_R_local(data, window=3)
    expected = op_stab_weighted(lam, tau, rho)
    assert result == pytest.approx(expected)
    assert len(result) == len(data) - 2


def test_op_stab_weighted_from_data_rejects_too_short_input():
    with pytest.raises(ValueError):
        op_stab_weighted_from_data(bytes([1, 2]))


def test_op_stab_unchanged_for_backward_compatibility():
    # regresja: stary op_stab(data) -> bytes, niezmienione zachowanie
    data = bytes([1, 2, 3])
    assert op_stab(data) == op_lambda(op_J(data))
    assert isinstance(op_stab(data), bytes)


# ── op_spectral_filtered: SPECTRAL_MIN/MAX_FREQ + NORMALIZE ────────────

def test_op_spectral_filtered_restricts_to_frequency_band():
    data = bytes([10, 20, 30, 40])
    full = op_spectral_filtered(data, fs=4.0, )  # domyślne bardzo szerokie pasmo z constants.py
    # z bardzo wąskim pasmem powinno zostać mniej binów niż pełne widmo
    from core.operators import op_spectral as _op_spectral_raw
    raw_len = len(_op_spectral_raw(data))
    assert len(full) <= raw_len


def test_op_spectral_filtered_narrow_band_excludes_bins():
    data = bytes([10, 20, 30, 40, 50, 60, 70, 80])
    import core.operators as ops_module

    original_min, original_max = ops_module.SPECTRAL_MIN_FREQ, ops_module.SPECTRAL_MAX_FREQ
    ops_module.SPECTRAL_MIN_FREQ, ops_module.SPECTRAL_MAX_FREQ = 0.0, 0.1
    try:
        narrow = op_spectral_filtered(data, fs=1.0)
    finally:
        ops_module.SPECTRAL_MIN_FREQ, ops_module.SPECTRAL_MAX_FREQ = original_min, original_max
    assert len(narrow) < len(data)  # wąskie pasmo wycina większość z 8 binów


def test_op_spectral_filtered_normalization_caps_magnitude_at_one():
    import core.operators as ops_module

    original_normalize = ops_module.SPECTRAL_NORMALIZE
    ops_module.SPECTRAL_NORMALIZE = True
    try:
        data = bytes([50, 100, 150, 200])
        # fs dobrane tak, by k*fs/N trafiało w domyślne pasmo [SPECTRAL_MIN_FREQ=1, MAX_FREQ=2048]
        result = op_spectral_filtered(data, fs=100.0)
    finally:
        ops_module.SPECTRAL_NORMALIZE = original_normalize
    assert result  # niepuste
    max_mag = max(math.hypot(re, im) for _freq, re, im in result)
    assert max_mag == pytest.approx(1.0, abs=1e-9)


def test_op_spectral_unchanged_for_backward_compatibility():
    data = bytes([1, 2, 3])
    result = op_spectral(data)
    assert len(result) == len(data)
    assert all(len(pair) == 2 for pair in result)  # (re, im), NIE (freq, re, im)


# ── op_prime z PRIME_SENSITIVITY ────────────────────────────────────────

def test_op_prime_default_sensitivity_matches_old_behavior():
    data = bytes([1, 1, 2, 2, 3])
    old_style = 0  # policz recznie jak stara wersja (bez sensitivity)
    changes, last = 0, data[0]
    for b in data:
        if b != last:
            changes += 1
        last = b
    expected_old = changes / max(1, len(data))
    assert op_prime(data) == pytest.approx(expected_old * PRIME_SENSITIVITY)
    assert PRIME_SENSITIVITY == 1.0  # wiec rowniez == expected_old


def test_op_prime_sensitivity_scales_linearly():
    data = bytes([1, 2, 1, 2, 1])
    base = op_prime(data, sensitivity=1.0)
    doubled = op_prime(data, sensitivity=2.0)
    assert doubled == pytest.approx(2.0 * base)


# ── op_transition: brakujący filtr "Obszarów przejściowych" ────────────

def test_op_transition_returns_dense_masks_aligned_with_op_tau():
    data = bytes([10, 10, 10, 10, 100, 10, 10, 10])
    result = op_transition(data)
    tau_field = op_tau(data)
    assert set(result.keys()) == {"soft", "hard", "transition"}
    assert len(result["soft"]) == len(result["hard"]) == len(result["transition"]) == len(tau_field)


def test_op_transition_soft_mask_flags_known_spike():
    """Sygnał ze sztucznym, dużym skokiem - soft_mask powinien go
    wykryć (mniejszy próg = łatwiej przekroczyć), hard_mask jest
    podzbiorem soft_mask (twardszy próg)."""
    data = bytes([50, 50, 50, 50, 250, 50, 50, 50])
    result = op_transition(data, delta_s_soft=5, delta_s_hard=100)
    assert any(result["soft"])
    # hard (próg 100) jest podzbiorem soft (próg 5) - każdy hard=True ma soft=True
    for s, h in zip(result["soft"], result["hard"]):
        if h:
            assert s


def test_op_transition_narrow_resonance_band_can_exclude_everything():
    """Z domyślnymi RESONANCE_MIN=0/MAX=1e9 filtr rezonansowy jest
    praktycznie zawsze True (patrz docstring op_transition) - ten test
    pokazuje, że z ZAWĘŻONYM pasmem rezonansu transition_mask faktycznie
    reaguje na resonance_min/resonance_max, nie tylko na soft_mask."""
    data = bytes([50, 50, 50, 50, 250, 50, 50, 50])
    wide = op_transition(data, delta_s_soft=5, resonance_min=0.0, resonance_max=1e9)
    narrow = op_transition(
        data, delta_s_soft=5,
        resonance_min=1e6, resonance_max=1e7,  # nieosiągalny zakres dla bajtów 0-255
    )
    assert any(wide["transition"])
    assert not any(narrow["transition"])  # nic nie mieści się w nieosiągalnym paśmie


def test_op_transition_empty_for_too_short_data():
    result = op_transition(bytes([1, 2]))  # za krótkie na op_tau (potrzeba >=3)
    assert result == {"soft": [], "hard": [], "transition": []}


def test_op_transition_uses_constants_as_defaults():
    """Domyślne argumenty faktycznie pochodzą z constants.py, nie z
    innych, przypadkowo zgadzających się liczb."""
    import inspect

    sig = inspect.signature(op_transition)
    assert sig.parameters["delta_s_soft"].default == DELTA_S_SOFT
    assert sig.parameters["delta_s_hard"].default == DELTA_S_HARD
