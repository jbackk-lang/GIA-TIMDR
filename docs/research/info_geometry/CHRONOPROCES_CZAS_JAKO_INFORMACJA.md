# Chronoproces: czas jako indeks, zdarzenie i kandydat na informację

**2026-11-14. Status:** hipoteza badawcza, bez zmiany aksjomatów TIMDR.

Autor wskazuje, że Chronoproces może obejmować zarówno czas okna, jak i chwile ekstremów, a czas sam może stanowić część informacji zawartej w przebiegu. Nie należy przedwcześnie wybrać jednego znaczenia „czasu” w redukcji MIN–MAX–CZAS.

## Rozdzielenie warstw

Dla okna `W_k` sygnału `x(t)`:

- `t_obs,k`: znacznik odbioru lub końca okna (czas obserwacji; przyczynowy online).
- `t_min,k=argmin_{t∈W_k} x(t)`: chwila minimum.
- `t_max,k=argmax_{t∈W_k} x(t)`: chwila maksimum.
- `Δt_k=t_max,k−t_min,k`: podpis kolejności i odległości zdarzeń (znak ma znaczenie).
- `Δt_obs,k=t_obs,k−t_obs,k−1`: tempo obserwacji.

Przy remisach ekstremów należy jawnie ustalić regułę wyboru (np. pierwsze wystąpienie) i przechować liczbę remisów. Zegar obserwatora i zegar źródła mogą różnić się dryftem/opóźnieniem; nie utożsamiać ich bez synchronizacji.

## Trzy cechy a bogatsza semantyka czasu

Publiczny wynik jednostkowy może pozostać trójką `R_k=(min_k,max_k,t_k)`, lecz `t_k` wymaga określenia semantyki. **Nie wolno ukrywać dodatkowych wymiarów** przez nazywanie całej krotki czasowej pojedynczą liczbą. Alternatywa: trójka jako widok, a metadane `t_obs,t_min,t_max` jako oddzielny rekord Chronoprocesu; jawnie przyznać, że całkowita reprezentacja zawiera więcej informacji niż trzy liczby.

## Co znaczy „czas niesie informację”?

To hipoteza zależna od zadania i punktu odniesienia, nie automatyczny aksjomat. Dla zmiennej etykiety/zdarzenia `Y` porównać informację predykcyjną `I(Y;min,max)` z `I(Y;min,max,t_min,t_max,Δt)` lub praktycznie poprawę wyniku modelu na danych odłożonych. Sama przewidywalność z czasu może być artefaktem zegara, harmonogramu lub przecieku etykiet.

Czas jako uporządkowany indeks `T` w `Ξ=(T,x,Γ,φ)` nie jest automatycznie tożsamy z czasem lokalnym K, geometrią G ani „substancją informacji”. Zachować trzy niezależne rzuty i jawne mosty.

## Protokół eksperymentalny

Przygotować pary przebiegów o tych samych `min,max,t_obs`, lecz innych `t_min,t_max` i odwrotnie. Porównać:
1. `(min,max)`;
2. `(min,max,t_obs)`;
3. `(min,max,t_min,t_max)`;
4. sekwencję okien z kolejnością;
5. kontrolę z przetasowaniem czasów zdarzeń między sesjami;
6. kontrolę przesunięcia i przeskalowania zegara, z opóźnieniem kanału.

Metryki: jakość detekcji, fałszywe alarmy, opóźnienie, zdolność odróżnienia historii, stabilność na zmianie zegara. Podział na całe sesje, nie na sąsiednie okna.

**Interpretacja:** dodatkowa wartość chwil ekstremów świadczyłaby o informacji predykcyjnej w ich relacji czasowej *dla danego zadania*, nie o uniwersalnej ontologii czasu.

## Konsekwencja dla „rurki”

Trajektoria `k↦(min_k,max_k,t_obs,k)` nadal jest krzywą 1D w R³. Aby otrzymać dopuszczalną powierzchnię gałęzi G, trzeba osobno zdefiniować rodzinę `Γ(t,s)` i sprawdzić regularność. Możliwy parametr `s` nie może być dodany arbitralnie tylko po to, by uzyskać powierzchnię.

**Zgodność:** `docs/theory/TIMDR_Chronoprocess.md`, `docs/theory/TIMDR_Branch_Specification.md`.
