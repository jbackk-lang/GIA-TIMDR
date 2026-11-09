"""Compare the +,-,+ scalar lobe word with signed Frenet torsion of the
repository's canonical trefoil. Analytic derivatives avoid finite-difference
artifacts. This is a correspondence audit, not a signal-to-knot proof.
"""
import json
from pathlib import Path
import numpy as np


def trefoil_torsion_sector_audit(samples=12000):
    t = np.linspace(0.0, 2*np.pi, samples, endpoint=False)
    v = np.stack([np.cos(t)+4*np.cos(2*t),
                  -np.sin(t)+4*np.sin(2*t),
                  -3*np.cos(3*t)], axis=1)
    a = np.stack([-np.sin(t)-8*np.sin(2*t),
                  -np.cos(t)+8*np.cos(2*t),
                  9*np.sin(3*t)], axis=1)
    j = np.stack([-np.cos(t)-16*np.cos(2*t),
                  np.sin(t)-16*np.sin(2*t),
                  27*np.cos(3*t)], axis=1)
    cross = np.cross(v, a)
    denom = np.sum(cross*cross, axis=1)
    tau = np.sum(cross*j, axis=1)/denom
    sectors = []
    for i in range(3):
        q = tau[(t >= i*2*np.pi/3) & (t < (i+1)*2*np.pi/3)]
        sectors.append({
            "sector": i,
            "mean_signed_torsion": float(np.mean(q)),
            "positive_fraction": float(np.mean(q > 0)),
            "negative_fraction": float(np.mean(q < 0)),
            "minimum": float(np.min(q)),
            "maximum": float(np.max(q)),
        })
    means = [x["mean_signed_torsion"] for x in sectors]
    return {
        "model": "canonical_trefoil_analytic_frenet_torsion",
        "samples": samples,
        "scalar_signal_lobe_word": [1, -1, 1],
        "trefoil_sector_torsion": sectors,
        "sector_mean_spread": float(max(means)-min(means)),
        "threefold_torsion_symmetry": bool(np.allclose(means, [means[0]]*3, atol=1e-10)),
        "each_sector_contains_both_torsion_signs": all(
            x["positive_fraction"] > 0 and x["negative_fraction"] > 0 for x in sectors
        ),
        "interpretation": (
            "The trefoil's three symmetry sectors have the same signed torsion "
            "distribution; torsion changes sign within every sector. Therefore "
            "the scalar +,-,+ lobe word does not map to a unique +,-,+ torsion "
            "orientation on the canonical trefoil."
        )
    }


if __name__ == "__main__":
    result = trefoil_torsion_sector_audit()
    print(json.dumps(result, indent=2))
    Path("trefoil_lobe_correspondence_audit.json").write_text(
        json.dumps(result, indent=2) + "\\n", encoding="utf-8"
    )
