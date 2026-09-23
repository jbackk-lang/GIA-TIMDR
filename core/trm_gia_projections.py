"""Reference construction v0.1: event graph -> branch representations.

Synthetic mathematical checks, not an empirical detector. The PCA reference
is fitted once on calibration positions. This module does not replace the
robust operational GIAFilter in filters/_vendor_senscore_gia_filter.py.
"""

from dataclasses import dataclass
import json
import numpy as np


def _finite(values, name):
    result = np.asarray(values, dtype=float)
    if not np.all(np.isfinite(result)):
        raise ValueError(f"{name} must be finite")
    return result


@dataclass(frozen=True)
class Event:
    id: str
    energy: float
    time: float
    position: tuple[float, float, float]

    def __post_init__(self):
        if not isinstance(self.id, str) or not self.id:
            raise ValueError("event id must be a nonempty string")
        energy, time = _finite([self.energy, self.time], "event weights")
        position = _finite(self.position, "position")
        if energy < 0 or position.shape != (3,):
            raise ValueError("energy must be nonnegative; position must have 3 coordinates")
        object.__setattr__(self, "energy", float(energy))
        object.__setattr__(self, "time", float(time))
        object.__setattr__(self, "position", tuple(position.tolist()))


@dataclass(frozen=True)
class EventGraph:
    events: tuple[Event, ...]
    edges: tuple[tuple[str, str], ...] = ()

    def __post_init__(self):
        events = tuple(self.events)
        if not all(isinstance(event, Event) for event in events):
            raise ValueError("events must contain Event objects")
        ids = {event.id for event in events}
        if len(ids) != len(events):
            raise ValueError("event ids must be unique")
        edges = tuple(tuple(edge) for edge in self.edges)
        if any(len(edge) != 2 or edge[0] == edge[1]
               or edge[0] not in ids or edge[1] not in ids for edge in edges):
            raise ValueError("edges must connect two distinct existing event ids")
        if len(set(edges)) != len(edges):
            raise ValueError("duplicate directed edges")
        object.__setattr__(self, "events", events)
        object.__setattr__(self, "edges", edges)


@dataclass(frozen=True)
class LineReference:
    center: tuple[float, float, float]
    direction: tuple[float, float, float]
    radius: float

    def __post_init__(self):
        center = _finite(self.center, "center")
        direction = _finite(self.direction, "direction")
        radius = float(_finite(self.radius, "radius"))
        if center.shape != (3,) or direction.shape != (3,) or radius < 0:
            raise ValueError("reference requires 3D vectors and nonnegative radius")
        norm = np.linalg.norm(direction)
        if not np.isfinite(norm) or norm == 0:
            raise ValueError("direction must have a finite positive norm")
        object.__setattr__(self, "center", tuple(center.tolist()))
        object.__setattr__(self, "direction", tuple((direction / norm).tolist()))
        object.__setattr__(self, "radius", radius)


def fit_line_reference(calibration_positions, radius, *, min_relative_gap=1e-6):
    """Fit one PCA axis; reject an unidentified leading eigenspace."""
    points = _finite(calibration_positions, "calibration positions")
    gap = float(_finite(min_relative_gap, "min_relative_gap"))
    if points.ndim != 2 or points.shape[1] != 3 or len(points) < 3:
        raise ValueError("at least three 3D calibration points required")
    if not 0 < gap <= 1:
        raise ValueError("min_relative_gap must be in (0, 1]")
    center = points.mean(axis=0)
    centered = points - center
    eigenvalues, vectors = np.linalg.eigh(centered.T @ centered / len(points))
    if eigenvalues[-1] <= 0 or eigenvalues[-1] - eigenvalues[-2] <= gap * eigenvalues[-1]:
        raise ValueError("PCA axis is not identified: insufficient eigengap")
    return LineReference(tuple(center), tuple(vectors[:, -1]), radius)


def gia_select(graph, reference):
    """Return an induced subgraph using a fixed spatial tube (inclusive boundary)."""
    center, direction = np.asarray(reference.center), np.asarray(reference.direction)
    selected = []
    for event in graph.events:
        delta = np.asarray(event.position) - center
        residual = delta - np.dot(delta, direction) * direction
        if np.linalg.norm(residual) <= reference.radius:
            selected.append(event)
    ids = {event.id for event in selected}
    return EventGraph(tuple(selected), tuple(edge for edge in graph.edges
                                            if edge[0] in ids and edge[1] in ids))


def _edges(values):
    edges = _finite(values, "bin edges")
    if edges.ndim != 1 or len(edges) < 2 or np.any(np.diff(edges) <= 0):
        raise ValueError("bin edges must be a strictly increasing vector")
    return edges


def _bin_indices(graph, edges):
    times = np.array([event.time for event in graph.events])
    if np.any(times < edges[0]) or np.any(times >= edges[-1]):
        raise ValueError("all events must lie in the half-open observation interval")
    return np.searchsorted(edges, times, side="right") - 1


def signal_projection(graph, bin_edges):
    """Energy/time in half-open bins; sum(x * bin_width) conserves energy."""
    edges = _edges(bin_edges)
    indices = _bin_indices(graph, edges)
    energy = np.array([event.energy for event in graph.events])
    totals = np.bincount(indices, weights=energy, minlength=len(edges) - 1)
    return totals / np.diff(edges)


def gaussian_signal(graph, sample_times, bandwidth):
    """Samples of sum(E_i * Gaussian_h(t-t_i)); tails extend outside the grid."""
    times = _finite(sample_times, "sample times")
    h = float(_finite(bandwidth, "bandwidth"))
    if times.ndim != 1 or h <= 0:
        raise ValueError("sample times must be a vector and bandwidth must be positive")
    values = np.zeros_like(times)
    for event in graph.events:
        z = (times - event.time) / h
        values += event.energy * np.exp(-0.5 * z * z) / (np.sqrt(2 * np.pi) * h)
    return values


def curve_projection(graph, query_times):
    """Time-ordered polyline. No extrapolation or surface reconstruction."""
    events = sorted(graph.events, key=lambda event: event.time)
    if len(events) < 2:
        raise ValueError("curve requires at least two events")
    times = np.array([event.time for event in events])
    points = np.array([event.position for event in events])
    if np.any(np.diff(times) <= 0):
        raise ValueError("a single trajectory requires distinct event times")
    if np.any(np.linalg.norm(np.diff(points, axis=0), axis=1) == 0):
        raise ValueError("successive positions must differ for a regular segment")
    query = _finite(query_times, "query times")
    if query.ndim != 1 or np.any(query < times[0]) or np.any(query > times[-1]):
        raise ValueError("query times must lie within the observed trajectory")
    return np.column_stack([np.interp(query, times, points[:, axis]) for axis in range(3)])


def tube_from_frames(centers, normals, binormals, radius, angles):
    """Sample an auxiliary tube from supplied frames; not a measured surface.

The caller supplies a smooth regular centerline and its normal frames.
This function checks orthonormal pairs, not smoothness or global embedding.
"""
    centers = _finite(centers, "centers")
    normals = _finite(normals, "normals")
    binormals = _finite(binormals, "binormals")
    angles = _finite(angles, "angles")
    radius = float(_finite(radius, "radius"))
    if centers.ndim != 2 or centers.shape[1] != 3 or len(centers) < 2:
        raise ValueError("at least two 3D centers required")
    if normals.shape != centers.shape or binormals.shape != centers.shape:
        raise ValueError("frames must match centers")
    if angles.ndim != 1 or len(angles) < 3 or radius <= 0:
        raise ValueError("positive radius and at least three angles required")
    if (not np.allclose(np.linalg.norm(normals, axis=1), 1)
            or not np.allclose(np.linalg.norm(binormals, axis=1), 1)
            or not np.allclose(np.sum(normals * binormals, axis=1), 0, atol=1e-12)):
        raise ValueError("normal and binormal must be orthonormal")
    return centers[:, None, :] + radius * (
        np.cos(angles)[None, :, None] * normals[:, None, :]
        + np.sin(angles)[None, :, None] * binormals[:, None, :])


def modal_projection(signal, sample_times):
    """Rectangular-window rFFT; phase is relative to sample_times[0].

Returns frequency, one-sided cosine amplitude, phase, raw coefficients.
Phase is NaN where the coefficient is numerically zero.
"""
    values = _finite(signal, "signal")
    times = _finite(sample_times, "sample times")
    if values.ndim != 1 or times.shape != values.shape or len(values) < 2:
        raise ValueError("matching one-dimensional signal and times required")
    dt = np.diff(times)
    if np.any(dt <= 0) or not np.allclose(dt, dt[0], rtol=1e-9, atol=0):
        raise ValueError("FFT requires uniformly spaced increasing sample times")
    coefficients = np.fft.rfft(values)
    amplitudes = np.abs(coefficients) / len(values)
    amplitudes[1:] *= 2
    if len(values) % 2 == 0:
        amplitudes[-1] /= 2
    phase = np.angle(coefficients)
    tolerance = np.finfo(float).eps * len(values) * np.max(np.abs(values))
    phase[np.abs(coefficients) <= tolerance] = np.nan
    return np.fft.rfftfreq(len(values), dt[0]), amplitudes, phase, coefficients


def meta_projection(graph, window_edges, reference, *, energy_reference,
                    energy_threshold, alignment_cosine, epsilon):
    """New event-graph adapter: Lambda, tau, rho, J per disjoint window.

J uses spatial edge alignment; rho uses energy residuals. Parameters must be
chosen on calibration data. Each window requires >=2 distinct event times.
No within-window edges means observed coupling fraction J=0; counts are
returned to distinguish this convention from a measured nonzero population.
"""
    edges = _edges(window_edges)
    indices = _bin_indices(graph, edges)
    baseline, threshold, cosine, eps = _finite(
        [energy_reference, energy_threshold, alignment_cosine, epsilon], "META parameters")
    if baseline < 0 or threshold < 0 or not 0 <= cosine <= 1 or eps <= 0:
        raise ValueError("invalid META parameters")
    states, edge_counts = [], []
    direction = np.asarray(reference.direction)
    for k in range(len(edges) - 1):
        events = sorted((event for i, event in enumerate(graph.events) if indices[i] == k),
                        key=lambda event: event.time)
        times = np.array([event.time for event in events])
        if len(events) < 2 or np.any(np.diff(times) <= 0):
            raise ValueError("each META window requires >=2 distinct event times")
        energy = np.array([event.energy for event in events])
        defect = np.abs(energy - baseline)
        dispersion = energy.std() / (energy.std() + abs(energy.mean()) + eps)
        tempo = np.mean(np.abs(np.diff(defect)) / np.diff(times))
        density = np.mean(defect > threshold)
        by_id = {event.id: event for event in events}
        aligned, count = 0, 0
        for a, b in graph.edges:
            if a not in by_id or b not in by_id:
                continue
            count += 1
            delta = np.asarray(by_id[b].position) - by_id[a].position
            norm = np.linalg.norm(delta)
            if norm > 0 and abs(np.dot(delta, direction)) / norm >= cosine:
                aligned += 1
        states.append((dispersion, tempo, density, aligned / count if count else 0.0))
        edge_counts.append(count)
    return edges[:-1].copy(), np.array(states), np.array(edge_counts)


def meta_evolution(states, window_times):
    """Forward state differences assigned to the later window; L1 magnitude."""
    states = _finite(states, "states")
    times = _finite(window_times, "window times")
    if states.ndim != 2 or states.shape[1] != 4 or times.shape != (len(states),):
        raise ValueError("states must have shape (n, 4), with n timestamps")
    if len(states) < 2 or np.any(np.diff(times) <= 0):
        raise ValueError("at least two increasing window times required")
    rate = np.diff(states, axis=0) / np.diff(times)[:, None]
    return rate, np.abs(rate).sum(axis=1)


def demo():
    times = np.arange(16, dtype=float)
    energy = 2 + np.cos(2 * np.pi * 2 * times / 16)
    events = tuple(Event(f"e{i}", value, t, (t, 0, 0))
                   for i, (t, value) in enumerate(zip(times, energy)))
    graph = EventGraph(events + (Event("outlier", 1, 7.5, (7.5, 5, 0)),),
                       tuple((f"e{i}", f"e{i+1}") for i in range(15)))
    reference = fit_line_reference([(-1, 0, 0), (0, 0, 0), (1, 0, 0)], 0.2)
    selected = gia_select(graph, reference)
    signal = signal_projection(selected, np.arange(17))
    frequency, amplitude, _, _ = modal_projection(signal, times)
    window_times, states, counts = meta_projection(
        selected, [0, 4, 8, 12, 16], reference,
        energy_reference=2, energy_threshold=0.8, alignment_cosine=0.9, epsilon=1e-12)
    rate, magnitude = meta_evolution(states, window_times)
    peak = 1 + np.argmax(amplitude[1:])
    return {"status": "SYNTHETIC_CONSTRUCTION_CHECK", "selected_events": len(selected.events),
            "total_energy": float(signal.sum()), "peak_frequency": float(frequency[peak]),
            "peak_amplitude": float(amplitude[peak]),
            "curve_endpoints": curve_projection(selected, [0, 15]).tolist(),
            "meta_states": states.tolist(), "meta_edge_counts": counts.tolist(),
            "meta_rate": rate.tolist(), "meta_rate_L1": magnitude.tolist()}


if __name__ == "__main__":
    print(json.dumps(demo(), indent=2, allow_nan=False))
