# 52A — Predictive Compression Frontier: zamknięcie i przekazanie

**Data:** 2026-11-17  
**Status:** seria 52A.1–52A.7 zamknięta roboczo. Nie deklarować dowodu ogólnej przewagi jakiejkolwiek reprezentacji.  
**Repozytorium:** `jbackk-lang/GIA-TIMDR`

## Teza poddana badaniu

Dla historii `H`, przyszłości `F` i reprezentacji `Z=C(H)` badamy kompromis między stratą predykcyjną `Delta(Z)=I(F;H|Z)`, kosztem kodowania `L(Z)`, kosztem modelu predykcyjnego i kosztem uczenia/wyboru reprezentacji. Wynik na jednym syntetycznym generatorze nie implikuje uniwersalnej przewagi ani poprawy operacyjnego `GIAFilter`.

## Mapa eksperymentów

| Etap | Pytanie | Najważniejsze ustalenie | Granica interpretacji |
|---|---|---|---|
| 52A.1 | Dokładne optimum w małej przestrzeni | Enumeracja 15 podziałów czterech stanów pokazuje, że zachowanie sygnału może dawać zerową stratę przy mniejszej entropii niż pełna historia | Znany generator, idealna entropia, bez rzeczywistego kodowania |
| 52A.2 | Koszt rzeczywistego kodowania | DEFLATE plus nagłówek i mapowanie: zachowanie sygnału może kosztować dużo mniej niż pełna historia | Jeden syntetyczny strumień, brak kosztu predyktora |
| 52A.3 | Granica Pareto: bity, Delta, czas | Dla testowanych czterech reprezentacji tylko stała i sygnał były niedominowane w raportowanym pomiarze | Czasy sprzętowe, 7 powtórzeń, bez kosztu ekstrakcji cech |
| 52A.4 | Koszt parametrów predyktora | Zysk z krótszej reprezentacji może przetrwać doliczenie parametrów, ale koszt modelu zależy od konwencji rozliczenia | Przyjęto 64 bity/parametr, nie zmierzono faktycznego pliku modelu |
| 52A.5 | Odkrywanie reprezentacji z danych | Wybór między dwiema cechami może być błędny przy małej próbie | Tylko dwóch kandydatów, znany syntetyczny proces |
| 52A.6 | Wielu kandydatów i walidacja | Oddzielna walidacja poprawiała wybór przy silnym sygnale i dodatkowych danych | Walidacja miała własne dodatkowe obserwacje |
| 52A.7 | Stały budżet, słabszy sygnał, korelacje | W raportowanym teście odjęcie danych treningowych na walidację mogło pogarszać wynik | Zależność od generatora, korelacji i procedury refitu |

## Wnioski, które można obronić

1. **Zadanie predykcyjne definiuje, co warto zachować.** Zachowanie całej historii może być niepotrzebne, jeżeli jej fragment jest wystarczający do przewidywania.
2. **Koszt reprezentacji ma kilka składników.** Entropia, długość faktycznego kodu, koszt metadanych, parametry predyktora, czas obliczeń oraz koszt wyboru cech nie są tym samym.
3. **Wybór reprezentacji jest problemem statystycznym.** Wynik z oracle, który zna właściwą cechę, nie jest równoważny wynikowi algorytmu uczącego się jej z danych.
4. **Walidacja nie jest darmowa.** Korzyść z niezależnego wyboru hiperparametrów może zniknąć, gdy walidacja uszczupla mały, stały budżet treningowy.
5. **Brak dowodu uniwersalności.** Seria 52A nie potwierdza przewagi GIA ani żadnej metody na rzeczywistych danych.

## Ważne ostrzeżenie replikacyjne

Wcześniejsze odpowiedzi w rozmowie raportowały lokalne wykonania i wyniki. Samo istnienie kodu na GitHubie **nie jest potwierdzeniem**, że dokładnie ten commit wygenerował przytoczone liczby. Szczególnie 52A.5–52A.7 wymagają niezależnego uruchomienia zapisanych wersji i sprawdzenia zgodności z raportowanymi tabelami. Przed wykorzystaniem liczb w publikacji: pobrać konkretne SHA, uruchomić kod, zapisać JSON, wersję Pythona i zależności, porównać kontrolne wartości oraz w razie rozbieżności poprawić raport. Nie przenosić do publikacji statusów PASS wyłącznie na podstawie tekstu rozmowy.

## Zalecany standard kolejnych badań

- Przed testem zamrozić generator/protokół, budżet i metryki.
- Porównywać pełen koszt: zakodowane Z + metadane + model + koszt wyboru i ekstrakcji.
- Rozdzielić train, validation, test według niezależnych jednostek, nie sąsiadujących okien.
- Powtarzać wyniki na wielu seedach i raportować niepewność oraz pełne rozkłady, nie tylko średnie.
- Testować także zmianę rozkładu, rzadkie zdarzenia i słabe sygnały.
- Nie przypisywać ogólnych gwarancji eksperymentom na znanym syntetycznym generatorze.

## Co dalej — wybór odrębnej gałęzi

**Rekomendowany kierunek 53A: predykcyjne stany wystarczające i odporność na zmianę środowiska.** Pytanie: czy reprezentacja wystarczająca predykcyjnie w środowisku treningowym zachowuje tę własność po zmianie rozkładu? Zdefiniować rodziny procesów, dokładne `Delta_e(Z)` dla każdego środowiska i sprawdzić, kiedy minimalny stan predykcyjny wymaga informacji, którą selekcja treningowa odrzuca.

Alternatywy:
- **53B — rzadkie zdarzenia:** średnia strata kontra warunkowa strata na rzadkim sygnale.
- **53C — koszt pełnego systemu:** rzeczywiste kodowanie modelu, dekodera i metadanych.
- **53D — operacyjna walidacja GIA:** oryginalny `GIAFilter` na niezależnych danych z fizycznymi hitami.

**Decyzja:** nie rozszerzać 52A o kolejne syntetyczne warianty tego samego procesu bez nowego falsyfikowalnego pytania.

## Indeks kodu

- `research/52A1_EXACT_FRONTIER.py`
- `research/52A2_ACTUAL_CODING.py`
- `research/52A3_PARETO.py`
- `research/52A4_TOTAL_COST.py`
- `research/52A5_LEARNED_REPRESENTATION.py`
- `research/52A6_MULTIPLE_CANDIDATES.py`
- `research/52A7_FIXED_BUDGET.py`

Wyniki JSON nie są automatycznie utrwalone w repozytorium przez zapis powyższych skryptów; wymagają osobnej replikacji i commitów.
