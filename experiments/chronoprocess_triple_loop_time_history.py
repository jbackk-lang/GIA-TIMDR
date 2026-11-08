"""Chronoprocess time-history probe for the whole three-loop state.

The three phase channels share one ordered carrier T. A temporary
frequency detuning is integrated over time, then the nominal frequency is
restored. The experiment measures whether phase relations return merely
because instantaneous frequency returns. It does not implement a coupled
repair law and does not claim information recovery.
"""
from __future__ import annotations

import json
import numpy as np


def run_probe(fs: float = 1000.0, duration: float = 8.0,
              f0: float = 4.0, detune_fraction: float = 0.05,
              start: float = 2.0, end: float = 4.0) -> dict:
    t = np.arange(int(fs * duration), dtype=float) / fs
    nominal = np.full((3, t.size), f0, dtype=float)
    disturbed = nominal.copy()
    active = (t >= start) & (t < end)

    # Whole-state disturbance cases: one, two, and all three loop clocks.
    cases = {
        "one_loop": (0,),
        "two_loops": (0, 1),
        "all_three_loops": (0, 1, 2),
    }
    results = {}
    for name, indices in cases.items():
        frequencies = nominal.copy()
        frequencies[list(indices), :] += (
            f0 * detune_fraction * active[np.newaxis, :]
        )
        # Integrate frequency over the shared carrier T: phase remembers
        # the duration of the detuning even after frequency returns.
        phases = 2.0 * np.pi * np.cumsum(frequencies, axis=1) / fs
        relative = phases - phases[0:1, :]
        coherence = np.abs(np.mean(np.exp(1j * relative), axis=0))
        windows = {
            "before": (t >= 0.5) & (t < 1.8),
            "during": (t >= 2.2) & (t < 3.8),
            "after": (t >= 4.5) & (t < 7.5),
        }
        results[name] = {
            "disturbed_loop_indices_1_based": [i + 1 for i in indices],
            "phase_relation_rms_rad": {
                key: float(np.sqrt(np.mean(
                    np.angle(np.exp(1j * relative[:, mask])) ** 2
                )))
                for key, mask in windows.items()
            },
            "three_loop_coherence_mean": {
                key: float(np.mean(coherence[mask]))
                for key, mask in windows.items()
            },
            "final_relative_phase_rad": [
                float(np.angle(np.exp(1j * relative[i, -1])))
                for i in range(3)
            ],
        }

    return {
        "status": "chronoprocess_time_history_probe_not_self_repair",
        "shared_carrier": "T",
        "loops_as_one_state": "Psi=(psi1,psi2,psi3)",
        "sample_rate_hz": fs,
        "nominal_frequency_hz": f0,
        "detuning_fraction": detune_fraction,
        "detuning_interval_seconds": [start, end],
        "cases": results,
        "interpretation": [
            "Instantaneous frequency can return to nominal while accumulated phase relations retain a history-dependent offset.",
            "Chronoprocess currently supplies a shared time carrier and independent projections; it does not provide a coupled phase-recovery dynamic.",
            "Any recovery claim requires an explicit, preregistered coupling law and controls.",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run_probe(), indent=2, sort_keys=True))
