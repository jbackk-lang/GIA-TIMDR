# Predykcja przyszłego reżimu na podstawie czasu ekstremów — 2026-11-14

**Status:** wykonany lokalnie eksperyment syntetyczny, nie walidacja TIMDR ani ontologii czasu.

## Konstrukcja
Wcześniejsze okno: 64 próbki; losowe tło [-0.6,0.6], dwa zdarzenia ±1. W każdym przypadku `MIN=-1`, `MAX=+1`, `t_end=63`. Kolejność ekstremów jest skorelowana z **późniejszym parametrem** generatora AR(1) z prawdopodobieństwem 0.85. Przyszłe 128 próbek generowane niezależnie warunkowo od reżimu: `alpha=0.15` dla etykiety 0, `alpha=0.85` dla etykiety 1. Etykieta nie jest zdefiniowana jako kolejność ekstremów, ale generator celowo wiąże je wspólną zmienną.

Trening: 300 ziaren × 2 klasy = 600 przypadków; test: 100 ziaren × 2 klasy = 200 przypadków. Rozdzielne zakresy ziaren. Klasyfikator najbliższego centroidu z normalizacją na treningu.

## Wyniki rzeczywistego wykonania

```
mode,correct,total,accuracy
VALUES,100,200,0.5000
SHUFFLE,100,200,0.5000
EVENT,173,200,0.8650
future_lag1_mean_by_label 0.136 0.817
```

- VALUES = (MIN,MAX,t_end), wszystkie identyczne; klasyfikator wybiera etykietę 0.
- SHUFFLE = VALUES + losowy znak odstępu czasowego, niezależny od klasy, przypisany per ziarno; kontrola zerwania kierunku kolejności.
- EVENT = VALUES + (t_max-t_min), **cztery liczby, nie trzy**.

Macierz pomyłek EVENT: etykieta 0: 81/100 poprawnie; etykieta 1: 92/100 poprawnie. Zysk względem VALUES = 36.5 punktu procentowego. Bootstrap sparowany po 100 ziarnach, 5000 replik, 95% przedział percentylowy przybliżony **[31.5, 41.0] pp**.

## Interpretacja
W tym zadaniu chwile zdarzeń niosą predykcyjną informację o przyszłym reżimie, której nie ma w samych wartościach MIN/MAX i czasie końca. **Zależność 85% została wbudowana w generator**, więc eksperyment nie dowodzi, że występuje w naturze, ani że TIMDR ją odkrył.

Nie mylić tego z analizą spektralną: redukcja do MIN/MAX/czas nie pozwala odtworzyć ogólnego widma oryginału. Czteroelementowy wariant EVENT nie rozstrzyga, jak zapisać informację zdarzeń w **dokładnie trzech** cechach. Potrzebna decyzja semantyczna, czy trzecia cecha jest czasem końca, czasem względnym, czy złożonym obiektem czasowym.

## Następne testy
1. Wybór `t` jako czasu względnego vs czasu obserwacji, przy zachowaniu znaczników w Chronoprocesie.
2. Predykcja na rzeczywistych danych z odłożonymi sesjami.
3. Przesunięcie/skala zegara i błędy synchronizacji.
4. Brak związku czas–przyszłość jako kontrola negatywna.
5. Rozróżnienie geometrii trajektorii 1D od prawdziwej powierzchni G.

Kod: `chronoprocess_future_test.py`.
