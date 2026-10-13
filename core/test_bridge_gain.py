"""Testy bridge_gain: zgodnosc wzoru z LDA, kontrola negatywna, przewidywanie vs obserwacja na zbiorze testowym."""
import numpy as np
from bridge_gain import (predict_bridge, bridge_gain_d2, bridge_dprime, n_min,
                         reference_gain, auc_from_d, compare)


def sample(n1, n0, d1, d2, rho, rng):
    C = np.array([[1, rho], [rho, 1]])
    L = np.linalg.cholesky(C)
    X0 = rng.standard_normal((n0, 2)) @ L.T
    X1 = rng.standard_normal((n1, 2)) @ L.T + np.array([d1, d2])
    return X1[:, 0], X1[:, 1], X0[:, 0], X0[:, 1]


def auc_empirical(s1, s0):
    allv = np.concatenate([s1, s0])
    ranks = allv.argsort().argsort() + 1
    n1, n0 = len(s1), len(s0)
    return (ranks[:n1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)


def bridge_auc_on(test, pred_train_weights):
    A1, B1, A0, B0 = test
    w = pred_train_weights
    return auc_empirical(w[0] * A1 + w[1] * B1, w[0] * A0 + w[1] * B0)


def lda_weights(A1, B1, A0, B0):
    X1, X0 = np.column_stack([A1, B1]), np.column_stack([A0, B0])
    mu = X1.mean(0) - X0.mean(0)
    n1, n0 = len(X1), len(X0)
    S = ((n1 - 1) * np.cov(X1, rowvar=False) + (n0 - 1) * np.cov(X0, rowvar=False)) / (n1 + n0 - 2)
    return np.linalg.solve(S, mu)


def test_formula_matches_lda():
    rng = np.random.default_rng(0)
    for d1, d2, rho in [(1.5, 1.0, 0.0), (1.5, 1.0, 0.4), (1.5, 1.0, -0.5), (2.0, 0.5, 0.7)]:
        p = predict_bridge(*sample(40000, 40000, d1, d2, rho, rng))
        assert abs(p.d_bridge - p.lda_check) < 0.05, (d1, d2, rho, p.d_bridge, p.lda_check)
        assert abs(p.d_bridge - bridge_dprime(d1, d2, rho)) < 0.06


def test_negative_control_zero_gain():
    # rho = d2/d1 -> zysk mostu = 0 (druga galaz nic nie wnosi)
    assert abs(bridge_gain_d2(2.0, 1.0, 0.5)) < 1e-12
    assert bridge_gain_d2(2.0, 1.0, 0.0) > 0.99        # niezalezne: zysk = d2^2
    assert bridge_gain_d2(2.0, 1.0, -0.5) > bridge_gain_d2(2.0, 1.0, 0.0)  # ujemna korelacja zwieksza zysk


def test_naive_sum_can_lose():
    # naiwna suma A+B bez wag moze byc gorsza od samej A
    rng = np.random.default_rng(1)
    A1, B1, A0, B0 = sample(40000, 40000, 2.0, 0.2, 0.0, rng)
    assert auc_empirical(A1 + B1, A0 + B0) < auc_empirical(A1, A0)


def test_prediction_vs_observed_out_of_sample():
    rng = np.random.default_rng(2)
    tr = sample(300, 300, 1.2, 0.9, 0.3, rng)
    te = sample(5000, 5000, 1.2, 0.9, 0.3, rng)
    p = predict_bridge(*tr)
    obs = bridge_auc_on(te, lda_weights(*tr))
    assert compare(p, obs, tol=0.03)["within_tol"], (p.auc_bridge, obs)


def test_violated_assumption_is_detected():
    # naruszone A2: rozne rho pod H0 i H1 -> przewidywanie moze odbiegac; test sprawdza tylko, ze compare to raportuje
    rng = np.random.default_rng(3)
    A1, B1, A0, B0 = sample(300, 300, 1.2, 0.9, 0.0, rng)
    # H1 z silna korelacja
    C = np.array([[1, 0.9], [0.9, 1]]); L = np.linalg.cholesky(C)
    X1 = rng.standard_normal((300, 2)) @ L.T + np.array([1.2, 0.9])
    p = predict_bridge(X1[:, 0], X1[:, 1], A0, B0)
    te1 = rng.standard_normal((5000, 2)) @ L.T + np.array([1.2, 0.9])
    te0 = rng.standard_normal((5000, 2))
    obs = bridge_auc_on((te1[:, 0], te1[:, 1], te0[:, 0], te0[:, 1]),
                        lda_weights(X1[:, 0], X1[:, 1], A0, B0))
    r = compare(p, obs, tol=0.01)
    assert "diff" in r  # wynik raportowany, nie ukrywany


def test_n_min_and_reference():
    assert abs(n_min(0.5, 0.05, 0.9) - ((1.6449 + 1.2816) / 0.5) ** 2) < 0.05
    assert reference_gain(4.0, 1.0, 0.5) > 1       # var_z > var_n2 -> oplaca sie
    assert reference_gain(0.2, 1.0, 0.5) < 1       # zaklocenie wspolne slabsze od szumu odniesienia
    assert abs(auc_from_d(0.0) - 0.5) < 1e-12


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("ok", name)
