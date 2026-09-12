"""_vendor_senscore_gia_filter.py -- ZWENDOROWANA (skopiowana 1:1, NIE
sibling-importowana) kopia naprawionej klasy GIAFilter z jbackk-lang/Senscore,
plus minimalne dataclassy (Hit, Event) potrzebne, zeby dzialala samodzielnie.

POCHODZENIE: Senscore (github.com/jbackk-lang/Senscore), senscoreAll.py,
klasa GIAFilter (+ Hit, Event) -- skopiowane bez zmian logiki dnia
2026-09-11, PO poprawce znalezionej i zweryfikowanej wczesniej tego samego
dnia (26/26 testow w Senscore, patrz test_senscoreAll.py w tamtym repo).

DLACZEGO TA KLASA TRAFIA TU: nazywa sie "GIAFilter" i jest fizyczno-
-semantycznym filtrem toru (odrzuca hity nie ukladajace sie w linie/luk),
konceptualnie nalezy do GIA-TIMDR tak samo jak reszta plikow w filters/
(prime_spectrum_filter.py, timdr_*.py) -- na wyrazna prosbe uzytkownika,
zeby scentralizowac ten filtr "w jednym miejscu, tak jak pozostale".

BLAD, KTORY BYL NAPRAWIONY (przed zwendorowaniem, w samym Senscore):
pierwotna wersja liczyla os toru zwyklym PCA na WSZYSTKICH hitach naraz.
Zwykle PCA nie jest odporne na odstajace punkty -- jeden hit daleko od
toru potrafi zdominowac wariancje i obrocic glowna os PCA w swoim
kierunku. W efekcie filtr odrzucal prawdziwe hity z toru, a zachowywal
sam szum (zweryfikowane testem: linia 10 hitow wzdluz osi X + jeden
odstajacy punkt (5, 50, 0) -> stara wersja zachowywala 3 hity blisko
srodka + szum, odrzucajac 7 poprawnych hitow z koncow toru). Poprawiona
wersja ponizej szacuje os metoda zblizona do RANSAC: losuje pary punktow
jako kandydackie proste, wybiera kandydata z najwieksza liczba
"inlierow" (hitow w zasiegu max_residual), a finalna os dopasowuje PCA
tylko do tych inlierow. Dodatkowo np.linalg.eig -> np.linalg.eigh
(macierz kowariancji jest symetryczna, wiec eigh jest szybsze i zawsze
zwraca wartosci rzeczywiste).

DLACZEGO ZWENDOROWANE, NIE SIBLING-IMPORT: to repo ma byc SAMOWYSTARCZALNE
-- dzialac po sklonowaniu WYLACZNIE tego jednego repo, bez wymogu, zeby
Senscore lezalo obok jako folder-siostra na dysku. Ten sam wzorzec co
Synoptyk-v3/membrane/_vendor_timdr_meta_dynamics_core.py.

UWAGA O UTRZYMANIU: to jest KOPIA, nie link. Jesli Senscore kiedys
zmieni ta klase (np. inny domyslny max_residual, inna metoda odpornego
dopasowania), ta kopia NIE zaktualizuje sie automatycznie -- trzeba by
recznie zsynchronizowac. Swiadomie zaakceptowany kompromis, tak samo
jak w pozostalych zwendorowanych plikach tego ekosystemu.

ZNANE OGRANICZENIE (znalezione przy pisaniu testow dla tej kopii,
2026-09-11, NIE cofniecie oryginalnej naprawy): domyslny max_residual=5.0
NIE jest bezpieczny dla kazdego ukladu danych. Przyklad: tor 10 punktow
wzdluz osi X (x=0..9) plus jeden odstajacy punkt (5, 50, 0) -- z
max_residual=5.0 prosta PROSTOPADLA do toru, przechodzaca przez jego
srodek i przez szum, przypadkowo zbiera WIECEJ "inlierow" (11) niz
prawdziwa os toru (10), bo polowa rozciaglosci toru w X (4.5) jest
mniejsza niz max_residual (5.0) -- wiec RANSAC wybiera zla os, a szum
zostaje zachowany (patrz test_default_max_residual_can_fail_on_wide_tracks
w tests/test_vendor_senscore_gia_filter.py). Zweryfikowany test w
Senscore (test_off_axis_point_removed) przechodzi, bo jawnie ustawia
max_residual=1.0, nie polega na wartosci domyslnej. Wniosek: max_residual
trzeba dobierac wzgledem skali/rozciaglosci konkretnych danych, nie
ufac domyslnej wartosci klasy.

UWAGA HISTORYCZNA (2026-09-12): ten plik i jego testy zostaly juz raz
napisane (commit bbd157c) i STRACONE -- lokalny folder GIA-TIMDR zostal
przypadkowo nadpisany starszym backupem PRZED wypchnieciem tego commita
na GitHub, wiec zniknal i lokalnie, i zdalnie (nigdy nie istniat na
origin). Odtworzone od zera z tresci tej samej rozmowy. Lekcja: push
zaraz po commicie dla nowej pracy, nie odkladac na pozniej.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List

import numpy as np


@dataclass
class Hit:
    sensor_id: int
    x: float
    y: float
    z: float
    t: float
    energy: float
    raw_value: float  # surowy sygnal z kanalu


@dataclass
class Event:
    hits: List[Hit]


class GIAFilter:
    """
    Filtr fizyczno-semantyczny GIA:
    - sprawdza zgodnosc z prostym modelem fizycznym:
      np. tor w polu magnetycznym ~ luk / helisa.
    Tu: uproszczony wariant -> preferujemy hity ukladajace sie w
    mniej wiecej liniowa / lukowa strukture.

    Patrz naglowek modulu dla pelnego opisu poprawki (RANSAC-podobne
    dopasowanie osi zamiast zwyklego PCA na calym zbiorze).
    """

    def __init__(self, max_residual: float = 5.0):
        self.max_residual = max_residual

    def apply(self, event: Event) -> Event:
        hits = event.hits
        if len(hits) < 3:
            return event

        positions = np.array([[h.x, h.y, h.z] for h in hits])

        main_dir, mean_pos = self._robust_axis(positions)
        residuals = self._residuals(positions, mean_pos, main_dir)

        kept_hits = [h for h, r in zip(hits, residuals) if r <= self.max_residual]
        return Event(hits=kept_hits)

    @staticmethod
    def _residuals(positions, mean_pos, main_dir):
        centered = positions - mean_pos
        proj_len = centered @ main_dir
        proj = np.outer(proj_len, main_dir)
        return np.linalg.norm(centered - proj, axis=1)

    @staticmethod
    def _pca_axis(positions):
        mean_pos = positions.mean(axis=0)
        centered = positions - mean_pos
        cov = centered.T @ centered
        # macierz kowariancji jest symetryczna -> eigh (szybsze, zawsze
        # zwraca wartosci/wektory rzeczywiste, w przeciwienstwie do eig)
        eigvals, eigvecs = np.linalg.eigh(cov)
        main_dir = eigvecs[:, -1]  # eigh zwraca wartosci rosnaco
        norm = np.linalg.norm(main_dir)
        if norm > 0:
            main_dir = main_dir / norm
        return main_dir, mean_pos

    def _robust_axis(self, positions, n_trials=200, seed=0):
        n = len(positions)
        rng = np.random.default_rng(seed)

        # dla malych zbiorow zwykle PCA na calosci wystarczy
        if n < 5:
            return self._pca_axis(positions)

        idx_pairs = set()
        attempts = 0
        max_attempts = n_trials * 3
        max_pairs = min(n_trials, n * (n - 1) // 2)
        while len(idx_pairs) < max_pairs and attempts < max_attempts:
            i, j = rng.integers(0, n, size=2)
            attempts += 1
            if i == j:
                continue
            idx_pairs.add((min(i, j), max(i, j)))

        best_inliers = None
        best_count = -1
        for i, j in idx_pairs:
            p1, p2 = positions[i], positions[j]
            direction = p2 - p1
            norm = np.linalg.norm(direction)
            if norm < 1e-9:
                continue
            direction = direction / norm

            centered = positions - p1
            proj_len = centered @ direction
            proj = np.outer(proj_len, direction)
            residuals = np.linalg.norm(centered - proj, axis=1)

            inliers = residuals <= self.max_residual
            count = int(np.sum(inliers))
            if count > best_count:
                best_count, best_inliers = count, inliers

        if best_inliers is None or best_inliers.sum() < 2:
            # brak sensownego kandydata (np. wszystkie punkty w tym samym
            # miejscu) -> zwykle PCA na calym zbiorze
            return self._pca_axis(positions)

        # finalna os: PCA dopasowane tylko do znalezionych inlierow
        return self._pca_axis(positions[best_inliers])
