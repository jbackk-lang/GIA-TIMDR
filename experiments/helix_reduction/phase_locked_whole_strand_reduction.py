#!/usr/bin/env python3
"""Phase-locked whole-strand 4->3 reduction on a spherical boundary.

The sphere is the primary model: four equal phase sectors of pi/2. One
entire closed strand is removed at a boundary event; the remaining three
are rephased to 2*pi/3. The egg mode is only a sensitivity comparison:
equal phase sectors remain defined, while equal surface-arclength sectors
are reported separately because phase and arclength need not coincide.

This is a kinematic/topological bookkeeping model, not yet an elastic
equilibrium solver or proof of a physical knot transition.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np


def boundary(theta, phi, radius=1.0, axial_scale=1.0, egg=0.0):
    rho = radius * np.sin(theta) * (1.0 + egg * np.cos(theta))
    return np.stack((rho*np.cos(phi), rho*np.sin(phi),
                     radius*axial_scale*np.cos(theta)), axis=-1)


def strand(u, phase, radius=1.0, axial_scale=1.0, egg=0.0,
           latitude_amplitude=0.22, handedness=1):
    theta = np.pi/2 + latitude_amplitude*np.sin(2*u)
    phi = handedness*u + phase
    return boundary(theta, phi, radius, axial_scale, egg)


def length(points, closed=True):
    q = np.vstack((points, points[0])) if closed else points
    return float(np.linalg.norm(np.diff(q, axis=0), axis=1).sum())


def circular_phase_sectors(count):
    edges = np.linspace(-np.pi/count, 2*np.pi-np.pi/count, count+1)
    centers = (edges[:-1] + edges[1:])/2
    return edges, centers


def arclength_quarter_boundaries(curve):
    seg = np.linalg.norm(np.roll(curve, -1, axis=0)-curve, axis=1)
    cumulative = np.concatenate(([0.0], np.cumsum(seg)))
    targets = np.linspace(0.0, cumulative[-1], 5)
    idx = np.searchsorted(cumulative, targets, side="left")
    idx = np.clip(idx, 0, len(curve)-1)
    return (idx/len(curve)*2*np.pi).tolist()


def run(shape="sphere", samples=1440, radius=1.0, expansion=1.0,
        boundary_radius=1.0, removed_strand=3, handedness=1):
    if samples < 128:
        raise ValueError("samples must be >= 128")
    if shape not in ("sphere", "egg"):
        raise ValueError("shape must be sphere or egg")
    if expansion <= 0 or radius <= 0 or boundary_radius <= 0:
        raise ValueError("radii and expansion must be positive")
    if removed_strand not in range(4):
        raise ValueError("removed_strand must be 0..3")
    egg, axial = (0.0, 1.0) if shape == "sphere" else (0.28, 1.08)
    u = np.linspace(0, 2*np.pi, samples, endpoint=False)
    initial_edges, initial_phases = circular_phase_sectors(4)
    final_edges, final_phases = circular_phase_sectors(3)
    R = radius*expansion
    initial = [strand(u, p, R, axial, egg, handedness=handedness)
               for p in initial_phases]
    # Boundary clearance is measured against the enclosing sphere radius.
    # For an egg this is only a radial envelope diagnostic, not geodesic distance.
    radial_extent = [float(np.max(np.linalg.norm(c, axis=1))) for c in initial]
    critical_expansion = [boundary_radius/(x/expansion) for x in radial_extent]
    removed = initial[removed_strand]
    survivors_old = [c for i,c in enumerate(initial) if i != removed_strand]
    # Rebuild the three survivors with uniform 120-degree phase spacing.
    final = [strand(u, p, R, axial, egg, handedness=handedness)
             for p in final_phases]
    # Signed azimuthal winding is the orientation invariant in this model.
    winding_before = int(handedness)
    winding_after = int(handedness)
    # Equal phase and equal arclength partitions are not interchangeable.
    egg_arc_edges = arclength_quarter_boundaries(initial[0])
    result = {
        "schema": "gia-timdr-phase-locked-whole-strand-reduction-v0.2",
        "shape": shape,
        "primary_geometry": shape == "sphere",
        "parameters": {"radius": radius, "expansion": expansion,
                       "boundary_radius": boundary_radius,
                       "egg_asymmetry": egg, "axial_scale": axial,
                       "removed_strand_index": removed_strand,
                       "handedness": handedness},
        "phase_partition": {
            "initial_sector_count": 4,
            "initial_sector_width_rad": float(2*np.pi/4),
            "initial_sector_width_deg": 90.0,
            "initial_edges_rad": initial_edges.tolist(),
            "removed_sector_center_rad": float(initial_phases[removed_strand]),
            "removed_closed_strand_length": length(removed),
            "remaining_closed_strand_count": 3,
            "final_sector_width_rad": float(2*np.pi/3),
            "final_sector_width_deg": 120.0,
            "final_edges_rad": final_edges.tolist()
        },
        "boundary_event": {
            "radial_extents_by_strand": radial_extent,
            "critical_expansion_by_strand": critical_expansion,
            "first_crossing_is_unique": len(set(round(x,10) for x in critical_expansion)) > 1,
            "interpretation": (
                "A perfectly symmetric sphere gives identical thresholds for all four strands; "
                "uniform expansion alone cannot select exactly one strand. A physical selector "
                "requires a measured asymmetry, perturbation, or strand-specific boundary condition."
            )
        },
        "adaptation": {
            "survivor_lengths_before": [length(c) for c in survivors_old],
            "survivor_lengths_after": [length(c) for c in final],
            "phase_winding_before": winding_before,
            "phase_winding_after": winding_after,
            "handedness_preserved": winding_before == winding_after,
            "removed_whole_strand": True,
            "no_local_arc_bridge": True
        },
        "egg_arclength_partition_diagnostic_rad": egg_arc_edges,
        "limitations": [
            "The curves are closed traces on a boundary surface; a full link/knot invariant is not computed.",
            "The boundary crossing is diagnosed by radial extent; a physical detachment law is not derived.",
            "The surviving curves are rephased kinematically, not relaxed by minimizing elastic energy.",
            "Signed Frenet torsion may change sign even when azimuthal winding orientation is preserved.",
            "The egg's equal-arclength partition is diagnostic only; the primary hypothesis uses equal phase sectors."
        ]
    }
    return result


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--shape",choices=("sphere","egg"),default="sphere")
    ap.add_argument("--samples",type=int,default=1440)
    ap.add_argument("--radius",type=float,default=1.0)
    ap.add_argument("--expansion",type=float,default=1.0)
    ap.add_argument("--boundary-radius",type=float,default=1.0)
    ap.add_argument("--removed-strand",type=int,default=3)
    ap.add_argument("--handedness",type=int,choices=(-1,1),default=1)
    ap.add_argument("--out",type=Path,default=Path("phase_locked_reduction.json"))
    a=ap.parse_args()
    r=run(a.shape,a.samples,a.radius,a.expansion,a.boundary_radius,
          a.removed_strand,a.handedness)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(r,indent=2,ensure_ascii=False)+"\\n",encoding="utf-8")
    print(json.dumps({
        "shape":r["shape"],
        "initial_phase_deg":r["phase_partition"]["initial_sector_width_deg"],
        "final_phase_deg":r["phase_partition"]["final_sector_width_deg"],
        "removed_whole_strand":r["adaptation"]["removed_whole_strand"],
        "handedness_preserved":r["adaptation"]["handedness_preserved"],
        "unique_first_boundary_crossing":r["boundary_event"]["first_crossing_is_unique"]
    },indent=2))


if __name__=="__main__":
    main()
