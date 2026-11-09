# Druga droga redukcji TIMDR: analogia π idealne → π rzeczywiste oraz √2 / √3 (v0.2)

**Data:** 2026-11-09  
**Status:** korekta interpretacji autora; formalny operator redukcji pozostaje do odtworzenia.

## 1. Korekta sensu analogii

Pierwiastki √2 i √3 nie miały być po prostu składnikami sumy przybliżającej π ani długościami dwóch cięciw, których dodanie daje obwód. Miały pełnić rolę **odpowiednika naszej redukcji** w analogii przejścia od π idealnego do π rzeczywistego.

Czyli badamy relację strukturalną:
[
\text{ideał / konstrukcja idealna}
\xrightarrow{\text{redukcja}}
\text{postać rzeczywista / realizowalna}
]
a nie równość liczbową:
[
\sqrt2+\sqrt3=\pi.
]

W języku TIMDR pytanie brzmi: czy relacja między √2 i √3 koduje podobny mechanizm przejścia/redukcji, jaki obserwujemy w geometrii helisy (np. przejście konfiguracji do postaci dopuszczalnej), podczas gdy π idealne i π rzeczywiste stanowią analogiczny wzorzec idealizacji i realizacji?

To jest interpretacja robocza, nie dowiedzione twierdzenie. Nie przesądzamy jeszcze, czy √2 i √3 są dwoma stanami, granicami, współczynnikami, wymiarami czy elementami konstrukcji.

## 2. Rozróżnienie matematyczne, którego nie wolno zgubić

W matematyce π jest jedną dokładną liczbą rzeczywistą i nie ma odrębnej „wartości idealnej” oraz „wartości rzeczywistej”. Można natomiast rozróżnić:
- idealny obiekt geometryczny — doskonały okrąg;
- jego idealną wielkość — dokładny obwód (C=2\pi r);
- skończone konstrukcje/przybliżenia — wielokąty, pomiary i algorytmy, których wyniki zbliżają się do π;
- fizyczną realizację — obiekt o tolerancjach, ziarnistości i błędzie pomiaru.

Dlatego sformułowanie „π idealne → π rzeczywiste” należy rozumieć jako analogię między ideałem a skończoną realizacją/przybliżeniem, a nie jako dwie różne matematyczne wartości π.

## 3. Fakty kontrolne o √2 i √3

[
\sqrt2\approx1.41421356237,\qquad
\sqrt3\approx1.73205080757.
]
[
\sqrt2+\sqrt3\approx3.14626436994\ne\pi.
]

Suma jest algebraiczna, π jest przestępne, więc nie są równe. Ta kontrola obala wyłącznie prostą interpretację sumy jako dokładnego π; **nie obala analogii redukcyjnej**, którą wskazuje autor.

Dla okręgu jednostkowego √2 i √3 występują też jako długości określonych cięciw, lecz bez źródłowego diagramu nie wolno uznać tego za zamierzone znaczenie w TIMDR.

## 4. Co trzeba odzyskać, aby sformalizować analogię

1. **Obiekt idealny:** co dokładnie nazywaliśmy π idealnym — okrąg, obwód, stosunek obwodu do średnicy, czy konstrukcję graniczną?
2. **Obiekt realizowany:** co było π rzeczywistym — przybliżenie wielokątne, skończony pomiar, czy inna reprezentacja?
3. **Rola pierwiastków:** czy √2 i √3 są dwoma poziomami/stadiami redukcji, czy parametrami transformacji między nimi?
4. **Operator:** jaka operacja przeprowadza stan idealny w realizowany i co zachowuje?
5. **Błąd/reszta:** co zostaje utracone lub pozostaje jako reszta po redukcji?
6. **Niezmiennik:** jaka wielkość pozostaje zachowana — stosunek, długość, pole, orientacja, faza, liczba stopni swobody?
7. **Odpowiednik helisy:** jaki obiekt TIMDR odpowiada idealnemu okręgowi, a jaki jego skończonej realizacji?

## 5. Program porównawczy z redukcją helisy

Nie utożsamiamy obu dróg. Budujemy tabelę odwzorowania dopiero po zdefiniowaniu obiektów:

| Analogia kołowa | Kandydat w TIMDR | Status |
|---|---|---|
| Okrąg / π idealne | źródłowa konstrukcja geometryczna helisy | do zdefiniowania |
| Skończone przybliżenie / realizacja | konfiguracja po redukcji | do zdefiniowania |
| √2, √3 | elementy/parametry przejścia redukcyjnego | rola nieustalona |
| Błąd lub reszta przybliżenia | informacja tracona/zachowywana w redukcji | do zmierzenia |
| Granica procesu | stan graniczny / warunek brzegowy TIMDR | do wykazania |

Kryterium wspólnego mechanizmu: oba modele muszą mieć jawny operator redukcji i dawać zgodny, niezależnie zdefiniowany niezmiennik. Samo podobieństwo liczb lub rysunków nie wystarczy.

## 6. Status w repozytorium

W przeszukanym drzewie bieżącej gałęzi main nie znaleziono jeszcze źródłowego rysunku/notatki odtwarzającej tę analogię. Zachowujemy ją jako odrębną gałąź i nie dopowiadamy brakującej konstrukcji.

## 7. Decyzja

Zachować ideę autora: **√2 i √3 mają reprezentować mechanizm redukcji analogiczny do przejścia od π idealnego do π rzeczywistego**. Nie interpretować ich jako sumy równej π. Następny krok to odzyskanie definicji stanów idealnego i realizowanego oraz operatora przejścia. Dopiero wtedy można porównać ten mechanizm z redukcją helisy 4→3.
