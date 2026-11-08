from experiments.phase_recovery_probe import run


def test_phase_step_is_not_removed_by_frequency_only_concept():
    result = run()
    during = result["pure_phase_step"]["during"]
    after = result["pure_phase_step"]["after"]
    # Phase follows the stepped signal, but the phase offset relative to the
    # original reference remains. That is not phase restoration.
    assert during["phase_error_vs_nominal_rms_rad"] > 1.0
    assert after["phase_error_vs_nominal_rms_rad"] > 1.0


def test_frequency_return_does_not_erase_accumulated_phase_offset():
    result = run()
    after = result["temporary_detune_then_return"]["after"]
    assert after["frequency_error_rms_hz"] < 0.2
    assert after["phase_error_vs_nominal_rms_rad"] > 0.5


def test_payload_sentinel_is_unchanged_but_not_reconstructed():
    result = run()
    assert result["payload_digest_unchanged"] is True
    assert "not_information_recovery" in result["status"]
