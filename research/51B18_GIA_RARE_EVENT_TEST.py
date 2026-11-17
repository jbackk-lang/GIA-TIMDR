"""51B.18 — exact counterexample against unconditional predictive sufficiency.

Run from repository root: python -m research.51B18_GIA_RARE_EVENT_TEST
(or python research/51B18_GIA_RARE_EVENT_TEST.py).
Uses actual core.trm_gia_projections.gia_select, not a rewritten copy.
No CI trigger or external data. Nats use natural logarithms.
"""
import math
from core.trm_gia_projections import Event, EventGraph, LineReference, gia_select

P_C = 0.05
P_F1_C = 0.99
P_F1_NOT_C = 0.01

def binary_entropy(p):
    return -p * math.log(p) - (1 - p) * math.log(1 - p)

def kl_bernoulli(p, q):
    return p * math.log(p / q) + (1 - p) * math.log((1 - p) / (1 - q))

def compressed(c, radius):
    # The graph has the same node IDs, times, edges, and node count for
    # both cases. Only the energy of the OUTSIDE event carries C.
    graph = EventGraph((
        Event("anchor", 1.0, 0.0, (0.0, 0.0, 0.0)),
        Event("signal", 1.0 + c, 1.0, (1.0, 1.0, 0.0)),
    ))
    ref = LineReference((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), radius)
    kept = gia_select(graph, ref)
    return tuple((e.id, e.energy, e.time, e.position) for e in kept.events), kept.edges

def run():
    q = P_C * P_F1_C + (1 - P_C) * P_F1_NOT_C
    # I(F;C) = H(F) - H(F|C), NOT H(F)-H(F|not C).
    full_loss = binary_entropy(q) - (
        P_C * binary_entropy(P_F1_C)
        + (1 - P_C) * binary_entropy(P_F1_NOT_C)
    )
    results = []
    for radius in (0.2, 0.8, 1.0, 1.2):
        z0, z1 = compressed(0, radius), compressed(1, radius)
        hidden = z0 == z1
        loss = full_loss if hidden else 0.0
        conditional = kl_bernoulli(P_F1_C, q) if hidden else 0.0
        results.append({
            "radius": radius, "same_code_for_C_and_not_C": hidden,
            "selected_nodes_if_not_C": len(z0[0]),
            "selected_nodes_if_C": len(z1[0]),
            "delta_nats": loss, "conditional_C_KL_nats": conditional,
        })
    assert results[0]["same_code_for_C_and_not_C"]
    assert not results[2]["same_code_for_C_and_not_C"]
    assert abs(results[0]["delta_nats"] - 0.168205541) < 1e-8
    assert results[2]["delta_nats"] == 0.0
    return results

if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2))
