# PREREG — TIMDR-INFO-GEOMETRY v0.1

**Data:** 2026-11-14. **Status:** protokół przed pierwszym uruchomieniem; nie stanowi jeszcze prerejestracji z niezależnym znacznikiem czasu. **Zakres:** syntetyczny pilot H1 (detekcja zmiany reżimu), z kontrolami. Wyniki innych hipotez pozostają eksploracyjne.

## Pytanie i wynik główny

Czy dodanie geometrii rekonstrukcji opóźnieniowej poprawia wykrywanie przełączeń między reżimami procesu AR(1), gdy rozkład stacjonarny amplitud w obu reżimach jest taki sam?

Proces: `x[t] = a x[t-1] + sqrt(1-a*a) epsilon[t]`, `epsilon ~ N(0,1)`. Reżimy: `a=0.2` i `a=0.85`. Zmiana w środku każdej niezależnej sesji, z losową kolejnością reżimów. Pierwsze 256 próbek sesji to burn-in; sesja testowa ma 4096 próbek po burn-in. Dla uniknięcia trywialnej detekcji, szacujemy okna po 128 próbek i klasyfikujemy reżim w oknie; okna obejmujące granicę zmiany wykluczamy z głównej oceny, a opóźnienie detekcji raportujemy osobno. Celem nie jest „udowodnienie kwantu informacji”.

## Podział i reprodukowalność

- 100 niezależnych sesji train, 40 calibration, 60 test, generatory `numpy.random.default_rng`, odpowiednio ziarna bazowe 1100, 2200, 3300, pochodne identyfikatory sesji.
- Test nie jest używany do wyboru opóźnienia, wygładzania, klasyfikatora, progów ani cech.
- Przed pierwszym testem należy utrwalić wersje bibliotek, skrypt i SHA commita. Jakakolwiek zmiana po obejrzeniu testu wymaga nowej wersji prerejestracji i nowego holdoutu.

## Cechy i modele

Baseline w każdym oknie: średnia, odchylenie standardowe, RMS, lag-1 i lag-2 autokorelacja, energia w czterech równych pasmach widma. Geometryczne cechy dodatkowe: mediany i IQR krzywizny oraz skrętu trajektorii `(x[t],x[t-2],x[t-4])`, z różnicami skończonymi; pochodne i osobliwości zabezpieczone maską. **Uwaga:** dla krótkich, zaszumionych okien krzywizna i skręt mogą być niestabilne; odsetek zamaskowanych punktów jest osobną cechą kontrolną. Zestaw porównywany: baseline kontra baseline+geometria, identyczny `StandardScaler + LogisticRegression` z `class_weight=balanced`; regularyzacja `C` wybierana na calibration z siatki `{0.01,0.1,1,10}`. Nie wolno zwiększać liczby prób strojenia tylko dla jednego ramienia.

## Metryka i decyzja

Jednostka niepewności: **sesja**, nie okno. Metryka główna: różnica macro-F1 (baseline+geometria minus baseline) na odłożonych sesjach testowych, agregacja przez średnią różnic sesyjnych. Próg **praktycznego sukcesu**: średnia poprawa co najmniej 0.03 punktu F1 **oraz** dolna granica dwustronnego 95% przedziału bootstrap (10 000 resamplowań sesji, seed 4400) powyżej zera. W przeciwnym wypadku H1 nie otrzymuje werdyktu SUPPORTED; brak istotności nie dowodzi równoważności.

## Kontrole obowiązkowe

1. Tasowanie próbek w sesji: efekt oparty na porządku czasowym powinien zaniknąć (osobno trenowane i testowane na tasowanych sekwencjach).
2. Niezależny szum biały: brak stabilnej poprawy, przy losowych etykietach.
3. Wrażliwość: poziom szumu pomiarowego 0, 0.2, 0.5 SD; analiza wyłącznie wtórna.
4. Raportowanie autokorelacji jako mocnego baseline'u: bez niego przewaga geometrii nie jest interpretowalna.

## Granica interpretacji: źródło kontra odbiornik

Ten pilot symuluje znane przełączenie generatora AR(1) przy stałym torze obserwacji. Wynik nie pozwala identyfikować źródła zmian w nieznanym rzeczywistym układzie. Warianty z osobno zmienianym generatorem, kanałem i odbiornikiem wymagają odrębnego zamrożonego testu: [model i macierz G/H/R](GENERATOR_KANAL_ODBIORNIK.md).

## Ograniczenia

To test dodatkowej wartości predykcyjnej cech, nie miara fundamentalnej informacji. AR(1) może być dobrze opisywany przez autokorelację; brak poprawy geometrii jest sensownym i oczekiwanym wynikiem kontrolnym. Dane syntetyczne nie uzasadniają uogólnień na fizykę, EEG ani sejsmikę.

**Przed uruchomieniem:** zweryfikować implementację i zamrozić kod. Dopiero potem wykonywać ocenę testową.
