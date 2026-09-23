"""Algebraic and synthetic tests for construction v0.1; no empirical verdict."""
import unittest
import numpy as np

from core.trm_gia_projections import (
    Event, EventGraph, LineReference, fit_line_reference, gia_select,
    signal_projection, gaussian_signal, curve_projection, tube_from_frames,
    modal_projection, meta_projection, meta_evolution, demo,
)


def graph(energies=(1, 2, 3, 4), positions=None):
    if positions is None:
        positions = [(i, 0, 0) for i in range(len(energies))]
    return EventGraph(tuple(Event(str(i), e, float(i), tuple(p))
                            for i, (e, p) in enumerate(zip(energies, positions))),
                      tuple((str(i), str(i + 1)) for i in range(len(energies) - 1)))


class ProjectionTests(unittest.TestCase):
    def setUp(self):
        self.reference = LineReference((0, 0, 0), (1, 0, 0), 0.2)

    def test_invalid_graph_inputs(self):
        for energy, time, pos in [(-1, 0, (0, 0, 0)), (1, np.nan, (0, 0, 0)),
                                   (1, 0, (0, np.inf, 0)), (1, 0, (0, 0))]:
            with self.subTest(energy=energy, time=time, pos=pos), self.assertRaises(ValueError):
                Event("a", energy, time, pos)
        event = Event("a", 1, 0, (0, 0, 0))
        for events, edges in [((event, event), ()), ((event,), (("a", "missing"),)),
                               ((event,), (("a", "a"),))]:
            with self.assertRaises(ValueError):
                EventGraph(events, edges)

    def test_pca_axis_and_degeneracy(self):
        reference = fit_line_reference([(-1, 0, 0), (0, 0, 0), (1, 0, 0)], 0.2)
        self.assertAlmostEqual(abs(reference.direction[0]), 1)
        for points in [np.zeros((3, 3)), [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0)]]:
            with self.assertRaises(ValueError):
                fit_line_reference(points, 0.2)

    def test_selection_induced_idempotent_and_monotone(self):
        source = graph(positions=[(0, 0, 0), (1, 0.1, 0), (2, 2, 0), (3, 0, 0)])
        selected = gia_select(source, self.reference)
        self.assertEqual([e.id for e in selected.events], ["0", "1", "3"])
        self.assertEqual(selected.edges, (("0", "1"),))
        self.assertEqual(gia_select(selected, self.reference), selected)
        smaller = EventGraph(source.events[:2], source.edges[:1])
        self.assertTrue(set(gia_select(smaller, self.reference).events) <= set(selected.events))

    def test_selection_rigid_motion_equivariance(self):
        source = graph(positions=[(0, 0, 0), (1, 0.1, 0), (2, 2, 0), (3, 0, 0)])
        rotation = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
        offset = np.array([4, 2, 7])
        moved = EventGraph(tuple(Event(e.id, e.energy, e.time, rotation @ e.position + offset)
                                  for e in source.events), source.edges)
        reference = LineReference(tuple(offset), (0, 1, 0), 0.2)
        self.assertEqual([e.id for e in gia_select(source, self.reference).events],
                         [e.id for e in gia_select(moved, reference).events])

    def test_threshold_is_not_globally_continuous(self):
        inside = EventGraph((Event("a", 1, 0, (0, 0.2 - 1e-8, 0)),))
        outside = EventGraph((Event("a", 1, 0, (0, 0.2 + 1e-8, 0)),))
        self.assertEqual(len(gia_select(inside, self.reference).events), 1)
        self.assertEqual(len(gia_select(outside, self.reference).events), 0)

    def test_signal_mass_and_half_open_boundaries(self):
        source = graph()
        edges = np.array([0, 1, 3, 4])
        values = signal_projection(source, edges)
        np.testing.assert_allclose(values, [1, 2.5, 4])
        self.assertAlmostEqual(np.dot(values, np.diff(edges)), 10)
        with self.assertRaises(ValueError):
            signal_projection(source, [0, 3])
        np.testing.assert_array_equal(signal_projection(EventGraph(()), [0, 1, 2]), [0, 0])

    def test_signal_linearity_and_order_invariance(self):
        source = graph()
        a, b = EventGraph(source.events[:2]), EventGraph(source.events[2:])
        edges = [0, 2, 4]
        np.testing.assert_allclose(signal_projection(source, edges),
                                   signal_projection(a, edges) + signal_projection(b, edges))
        np.testing.assert_allclose(signal_projection(source, edges),
                                   signal_projection(EventGraph(tuple(reversed(source.events))), edges))

    def test_binning_has_boundary_jump(self):
        a = EventGraph((Event("a", 1, 1 - 1e-10, (0, 0, 0)),))
        b = EventGraph((Event("a", 1, 1 + 1e-10, (0, 0, 0)),))
        self.assertEqual(np.abs(signal_projection(a, [0, 1, 2])
                                - signal_projection(b, [0, 1, 2])).sum(), 2)

    def test_gaussian_mass_and_shift_bound(self):
        source = EventGraph((Event("a", 2, 0, (0, 0, 0)),))
        shifted = EventGraph((Event("a", 2, 1e-3, (0, 0, 0)),))
        grid, h = np.linspace(-4, 4, 8001), 0.5
        values = gaussian_signal(source, grid, h)
        self.assertAlmostEqual(values.sum() * (grid[1] - grid[0]), 2, places=9)
        bound = 2 * np.exp(-0.5) / np.sqrt(2 * np.pi) * 1e-3 / h**2
        self.assertLessEqual(np.max(np.abs(values - gaussian_signal(shifted, grid, h))), bound)
        with self.assertRaises(ValueError):
            gaussian_signal(source, grid, 0)

    def test_curve_interpolation_and_ambiguity(self):
        source = graph()
        np.testing.assert_allclose(curve_projection(source, [0.5, 2.5]), [[0.5, 0, 0], [2.5, 0, 0]])
        same_time = EventGraph((Event("a", 1, 0, (0, 0, 0)), Event("b", 1, 0, (1, 0, 0))))
        with self.assertRaises(ValueError):
            curve_projection(same_time, [0])
        with self.assertRaises(ValueError):
            curve_projection(source, [-1])

    def test_auxiliary_tube_radius(self):
        centers = np.array([[0, 0, 0], [1, 0, 0], [2, 0, 0]])
        normal = np.tile([0, 1, 0], (3, 1))
        binormal = np.tile([0, 0, 1], (3, 1))
        surface = tube_from_frames(centers, normal, binormal, 0.5,
                                   np.linspace(0, 2 * np.pi, 12, endpoint=False))
        np.testing.assert_allclose(np.linalg.norm(surface - centers[:, None, :], axis=2), 0.5)
        with self.assertRaises(ValueError):
            tube_from_frames(centers, normal, normal, 0.5, [0, 1, 2])

    def test_fft_known_mode_reconstruction_and_parseval(self):
        n, dt, phase = 32, 0.25, 0.3
        signal = 2 + 0.7 * np.cos(2 * np.pi * 3 * np.arange(n) / n + phase)
        frequencies, amplitudes, phases, coefficients = modal_projection(signal, 10 + dt * np.arange(n))
        self.assertAlmostEqual(frequencies[3], 3 / (n * dt))
        self.assertAlmostEqual(amplitudes[3], 0.7)
        self.assertAlmostEqual(phases[3], phase)
        np.testing.assert_allclose(np.fft.irfft(coefficients, n=n), signal)
        spectrum_power = abs(coefficients[0])**2 + abs(coefficients[-1])**2
        spectrum_power += 2 * np.sum(abs(coefficients[1:-1])**2)
        self.assertAlmostEqual(np.sum(signal**2), spectrum_power / n)

    def test_fft_nyquist_odd_length_and_zero_phase(self):
        _, amplitude, _, _ = modal_projection((-1.) ** np.arange(8), np.arange(8))
        self.assertAlmostEqual(amplitude[-1], 1)
        _, amplitude, _, _ = modal_projection(np.cos(2*np.pi*3*np.arange(9)/9), np.arange(9))
        self.assertAlmostEqual(amplitude[3], 1)
        _, _, phase, _ = modal_projection(np.zeros(8), np.arange(8))
        self.assertTrue(np.isnan(phase).all())
        with self.assertRaises(ValueError):
            modal_projection([1, 2, 3], [0, 1, 3])

    def meta(self, source):
        return meta_projection(source, [0, 4], self.reference, energy_reference=1,
                               energy_threshold=0.5, alignment_cosine=0.9, epsilon=1e-12)[1][0]

    def test_meta_channel_sources_are_separate(self):
        base = self.meta(graph((1, 1, 1, 1)))
        energy_changed = self.meta(graph((1, 3, 1, 3)))
        geometry_changed = self.meta(graph((1, 1, 1, 1), [(0, i, 0) for i in range(4)]))
        np.testing.assert_allclose(base, [0, 0, 0, 1])
        self.assertGreater(energy_changed[2], base[2])
        self.assertEqual(energy_changed[3], base[3])
        self.assertEqual(geometry_changed[2], base[2])
        self.assertEqual(geometry_changed[3], 0)
        self.assertTrue(0 <= energy_changed[0] < 1)
        self.assertGreaterEqual(energy_changed[1], 0)

    def test_meta_empty_window_and_no_edges(self):
        with self.assertRaises(ValueError):
            self.meta(EventGraph(()))
        source = EventGraph(graph((1, 1, 1, 1)).events)
        _, states, count = meta_projection(source, [0, 4], self.reference, energy_reference=1,
                                           energy_threshold=0.5, alignment_cosine=0.9, epsilon=1e-12)
        self.assertEqual(states[0, 3], 0)
        self.assertEqual(count[0], 0)

    def test_meta_evolution(self):
        rate, magnitude = meta_evolution([[0, 0, 0, 1], [0.5, 2, 0.5, 0]], [0, 2])
        np.testing.assert_allclose(rate, [[0.25, 1, 0.25, -0.5]])
        np.testing.assert_allclose(magnitude, [2])
        with self.assertRaises(ValueError):
            meta_evolution([[0, 0, 0, 0], [0, 0, 0, 0]], [1, 1])

    def test_demo(self):
        result = demo()
        self.assertEqual(result["selected_events"], 16)
        self.assertAlmostEqual(result["total_energy"], 32)
        self.assertAlmostEqual(result["peak_frequency"], 0.125)
        self.assertAlmostEqual(result["peak_amplitude"], 1)


if __name__ == "__main__":
    unittest.main()
