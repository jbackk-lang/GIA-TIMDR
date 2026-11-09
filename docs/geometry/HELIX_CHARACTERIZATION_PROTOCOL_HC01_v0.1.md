# HELIX-CHAR-01: niezależna charakterystyka właściwości helisy TIMDR (v0.1)

**Data:** 2026-11-09  
**Cel:** poznać właściwości i ograniczenia helisy bez narzucania mechanizmu redukcji ani oczekiwanych progów.  
**Status:** protokół badawczy; brak wyników pomiarowych dla pełnej macierzy.

## 1. Pytanie badawcze

Jakie właściwości geometryczne, topologiczne i numeryczne ma każda badana klasa helisy, jak zmieniają się one z parametrami i które pozostają stabilne przy zmianie skali, orientacji, parametryzacji oraz perturbacjach?

Przydatność konstrukcji będzie oceniana dopiero na podstawie wyników. Redukcja 4→3, próg 90°, model π–√2–√3 i interpretacje TRM nie są założeniami eksperymentu.

## 2. Rozdzielenie obiektów

Każdy model otrzymuje osobny identyfikator i nie dziedziczy wyników innego modelu.

| ID | Rodzina | Rola |
|---|---|---|
| HC-01 | Helisa kołowa o stałym promieniu i skoku | przypadek analityczny kontrolny |
| HC-02 | Helisa o zmiennym skoku | wpływ niejednorodności osiowej |
| HC-03 | Helisa stożkowa / zmienny promień | wpływ geometrii promienia |
| HC-04 | Helisa na zadanej osi zakrzywionej | wpływ krzywizny osi i ramy transportowanej |
| HC-05 | Krzywa zamknięta o lokalnej helikalności | osobna klasa topologiczna; nie utożsamiać z trefoilem |
| HC-06 | Trefoil | kontrola węzłowa, nie wzorzec zwykłej helisy |

## 3. Przypadek analityczny HC-01

Dla:
`r(t)=(a cos t, a sin t, ht), a>0`
obowiązują:
`κ=a/(a²+h²)`, `τ_FS=h/(a²+h²)`.

Dalej:
`τ_FS/κ=h/a`, `α=atan(h/a)`, `p=2πh`,
`L_1turn=2π√(a²+h²)`.

Wartości te są odniesieniem do walidacji implementacji. Dla odbicia lustrzanego zmienia się znak torsji przy zachowaniu krzywizny i długości. Zmiana parametru orientacji musi być jawna.

Parametry bezwymiarowe:
`η=h/a`, `κ_hat=aκ=1/(1+η²)`, `τ_hat=aτ_FS=η/(1+η²)`.
Porównania między skalami prowadzić przede wszystkim przez η i wielkości bezwymiarowe.

## 4. Karta pomiarowa — raportować osobno

### Geometria lokalna
- pozycja, styczna jednostkowa, szybkość;
- krzywizna κ(s), promień krzywizny tam, gdzie κ>0;
- podpisana torsja Freneta τ_FS(s), z maską obszarów degeneracji;
- kąt nachylenia stycznej do płaszczyzny poprzecznej;
- długość łuku, skok, promień i ich zmienność.

### Geometria ramy i tunelu
- rama Freneta tam, gdzie jest regularna;
- rama Bishop/parallel jako stabilna rama odniesienia;
- obrót przekroju względem ramy, mierzony jako osobna wielkość;
- holonomia po zamknięciu;
- promień rurki dopuszczalny lokalnie i globalnie;
- minimalna odległość nieprzyległych fragmentów krzywej;
- luz i pierwsze samoprzecięcie / nakładanie sąsiednich przekrojów.

### Globalne i topologiczne
- otwarta / zamknięta;
- domknięcie pozycji, stycznej i ramy;
- liczba obrotów fazy bez redukcji modulo 2π;
- znak orientacji/chiralność;
- linking/writhe/twist tylko wtedy, gdy obiekt i definicje tych wielkości są właściwe;
- niezmienniki węzła tylko dla zamkniętych krzywych bez samoprzecięć.

### Odporność numeryczna
- błąd względem rozwiązania analitycznego;
- zbieżność względem liczby próbek;
- wrażliwość na szum, nieregularne próbkowanie i kwantyzację;
- wrażliwość na wybór ramy i wygładzania;
- jawna maska punktów, w których torsja nie jest wiarygodna.

## 5. Macierz eksperymentów

### A. Walidacja analityczna
Dla HC-01 porównać pochodne analityczne z estymacją numeryczną. Wykonać testy dla obu znaków h, wielu a i η oraz N = 128, 256, 512, 1024, 2048. Zbadać błąd w środku domeny i na szwach oddzielnie.

### B. Sweep parametrów
Zmieniać niezależnie:
- a przy stałym h;
- h przy stałym a;
- η przy stałej skali;
- liczbę obrotów;
- fazę początkową;
- orientację lewą/prawą.

Nie mieszać zmiany skali ze zmianą kształtu. Raportować krzywe metryk, nie tylko pojedyncze wartości.

### C. Porównanie rodzin
Dla HC-02–HC-05 zmierzyć te same wielkości, o ile są zdefiniowane. Brak definicji oznaczyć NOT_APPLICABLE, nie zastępować zerem. Porównywać przy dopasowanej długości, promieniu charakterystycznym lub innych jawnych skalach.

### D. Tunel
Dla każdej krzywej oszacować maksymalny promień tubularnego otoczenia na podstawie ograniczeń lokalnych i globalnych. Oddzielić:
- lokalną utratę regularności przekroju;
- globalne zbliżenie odległych fragmentów;
- fizyczną kolizję gałęzi;
- samoprzecięcie osi.

Nie utożsamiać żadnego z tych zdarzeń automatycznie z redukcją.

### E. Perturbacje
Wprowadzać pojedynczo: szum pozycji, jitter parametru, dropout, lokalne deformacje i perturbacje parametrów. Każdy eksperyment ma mieć kontrolę bez perturbacji, seed i raport błędu.

## 6. Zasady analizy skrętu

Nie istnieje jeden uniwersalny „skręt”. W każdym wyniku podać, czy mowa o:
1. podpisanej torsji Freneta–Serreta;
2. obrocie ramy przekroju względem ramy transportowanej;
3. całkowitym skręcie pasma;
4. writhe/linking obiektu zamkniętego;
5. fazie/winding liczonym z konkretnego pola lub sygnału.

Nie redukować znaku do wartości bezwzględnej w analizie chiralności. Kąt modulo 360° raportować obok wartości rozwiniętej (unwrapped), nie zamiast niej. Próg 90° może być analizowany jako obserwacja, ale nie jest kryterium sukcesu ani założonym limitem.

## 7. Kryteria jakości i falsyfikacji

- W HC-01 estymatory muszą zbiegać do wzorów analitycznych.
- Właściwości geometryczne nie mogą zmieniać się pod translacją ani obrotem sztywnym.
- Przy jednolitej zmianie skali krzywizna i torsja muszą skalować się odwrotnie do długości, a długość łuku proporcjonalnie.
- Odbicie lustrzane musi zachować miary nieorientowane i poprawnie odwrócić miary orientowane.
- Wynik nie może zależeć istotnie od liczby próbek po osiągnięciu zbieżności.
- Każda własność niestabilna numerycznie musi otrzymać zakres wiarygodności, nie pojedynczą pozornie dokładną liczbę.
- Nie wolno przenosić wyników HC-06 (trefoil) na HC-01 (helisę kołową).

## 8. Ocena przydatności — dopiero po charakterystyce

Po zebraniu wyników można ocenić zastosowania:
- prowadzenie lub transport sygnału;
- kodowanie orientacji/chiralności;
- separacja kanałów;
- odporność na zakłócenia;
- kompaktowość geometryczna;
- stabilność mechaniczna lub modalna — wymaga osobnego modelu fizycznego;
- rekonstrukcja informacji i odwracalność.

Każda deklaracja zastosowania wymaga porównania z geometrią odniesienia (linia prosta, okrąg, sprężyna/helisa klasyczna, krzywa kontrolna) przy równych zasobach i tych samych warunkach.

## 9. Minimalny wynik każdego uruchomienia

Zachować: definicję rodziny i równania, parametry z jednostkami, orientację, liczbę próbek, metodę różniczkowania, ramę, tolerancje, surowe metryki, maski degeneracji, wykresy, seed, wersje bibliotek, komendę uruchomienia i commit SHA.

**Decyzja:** charakterystyka helisy ma pierwszeństwo przed badaniem redukcji. Redukcja, TRM i hipotezy konstrukcyjne są interpretacjami wtórnymi, które mogą zostać potwierdzone, zmienione albo odrzucone przez pomiary.
