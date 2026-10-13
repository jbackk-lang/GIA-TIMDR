"""bridge_gain.py -- przewidywanie zysku mostu TIMDR PRZED testem (model gaussowski).

Struktura: detekcja = kompromis P_d vs P_fa (front Pareto = krzywa ROC). Zysk bez straty
to przesuniecie frontu, czyli wzrost d'. Ten modul liczy z DANYCH TRENINGOWYCH, o ile
d' wzrosnie po polaczeniu dwoch statystyk (mostu), ile cykli trzeba i czy odniesienie
warto budowac -- i zapisuje to jako przewidywanie do PREREG.

ZALOZENIA (sprawdz je; ich naruszenie jest wynikiem, nie bledem):
  A1. Statystyki ~ gaussowskie, przesuniecie sredniej miedzy H0 i H1.
  A2. Ta sama macierz kowariancji pod H0 i H1 (rho liczone pod H0).
  A3. Cykle/probki niezalezne (dla wzoru na N_min).
Odchylenie wyniku od przewidywania mowi, ktore zalozenie nie trzyma.

Wzory:
  d'^2 (most)  = (d1^2 - 2 rho d1 d2 + d2^2) / (1 - rho^2)
  zysk mostu   = d'^2 - max(d1,d2)^2 = (d_slabsza - rho d_lepsza)^2 / (1 - rho^2)
  N_min        = ((Q^-1(alpha) - Q^-1(1-beta)) / d1)^2
  zysk odn.    = (var_z + var_n1) / (var_n1 + var_n2)        [w d'^2]
  AUC (gauss)  = Phi(d' / sqrt(2));   P_d(alpha) = Q(Q^-1(alpha) - d')
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass, asdict
from statistics import NormalDist

import numpy as np

_N = NormalDist()


def Q(x: float) -> float:
    """Ogon standardowego rozkladu normalnego, P(Z > x)."""
    return 1.0 - _N.cdf(x)


def Qinv(p: float) -> float:
    return _N.inv_cdf(1.0 - p)


# ---------- wzory zamkniete ----------

def auc_from_d(d: float) -> float:
    return _N.cdf(d / math.sqrt(2.0))


def pd_at_alpha(d: float, alpha: float) -> float:
    return Q(Qinv(alpha) - d)


def bridge_dprime(d1: float, d2: float, rho: float) -> float:
    """d' optymalnego polaczenia dwoch statystyk (wzor 1). Wymaga |rho| < 1."""
    if abs(rho) >= 1.0:
        raise ValueError("|rho| musi byc < 1 (statystyki zdegenerowane)")
    v = (d1 * d1 - 2.0 * rho * d1 * d2 + d2 * d2) / (1.0 - rho * rho)
    return math.sqrt(max(v, 0.0))


def bridge_gain_d2(d1: float, d2: float, rho: float) -> float:
    """Zysk mostu w d'^2 wzgledem lepszej galezi: (d_slab - rho d_lepsza)^2 / (1-rho^2)."""
    hi, lo = (d1, d2) if abs(d1) >= abs(d2) else (d2, d1)
    return (lo - rho * hi) ** 2 / (1.0 - rho * rho)


def n_min(d_per_cycle: float, alpha: float, power: float) -> float:
    """Minimalna liczba niezaleznych cykli dla P_fa=alpha i P_d=power (wzor 2)."""
    return ((Qinv(alpha) - Qinv(power)) / d_per_cycle) ** 2


def reference_gain(var_z: float, var_n1: float, var_n2: float) -> float:
    """Mnoznik d'^2 po zastosowaniu odniesienia z tego samego osrodka (wzor 3).
    >1 oplaca sie budowac odniesienie; <=1 nie (warunek: var_z > var_n2)."""
    return (var_z + var_n1) / (var_n1 + var_n2)


# ---------- estymacja z danych treningowych ----------

def dprime_1d(x1: np.ndarray, x0: np.ndarray) -> float:
    """d' = (mean1-mean0)/sqrt(pooled var); znak zachowany."""
    n1, n0 = len(x1), len(x0)
    pooled = ((n1 - 1) * np.var(x1, ddof=1) + (n0 - 1) * np.var(x0, ddof=1)) / (n1 + n0 - 2)
    return float((np.mean(x1) - np.mean(x0)) / math.sqrt(pooled))


def lda_dprime(X1: np.ndarray, X0: np.ndarray) -> float:
    """d' = sqrt(mu^T Sigma^-1 mu) z kowariancji zbiorczej (kontrola wzoru 1 i estymator wprost)."""
    mu = X1.mean(0) - X0.mean(0)
    n1, n0 = len(X1), len(X0)
    S = ((n1 - 1) * np.cov(X1, rowvar=False) + (n0 - 1) * np.cov(X0, rowvar=False)) / (n1 + n0 - 2)
    return float(math.sqrt(max(mu @ np.linalg.solve(S, mu), 0.0)))


@dataclass
class BridgePrediction:
    d1: float            # d' galezi A (train)
    d2: float            # d' galezi B (train)
    rho_H0: float        # korelacja A,B pod H0 (train)
    d_bridge: float      # przewidywane d' mostu
    gain_d2: float       # przewidywany zysk w d'^2
    auc_A: float
    auc_B: float
    auc_bridge: float    # przewidywane AUC mostu
    pd_bridge_at_alpha: float
    alpha: float
    n_train_H1: int
    n_train_H0: int
    lda_check: float     # d' z LDA wprost -- powinno ~ d_bridge (kontrola A1/A2)


def predict_bridge(A1, B1, A0, B0, alpha: float = 0.05) -> BridgePrediction:
    """Z cech galezi A i B na danych TRENINGOWYCH (H1: *1, H0: *0) -> przewidywanie mostu.
    Wywolaj PRZED odslonieciem danych testowych i zapisz wynik w PREREG."""
    A1, B1, A0, B0 = (np.asarray(v, float) for v in (A1, B1, A0, B0))
    d1, d2 = dprime_1d(A1, A0), dprime_1d(B1, B0)
    rho = float(np.corrcoef(A0, B0)[0, 1])
    db = bridge_dprime(d1, d2, rho)
    X1, X0 = np.column_stack([A1, B1]), np.column_stack([A0, B0])
    return BridgePrediction(
        d1=d1, d2=d2, rho_H0=rho, d_bridge=db,
        gain_d2=bridge_gain_d2(d1, d2, rho),
        auc_A=auc_from_d(abs(d1)), auc_B=auc_from_d(abs(d2)), auc_bridge=auc_from_d(db),
        pd_bridge_at_alpha=pd_at_alpha(db, alpha), alpha=alpha,
        n_train_H1=len(A1), n_train_H0=len(A0), lda_check=lda_dprime(X1, X0),
    )


def compare(pred: BridgePrediction, observed_auc_bridge: float, tol: float = 0.03) -> dict:
    """Po ttescie: czy zaobserwowane AUC mostu zgadza sie z przewidzianym? Wynik rozbieznosci
    jest wynikiem (model gaussowski nie opisuje tego mostu), nie powodem do strojenia."""
    diff = observed_auc_bridge - pred.auc_bridge
    return {"predicted_auc": pred.auc_bridge, "observed_auc": observed_auc_bridge,
            "diff": diff, "within_tol": abs(diff) <= tol, "tol": tol}


def prereg_block(name: str, pred: BridgePrediction, tol: float = 0.03) -> str:
    """Tekst do wklejenia w PREREG_*.md przed uruchomieniem testu."""
    return (
        f"## Przewidywanie mostu: {name}\n"
        f"Model: gaussowski (A1-A3, patrz bridge_gain.py). Dane: wylacznie treningowe.\n"
        f"- d1 = {pred.d1:.3f}, d2 = {pred.d2:.3f}, rho_H0 = {pred.rho_H0:.3f}\n"
        f"- przewidywane d' mostu = {pred.d_bridge:.3f} (kontrola LDA: {pred.lda_check:.3f})\n"
        f"- przewidywane AUC: A = {pred.auc_A:.3f}, B = {pred.auc_B:.3f}, most = {pred.auc_bridge:.3f}\n"
        f"- przewidywane P_d przy P_fa = {pred.alpha}: {pred.pd_bridge_at_alpha:.3f}\n"
        f"- zysk w d'^2 wzgledem lepszej galezi: {pred.gain_d2:.3f}\n"
        f"Kryterium: |AUC_obs - AUC_pred| <= {tol}. Jedno uruchomienie na danych nieogladanych.\n"
        f"Rozbieznosc = wynik negatywny dla modelu gaussowskiego; bez strojenia po fakcie.\n"
    )


if __name__ == "__main__":
    import sys
    # uzycie: python bridge_gain.py train.npz   (klucze: A1,B1,A0,B0)
    if len(sys.argv) == 2:
        z = np.load(sys.argv[1])
        p = predict_bridge(z["A1"], z["B1"], z["A0"], z["B0"])
        print(prereg_block(sys.argv[1], p))
        print(json.dumps(asdict(p), indent=2))
    else:
        print(__doc__)
