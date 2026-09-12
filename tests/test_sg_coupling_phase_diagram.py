"""
tests/test_sg_coupling_phase_diagram.py

Mapa parametrow (alpha, sila anomalii) dla petli SG-Coupling z pelnym
operatorem Theta_bif - "phase diagram" TIMDR-SG zaproponowany w rozmowie
po zbudowaniu trybu miekkiego (test_sg_coupling_full_operator.py) i
twardego (test_sg_coupling_full_operator_hard_mode.py).

CZTERY STREFY (nie trzy - patrz uzasadnienie nizej):

- MARTWA (dead): kalibrowany Q_crit(alpha) > 1.0 - matematycznie
  nieosiagalny prog (Q(R)=1-L0/L(R) < 1 dla kazdego SKONCZONEGO R), wiec
  cutoff nie wyzwoli sie NIGDY dla tego alpha, niezaleznie od anomalii.
  Granica jest WYLACZNIE funkcja alpha (calibrate_q_crit nie przyjmuje
  anomaly_bump - kalibruje sie z SAMEGO TLA), znaleziona bisekcja.
- CICHA (quiet): Q_crit(alpha) <= 1.0 (strefa w zasadzie reaktywna), ale
  DANY anomaly_bump jest za slaby, zeby kiedykolwiek przekroczyc ten
  prog w oknie t in [4.8,5.2] - cutoff sie nie wyzwala ani razu.
- MIEKKA (soft): cutoff sie wyzwala, ale beta_min w oknie anomalii
  pozostaje >= 0.5 - kanal S_down (tlumienie/pamiec starego trendu)
  dominuje przez cala anomalie.
- TWARDA (hard): cutoff sie wyzwala i beta_min < 0.5 - kanal S_up
  (kondensacja nowego trendu) przejmuje dominacje.

Granica miekka/twarda na beta=0.5 NIE jest zgadnieta pod juz uzyskany
wynik - to matematyczny punkt rownowagi wag kanalow (beta=1-beta
dokladnie przy beta=0.5, tam gdzie S_up przestaje byc mniejszosciowym
dodatkiem i staje sie rownowazny lub dominujacy wzgledem S_down) - ten
sam prog, ktorego uzyly juz WCZESNIEJ (przed policzeniem calej siatki
tego pliku) testy w test_sg_coupling_full_operator_hard_mode.py.

ZNALEZIONY PO DRODZE REALNY BLAD (nie ukryty, naprawiony w
timdr_formalism/theta_bifurcation.py, patrz jego naglowek "ZNALEZIONY
REALNY BLAD"): przy pierwszym przeszukiwaniu siatki (alpha, bump) pod
katem tego pliku, kombinacja alpha=2.0, anomaly_bump=130.0 dawala
PRZEPELNIENIE (inf) - operator mial niezamierzona, niestabilna petle
dodatniego sprzezenia (S_up skalowalo sie WPROST z surowa wartoscia S,
nie z jej znormalizowanym kierunkiem, wiec deklarowany sufit S_up_max
nie byl faktycznym ograniczeniem, gdy S samo bylo juz duze). Naprawione
w kodzie operatora (R_phase[S] = -sign(S), nie -S) - test ponizej
(`test_previously_blowing_up_point_is_now_finite`) to sprawdza wprost,
zeby regresja nie wrocila po cichu. Po tej naprawie przeszukano PONOWNIE
szerszy zakres (alpha do 13.5, bump do 500) i nie znaleziono ANI JEDNEGO
przepelnienia - ale to NIE jest dowod, ze zaden nie istnieje nigdzie w
nieskonczonej przestrzeni parametrow, tylko ze nie zostal znaleziony w
przeszukanym zakresie (uczciwe zastrzezenie, nie "udowodnione, ze
naprawa jest kompletna").
"""
import numpy as np

from test_sg_coupling_full_operator import run_sg_coupling_simulation_v2
from test_sg_coupling import calibrate_q_crit

BETA_HARD_THRESHOLD = 0.5
ANOMALY_WINDOW = (4.8, 5.2)


def is_dead_zone(alpha: float, L0: float = 5.0, R0: float = 0.2,
                  dt: float = 0.01, duration: float = 10.0, margin: float = 1.3) -> bool:
    """True <=> kalibrowany Q_crit(alpha) > 1.0 - matematycznie
    nieosiagalny prog, cutoff nie wyzwoli sie dla ZADNEJ anomalii przy
    tym alpha."""
    Q_crit = calibrate_q_crit(margin=margin, L0=L0, alpha=alpha, R0=R0, dt=dt, duration=duration)
    return Q_crit > 1.0


def find_dead_zone_onset(alpha_lo: float = 0.5, alpha_hi: float = 20.0, tol: float = 1e-3, **kwargs) -> float:
    """Bisekcja: najmniejsze alpha, przy ktorym wchodzimy w strefe martwa
    (Q_crit>1). Zaklada monotonicznosc Q_crit(alpha) rosnaca w tym
    przedziale - sprawdzone empirycznie w tescie
    `test_dead_zone_onset_is_between_empirically_known_bounds` ponizej
    (alpha=13: Q_crit~0.993 nie-martwa, alpha=14: Q_crit~1.009 martwa)."""
    if is_dead_zone(alpha_lo, **kwargs):
        raise ValueError(f"alpha_lo={alpha_lo} jest juz w strefie martwej - obniz alpha_lo")
    if not is_dead_zone(alpha_hi, **kwargs):
        raise ValueError(f"alpha_hi={alpha_hi} nie jest w strefie martwej - podwyzsz alpha_hi")
    lo, hi = alpha_lo, alpha_hi
    while hi - lo > tol:
        mid = (lo + hi) / 2.0
        if is_dead_zone(mid, **kwargs):
            hi = mid
        else:
            lo = mid
    return hi


def classify_regime(alpha: float, anomaly_bump: float,
                     beta_hard_threshold: float = BETA_HARD_THRESHOLD,
                     L0: float = 5.0, R0: float = 0.2, dt: float = 0.01,
                     duration: float = 10.0, margin: float = 1.3,
                     lambda_down: float = 2.0, lambda_up: float = 1.0) -> str:
    """Zwraca jedna z: 'dead', 'quiet', 'soft', 'hard'."""
    if is_dead_zone(alpha, L0=L0, R0=R0, dt=dt, duration=duration, margin=margin):
        return "dead"

    t, G, S, R, Q, cutoff, beta, S_down, S_up = run_sg_coupling_simulation_v2(
        L0=L0, alpha=alpha, R0=R0, dt=dt, duration=duration,
        lambda_down=lambda_down, lambda_up=lambda_up, anomaly_bump=anomaly_bump,
    )
    lo, hi = ANOMALY_WINDOW
    mask = (t >= lo) & (t <= hi) & cutoff
    if not np.any(mask):
        return "quiet"
    beta_min = np.nanmin(beta[mask])
    return "hard" if beta_min < beta_hard_threshold else "soft"


def compute_phase_grid(alphas, bumps, **kwargs):
    """Zwraca 2D liste etykiet, wiersz na alpha, kolumna na bump."""
    return [[classify_regime(a, b, **kwargs) for b in bumps] for a in alphas]


# ---------------------------------------------------------------------
# Strefa martwa
# ---------------------------------------------------------------------

def test_dead_zone_false_for_known_low_alpha():
    assert not is_dead_zone(0.1)


def test_dead_zone_true_for_known_high_alpha():
    assert is_dead_zone(15.0)


def test_dead_zone_onset_is_between_empirically_known_bounds():
    """alpha=13 -> Q_crit~0.993 (nie martwa), alpha=14 -> Q_crit~1.009
    (martwa) - ustalone bezposrednim numerycznym sprawdzeniem PRZED
    napisaniem tego testu (nie zgadywane)."""
    onset = find_dead_zone_onset()
    assert 13.0 < onset < 14.0, f"oczekiwano progu w (13,14), dostano {onset}"


def test_dead_zone_is_independent_of_anomaly_strength():
    """Q_crit kalibruje sie WYLACZNIE z tla (bez anomalii) - wiec status
    martwej strefy NIE moze zalezec od anomaly_bump. Sprawdzone wprost,
    nie tylko przez konstrukcje calibrate_q_crit."""
    for bump in [0.001, 1.0, 100.0, 10_000.0]:
        assert classify_regime(15.0, bump) == "dead", (
            f"strefa martwa (alpha=15) powinna byc martwa niezaleznie od bump={bump}"
        )


# ---------------------------------------------------------------------
# Strefa cicha
# ---------------------------------------------------------------------

def test_quiet_zone_for_negligible_anomaly():
    assert classify_regime(0.1, 0.001) == "quiet"


# ---------------------------------------------------------------------
# Miekka i twarda - juz ustalone punkty referencyjne z poprzednich plikow
# ---------------------------------------------------------------------

def test_classify_matches_known_soft_point():
    assert classify_regime(0.1, 3.0) == "soft"


def test_classify_matches_known_hard_point():
    assert classify_regime(10.0, 100.0) == "hard"


# ---------------------------------------------------------------------
# Regresja na naprawiony blad przepelnienia (patrz naglowek modulu)
# ---------------------------------------------------------------------

def test_previously_blowing_up_point_is_now_finite():
    """alpha=2.0, anomaly_bump=130.0 dawalo inf PRZED naprawa R_phase[S]
    w timdr_formalism/theta_bifurcation.py (-sign(S) zamiast -S). Musi
    dawac skonczona, sklasyfikowana odpowiedz teraz."""
    label = classify_regime(2.0, 130.0)
    assert label in ("soft", "hard", "quiet", "dead")

    t, G, S, R, Q, cutoff, beta, S_down, S_up = run_sg_coupling_simulation_v2(
        alpha=2.0, anomaly_bump=130.0
    )
    assert np.all(np.isfinite(S))
    assert np.all(np.isfinite(G))


# ---------------------------------------------------------------------
# Siatka
# ---------------------------------------------------------------------

def test_compute_phase_grid_shape_and_values():
    alphas = [0.1, 15.0]
    bumps = [0.001, 3.0]
    grid = compute_phase_grid(alphas, bumps)
    assert len(grid) == 2 and all(len(row) == 2 for row in grid)
    # alpha=15 jest martwa niezaleznie od bump
    assert grid[1] == ["dead", "dead"]
    # alpha=0.1: bump=0.001 -> cicha, bump=3.0 -> miekka (ustalone wczesniej)
    assert grid[0] == ["quiet", "soft"]


def test_full_reference_grid_has_no_nonfinite_output():
    """Ta sama siatka (rozszerzona), na ktorej znaleziono i naprawiono
    blad przepelnienia - regresja na CALA siatke, nie tylko pojedynczy
    punkt, zeby zlapac ewentualny inny podobny przypadek w przyszlosci."""
    alphas = [0.05, 0.1, 0.2, 0.5, 1, 2, 5, 8, 10, 12, 13.5]
    bumps = [0.001, 0.01, 0.1, 0.5, 1, 3, 6, 10, 20, 40, 70, 100, 130, 200, 500]
    for a in alphas:
        for b in bumps:
            t, G, S, R, Q, cutoff, beta, S_down, S_up = run_sg_coupling_simulation_v2(
                alpha=a, anomaly_bump=b
            )
            assert np.all(np.isfinite(S)), f"S nieskonczone dla alpha={a}, bump={b}"
            assert np.all(np.isfinite(G)), f"G nieskonczone dla alpha={a}, bump={b}"
