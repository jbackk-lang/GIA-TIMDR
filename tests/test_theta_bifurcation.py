"""
tests/test_theta_bifurcation.py

Testy dla pelnego operatora Theta_bif (timdr_formalism/theta_bifurcation.py).
Patrz PRE-REJESTRACJA w naglowku tego modulu dla pelnego uzasadnienia
progow/oczekiwan ponizej.
"""
import numpy as np
import pytest

from timdr_formalism.theta_bifurcation import (
    theta_bifurcation,
    compute_beta,
    S_UP_MAX_DEFAULT,
)


# ---------------------------------------------------------------------
# Poza trybem bifurkacji: brak ingerencji
# ---------------------------------------------------------------------

def test_below_threshold_returns_unchanged_signal():
    result = theta_bifurcation(S=0.7, Q=0.2, Q_crit=0.35, time_since_cutoff_start=0.0)
    assert result.in_bifurcation is False
    assert result.S_new == 0.7


def test_exactly_at_threshold_returns_unchanged_signal():
    result = theta_bifurcation(S=0.7, Q=0.35, Q_crit=0.35, time_since_cutoff_start=0.0)
    assert result.in_bifurcation is False
    assert result.S_new == 0.7


# ---------------------------------------------------------------------
# compute_beta: monotonicznosc i granice
# ---------------------------------------------------------------------

def test_beta_is_one_deep_below_the_soft_margin():
    """ZMIENIONE 2026-09-12 (patrz timdr_formalism/theta_bifurcation.py,
    "DODANY MARGINES OSTRZEGAWCZY"): przed dodaniem anticipation_fraction,
    ta funkcja nazywala sie test_beta_is_one_just_above_threshold i
    sprawdzala beta(Q=0.351, Q_crit=0.35) - to juz NIE jest prawda,
    bo Q=0.351 wpada teraz w miekki margines ostrzegawczy PONIZEJ
    prawdziwego progu (Q_eff_crit=0.285 dla Q_crit=0.35,
    anticipation_fraction=0.1 domyslne) i celowo NIE daje juz beta~1 -
    patrz test_beta_is_in_class_II_range_at_threshold ponizej dla
    nowego, zamierzonego zachowania W TYM miejscu. Ten test sprawdza
    zamiast tego to, co WCIAZ powinno byc prawda: DALEKO ponizej
    marginesu (tu Q=0.2, wyraznie < Q_eff_crit=0.285) beta jest
    dokladnie 1.0 - Klasa I, brak jakiejkolwiek antycypacji."""
    beta = compute_beta(Q=0.2, Q_crit=0.35)
    assert beta == 1.0


def test_beta_is_in_class_II_range_at_threshold():
    """Bezposrednia weryfikacja zamierzonego skutku marginesu
    ostrzegawczego: PRZY samym progu Q=Q_crit (i tuz nad nim), beta
    powinno byc w przedziale (0.8,1.0) - dokladnie wymog oficjalnej
    definicji Klasy II (`docs/theory/Signal_Classes.md`), NIE ~1.0 jak
    w starym, czysto skokowym wzorze."""
    beta_at_crit = compute_beta(Q=0.35, Q_crit=0.35)
    assert 0.8 < beta_at_crit < 1.0
    beta_just_above = compute_beta(Q=0.351, Q_crit=0.35)
    assert 0.8 < beta_just_above < 1.0


def test_beta_approaches_zero_near_q_equals_one():
    beta = compute_beta(Q=0.999, Q_crit=0.35)
    assert beta < 0.01


def test_beta_is_monotonically_decreasing_in_Q():
    Qs = np.linspace(0.35, 0.999, 50)
    betas = [compute_beta(q, Q_crit=0.35) for q in Qs]
    assert all(b1 >= b2 for b1, b2 in zip(betas, betas[1:])), "beta powinno byc nierosnace wraz z Q"


def test_beta_always_in_unit_interval():
    for q in np.linspace(0.0, 1.0, 200):
        b = compute_beta(q, Q_crit=0.35)
        assert 0.0 <= b <= 1.0


# ---------------------------------------------------------------------
# Kontrola 1: lekkie przekroczenie -> dominuje tlumienie, |S| maleje
# ---------------------------------------------------------------------

def test_mild_exceedance_converges_to_small_nonzero_plateau_not_zero():
    """ZNALEZIONE PRZY PISANIU TESTOW (nie zalozone z gory): pierwsza
    wersja tego testu zakladala, ze lekkie przekroczenie progu powinno
    zanikac do ~0 w dlugim czasie. To bylo bledne zalozenie o WLASNYM
    modelu, nie blad kodu -- rzeczywista struktura operatora (kanal
    S_up nasyca sie przez tanh do (1-beta)*S_up_max, NIE do zera, dla
    KAZDEGO niezerowego (1-beta)) oznacza, ze nawet BARDZO lekkie
    przekroczenie progu zostawia TRWALY, niezerowy "odcisk" w sygnale,
    zamiast w pelni zanikac. To jest uczciwie odnotowana wlasciwosc
    modelu (kompromis wprowadzony poprawka nasycenia z blow-up), nie
    cicho poprawiony test, zeby przeszedl.

    ZMIENIONE 2026-09-12 (margines ostrzegawczy w compute_beta - patrz
    modul theta_bifurcation.py, anticipation_fraction=0.05 wyliczone z
    wymogow Klasy II): przy Q_mild=0.36, Q_crit=0.35 beta wynosi teraz
    ~0.938 (bylo ~0.9846 przed dodaniem anticipation_fraction), wiec
    plateau ~0.623 (bylo <0.6 przed zmiana) - zweryfikowane
    bezposrednio, nie zgadywane; granica testu zaktualizowana zeby
    odzwierciedlac PRAWDZIWA, nowa wartosc, nie zeby ukryc zmiane
    zachowania."""
    Q_mild = 0.36  # tuz nad Q_crit=0.35 -> beta~0.938 (z domyslnym anticipation_fraction=0.05)
    S0 = 2.0
    magnitudes = [
        abs(theta_bifurcation(S=S0, Q=Q_mild, Q_crit=0.35, time_since_cutoff_start=dt).S_new)
        for dt in [0.0, 5.0, 20.0, 100.0]
    ]
    # Powinno ZBIEGAC (roznica miedzy kolejnymi coraz mniejsza), nie
    # koniecznie malec caly czas (przejsciowo moze przejsc przez zero,
    # bo S_down i S_up maja przeciwne znaki - zobacz wydruk w konwersacji).
    assert abs(magnitudes[-1] - magnitudes[-2]) < 1e-3, "powinno ustabilizowac sie na plateau"
    # Plateau jest NIEZEROWE, ale nadal wyraznie mniejsze niz S_UP_MAX (10.0)
    # - lekkie przekroczenie progu nie kondensuje w pelni.
    assert 0.2 * abs(S0) < magnitudes[-1] < 10.0


def test_deeper_exceedance_gives_larger_plateau_than_milder_one():
    """Test WZGLEDNY, ktory faktycznie oddaje zamierzona wlasciwosc:
    powaga przekroczenia progu kontroluje ROZMIAR trwalego residuum,
    nie jego istnienie/nieistnienie."""
    mild = abs(theta_bifurcation(S=2.0, Q=0.36, Q_crit=0.35, time_since_cutoff_start=100.0).S_new)
    deep = abs(theta_bifurcation(S=2.0, Q=0.90, Q_crit=0.35, time_since_cutoff_start=100.0).S_new)
    assert deep > mild, f"gliebsze przekroczenie powinno dawac wieksze plateau: mild={mild}, deep={deep}"


# ---------------------------------------------------------------------
# Kontrola 2: glebokie/dlugie przekroczenie -> nasycenie, NIE wybuch
# ---------------------------------------------------------------------

def test_deep_exceedance_saturates_instead_of_exploding():
    Q_deep = 0.95  # bardzo glebokie przekroczenie -> beta bliskie 0
    S0 = 0.5
    results = [
        theta_bifurcation(S=S0, Q=Q_deep, Q_crit=0.35, time_since_cutoff_start=dt_since)
        for dt_since in [0.0, 1.0, 5.0, 20.0, 100.0, 1000.0]
    ]
    magnitudes = [abs(r.S_new) for r in results]
    # nasycenie: nigdy nie przekracza S_UP_MAX (z zapasem na czesc tlumiona)
    for m in magnitudes:
        assert np.isfinite(m), "operator wyprodukowal nie-skonczona wartosc (inf/NaN)"
        assert m <= S_UP_MAX_DEFAULT + 1e-6, f"amplituda {m} przekroczyla S_UP_MAX={S_UP_MAX_DEFAULT}"
    # rosnie (a przynajmniej nie maleje) w kierunku nasycenia dla rosnacego czasu
    assert magnitudes[-1] >= magnitudes[0]


def test_no_overflow_at_extreme_duration():
    """Test bezposrednio na to, co bylo NIEFIZYCZNE/NIESTABILNE w
    oryginalnym wzorze (czysty exp(+lambda*dt) bez ograniczenia):
    nawet przy bardzo dlugim czasie trwania epizodu, operator NIE
    produkuje inf/NaN."""
    result = theta_bifurcation(S=1.0, Q=0.99, Q_crit=0.35, time_since_cutoff_start=1e6)
    assert np.isfinite(result.S_new)
    assert np.isfinite(result.S_up)
    assert np.isfinite(result.S_down)


# ---------------------------------------------------------------------
# Walidacja wejscia
# ---------------------------------------------------------------------

def test_rejects_negative_time_since_cutoff():
    with pytest.raises(ValueError):
        theta_bifurcation(S=1.0, Q=0.5, Q_crit=0.35, time_since_cutoff_start=-1.0)


def test_rejects_nonpositive_lambda():
    with pytest.raises(ValueError):
        theta_bifurcation(S=1.0, Q=0.5, Q_crit=0.35, time_since_cutoff_start=0.0, lambda_down=0.0)
    with pytest.raises(ValueError):
        theta_bifurcation(S=1.0, Q=0.5, Q_crit=0.35, time_since_cutoff_start=0.0, lambda_up=-1.0)


def test_rejects_nonpositive_S_up_max():
    with pytest.raises(ValueError):
        theta_bifurcation(S=1.0, Q=0.5, Q_crit=0.35, time_since_cutoff_start=0.0, S_up_max=0.0)
