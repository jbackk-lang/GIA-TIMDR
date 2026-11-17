# 54A.6 — dynamiczne sprzężenie: eksperyment eksploracyjny

## Źródła i ograniczenie interpretacji
README GIA-TIMDR wskazuje cztery gałęzie M/S, G, K i META. Chronoproces Ξ=(T,x,Γ,φ) zapewnia wspólny indeks czasu, lecz nie utożsamia operatorów. Dokumentacja: docs/theory/TIMDR_Chronoprocess.md oraz docs/theory/TIMDR_EventGraph_Branch_Construction.md.

Poniższy wariant **nie jest wyprowadzony ze źródłowych równań ewolucji TIMDR**. Jest eksploracyjnym predyktorem z karą sprzęgającą inspirowaną macierzą J(Λ) przy Λ=2. Nie można nazywać go walidacją pełnego TIMDR.

## Metoda
32768 bajtów na zbiór; cztery syntetyczne deterministyczne zbiory: random, periodic, drift, correlated. Reszty modulo 256, gzip level 9, jeden ciągły strumień. Każdy tryb sprawdzony przez bezstratne dekodowanie. Porównania nie obejmują nagłówka identyfikującego kodek.

## Wyniki — bajty
| Dane | gzip | statyczna | adaptacyjna | sprzężona |
|---|---:|---:|---:|---:|
| random | 32796 | 32796 | 32796 | 32796 |
| periodic | 170 | 395 | 172 | 172 |
| drift | 167 | 167 | 170 | 173 |
| correlated | 6624 | 9368 | 6624 | 6624 |

## Wniosek
W tym eksperymencie sprzężenie nie daje przewagi nad predyktorem adaptacyjnym ani gzip. Wynik negatywny dotyczy tego prototypu i tych zbiorów. Następny krok: znaleźć źródłowe równania aktualizacji Λ, τ, ρ, J, zamrozić regułę i testować na danych rzeczywistych.

## Reprodukcja
Lokalny skrypt 54A6_DYNAMIC.py wykonano w sesji eksperymentalnej. Wyniki zapisane w 54A6_RESULTS.json.
