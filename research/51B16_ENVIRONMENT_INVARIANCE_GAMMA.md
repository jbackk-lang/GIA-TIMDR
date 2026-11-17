# 51B.16 — środowiskowa niezmienniczość i miara Gamma

Data: 2026-11-17. Status: formalna interpretacja i rozszerzenie protokołu 51B.15, **bez nowych wyników empirycznych**.

## Teza
Nie utożsamiać trzech odrębnych własności: wystarczalności predykcyjnej, kompresji oraz transferu. Niech H oznacza historię, F przyszłość, E środowisko (RPM/obciążenie/maszyna/czujnik), a Z=C(H) reprezentację, przy wspólnym ustalonym rozkładzie P(H,F,E).

- **Utrata informacji z historii**: Δ(Z)=I(F;H|Z).
- **Pozostała zależność przyszłości od środowiska przy Z**: Γ(Z)=I(F;E|Z).
- **Koszt opisu**: liczba bitów i zasoby obliczeniowe; osobne osie, nie wynika z Δ ani Γ.

Przy standardowych założeniach mierzalności Γ=E_{Z,E}[KL(P(F|Z,E)||P(F|Z))]≥0, także z możliwością +∞. Γ=0 wtedy i tylko wtedy, gdy F ⟂ E | Z względem badanego rozkładu. Wspólna predykcja P(F|Z) nie potrzebuje wtedy dodatkowej informacji o E na nośniku rozkładu. Nie dowodzi to transferu na niewidziane środowiska ani poprawnej predykcji F z Z.

## Kontrprzykłady interpretacyjne

**Gamma=0 nie implikuje wystarczalności.** Niech F=H będzie losowym bitem niezależnym od E, a Z=const. Wtedy Γ=I(F;E)=0, lecz Δ=I(F;H)>0. Reprezentacja jest bezużyteczna predykcyjnie mimo idealnego Gamma.

**Delta=0 nie implikuje Gamma=0.** Niech E jest losowym bitem, H=E, F=E i Z=H. Wtedy Δ=0, ale Γ=I(F;E|Z)=0 (ponieważ E jest już w Z). Aby uzyskać Δ=0 oraz Γ>0, niech E jest losowym bitem, H=const, Z=const, F=E. Wtedy Δ=0 (historia nie wnosi nic), ale Γ=I(F;E)>0. To ilustruje, że wystarczalność względem H nie musi oznaczać niezależności od dodatkowej zmiennej środowiska.

**Gamma zależy od mieszanki środowisk.** Zmiana P(E) i nośnika Z może zmienić Γ, nawet bez zmiany lokalnych mechanizmów P_e(F|Z). Zawsze raportować schemat ważenia środowisk i zakres wsparcia.

**Ważna subtelność:** Jeśli E jest częścią H i Z jest predykcyjnie wystarczające dla F względem H, wówczas Γ=0; gdy E jest dodatkową informacją niedostępną w H, może zachodzić Δ=0 i Γ>0. Dlatego specyfikacja dostępności E w chwili predykcji jest obowiązkowa.

## Rozszerzenie benchmarku

1. Ustalić, czy E jest obserwowane przy predykcji, czy tylko używane do ewaluacji; osobno rozważyć Z=C(H) i Z=C(H,E).
2. Zamrozić C i predyktor na środowiskach treningowych; nie używać target E do strojenia.
3. Raportować Δ_source, Δ_target (jeśli możliwe do oszacowania), Γ na z góry ustalonej mieszance środowisk, target log-loss, kalibrację, gap target−source i bity opisu.
4. Używać niezależnych trajektorii/maszyn; porównywać pełną historię, GIA, PCA, autoenkoder, HMM posterior (oracle, gdy znany), state-space model i mocny baseline sekwencyjny.
5. Przeprowadzić testy: nowe RPM, nowe obciążenie, nowa maszyna, nowy czujnik; zmiana nośnika i mechanizmu P(F|Z,E) analizowane oddzielnie.
6. Kontrpróba: Z=const z małym Γ i dużym Δ; kontrpróba z Δ=0 i dużym Γ przy E poza historią.
7. Estymacja Γ dla ciągłych zmiennych może być trudna: podawać estymator, bias, niepewność i rozmiar próby; korzystać z proper scoring rules jako komplementu.
8. Porównania Pareto: Δ vs bity vs koszt; Γ i transfer out-of-environment raportować osobno. Nie redukować do arbitralnego jednego rankingu.

## Status
Tożsamości informacyjne są klasyczne; nie stanowią nowego odkrycia TIMDR. Otwarta hipoteza TIMDR: czy zamrożona implementacja GIA zachowuje predykcyjnie istotną informację przy mniejszym koszcie i lepszym transferze niż adekwatne kontrole. Bez uruchomienia eksperymentów nie wolno deklarować sukcesu.
