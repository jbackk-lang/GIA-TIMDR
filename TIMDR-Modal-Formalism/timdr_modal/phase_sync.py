"""
timdr_modal/phase_sync.py

Galaz K (modalna) chronoprocesu: mapa synchronizacji faz `f`, ktora
daje sprawdzalna tresc postulatowi "t_lokalne = f(tau_globalne)" z
sekcji 7.3 glownego README GIA-TIMDR. Pelny opis Chronoprocesu
Xi=(T,x,Gamma,phi), w tym tej konstrukcji: `GIA-TIMDR/docs/theory/
TIMDR_Chronoprocess.md` (sekcja 4) oraz `GIA-TIMDR/SKILL_timdr-signal-
framework.md` (sekcja 5, skrocona wersja).

Obiekt modalnosci `(f,phi,A)` -- czestotliwosc/faza/amplituda -- jest
DOKLADNIE Aksjomatem 3 z GIA-TIMDR/docs/theory/Axioms_K_TIMDR.md:

    M = M(I) = {(f_i, phi_i, A_i)}

Aksjomat 4 definiuje interferencje:

    I(t) = sum_i A_i * sin(2*pi*f_i*t + phi_i)

-- czyli FAZA CHWILOWA modalnosci i w chwili t to
theta_i(t) = 2*pi*f_i*t + phi_i (argument sinusa), a phi_i samo w
sobie jest tylko faza POCZATKOWA (stala, wartosc w t=0). Aksjomat 5
definiuje rezonans jako wyrownanie (f_i,phi_i) MIEDZY DWIEMA
modalnosciami -- porownanie czestotliwosci oraz KOLOWEGO dystansu faz
POCZATKOWYCH (fazy sa okreslone modulo 2*pi), nie faz chwilowych.

## Mapa synchronizacji faz f

Dwie modalnosci, "lokalna" i "globalna", kazda monochromatyczna (stale
f,phi,A -- DOKLADNIE tak, jak Aksjomat 3 je definiuje, zaden nowy
aksjomat nie zostal dodany). "t_lokalne=f(tau_globalne)" jest
formalizowane jako: znajdz taki czas lokalny t_lokalne, przy ktorym
FAZA CHWILOWA oscylatora lokalnego rownai sie fazie chwilowej
oscylatora globalnego w chwili tau_globalne:

    theta_lokalne(t_lokalne) = theta_globalne(tau_globalne)
    2*pi*f_lokalne*t_lokalne + phi_lokalne = 2*pi*f_globalne*tau_globalne + phi_globalne

Rozwiazujac wprost dla t_lokalne (wymaga f_lokalne != 0, inaczej
theta_lokalne jest stala -- nie da sie odwrocic):

    t_lokalne = (f_globalne/f_lokalne)*tau_globalne
                + (phi_globalne - phi_lokalne)/(2*pi*f_lokalne)

To jest funkcja `local_time_from_global()` ponizej -- DOKLADNIE ten
sam obiekt matematyczny co "mapa resynchronizacji faz
f:=phi_lokalne∘phi_globalne^-1" z dyskusji w czacie, tylko rozpisana
jawnie na czas->czas zamiast czas->faza->czas.

## Granica zakresu -- jawnie, uczciwie

Ta mapa jest AFINICZNA (liniowa + przesuniecie) -- bo Aksjomaty
K3/K4 modeluja kazda modalnosc jako oscylator o STALYCH parametrach,
nie oscylator SPRZEZONY o dynamicznie zmieniajacej sie czestotliwosci.
Pelniejsza, NIELINIOWA mapa synchronizacji w stylu Kuramoto (gdzie
oscylatory wzajemnie dostrajaja swoja czestotliwosc przez sile
sprzezenia) wymagalaby ROZSZERZENIA Axioms_K o dynamike sprzezenia,
ktorej tam dzis NIE MA -- to jest jawnie NIE zrobione tutaj, nie
ukryte uproszczenie. To, co jest tutaj, jest poprawna, sprawdzalna
formalizacja postulatu "t_lokalne=f(tau_globalne)" DANE aksjomaty
dokladnie takie, jakie sa dzisiaj -- pierwsza instancja galezi K jako
kodu (K nie mialo dotad ZADNEJ implementacji w tym ekosystemie).

STATUS WYKONANIA: historyczne 17/17 dotyczyło wcześniejszego zestawu.
Po dodaniu testów niezmienniczości fazy kołowej pełny zestaw Modal
przeszedł w GitHub Actions dla commitu `80693941`: 31 passed, 5 skipped.
Pominięte testy nie są zaliczonym wynikiem; patrz warunki skip w testach
walidacji danych.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np

__all__ = [
    "Modality",
    "instantaneous_phase",
    "interference",
    "is_resonant",
    "local_time_from_global",
]


@dataclass(frozen=True)
class Modality:
    """(f,phi,A) -- Aksjomat 3 z Axioms_K_TIMDR.md, doslownie.

    f: czestotliwosc (Hz, jednostki 1/[t]), MOZE byc ujemna (kierunek
        fazy) ale nie sprawdzana tu jako > 0 -- tylko != 0 jest
        wymagane tam, gdzie potrzebna jest odwracalnosc (patrz
        `local_time_from_global`).
    phi: faza poczatkowa (radiany), wartosc w t=0.
    A: amplituda.
    """

    f: float
    phi: float
    A: float = 1.0

    def __post_init__(self) -> None:
        if not np.all(np.isfinite([self.f, self.phi, self.A])):
            raise ValueError("f, phi i A musza byc skonczone")


def instantaneous_phase(modality: Modality, t) -> np.ndarray:
    """theta(t) = 2*pi*f*t + phi -- argument sinusa z Aksjomatu 4,
    ODCZYTANY jako funkcja czasu (Aksjomat 4 sam pisze go tylko w
    srodku sumy interferencji; to jest ten sam wzor, wyciagniety jako
    samodzielna funkcja fazy chwilowej, potrzebna do mapy f)."""
    t = np.asarray(t, dtype=float)
    if not np.all(np.isfinite(t)):
        raise ValueError("t musi zawierac wylacznie skonczone wartosci")
    with np.errstate(over="ignore", invalid="ignore"):
        phase = 2.0 * np.pi * modality.f * t + modality.phi
    if not np.all(np.isfinite(phase)):
        raise ValueError("obliczona faza przekracza zakres reprezentacji float")
    return phase


def interference(modalities: Sequence[Modality], t) -> np.ndarray:
    """I(t) = sum_i A_i*sin(2*pi*f_i*t+phi_i) -- Aksjomat 4, doslownie."""
    if len(modalities) == 0:
        raise ValueError("interference() wymaga >=1 modalnosci")
    if any(not isinstance(m, Modality) for m in modalities):
        raise ValueError("modalities musi zawierac obiekty Modality")
    t = np.asarray(t, dtype=float)
    if not np.all(np.isfinite(t)):
        raise ValueError("t musi zawierac wylacznie skonczone wartosci")
    total = np.zeros_like(t)
    for m in modalities:
        total = total + m.A * np.sin(instantaneous_phase(m, t))
    return total


def is_resonant(
    m_i: Modality, m_j: Modality, eps_f: float = 1e-6, eps_phi: float = 1e-6
) -> bool:
    """Aksjomat 5: |f_i-f_j| < eps_f ORAZ kolowy dystans faz < eps_phi.

    Fazy sa katami modulo 2*pi, wiec porownanie jest niezmiennicze
    wzgledem dodania dowolnej wielokrotnosci 2*pi do phi_i lub phi_j.
    Nierownosci sa SCISLE (<): rownosc dokladnie na progu nie jest
    rezonansem.
    """
    if not isinstance(m_i, Modality) or not isinstance(m_j, Modality):
        raise ValueError("m_i i m_j musza byc obiektami Modality")
    if not np.all(np.isfinite([eps_f, eps_phi])) or eps_f < 0 or eps_phi < 0:
        raise ValueError("eps_f i eps_phi musza byc skonczone i >= 0")
    phase_i = np.remainder(m_i.phi, 2.0 * np.pi)
    phase_j = np.remainder(m_j.phi, 2.0 * np.pi)
    phase_delta = (phase_i - phase_j + np.pi) % (2.0 * np.pi) - np.pi
    return abs(m_i.f - m_j.f) < eps_f and abs(phase_delta) < eps_phi


def local_time_from_global(local: Modality, global_: Modality, tau_global) -> np.ndarray:
    """Mapa f: t_lokalne=f(tau_globalne), zdefiniowana przez dopasowanie
    FAZY CHWILOWEJ (patrz wyprowadzenie w naglowku modulu):

        t_lokalne = (f_globalne/f_lokalne)*tau_globalne
                    + (phi_globalne-phi_lokalne)/(2*pi*f_lokalne)

    Wymaga local.f != 0 -- inaczej theta_lokalne jest stala funkcja
    czasu (oscylator lokalny "nie plynie"), wiec nie da sie jej
    odwrocic, zeby znalezc t_lokalne (dokladnie ten warunek
    odwracalnosci/monotonicznosci, ktory byl flagowany jako wymagany w
    dyskusji przed napisaniem tego kodu).
    """
    if not isinstance(local, Modality) or not isinstance(global_, Modality):
        raise ValueError("local i global_ musza byc obiektami Modality")
    if local.f == 0:
        raise ValueError(
            "local.f == 0 -- faza lokalna jest stala, mapa f nie jest "
            "odwracalna (wymagana monotonicznosc theta_lokalne(t))"
        )
    tau_global = np.asarray(tau_global, dtype=float)
    theta_g = instantaneous_phase(global_, tau_global)
    with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
        local_time = (theta_g - local.phi) / (2.0 * np.pi * local.f)
    if not np.all(np.isfinite(local_time)):
        raise ValueError("mapowany czas lokalny przekracza zakres reprezentacji float")
    return local_time
