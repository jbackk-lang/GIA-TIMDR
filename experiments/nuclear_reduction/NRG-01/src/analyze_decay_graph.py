#!/usr/bin/env python3
"""Analyze decay-graph branching and conservative 4->3 quotient candidates."""
import argparse
import json
from collections import Counter, defaultdict, deque
from pathlib import Path


def analyze(data):
    nodes = {n["id"]: n for n in data["nodes"]}
    edges = data["edges"]
    outgoing = defaultdict(list)
    incoming = defaultdict(list)
    for e in edges:
        outgoing[e["source"]].append(e)
        incoming[e["target"]].append(e)

    out_hist = Counter(len(outgoing[k]) for k in nodes)
    in_hist = Counter(len(incoming[k]) for k in nodes)
    branchpoints = []
    for key in nodes:
        degree = len(outgoing[key])
        if degree >= 2:
            branchpoints.append({
                "node": key,
                "outdegree": degree,
                "channels": [e["mode"] for e in outgoing[key]],
                "targets": [e["target"] for e in outgoing[key]],
                "branching_sum_percent": sum(
                    e["branching_percent"] or 0 for e in outgoing[key]
                ),
            })

    # A conservative bisimulation-style partition: states can share a class
    # only when their observed state labels and labelled successor classes agree.
    # It never merges solely to force a desired 4->3 result.
    labels = {
        k: (
            n.get("z"), n.get("n"), n.get("stability_status"),
            tuple(sorted(x["mode"] for x in n.get("decay_modes", []))),
        )
        for k, n in nodes.items()
    }
    classes = {k: str(labels[k]) for k in nodes}
    for _ in range(max(1, len(nodes))):
        signatures = {}
        for k in nodes:
            successors = tuple(sorted(
                (e["mode"], classes.get(e["target"], "UNRESOLVED"))
                for e in outgoing[k]
            ))
            signatures[k] = (labels[k], successors)
        unique = {sig: str(i) for i, sig in enumerate(sorted(set(signatures.values()), key=repr))}
        new_classes = {k: unique[signatures[k]] for k in nodes}
        if new_classes == classes:
            break
        classes = new_classes

    groups = defaultdict(list)
    for k, c in classes.items():
        groups[c].append(k)
    merge_candidates = [v for v in groups.values() if len(v) > 1]

    # Find connected 4-node induced motifs with at least one outgoing branch.
    undirected = defaultdict(set)
    for e in edges:
        undirected[e["source"]].add(e["target"])
        undirected[e["target"]].add(e["source"])
    motifs = set()
    for root in nodes:
        seen, q = {root}, deque([root])
        while q and len(seen) < 4:
            cur = q.popleft()
            for nxt in sorted(undirected[cur]):
                if nxt not in seen:
                    seen.add(nxt)
                    q.append(nxt)
                    if len(seen) == 4:
                        break
        if len(seen) == 4 and any(len(outgoing[x]) >= 2 for x in seen):
            motifs.add(tuple(sorted(seen)))

    return {
        "schema": "gia-timdr-nrg01-analysis-v0.1",
        "input_schema": data.get("schema"),
        "graph_counts": {
            "nodes": len(nodes), "resolved_edges": len(edges),
            "unresolved_edges": len(data.get("unresolved_edges", [])),
            "outdegree_histogram": dict(sorted(out_hist.items())),
            "indegree_histogram": dict(sorted(in_hist.items())),
        },
        "branchpoints": branchpoints,
        "four_state_branching_motifs": [list(x) for x in sorted(motifs)],
        "conservative_equivalence_classes": merge_candidates,
        "interpretation_guardrails": [
            "A graph vertex is a nuclide state, not a topological knot component.",
            "A branch point is a transition event, not automatically a helix cardinal point.",
            "No 4->3 reduction is accepted unless the equivalence relation preserves declared observables.",
            "Unresolved decay channels are excluded from resolved degree counts and remain visible in input data.",
        ],
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("graph", type=Path)
    p.add_argument("--out", type=Path, default=Path("graph_analysis.json"))
    a = p.parse_args()
    result = analyze(json.loads(a.graph.read_text(encoding="utf-8")))
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result["graph_counts"], indent=2))
    print(f"branchpoints={len(result['branchpoints'])}; four_state_motifs={len(result['four_state_branching_motifs'])}; equivalence_classes={len(result['conservative_equivalence_classes'])}")
    print(f"Wrote {a.out}")


if __name__ == "__main__":
    main()
