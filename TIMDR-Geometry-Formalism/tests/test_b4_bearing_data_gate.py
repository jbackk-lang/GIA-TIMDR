import numpy as np
import pytest

from timdr_geometry.b4_bearing_data_gate import (
    assess_measured_sensor_mesh,
    load_synchronous_cwru_channels,
)


def test_loads_same_recording_channels_on_explicit_sample_grid(tmp_path):
    path = tmp_path / "bearing.npz"
    np.savez(path, DE=np.array([[1.0], [2.0], [3.0]]), FE=np.array([4.0, 5.0, 6.0]), BA=np.array([7.0, 8.0, 9.0]))

    record = load_synchronous_cwru_channels(path, sample_rate_hz=12_000.0)

    assert np.array_equal(record.time, np.array([0.0, 1 / 12_000, 2 / 12_000]))
    assert tuple(record.signals) == ("DE", "FE", "BA")


def test_rejects_missing_or_misaligned_channels(tmp_path):
    missing = tmp_path / "missing.npz"
    np.savez(missing, DE=np.ones(3), FE=np.ones(3))
    with pytest.raises(ValueError, match="BA"):
        load_synchronous_cwru_channels(missing)

    unequal = tmp_path / "unequal.npz"
    np.savez(unequal, DE=np.ones(3), FE=np.ones(2), BA=np.ones(3))
    with pytest.raises(ValueError, match="identycznej"):
        load_synchronous_cwru_channels(unequal)


def test_three_sensor_triplet_is_not_a_weingarten_mesh():
    result = assess_measured_sensor_mesh(
        sensor_coordinates=np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]),
        faces=np.array([[0, 1, 2]]),
        n_signal_channels=3,
    )

    assert not result.ready
    assert any("co najmniej 4" in reason for reason in result.reasons)


def test_measured_closed_four_node_mesh_is_ready():
    result = assess_measured_sensor_mesh(
        sensor_coordinates=np.array(
            [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
        ),
        faces=np.array([[0, 1, 2], [0, 3, 1], [0, 2, 3], [1, 3, 2]]),
        n_signal_channels=4,
    )

    assert result.ready
