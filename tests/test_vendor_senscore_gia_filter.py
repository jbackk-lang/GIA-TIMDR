"""
tests/test_vendor_senscore_gia_filter.py

Testy dla zwendorowanego GIAFilter (filters/_vendor_senscore_gia_filter.py).
Kluczowy test to regresja dla bledu naprawionego w Senscore: zwykle PCA na
calym zbiorze dawalo sie zdominowac przez jeden odstajacy punkt i odrzucalo
prawdziwy tor. Te same przypadki testowe co w Senscore/test_senscoreAll.py,
przeniesione tutaj razem z kodem.
"""
import numpy as np

from filters._vendor_senscore_gia_filter import Hit, Event, GIAFilter


def _linear_track_hits(n=10):
    return [
        Hit(sensor_id=1, x=float(i), y=0.0, z=0.0, t=float(i), energy=1.0, raw_value=1.0)
        for i in range(n)
    ]


def test_fewer_than_three_hits_passthrough():
    hits = [
        Hit(sensor_id=1, x=0.0, y=0.0, z=0.0, t=0.0, energy=1.0, raw_value=1.0),
        Hit(sensor_id=1, x=1.0, y=1.0, z=1.0, t=1.0, energy=1.0, raw_value=1.0),
    ]
    event = Event(hits=hits)
    result = GIAFilter().apply(event)
    assert len(result.hits) == 2


def test_linear_track_kept():
    # max_residual=0.5, zgodnie z rzeczywistym testem w Senscore
    # (test_senscoreAll.py::TestGIA::test_linear_track_kept) - NIE
    # domyslnym max_residual=5.0 klasy.
    hits = _linear_track_hits(10)
    event = Event(hits=hits)
    result = GIAFilter(max_residual=0.5).apply(event)
    assert len(result.hits) == 10


def test_off_axis_point_removed_regression():
    """Regresja dla naprawionego bledu: linia 10 hitow wzdluz osi X plus
    jeden odstajacy punkt (5, 50, 0). Stara (zepsuta) wersja zachowywala
    tylko 3 hity (2 blisko srodka + sam szum), odrzucajac 7 poprawnych
    hitow z koncow toru. Naprawiona wersja musi zachowac caly tor (10) i
    odrzucic szum (1).

    max_residual=1.0, zgodnie z rzeczywistym testem w Senscore. UWAGA
    (znalezione przy pisaniu tego testu): z DOMYSLNYM max_residual=5.0
    ten sam test FAILUJE (11 zachowanych, nie 10) - przy tym progu
    prosta prostopadla przez (5,0,0)-(5,50,0) przypadkowo zbiera wiecej
    "inlierow" (wszystkie punkty toru maja |x-5|<=5) niz prawdziwa os
    toru, wiec RANSAC wybiera zla os. To NIE jest cofniecie naprawy -
    to prawdziwe, wazne ograniczenie: dobor max_residual WZGLEDEM
    rozciaglosci toru ma znaczenie, i domyslna wartosc 5.0 nie jest
    bezpieczna dla kazdego ukladu danych. Warte odnotowania jako
    znane ograniczenie, nie do cichego zamiecenia."""
    hits = _linear_track_hits(10) + [
        Hit(sensor_id=2, x=5.0, y=50.0, z=0.0, t=5.0, energy=1.0, raw_value=1.0)
    ]
    event = Event(hits=hits)
    result = GIAFilter(max_residual=1.0).apply(event)
    kept_positions = {(h.x, h.y) for h in result.hits}
    assert len(result.hits) == 10, f"oczekiwano 10 hitow toru, dostano {len(result.hits)}"
    assert (5.0, 50.0) not in kept_positions, "odstajacy punkt nie powinien zostac zachowany"


def test_default_max_residual_can_fail_on_wide_tracks():
    """Dokumentuje uczciwie znalezione ograniczenie (NIE regresja,
    NIE cofniecie naprawy): z domyslnym max_residual=5.0 (a nie
    jawnie ustawionym 1.0 jak w tescie powyzej), ten sam scenariusz
    -- prosta prostopadla przez srodek toru przypadkowo zbiera wiecej
    inlierow niz prawdziwa os, bo max_residual akurat pokrywa sie z
    polowa rozciaglosci toru w X. RANSAC wybiera zla os, a koncowe PCA
    (dopasowane do WSZYSTKICH "inlierow" tej zlej osi, w tym samego
    szumu) odtwarza pierwotny blad. Wniosek: max_residual trzeba dobierac
    wzgledem skali danych, nie polegac na wartosci domyslnej "z powietrza"."""
    hits = _linear_track_hits(10) + [
        Hit(sensor_id=2, x=5.0, y=50.0, z=0.0, t=5.0, energy=1.0, raw_value=1.0)
    ]
    event = Event(hits=hits)
    result = GIAFilter().apply(event)  # domyslny max_residual=5.0
    assert len(result.hits) == 11, (
        f"znane ograniczenie: oczekiwano 11 (szum NIE odrzucony przy domyslnym "
        f"progu), dostano {len(result.hits)} - jesli to sie zmienilo, sprawdz "
        f"czy zmienila sie implementacja _robust_axis()"
    )


def test_identical_points_no_crash():
    hits = [
        Hit(sensor_id=1, x=1.0, y=1.0, z=1.0, t=float(i), energy=1.0, raw_value=1.0)
        for i in range(5)
    ]
    event = Event(hits=hits)
    result = GIAFilter().apply(event)  # nie powinno rzucic wyjatku
    assert isinstance(result, Event)


def test_residuals_are_real_not_complex():
    # Parametry (seed=42, normal(0,10), max_residual=3.0, n w [3,15))
    # zgodne 1:1 z rzeczywistym testem w Senscore.
    rng = np.random.default_rng(42)
    for _ in range(200):
        n = int(rng.integers(3, 15))
        hits = [
            Hit(
                sensor_id=1,
                x=float(rng.normal(0, 10)),
                y=float(rng.normal(0, 10)),
                z=float(rng.normal(0, 10)),
                t=float(i),
                energy=1.0,
                raw_value=1.0,
            )
            for i in range(n)
        ]
        event = Event(hits=hits)
        result = GIAFilter(max_residual=3.0).apply(event)
        assert isinstance(result, Event)
        assert len(result.hits) <= n


def test_empty_event():
    result = GIAFilter().apply(Event(hits=[]))
    assert result.hits == []
