"""
tests/test_sg_coupling_full_operator_hard_mode.py

Drugi ("twardy") rezim dla pelnego operatora Theta_bif, uzupelniajacy
"miekki" rezim juz przetestowany w test_sg_coupling_full_operator.py
(domyslne alpha=0.1, anomaly_bump=3.0, gdzie beta zostaje bliskie 1 -
patrz test_v2_beta_is_responsive_but_stays_high_for_this_specific_example).
Cel: pokazac DRUGA faze pracy operatora - wyrazne wejscie w tryb
kondensacji (beta wyraznie < 1, kanal S_up dominuje wzglednie nad S_down),
w odroznieniu od trybu miekkiego (beta~0.98, S_up praktycznie zerowe).

PRE-REJESTRACJA / JAK DOBRANO PARAMETRY (przed napisaniem testow ponizej):

Naiwna hipoteza "wiekszy alpha LUB silniejsza anomalia -> gleboko w Q"
okazala sie CZESCIOWO bledna przy pierwszym sprawdzeniu (siatka
(alpha, anomaly_bump) w [0.1..5]x[3..10]): beta_min zostawalo w zakresie
0.89-0.98 nawet dla alpha=2, bump=10 - bo mechanizm ma WBUDOWANE
SPRZEZENIE ZWROTNE OGRANICZAJACE SAME SIEBIE: gdy tylko Q>Q_crit,
operator natychmiast tlumi S (kanal S_down), co obniza Q w NASTEPNYM
kroku (dt=0.01, wiec bardzo czesto) - petla domyka sie sama, zanim Q
zdazy "uciec" daleko powyzej progu. To NIE jest blad operatora, tylko
realna wlasciwosc petli ujemnego sprzezenia zwrotnego (ten sam rodzaj
samoograniczenia, co pierwotny cel calego Theta_bif).

Dopiero rozszerzenie siatki o rzad(y) wielkosci wyzej (alpha do 10-20,
anomaly_bump do 100-120) ujawnilo DWIE rzeczy:
1. Przy alpha=10.0, anomaly_bump=100.0: Q_crit kalibruje sie na ~0.9359
   (samo tlo, z alpha=10, ma juz spora wlasna amplitude Q), a anomalia
   pcha Q do ~0.98 - naprawde gleboko - dajac beta_min~0.29 (i beta
   nawet w OSTATNIEJ probce okna anomalii ~0.51). To wybrany tu tryb
   "twardy" (HARD_ALPHA, HARD_ANOMALY_BUMP ponizej).
2. Przy alpha=15.0 (z domyslnym anomaly_bump): kalibrowane Q_crit
   WYCHODZI > 1.0 (~1.0225) - co jest niemozliwe do osiagniecia, bo
   Q(R) < 1 dla kazdego skonczonego R z definicji (Q=1-L0/L(R)). Oznacza
   to, ze dla dostatecznie duzego alpha kalibracja tla (margines 1.3x)
   moze wyprodukowac PROG NIEOSIAGALNY - cutoff nie wyzwoli sie NIGDY,
   niezaleznie od tego, jak silna bedzie anomalia. To realne, uczciwie
   odnotowane ograniczenie funkcji kalibracji (calibrate_q_crit w
   test_sg_coupling.py), NIE naprawiane tutaj (poza zakresem tego zadania -
   wymagaloby np. clampowania Q_crit do np. min(0.95, margines*tlo)) -
   udokumentowane jako test regresyjny ponizej, zeby nie zostac cicho
   zgubione.

HARD_ALPHA/HARD_ANOMALY_BUMP ponizej NIE sa "fizycznie realistyczne" -
to celowo ekstremalne wartosci testowe, dobrane WYLACZNIE zeby wymusic
Q daleko w gleb przedzialu [Q_crit, 1), analogicznie do tego, jak
test_theta_bifurcation.py uzywa Q=0.95 (kontrola 2) do testowania samego
operatora w oderwaniu od pelnej symulacji ze sprzezeniem zwrotnym.
"""
import numpy as np

from test_sg_coupling_full_operator import run_sg_coupling_simulation_v2
from test_sg_coupling import calibrate_q_crit

HARD_ALPHA = 10.0
HARD_ANOMALY_BUMP = 100.0


def _anomaly_slice(t, cutoff):
    return (t >= 4.8) & (t <= 5.2) & cutoff


def test_hard_mode_reaches_much_deeper_Q_than_soft_mode():
    t_soft, G_s, S_s, R_s, Q_soft, cutoff_soft, beta_s, sd_s, su_s = run_sg_coupling_simulation_v2()
    t_hard, G_h, S_h, R_h, Q_hard, cutoff_hard, beta_h, sd_h, su_h = run_sg_coupling_simulation_v2(
        alpha=HARD_ALPHA, anomaly_bump=HARD_ANOMALY_BUMP
    )
    mask_soft = _anomaly_slice(t_soft, cutoff_soft)
    mask_hard = _anomaly_slice(t_hard, cutoff_hard)
    assert Q_hard[mask_hard].max() > 0.9, "tryb twardy powinien pchnac Q naprawde gleboko (blisko sufitu 1.0)"
    assert Q_hard[mask_hard].max() > Q_soft[mask_soft].max(), "twardy rezim musi byc GLEBSZY niz miekki"


def test_hard_mode_beta_drops_clearly_below_half():
    t, G, S, R, Q, cutoff, beta, S_down, S_up = run_sg_coupling_simulation_v2(
        alpha=HARD_ALPHA, anomaly_bump=HARD_ANOMALY_BUMP
    )
    mask = _anomaly_slice(t, cutoff)
    assert np.any(mask), "brak probek cutoff w oknie anomalii dla trybu twardego"
    beta_hard = beta[mask]
    assert np.nanmin(beta_hard) < 0.5, (
        f"tryb twardy powinien dac wyrazne wejscie w kondensacje (beta<0.5), "
        f"dostano min beta={np.nanmin(beta_hard)}"
    )


def test_hard_mode_beta_minimum_is_clearly_lower_than_soft_mode_minimum():
    """Bezposrednie porownanie 'dwoch faz pracy operatora' - nie tylko
    ze twardy < 0.5, ale ze jest WYRAZNIE nizszy niz miekki (nie
    przypadkiem oba w podobnym zakresie)."""
    t_soft, G, S, R, Q, cutoff_soft, beta_soft, sd, su = run_sg_coupling_simulation_v2()
    t_hard, G2, S2, R2, Q2, cutoff_hard, beta_hard, sd2, su2 = run_sg_coupling_simulation_v2(
        alpha=HARD_ALPHA, anomaly_bump=HARD_ANOMALY_BUMP
    )
    min_soft = np.nanmin(beta_soft[_anomaly_slice(t_soft, cutoff_soft)])
    min_hard = np.nanmin(beta_hard[_anomaly_slice(t_hard, cutoff_hard)])
    assert min_hard < min_soft - 0.3, (
        f"oczekiwano wyraznej roznicy miedzy fazami: miekki={min_soft:.4f}, twardy={min_hard:.4f}"
    )


def test_soft_mode_condensation_channel_stays_negligible():
    """Kotwica regresyjna dla trybu miekkiego (kontrast dla testu
    ponizej): kanal S_up powinien byc PRAKTYCZNIE nieobecny wzgledem
    S_down w miekkim rezimie - to jest znany, juz wczesniej ustalony
    wynik (beta~0.98), tu wyrazony przez udzial |S_up| w calkowitej
    amplitudzie kanalow."""
    t, G, S, R, Q, cutoff, beta, S_down, S_up = run_sg_coupling_simulation_v2()
    mask = _anomaly_slice(t, cutoff)
    sd, su = np.abs(S_down[mask]), np.abs(S_up[mask])
    ratio_up = su[-1] / (sd[-1] + su[-1])
    assert ratio_up < 0.05, f"tryb miekki powinien miec znikomy udzial S_up, dostano {ratio_up:.4f}"


def test_hard_mode_condensation_channel_becomes_clearly_more_prominent():
    """Odwrotnosc powyzszego dla trybu twardego: udzial kanalu S_up w
    ostatniej probce okna anomalii powinien byc WYRAZNIE wiekszy niz w
    trybie miekkim - to jest empiryczna tresc 'wyraznej kondensacji',
    nie sam spadek beta w oderwaniu od reszty ukladu."""
    t, G, S, R, Q, cutoff, beta, S_down, S_up = run_sg_coupling_simulation_v2(
        alpha=HARD_ALPHA, anomaly_bump=HARD_ANOMALY_BUMP
    )
    mask = _anomaly_slice(t, cutoff)
    sd, su = np.abs(S_down[mask]), np.abs(S_up[mask])
    ratio_up = su[-1] / (sd[-1] + su[-1])
    assert ratio_up > 0.15, (
        f"tryb twardy powinien dac wyraznie wiekszy udzial kanalu kondensujacego, "
        f"dostano udzial={ratio_up:.4f}"
    )


def test_hard_mode_still_finite_no_overflow():
    """Nawet w ekstremalnym rezimie (alpha=10, bump=100) operator nie
    moze wyprodukowac inf/NaN - to byla glowna motywacja poprawki
    nasycenia tanh w theta_bifurcation.py, wiec musi to przetrwac i w
    trybie twardym, nie tylko w domyslnym miekkim."""
    t, G, S, R, Q, cutoff, beta, S_down, S_up = run_sg_coupling_simulation_v2(
        alpha=HARD_ALPHA, anomaly_bump=HARD_ANOMALY_BUMP
    )
    assert np.all(np.isfinite(S))
    assert np.all(np.isfinite(G))
    assert np.all(np.isfinite(R))
    assert np.all(np.isfinite(Q))


def test_calibration_can_become_unreachable_at_very_high_alpha():
    """UCZCIWIE ODNOTOWANE OGRANICZENIE (nie naprawiane tutaj, poza
    zakresem tego zadania): przy dostatecznie duzym alpha, sama
    kalibracja Q_crit (margines 1.3x nad maksimum tla) moze
    wyprodukowac prog > 1.0 - a Q(R) < 1 dla kazdego SKONCZONEGO R
    (Q=1-L0/L(R)), wiec taki prog jest MATEMATYCZNIE NIEOSIAGALNY.
    Skutek: cutoff nie wyzwoli sie NIGDY dla tego alpha, niezaleznie od
    tego, jak silna bedzie anomalia - odkryte przy szukaniu parametrow
    trybu twardego (alpha=15 z domyslnym anomaly_bump dawalo brak
    jakiegokolwiek zdarzenia cutoff). Test ponizej sprawdza to WPROST,
    zeby to ograniczenie bylo widoczne w pakiecie testow, a nie tylko
    w komentarzu."""
    Q_crit = calibrate_q_crit(margin=1.3, alpha=15.0)
    assert Q_crit > 1.0, "oczekiwano zademonstrowania nieosiagalnego progu przy tym alpha"

    t, G, S, R, Q, cutoff, beta, S_down, S_up = run_sg_coupling_simulation_v2(
        alpha=15.0, anomaly_bump=100.0
    )
    assert np.sum(cutoff) == 0, (
        "przy Q_crit>1 cutoff nie powinien wyzwolic sie ani razu, nawet z duza anomalia - "
        "potwierdza to realne ograniczenie kalibracji przy wysokim alpha"
    )
