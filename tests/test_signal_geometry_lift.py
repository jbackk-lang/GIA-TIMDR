import unittest
import numpy as np

from core.signal_geometry_lift import lift_phasor_to_3d, recover_phasor_coordinates


class SignalGeometryLiftTests(unittest.TestCase):
    def test_circular_phasor_with_linear_axis_is_a_helix_and_roundtrips(self):
        phase = np.linspace(0.0, 4.0 * np.pi, 401)
        amplitude = 2.5
        q1 = amplitude * np.cos(phase)
        q2 = amplitude * np.sin(phase)
        z = 0.3 * phase
        frame = np.eye(3)
        points = lift_phasor_to_3d(q1, q2, z, frame, origin=(1.0, -2.0, 0.5))
        r1, r2, rz = recover_phasor_coordinates(points, frame, origin=(1.0, -2.0, 0.5))
        np.testing.assert_allclose(r1, q1, atol=1e-12)
        np.testing.assert_allclose(r2, q2, atol=1e-12)
        np.testing.assert_allclose(rz, z, atol=1e-12)
        radius = np.hypot(points[:, 0] - 1.0, points[:, 1] + 2.0)
        np.testing.assert_allclose(radius, amplitude, atol=1e-12)
        self.assertAlmostEqual(z[-1] - z[0], 0.3 * 4.0 * np.pi)

    def test_moving_frame_is_supported_and_coordinates_are_recoverable(self):
        n = 101
        theta = np.linspace(0.0, np.pi / 2.0, n)
        frames = np.zeros((n, 3, 3))
        for i, angle in enumerate(theta):
            c, s = np.cos(angle), np.sin(angle)
            frames[i] = np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]])
        q1 = np.linspace(-1.0, 1.0, n)
        q2 = np.sin(np.linspace(0.0, 3.0, n))
        z = np.linspace(0.0, 5.0, n)
        points = lift_phasor_to_3d(q1, q2, z, frames)
        a, b, axial = recover_phasor_coordinates(points, frames)
        np.testing.assert_allclose(a, q1, atol=1e-12)
        np.testing.assert_allclose(b, q2, atol=1e-12)
        np.testing.assert_allclose(axial, z, atol=1e-12)

    def test_rejects_left_handed_frame(self):
        left_handed = np.diag([1.0, 1.0, -1.0])
        with self.assertRaises(ValueError):
            lift_phasor_to_3d([1.0], [0.0], [0.0], left_handed)

    def test_rejects_non_orthonormal_frame(self):
        bad_frame = np.array([[1.0, 0.2, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
        with self.assertRaises(ValueError):
            lift_phasor_to_3d([1.0], [0.0], [0.0], bad_frame)


if __name__ == "__main__":
    unittest.main()
