# TIMDR — parametry przejść między gałęziami (2026-09-27)

Kod: `core/transition_params.py`, testy: `tests/test_transition_params.py`.
Źródło: wnioski z testów Paderborn, turbina LBF, Open Radar, budynek LANL (docs/geometry). Parametry **wyjaśniają**
znane wyniki; status „potwierdzone” dostają dopiero po przewidywaniu zapisanym przed nowymi danymi.

## 1. Parametry

| Parametr | Przejście | Definicja | Co rozstrzyga |
|---|---|---|---|
| **N_cyk** | sygnał → pole | liczba cykli rytmu w oknie, N = T·f | ile „szczelin” ma sito; N < 10 → grzebień rozmyty |
| **kotwica** | K → sito | skąd znana częstotliwość hipotezy: stała / śledzona / wolna | czy samokorekta ma punkt startu |
| **D** | pole → rura → META | wypełnienie obwiedni η = (E e)² / E e², D = η/(1−η) ≈ 2·f·τ dla rzadkich zdarzeń | cząsteczka (D < 0,3) / pakiet / fala (D > 3); szum gaussowski D ≈ 3,7 |
| **L_koh** | rura → zegar | f0 / szerokość linii (w cyklach) | L_koh < N_cyk → wyprostować rurę (zegar kątowy/zdarzeniowy) |
| **typ zegara** | Chronoproces | czas / kąt / zdarzenie | pierwszy krok łańcucha; zły zegar psuje dalsze przejścia |
| **środek oczek** | rura → rodzina Γ | środek ciężkości oczek sita w polu kanał × pasmo | lokalizacja źródła |
| **χ** | skręt rury | log(obieg w przód / w tył) orbity x + iy | kierunek obiegu (niewyważenie vs tarcie) — bez danych |

META-DYNAMICS dostaje treść mierzalną: τ = czas wygaszania zdarzenia, ρ = D (gęstość, ρ ≈ f·τ), J = rozkład oczek
między kanałami.

## 2. Macierz reżimów (D × kotwica) i stan testów

| | kotwica stała | śledzona | wolna |
|---|---|---|---|
| cząsteczka | Paderborn: **+** | turbina: **+** | budynek (duża szczelina): częściowo |
| pakiet | — | — | radar (wirnik): − |
| fala | przekładnia SEU: mieszany; prądy: − | — | radar (kończyny), budynek (mała szczelina): − |

## 3. Reguła wykonalności (liczona PRZED testem)

1. N_cyk < 10 → sito nie ma szans (za mało cykli).
2. Kotwica wolna → sito nie ma szans (samokorekta bez punktu startu); dostarczyć kotwicę z gałęzi K.
3. L_koh < N_cyk → najpierw wyprostować rurę (zmiana zegara).
4. Reżim wg D: cząsteczka → miara P (błyski); pakiet → sito z kotwicą (grzebień Q); fala → linie K (harmoniczne kotwicy).

Konsekwencja dla miar stanu: miara oparta tylko na P spada, gdy zdarzenia gęstnieją (D rośnie) — P jest
niemonotoniczne względem ciężkości; potrzebne przełączenie P → Q/K według D.
