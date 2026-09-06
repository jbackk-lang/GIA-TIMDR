# tests/test_trefoil_frenet_torsion.py
"""
test_trefoil_frenet_torsion.py -- testy dla core/trefoil_frenet_torsion.py.

Powtarza protokol timdr-signal-framework SS2 (definicja PRZED danymi,
kontrola pozytywna + negatywna) dla hipotezy uzytkownika o trojwezle
helikalnym: "os wzdluz figury reprezentuje skret [tu: torsja
Freneta-Serreta], odstepstwa [deformacje] pierwszego wezla to defekty,
calosc [powinna byc] rewidowana rezonansem".

Cztery testy, w kolejnosci narastajacej surowosci:
1. Kontrola negatywna: czysty (niezdeformowany) trojwezel -- zero
   fałszywych alarmow na jakimkolwiek kanale i w rezonansie.
2. Kontrola pozytywna, wezel na granicy tablicy (t0=0): deformacja
   wykrywalna w rezonansie, zlokalizowana blisko wezla.
3. Kontrola pozytywna, wezel WEWNETRZNY (t0=2*pi/3, z dala od granicy
   tablicy probek) -- sprawdza, ze lokalizacja dziala niezaleznie od
   artefaktu brzegowego liczenia roznic skonczonych.
4. Dwie jednoczesne deformacje o roznej amplitudzie na dwoch roznych
   wezlach -- obie musza zostac wykryte OSOBNO, bez trzeciego,
   falszywego wykrycia na nietknietym wezle.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
import pytest

from core.trefoil_frenet_torsion import (
    trefoil_points,
    inject_node_deformation,
    detect_channels,
    rezonans,
    nearest_sample_to_t0,
)

N = 300
LOCALIZATION_TOLERANCE = 6  # probek, na 300 (2% okresu) -- patrz uzasadnienie w README/docs


def test_negatywna_kontrola_czysty_trojwezel_zero_falszywych_alarmow():
    t, pts = trefoil_points(N)
    flags = detect_channels(pts, t)
    rez = rezonans(flags, k=2)

    for name, f in flags.items():
        assert not f.any(), f"kanal {name} falszywie zaalarmowal na czystym, niezdeformowanym trojwezle"
    assert not rez.any(), "rezonans falszywie zaalarmowal na czystym trojwezle"


def test_pozytywna_kontrola_wezel_na_granicy_tablicy():
    t, pts = trefoil_points(N)
    t0 = 0.0
    pts_def = inject_node_deformation(pts, t, t0=t0, amp=1.5, width=0.15)
    flags = detect_channels(pts_def, t)
    rez = rezonans(flags, k=2)

    assert rez.any(), "rezonans nie wykryl deformacji wezla przy t0=0"
    idx_expected = nearest_sample_to_t0(t, t0)
    idx_hit = np.where(rez)[0]
    # odleglosc cykliczna (wezel jest na szwie tablicy: idx 0 i idx N-1 sasiaduja)
    dist = np.minimum(np.abs(idx_hit - idx_expected), N - np.abs(idx_hit - idx_expected))
    assert dist.min() <= LOCALIZATION_TOLERANCE, (
        f"najblizsze wykrycie rezonansu ({dist.min()} probek od wezla) "
        f"przekracza tolerancje lokalizacji"
    )


def test_pozytywna_kontrola_wezel_wewnetrzny_bez_artefaktu_brzegowego():
    t, pts = trefoil_points(N)
    t0 = 2 * np.pi / 3  # drugi lob, idx ~100 z 300 -- z dala od brzegow tablicy
    pts_def = inject_node_deformation(pts, t, t0=t0, amp=1.5, width=0.15)
    flags = detect_channels(pts_def, t)
    rez = rezonans(flags, k=2)

    assert rez.any(), "rezonans nie wykryl deformacji wezla wewnetrznego (t0=2*pi/3)"
    idx_expected = nearest_sample_to_t0(t, t0)
    idx_hit = np.where(rez)[0]
    dist = np.abs(idx_hit - idx_expected)
    assert dist.min() <= LOCALIZATION_TOLERANCE

    # zero wykryc daleko od ktoregokolwiek z dwoch nietknietych wezlow (t=0, t=4*pi/3)
    other_nodes_idx = [nearest_sample_to_t0(t, 0.0), nearest_sample_to_t0(t, 4 * np.pi / 3)]
    for idx in idx_hit:
        dist_to_others = min(
            min(abs(idx - o), N - abs(idx - o)) for o in other_nodes_idx
        )
        assert dist_to_others > LOCALIZATION_TOLERANCE, (
            f"rezonans falszywie zaalarmowal przy idx={idx}, blisko nietknietego wezla"
        )


def test_dwie_jednoczesne_deformacje_wykryte_osobno_bez_trzeciego_falszywego_alarmu():
    t, pts = trefoil_points(N)
    t0_a, amp_a = 0.0, 1.5
    t0_b, amp_b = 4 * np.pi / 3, 0.8  # slabsza deformacja na trzecim lobie
    untouched_node_t0 = 2 * np.pi / 3  # drugi lob NIE jest deformowany

    pts_def = inject_node_deformation(pts, t, t0=t0_a, amp=amp_a, width=0.15)
    pts_def = inject_node_deformation(pts_def, t, t0=t0_b, amp=amp_b, width=0.15)
    flags = detect_channels(pts_def, t)
    rez = rezonans(flags, k=2)

    assert rez.any(), "rezonans nie wykryl zadnej z dwoch jednoczesnych deformacji"
    idx_hit = np.where(rez)[0]

    idx_a = nearest_sample_to_t0(t, t0_a)
    idx_b = nearest_sample_to_t0(t, t0_b)
    idx_untouched = nearest_sample_to_t0(t, untouched_node_t0)

    def cyclic_dist(i, j):
        return min(abs(i - j), N - abs(i - j))

    hit_near_a = any(cyclic_dist(i, idx_a) <= LOCALIZATION_TOLERANCE for i in idx_hit)
    hit_near_b = any(cyclic_dist(i, idx_b) <= LOCALIZATION_TOLERANCE for i in idx_hit)
    assert hit_near_a, "brak wykrycia przy silniejszej deformacji (wezel a)"
    assert hit_near_b, "brak wykrycia przy slabszej deformacji (wezel b)"

    for i in idx_hit:
        assert cyclic_dist(i, idx_untouched) > LOCALIZATION_TOLERANCE, (
            f"falszywy alarm przy idx={i}, blisko NIETKNIETEGO wezla (drugi lob)"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
