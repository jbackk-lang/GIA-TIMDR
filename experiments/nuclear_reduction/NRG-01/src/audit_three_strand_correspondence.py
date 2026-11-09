#!/usr/bin/env python3
"""Audit whether NRG-01 decay components identify three TIMDR helix strands.

The audit deliberately separates graph facts from geometric assumptions.
It never invents coordinates for nuclides and never equates a graph branch
with a geometric knot crossing or cardinal point.
"""
from __future__ import annotations
import argparse, itertools, json
from collections import Counter, defaultdict, deque
from pathlib import Path


def weak_components(nodes, edges):
    adj = {k: set() for k in nodes}
    for e in edges:
        a, b = e["source"], e["target"]
        adj[a].add(b); adj[b].add(a)
    unseen = set(nodes); result = []
    while unseen:
        root = min(unseen); stack = [root]; comp = {root}; unseen.remove(root)
        while stack:
            x = stack.pop()
            for y in adj[x] & unseen:
                unseen.remove(y); comp.add(y); stack.append(y)
        result.append(comp)
    return sorted(result, key=lambda c: min(c))


def dag_path_metrics(comp, outgoing, incoming):
    indeg = {v: sum(e["source"] in comp for e in incoming[v]) for v in comp}
    q = deque(sorted(v for v, d in indeg.items() if d == 0))
    order = []
    while q:
        v = q.popleft(); order.append(v)
        for e in outgoing[v]:
            w = e["target"]
            if w in comp:
                indeg[w] -= 1
                if indeg[w] == 0: q.append(w)
    if len(order) != len(comp):
        return {"is_dag": False, "root_to_terminal_path_count": None, "longest_path_edges": None}
    ways, longest = {}, {}
    for v in reversed(order):
        succ = [e["target"] for e in outgoing[v] if e["target"] in comp]
        if not succ:
            ways[v], longest[v] = 1, 0
        else:
            ways[v] = sum(ways[w] for w in succ)
            longest[v] = 1 + max(longest[w] for w in succ)
    roots = [v for v in comp if not any(e["source"] in comp for e in incoming[v])]
    terminals = [v for v in comp if not any(e["target"] in comp for e in outgoing[v])]
    return {
        "is_dag": True,
        "roots": sorted(roots),
        "terminals": sorted(terminals),
        "root_to_terminal_path_count": sum(ways[v] for v in roots),
        "longest_path_edges": max((longest[v] for v in roots), default=0),
    }


def audit(graph):
    nodes = {n["id"]: n for n in graph["nodes"]}
    outgoing, incoming = defaultdict(list), defaultdict(list)
    for e in graph["edges"]:
        outgoing[e["source"]].append(e); incoming[e["target"]].append(e)
    comps = weak_components(nodes, graph["edges"])
    seeds = graph.get("seeds", [])
    profiles = []
    for i, comp in enumerate(comps, 1):
        edges = [e for e in graph["edges"] if e["source"] in comp]
        branches = sorted(v for v in comp if len(outgoing[v]) > 1)
        unresolved = [e for e in graph.get("unresolved_edges", []) if e["parent"] in comp]
        pm = dag_path_metrics(comp, outgoing, incoming)
        profiles.append({
            "component": i,
            "seed": next((s for s in seeds if s.lower() in {v.lower() for v in comp}), None),
            "nodes": len(comp), "resolved_edges": len(edges),
            "branchpoints": len(branches), "branchpoint_ids": branches,
            "branch_arities": dict(sorted(Counter(len(outgoing[v]) for v in comp).items())),
            "decay_modes": dict(sorted(Counter(e["mode"] for e in edges).items())),
            "unresolved_channels": len(unresolved),
            "A_range": [min(nodes[v]["a"] for v in comp), max(nodes[v]["a"] for v in comp)],
            **pm,
        })

    # Six bijections between three labelled graph components and three
    # putative helix strands are all equivalent: no spatial/phase/torsion
    # coordinates exist in the nuclide graph to rank them.
    permutations = list(itertools.permutations(range(1, len(comps)+1)))
    mapping_candidates = [
        {"strand_1_component": p[0], "strand_2_component": p[1], "strand_3_component": p[2]}
        for p in permutations
    ] if len(comps) == 3 else []

    all_components_branched = all(p["branchpoints"] > 0 for p in profiles)
    return {
        "schema": "gia-timdr-nrg01-three-strand-correspondence-audit-v0.1",
        "input_graph_schema": graph.get("schema"),
        "counts": {
            "weak_components": len(comps), "nodes": len(nodes),
            "resolved_edges": len(graph["edges"]),
            "unresolved_channels": len(graph.get("unresolved_edges", [])),
        },
        "component_profiles": profiles,
        "directed_graph": {
            "all_components_are_dags": all(p["is_dag"] for p in profiles),
            "each_component_has_internal_branching": all_components_branched,
            "three_way_branchpoints": [
                v for v in nodes if len(outgoing[v]) >= 3
            ],
        },
        "three_strand_mapping": {
            "candidate_bijections": mapping_candidates,
            "candidate_count": len(mapping_candidates),
            "ranking_possible_from_current_data": False,
            "reason": [
                "The nuclide graph has Z,N, decay labels and branching metadata, but no 3D coordinates, helix phase, signed geometric torsion or cardinal-point labels.",
                "All six assignments of three disconnected components to three named strands are therefore equally arbitrary.",
                "Every component contains branchpoints; a single smooth parametric strand cannot represent these forks without an explicit junction/branch object.",
                "The existing TIMDR trefoil reference is one closed 3D curve with three lobes, not three measured, independently parameterized helix strands."
            ],
            "strict_smooth_strand_compatibility": False if all_components_branched else None,
        },
        "cardinal_point_correspondence": {
            "identifiable": False,
            "reason": "No independent rule links nuclear branch events to geometric points on the TIMDR axis; assigning them by visual or ordinal similarity would be post hoc."
        },
        "handedness_preservation": {
            "nuclear_graph_has_signed_geometric_handedness": False,
            "helix_control_has_signed_torsion": True,
            "cross_domain_invariant_testable": False,
            "reason": "The nuclear graph contains no oriented 3D embedding; it cannot determine left/right helix handedness."
        },
        "conclusion": "Three disconnected decay components are observed, but they do not identify three TIMDR helix strands. A correspondence is not currently identifiable; the observed three-component count is conditional on the three selected decay-chain seeds.",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("graph", type=Path)
    ap.add_argument("--out", type=Path, default=Path("three_strand_correspondence_audit.json"))
    args = ap.parse_args()
    result = audit(json.loads(args.graph.read_text(encoding="utf-8")))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result["counts"], indent=2))
    for p in result["component_profiles"]:
        print(f"component {p['component']} seed={p['seed']} nodes={p['nodes']} edges={p['resolved_edges']} branches={p['branchpoints']} paths={p['root_to_terminal_path_count']}")
    print(result["conclusion"])
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
