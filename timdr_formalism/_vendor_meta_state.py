"""timdr_formalism/_vendor_meta_state.py -- ZWENDOROWANA (skopiowana 1:1,
NIE sibling-importowana) kopia MetaState + MetaOperatorM z
jbackk-lang/TIMDR-META-DYNAMICS (core_meta/meta_state.py,
core_meta/meta_operator_M.py).

POCHODZENIE: TIMDR-META-DYNAMICS (github.com/jbackk-lang/TIMDR-META-DYNAMICS),
core_meta/meta_state.py + core_meta/meta_operator_M.py -- skopiowane bez
zmian logiki dnia 2026-09-12, zgodnie z ustaloną wcześniej architekturą
vendoringu w tym ekosystemie (kod współdzielony kopiowany z prowencją, nie
importowany przez sciezke wzgledna do repo-siostry).

DLACZEGO TEN PLIK TRAFIA TU: timdr_formalism/signal_meta_bridge.py (ten
sam katalog) mapuje wynik klasyfikacji sygnału I/II/III na MetaState(Λ,τ,ρ,J)
i uzywa MetaOperatorM.classify_phase(), zeby wyliczyc faze systemu -
integracja zlecona wprost przez uzytkownika 2026-09-12 ("integracja klas
I/II/III z MetaState (Λ, τ, ρ, J)"), po opisaniu pelnego lancucha: sygnal
-> SG-Coupling -> Θ_bif -> klasa I/II/III -> MetaState -> faza systemu.

NIE ZMIENIONE WZGLEDEM ORYGINALU - w tym KLUCZOWE, dziedziczone wprost
zastrzezenie z oryginalnego docstringu classify_phase(): progi 0.1/1.0 sa
dobrane arbitralnie/heurystycznie w oryginalnym szkicu, NIE skalibrowane
na zadnych realnych danych pola - i, jak pokazuje
tests/test_signal_meta_bridge.py w TYM repo, rowniez NIE na skali sygnalu
SG-Coupling/Θ_bif (patrz wynik w tym pliku testowym: to jest SIODMA domena,
po szesciu juz opisanych w TIMDR_Branch_Specification.md, w ktorej ten sam
wzorzec "mechanizm dziala, progi nieskalibrowane" sie powtarza).
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MetaState:
    """Globalny stan pola TIMDR:
    Λ (Lambda) – struktura
    τ (tau)    – transformacja
    ρ (rho)    – anomalia
    J          – operator punktowy
    """

    Lambda: float
    tau: float
    rho: float
    J: float

    def delta(self, other: "MetaState") -> "MetaState":
        """Różnica (other - self), zgodnie z konwencją compute_meta_time(S_prev, S_now)."""
        return MetaState(
            Lambda=other.Lambda - self.Lambda,
            tau=other.tau - self.tau,
            rho=other.rho - self.rho,
            J=other.J - self.J,
        )


class MetaOperatorM:
    """Operator ewolucji pola: M = d/dt (Λ, τ, ρ, J)."""

    def compute(self, prev_state: MetaState, next_state: MetaState, dt: float) -> MetaState:
        if dt == 0:
            raise ValueError("dt musi być różne od zera")

        delta = prev_state.delta(next_state)

        return MetaState(
            Lambda=delta.Lambda / dt,
            tau=delta.tau / dt,
            rho=delta.rho / dt,
            J=delta.J / dt,
        )

    def magnitude(self, M_state: MetaState) -> float:
        """Suma wartości bezwzględnych składowych M."""
        return (
            abs(M_state.Lambda)
            + abs(M_state.tau)
            + abs(M_state.rho)
            + abs(M_state.J)
        )

    def classify_phase(self, M_state: MetaState) -> str:
        """Klasyfikacja fazy pola na podstawie wielkości M:
        - "stabilna"    magnitude < 0.1
        - "przejsciowa" 0.1 <= magnitude < 1.0
        - "krytyczna"   magnitude >= 1.0

        UWAGA (dziedziczona z oryginalu, patrz naglowek pliku): progi
        (0.1 / 1.0) sa dobrane arbitralnie/heurystycznie, nie
        skalibrowane na zadnych realnych danych pola - skala Λ/τ/ρ/J
        zalezy calkowicie od tego, co podlaczysz jako wejscie."""
        magnitude = self.magnitude(M_state)

        if magnitude < 0.1:
            return "stabilna"
        elif magnitude < 1.0:
            return "przejsciowa"
        else:
            return "krytyczna"
