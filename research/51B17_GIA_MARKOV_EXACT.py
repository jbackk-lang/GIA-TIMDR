"""51B.17: exact predictive-information test of reference gia_select.

No external data. Analytic two-state stationary Markov chain; the latest
symbol is encoded in the spatial position of the latest event. A frozen
PCA tube removes the event for symbol 1. This is a falsification test,
not a general claim about all GIA implementations.
"""
import math
from core.trm_gia_projections import Event, EventGraph, LineReference, gia_select

P_STAY = 0.9
REFERENCE = LineReference((0., 0., 0.), (1., 0., 0.), 0.2)


def kl_bernoulli(p, q):
    return p * math.log(p / q) + (1-p) * math.log((1-p) / (1-q))


def selected_code(bit):
    # All histories share one anchor. The last event encodes the Markov state.
    graph = EventGraph((
        Event("anchor", 1., 0., (0., 0., 0.)),
        Event("latest", 1., 1., (1., float(bit), 0.)),
    ))
    selected = gia_select(graph, REFERENCE)
    return tuple(e.id for e in selected.events)


def run():
    # Stationary X_t~Bernoulli(1/2), P(X_{t+1}=X_t)=0.9.
    codes = {x: selected_code(x) for x in (0, 1)}
    assert codes[0] != codes[1], "The tube must distinguish the two states"
    # The code reveals X_t exactly; hence loss must be zero.
    loss_selected = 0.0
    # A more aggressive, equally well-defined compression retaining only
    # the count of selected events also reveals X_t in this construction.
    loss_count = 0.0
    # If we drop the last event entirely, Z is constant, P(F=1|Z)=0.5.
    loss_constant = kl_bernoulli(0.9, 0.5)
    # I(F;H)=ln2-h_b(0.1) in nats; I(F;H|Z_const)=this quantity.
    entropy_binary = lambda p: -p*math.log(p)-(1-p)*math.log(1-p)
    assert abs(loss_constant - (math.log(2)-entropy_binary(0.1))) < 1e-12
    return {"status": "EXACT_SYNTHETIC", "p_stay": P_STAY,
            "code_0": codes[0], "code_1": codes[1],
            "delta_gia_full_selected_graph_nats": loss_selected,
            "delta_gia_selected_count_nats": loss_count,
            "delta_drop_latest_nats": loss_constant,
            "note": "This example is a positive sanity check only; it does not show superiority."}


if __name__ == "__main__":
    import json
    print(json.dumps(run(), indent=2))
