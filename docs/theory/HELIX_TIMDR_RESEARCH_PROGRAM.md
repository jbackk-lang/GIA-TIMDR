# HELIX–TIMDR: program badań nad reprezentacjami helisy, pola i struny

**Status:** program badawczy / notatka ciągłości prac  
**Wersja:** 0.1  
**Repozytorium nadrzędne:** GIA-TIMDR  
**Miejsce prowadzenia postępu:** `docs/theory/HELIX_TIMDR_RESEARCH_PROGRAM.md`  
**Powiązany projekt aplikacyjny:** HELIX-LOCK (repozytorium siostrzane; nie jest miejscem przechowywania głównego postępu teorii)

## 0. Cel dokumentu i zasada ciągłości

Ten dokument jest kanonicznym punktem zapisu postępu badań nad możliwością wykorzystania struktur helikalnych TIMDR w przyszłych architekturach transformacji danych i kryptografii.

Wszystkie definicje, hipotezy, wyniki, decyzje, pytania otwarte i odnośniki do implementacji mają być dopisywane tutaj lub w dokumentach podrzędnych repozytorium GIA-TIMDR. Nie należy uzależniać ciągłości projektu od pamięci pojedynczej rozmowy.

**Ważne rozróżnienie repozytoriów:**
- GIA-TIMDR jest głównym repozytorium teorii, formalizacji, eksperymentów i rejestru postępu.
- HELIX-LOCK jest projektem aplikacyjnym, w którym można później badać zastosowania wyników GIA-TIMDR.
- Gałąź eksperymentalna HTKE w HELIX-LOCK nie definiuje ani nie zastępuje teorii TIMDR. Jej dokumentacja jest artefaktem pochodnym i powinna odwoływać się do ustaleń zapisanych tutaj.

## 1. Punkt wyjścia: nie zakładać z góry szyfru

Pytanie badawcze nie brzmi obecnie „jak zbudować nowy szyfr?”, lecz:

**Jakie matematyczne reprezentacje i transformacje struktury helikalnej TIMDR są poprawne, odwracalne lub informacyjnie kontrolowane, i czy mają jakąkolwiek mierzalną wartość dla przetwarzania danych lub kryptografii?**

Nie zakłada się, że:
- sama helisa jest bezpiecznym szyfrem;
- złożoność geometryczna oznacza odporność kryptograficzną;
- transformacja helisy w pole lub strunę jest już zdefiniowana w TIMDR;
- przejście między reprezentacjami zachowuje informację;
- nowa konstrukcja będzie lepsza od uznanych prymitywów kryptograficznych.

Własny szyfr jest jedną z możliwych, odległych hipotez aplikacyjnych, a nie celem przesądzonym na starcie.

## 2. Dotychczasowe ustalenia z rozmów i przeglądu kodu

### 2.1. Chronoproces TIMDR nie scala gałęzi w jeden obiekt

Przegląd `TIMDR-Time-Formalism/timdr_time/chronoprocess.py` potwierdził, że Chronoprocess orkiestruje trzy niezależne projekcje wspólnego nośnika:
- M/S: tempo i drift wyznaczane z próbek nośnika;
- G: powierzchnia kongruencji budowana z osi czasu i osobnej domeny parametrów;
- K: faza i interferencja modalności oceniane w punktach nośnika.

Kod jawnie zachowuje nieredukowalność projekcji. Nie wolno bez formalnego uzasadnienia sklejać M/S, G i K w jeden wektor stanu ani utożsamiać ich obiektów matematycznych.

### 2.2. Zakres obecnej gałęzi K

Przegląd `TIMDR-Modal-Formalism/timdr_modal/phase_sync.py` potwierdził, że obecny model modalności jest ograniczony do stałych parametrów `(f, phi, A)`, z fazą chwilową `2*pi*f*t + phi`, interferencją oraz afiniczną mapą synchronizacji faz. Nie jest to jeszcze dynamiczny, sprzężony układ oscylatorów ani ogólny model ewoluującego pola fazowego.

### 2.3. Eksperymenty trzech pętli

Eksperymenty trzech pętli i pamięci fazowej w HELIX-LOCK są modelami eksperymentalnymi z jawnie dodanymi prawami sprzężenia zwrotnego. Nie należy utożsamiać ich z produkcyjnym Chronoprocess ani traktować ich jako dowodu własności kryptograficznych.

### 2.4. Kierunek wybrany do zbadania

Wskazano dwie możliwe reprezentacje helisy:
1. **Helisa jako pole** — możliwa reprezentacja skalarna, wektorowa lub tensorowa, do formalnego zdefiniowania.
2. **Helisa jako struna** — możliwa reprezentacja obiektu jednowymiarowego z wewnętrznymi stopniami swobody, do formalnego zdefiniowania.

Nie ustalono jeszcze, czy pole i struna są:
- alternatywnymi reprezentacjami tej samej struktury;
- projekcjami zachowującymi tylko część informacji;
- różnymi modelami o odmiennych przestrzeniach stanów;
- powiązane transformacją odwracalną, częściowo odwracalną czy nieodwracalną.

To pozostaje otwartym pytaniem. Nie wolno opisywać tych reprezentacji jako już równoważnych.

## 3. Główne pytania badawcze

### R1. Definicja obiektu helikalnego
- Jaki jest minimalny zestaw danych definiujących helisę w danym formalizmie TIMDR?
- Które parametry są pierwotne, a które pochodne?
- Jakie są przestrzeń stanów, jednostki, warunki brzegowe i relacje równoważności?
- Czy istnieją niezmienniki, które powinny przetrwać zmianę reprezentacji?

### R2. Reprezentacja polowa
- Jaki typ pola jest uzasadniony: skalarne, wektorowe, tensorowe czy inne?
- Na jakiej przestrzeni pole jest zdefiniowane?
- Jak helisa wyznacza pole i czy odwrotna rekonstrukcja jest możliwa?
- Jakie regularności, warunki brzegowe i ograniczenia fizyczne/matematyczne są wymagane?

### R3. Reprezentacja strunowa
- Co dokładnie oznacza „struna” w tym programie: krzywa z polami wewnętrznymi, obiekt dynamiczny, czy inna konstrukcja?
- Jak definiuje się parametryzację, krzywiznę, skrętność, mody i dynamikę?
- Które wielkości są obserwowalne, a które zależą od parametryzacji?
- Czy model strunowy wnosi informację niewidoczną w reprezentacji polowej?

### R4. Przejścia między reprezentacjami
- Czy istnieje jawna mapa helisa → pole?
- Czy istnieje jawna mapa helisa → struna?
- Czy istnieją mapy pole ↔ struna?
- Czy mapy są jednoznaczne, ciągłe, stabilne i odwracalne?
- Jeśli nie są odwracalne, jaka informacja jest tracona i czy strata jest mierzalna?
- Jak zachowują się niezmienniki przy przejściu?

### R5. Wartość informacyjna i obliczeniowa
- Czy nowa reprezentacja upraszcza obliczenia lub ujawnia strukturę?
- Czy jest stabilna numerycznie?
- Czy daje przewagę nad bezpośrednim opisem helikalnym?
- Jak odróżnić rzeczywisty efekt od artefaktu parametryzacji, dyskretyzacji lub doboru danych?

### R6. Potencjał kryptograficzny
Dopiero po odpowiedziach na R1–R5:
- Czy reprezentacje mogą dostarczyć użytecznego modelu stanu lub zarządzania kluczami?
- Czy da się zdefiniować transformację danych będącą bijekcją na jasno określonej przestrzeni?
- Czy konstrukcja spełnia standardowe definicje bezpieczeństwa, a nie tylko ukrywa strukturę danych?
- Czy daje mierzalną przewagę nad standardowymi, publicznie analizowanymi konstrukcjami?
- Czy w ogóle istnieje powód, by budować nowy szyfr zamiast użyć sprawdzonego szyfru i zastosować TIMDR w warstwie zarządzania stanem?

## 4. Zasady metodologiczne

1. Każda hipoteza otrzymuje identyfikator, definicję, zakres i kryterium falsyfikacji.
2. Każda transformacja ma jawne dziedziny, przeciwdziedziny i założenia.
3. Oddzielać twierdzenia formalne, wyniki numeryczne, obserwacje empiryczne i intuicje.
4. Zachować niezależność gałęzi TIMDR; mapy między gałęziami wymagają osobnego uzasadnienia.
5. Używać testów kontrolnych, ablacją i przypadków negatywnych.
6. Rejestrować także wyniki negatywne i hipotezy odrzucone.
7. Nie nazywać konstrukcji kryptograficznie bezpieczną bez analizy i niezależnego przeglądu.
8. Nie traktować chaosu, nieliniowości, dużej liczby parametrów ani trudności wizualnej jako dowodu bezpieczeństwa.
9. Nie wprowadzać zmian do istniejącego szyfrowania HELIX-LOCK na etapie badań matematycznych.
10. Każdy wynik musi wskazywać commit, wersję kodu, dane wejściowe i instrukcję reprodukcji.

## 5. Proponowany plan badań

### Etap A — inwentaryzacja matematyki helisy
- znaleźć wszystkie definicje, równania, implementacje i eksperymenty helikalne w GIA-TIMDR i repozytoriach siostrzanych;
- rozdzielić definicje formalne od wizualizacji i eksperymentów;
- sporządzić tabelę symboli, parametrów, jednostek i niezmienników;
- wskazać sprzeczności i luki.

**Rezultat:** katalog istniejącej matematyki helikalnej.

### Etap B — helisa jako pole
- zdefiniować kandydatów na pole i przestrzeń definicji;
- wyprowadzić mapę z helisy do pola;
- sprawdzić regularność, stabilność i odwracalność;
- określić, co pole zachowuje, a co pomija.

**Rezultat:** formalna propozycja reprezentacji polowej oraz testy.

### Etap C — helisa jako struna
- zdefiniować obiekt strunowy i jego stopnie swobody;
- określić parametryzację i niezmienniki;
- zbadać dynamikę i stabilność;
- porównać z reprezentacją helikalną i polową.

**Rezultat:** formalna propozycja reprezentacji strunowej oraz testy.

### Etap D — relacje między reprezentacjami
- zdefiniować mapy i ich odwrotności, jeśli istnieją;
- sprawdzić rekonstrukcję na danych syntetycznych i przypadkach brzegowych;
- zmierzyć straty informacji;
- określić klasy równoważności.

**Rezultat:** mapa relacji helisa–pole–struna.

### Etap E — ocena zastosowań
- wybrać zastosowania wynikające z udowodnionych właściwości;
- porównać z prostszymi modelami bazowymi;
- kryptografię rozpatrywać dopiero po formalizacji i analizie bezpieczeństwa.

**Rezultat:** decyzja oparta na dowodach: kontynuować, zawęzić lub porzucić zastosowanie kryptograficzne.

## 6. Rejestr hipotez — wersja 0.1

| ID | Hipoteza | Status | Wymagany dowód |
|---|---|---|---|
| H-01 | Strukturę helikalną TIMDR można opisać reprezentacją polową | Otwarta | Jawna definicja i mapa |
| H-02 | Strukturę helikalną TIMDR można opisać reprezentacją strunową | Otwarta | Jawna definicja i mapa |
| H-03 | Pole i struna mogą być powiązane przez transformację zachowującą określone niezmienniki | Otwarta | Konstrukcja i test rekonstrukcji |
| H-04 | Przejścia między reprezentacjami mogą zachować wystarczającą informację do odwracalnego przetwarzania | Otwarta | Twierdzenie lub wyniki formalne/numeryczne |
| H-05 | Reprezentacje mogą wnieść wartość do architektury kryptograficznej | Spekulatywna | Analiza bezpieczeństwa i porównanie z baseline |
| H-06 | TIMDR może sterować ewolucją stanu kluczowego | Spekulatywna | Protokół, model zagrożeń, testy i niezależny przegląd |

Żadna z hipotez H-01–H-06 nie jest w tej wersji uznana za potwierdzoną.

## 7. Decyzje architektoniczne

- Główne postępy teoretyczne zapisujemy w GIA-TIMDR.
- HELIX-LOCK pozostaje projektem aplikacyjnym i laboratorium integracyjnym.
- Nie uzależniamy badań od AES ani nie zakładamy, że należy go zastąpić.
- Nie tworzymy jeszcze nowego szyfru.
- Nie redukujemy helisy do licznika epok ani skrótu fazy.
- Nie utożsamiamy pola i struny bez formalnej mapy.
- Najpierw badamy matematykę i zachowanie informacji, potem zastosowania.

## 8. Stan prac i następny krok

**Stan na 2026-11-09:**
- Ustalono, że głównym miejscem zapisu teorii i postępu ma być repozytorium GIA-TIMDR.
- Zidentyfikowano istniejący Chronoprocess jako orkiestrację trzech niezależnych projekcji M/S, G i K.
- Przejrzano ograniczony model fazowy obecnej gałęzi K.
- Wskazano helisę, pole i strunę jako kierunki reprezentacji do zbadania.
- Nie przeprowadzono jeszcze pełnego audytu wszystkich repozytoriów ani formalnej definicji transformacji helisa–pole–struna.
- Nie uzyskano żadnego wyniku potwierdzającego przydatność kryptograficzną tych reprezentacji.

**Najbliższe zadanie:** wykonać inwentaryzację istniejących definicji helisy w GIA-TIMDR oraz repozytoriach siostrzanych. Nie projektować jeszcze transformatora ani szyfru. Każdy znaleziony wzór i moduł należy sklasyfikować jako definicję, implementację, eksperyment lub wizualizację.

---

## Dziennik zmian

- **2026-11-09 / v0.1:** utworzono program badań; ustalono GIA-TIMDR jako kanoniczne repozytorium postępu; oddzielono teorię od implementacji HELIX-LOCK; zapisano otwarte hipotezy helisa–pole–struna i warunki przejścia do badań kryptograficznych.


## 9. Inwentaryzacja źródeł — pierwszy przebieg (2026-11-09)

Przeszukano strukturę plików repozytorium GIA-TIMDR oraz wybrane, bezpośrednio powiązane repozytoria siostrzane. Jest to **pierwszy przebieg inwentaryzacji**, a nie pełny audyt wszystkich 72 repozytoriów. Wyniki poniżej rozróżniają definicje, implementacje i eksperymenty.

### 9.1. GIA-TIMDR

| Źródło | Rodzaj | Co wnosi | Ograniczenie / uwaga |
|---|---|---|---|
| `docs/geometry/TIMDR_Trefoil_FrenetTorsion.md` | dokument + raport eksperymentu | Model krzywej trefoil, krzywizna i torsja Freneta-Serreta, lokalne deformacje węzłów, rezonans kanałów | Test syntetyczny konkretnej krzywej; nie jest szyfrem ani ogólną definicją helisy TIMDR |
| `core/trefoil_frenet_torsion.py` | implementacja numeryczna | Krzywizna/torsja z próbek, deformacje Gaussowskie, kanały detekcji i koincydencja | Implementacja diagnostyczna; nie definiuje transformacji danych ani kryptografii |
| `docs/theory/TIMDR_Twists.md` | indeks/specyfikacja pojęć | Rozdziela co najmniej siedem formalnie różnych znaczeń „skrętu” | Konieczne źródło kontroli terminologii; nie utożsamia torsji krzywej ze skrętem topologicznym |
| `docs/theory/Model_T_Field_Theory.md` | teoria pola | Kandydat na formalizację pola w ekosystemie | Wymaga osobnego przeglądu równań, dziedziny i statusu twierdzeń przed użyciem w mapie helisa→pole |
| `docs/geometry/tourosomobius.md` | notacja pojęciowa | Potrójny Tourosomobius, hybryda torus+Möbius+helisa | Sam dokument opisuje ją jako koncepcję bez kompletnej dziedziny, przeciwdziedziny, dowodu, kodu i testów |

**Wniosek GIA:** istnieje konkretny, policzalny model trefoil oraz odrębne pojęcia skrętu. Nie znaleziono podstaw, by traktować trefoil jako uniwersalną helisę TIMDR albo utożsamiać jego torsję Freneta z innymi wielkościami `τ`.

### 9.2. TIMDR-Math-Formalism

| Źródło | Rodzaj | Co wnosi | Ograniczenie / uwaga |
|---|---|---|---|
| `docs/theory/GS_Matrix_Helical_Coupling_DRAFT.md` | szkic modelu | Konstrukcja sprzężenia K↔Θ_bif i próg genuine rotation | Jawnie eksploracyjny toy model, nieaksjomatyzowany |
| `docs/theory/PREREG_HELICAL_SHAPE_ESTIMATOR.md` | prerejestracja + protokół | Test estymacji parametrów helikalnego kształtu z szumem | Test odzyskiwania parametrów znanego modelu, nie dowód, że realne dane mają taki kształt |
| `docs/theory/RESULT_HELICAL_COUPLING_SCOPE.md` | raport wyniku | Wykazuje ograniczony zakres: binarna klasyfikacja obecności rotacji była obiecująca, dokładna estymacja Re(λ) nie przeszła kryterium | Wynik opisowy na ograniczonych danych; brak podstaw do uogólnienia kryptograficznego |

**Wniosek Math-Formalism:** istnieje kandydat na opis helikalnego sprzężenia i procedura estymacji kształtu. Wynik jest asymetryczny: klasyfikacja obecności rotacji wypada lepiej niż odzyskiwanie dokładnego tempa obwiedni. Nie wolno przenosić jakościowego wyniku do twierdzeń o bezpieczeństwie.

### 9.3. TIMDR-META-DYNAMICS

| Źródło | Rodzaj | Co wnosi | Ograniczenie / uwaga |
|---|---|---|---|
| `models/evolution_helix.py` | model ewolucji | Klasyfikuje cykl życia helisy jako narodziny/stabilizacja/rozpad na podstawie `MetaState.tau` | Progi 0.2 i 1.0 są arbitralne i wymagają kalibracji |
| `models/evolution_field.py` | model pola | Generuje serię M-stanów z kolejnych S-stanów | To ewolucja globalnego pola w API tego repo; nie jest jeszcze mapą pola z krzywej helikalnej |
| `analysis/meta_torsion.py` | analiza geometryczna | Liczy krzywiznę i torsję trajektorii `(Λ, τ, ρ)` | Jawnie odróżnia geometryczną torsję od wejściowego `MetaState.tau`; wymaga równomiernego dt i wygładzania |
| `test_field_torsion_vs_tau.py` | test korelacyjny | Sprawdza korelację geometrycznej torsji z wejściowym τ | Dane demo syntetyczne; wynik nie jest dowodem tożsamości tych wielkości |

**Wniosek META-DYNAMICS:** w repozytorium występują co najmniej trzy różne sensy „helisy/pola/torsji”. Należy zachować ich rozdzielenie. Szczególnie `MetaState.tau` nie jest torsją Freneta-Serreta.

### 9.4. Pozostałe znalezione tropy — wymagają otwarcia i oceny

- `Helix-Astro/helix_spectrum.py` i `Helix-Astro/test_helix.py`: helikalny model widmowy; nie oceniono jeszcze jego równań ani statusu.
- `FIELDCORE/src/fieldcore.py`: implementacja pola; nie oceniono jeszcze relacji z helisą TIMDR.
- `THE_TIMDR_Hyperflow_Engine/the_geo_pro_4d.py`: wskazywany przez dokumentację jako implementacja geometrii 3D/4D z krzywizną i torsją; repozytorium i kod wymagają osobnego przeglądu.
- `TIMDR-Geometry-Formalism`: w spisie plików nie znaleziono nazw zawierających helix/helical/spiral/strun/torsion/trefoil/twist; nie wyklucza to treści ukrytej pod innymi nazwami.
- `TIMDR-Time-Formalism` i `TIMDR-Modal-Formalism`: brak nazw plików wskazujących wprost na helisę; wcześniej sprawdzone Chronoprocess i phase_sync pozostają istotne jako źródła niezależnych projekcji i modelu fazowego.

### 9.5. Wstępna mapa pojęć — nie utożsamiać

| Nazwa | Obiekt matematyczny | Status w przeglądzie |
|---|---|---|
| Helisa / krzywa helikalna | Krzywa parametryczna w przestrzeni | Wymaga wskazania konkretnej definicji TIMDR |
| Trefoil | Zamknięta krzywa węzłowa | Implementacja i test syntetyczny w GIA |
| Torsja Freneta-Serreta | Wielkość geometryczna krzywej | Zaimplementowana dla trefoil i trajektorii meta |
| Skręt topologiczny τ | Zdarzenie/parametr rodziny deformowanych powierzchni | Odrębna definicja w TIMDR_Twists |
| Helical coupling K↔Θ_bif | Eksploracyjny model sprzężenia | Wynik o ograniczonym zakresie |
| Meta field (Λ, τ, ρ) | Trajektoria stanu w R³ | Liczona geometrycznie; nie jest automatycznie polem przestrzennym |
| Pole TIMDR | Wymaga określenia typu i przestrzeni definicji | Kandydat do formalizacji |
| Struna | Nieustalony obiekt modelowy | Hipoteza otwarta, brak formalnej definicji znalezionej w tym przebiegu |

## 10. Aktualizacja priorytetów po inwentaryzacji

Nie rozpoczynać jeszcze implementacji transformatora ani szyfru. Następny krok to pogłębiony audyt źródeł z sekcji 9.4 oraz zebranie konkretnych definicji parametrycznych helisy z repozytoriów siostrzanych.

Kolejność:
1. Otworzyć `tourosomobius.md`, `Model_T_Field_Theory.md` oraz źródła teorii pola i sprawdzić, czy istnieje formalna mapa z krzywej do pola.
2. Otworzyć `Helix-Astro/helix_spectrum.py` i jego testy; sklasyfikować model widmowy.
3. Otworzyć `FIELDCORE/src/fieldcore.py` i określić, czy jest to pole skalarne/wektorowe/inny obiekt oraz jakie ma wejścia/wyjścia.
4. Otworzyć `THE_TIMDR_Hyperflow_Engine/the_geo_pro_4d.py` i porównać definicje helisy, krzywizny i torsji z GIA.
5. Dopiero po tych krokach zdefiniować kandydackie mapy helisa→pole i helisa→struna.

**Nie wolno nazywać „struną” zwykłej krzywej parametrycznej bez dodatkowej struktury.** Trzeba określić, jakie stopnie swobody lub pola wewnętrzne odróżniają model strunowy od samej krzywej.

## 11. Dziennik zmian — dopisek 2026-11-09

- Wykonano pierwszy przebieg inwentaryzacji plików w GIA-TIMDR oraz wybranych repozytoriach siostrzanych.
- Znaleziono konkretne źródła: trefoil/Frenet torsion, siedem rozróżnień pojęcia skrętu, GS-Matrix helical coupling, estymator kształtu helikalnego, ewolucję helisy i geometrię trajektorii pola meta.
- Wykryto ważne ograniczenia: część modeli jest eksperymentalna, część używa arbitralnych progów, a część wyników opiera się na danych syntetycznych.
- Ustalono, że pełna inwentaryzacja wszystkich repozytoriów siostrzanych pozostaje otwarta.


## 12. Pogłębiony przegląd kolejnych źródeł (2026-11-09)

### 12.1. `docs/geometry/tourosomobius.md` — ważna rozbieżność statusu

Dokument opisuje Potrójny Tourosomobius jako `(T × M × H)_{Λ,τ,ρ}`, przypisuje warstwom torus/Möbius/helisa role Λ–τ–ρ i deklaruje warunek boromejski oraz określone kąty/proporcje projekcji.

Jednocześnie dokument nie podaje konstrukcji osadzenia/zanurzenia, jawnych map między warstwami, definicji niezmiennika linkowania dla wskazanych obiektów ani dowodu warunku boromejskiego. Wcześniejszy raport `TIMDR_Trefoil_FrenetTorsion.md` określa Tourosomobius jako notację pojęciową bez kompletnej dziedziny/przeciwdziedziny i testów.

**Wniosek:** traktować Tourosomobius jako hipotezę/notację koncepcyjną, nie jako już zweryfikowany obiekt topologiczny. Sformułowania „formalny model” i „spełnia warunek boromejski” wymagają dowodu albo zmiany statusu na hipotezę.

### 12.2. `docs/theory/Model_T_Field_Theory.md` — pola TIMDR

Dokument wprowadza kandydackie pola informacyjne `I(x,t)`, modalne `M(x,t)=(f,φ,A)`, rezonansowe `R(x,t)` i emergentne `E(x,t)`, a następnie zapisuje Lagrangian i równania Eulera–Lagrange’a.

Nie znaleziono w tym dokumencie jawnej mapy:
- krzywa helikalna → pole TIMDR;
- helisa → konfiguracja pola modalnego;
- pole → obiekt strunowy.

Zapis `(∂μ M)(∂^μ M)` wymaga doprecyzowania, ponieważ M jest tu krotką parametrów modalnych, a nie zdefiniowanym polem o określonej przestrzeni wartości i metryce wewnętrznej. Także równania dla E wymagają jawnego uzasadnienia wynikającego z przyjętego Lagrangianu i definicji sprzężeń.

**Wniosek:** Model T jest kandydackim szkicem teorii pola, ale sam w sobie nie dostarcza transformatora helisa→pole. Przed wykorzystaniem wymaga pełnej definicji zmiennych, jednostek, metryki, symetrii, działania i wyprowadzenia równań.

### 12.3. `Helix-Astro/helix_spectrum.py` — helisa jako etykieta analizy widma

Kod przetwarza widmo: T0 zwraca intensywność, T1 normalizuje i wygładza, T2 liczy gradient; metryki to entropia histogramu, współczynnik zmienności i RMS pochodnej.

W tym module nazwa „Helix” nie oznacza reprezentacji krzywej helikalnej ani pola/struny. To narzędzie analizy widmowej z etykietą projektu. Testy dotyczą sygnału stałego, szumu i skoku.

**Wniosek:** nie jest to źródło geometrii helisy do transformacji.

### 12.4. `FIELDCORE/src/fieldcore.py` — status implementacji pola

Plik jest oznaczony jako „w przygotowaniu”, importuje modele pola/rezonansów/cząstek i pozwala przypisać model pola oraz topologię TorusMobius. W aktualnym pobranym pliku występuje też niepoprawne wcięcie przy `generuj_czastki`, więc nie można uznać go za działający, zwalidowany silnik pola bez dalszego sprawdzenia całego repozytorium.

Nie ma tu jawnej mapy helisa→pole ani transformacji strunowej.

**Wniosek:** FIELDCORE jest tropem architektonicznym, nie potwierdzoną implementacją reprezentacji polowej TIMDR.

### 12.5. `THE_TIMDR_Hyperflow_Engine/the_geo_pro_4d.py` — geometria krzywych 3D

Moduł liczy krzywiznę `κ`, torsję Freneta `τ` i helikalność `H=sqrt(κ²+τ²)` z kolejnych próbek krzywej 3D. Dokumentuje także istotny problem: potrójne różnicowanie surowych, zaszumionych próbek wzmacnia szum; wskazuje na potrzebę wygładzania przed różniczkowaniem.

To użyteczne źródło do geometrii krzywych i analizy stabilności numerycznej, ale nie jest modelem pola ani struny. „Helikalność” H jest tu skalarem z krzywizny i torsji, a nie automatycznie nową reprezentacją obiektu.

### 12.6. Korekta mapy statusów

- **Zaimplementowane i testowane:** wybrane metryki krzywych (κ, τ, H), detekcja deformacji trefoil na danych syntetycznych, proste narzędzia analizy widma.
- **Eksploracyjne / ograniczone:** GS-Matrix helical coupling i estymacja parametrów modelu helikalnego.
- **Koncepcyjne / wymagające formalizacji:** Potrójny Tourosomobius jako obiekt Borromejski, mapy helisa–pole–struna.
- **Niepotwierdzone:** odwracalny transformator helisa→pole, helisa→struna, pole↔struna oraz jakakolwiek korzyść kryptograficzna.



## 13. Kanoniczny katalog właściwości i wrażliwości

Na potrzeby odtwarzalności utworzono osobny dokument:
`docs/geometry/HELIX_SENSITIVITY_REPRODUCIBILITY.md`.

Jest to obowiązkowy rejestr właściwości, parametrów, wrażliwości, ograniczeń numerycznych, warunków eksperymentów i manifestów odtwarzalności. Rozróżnia wyniki zmierzone od definicji, hipotez i niewiadomych. Każdy kolejny eksperyment helikalny ma aktualizować ten katalog oraz wskazywać commit, kod, test, parametry i dane surowe.

**Zasada:** nie twierdzimy, że „wszystkie wrażliwości są już poznane”. Zapisujemy wszystkie zidentyfikowane czynniki i systematycznie mierzymy ich wpływ, zachowując również wyniki negatywne.


## 14. Geneza sygnału i warunki brzegowe węzła trójhelikalnego

Nowy dokument formalizacyjny: [TRIANGLE_HELIX_NODE_BOUNDARY_CONDITIONS.md](../geometry/TRIANGLE_HELIX_NODE_BOUNDARY_CONDITIONS.md). Zapisuje jako hipotezy robocze ciąg trajektoria trójkąta → redukcja → węzeł trójhelikalny, rolę osi i punktów kardynalnych, możliwe znaczenia redukcji czterowęzła do trójwęzła oraz macierz warunków brzegowych. Dokument rozdziela torsję Freneta-Serreta, skręt pasma, writhe, linking i fazę modalną. Nie uznaje jeszcze żadnej mapy redukcji za dowiedzioną.


## 15. Trop chemiczno-jądrowy z archiwum TRM (2026-11-09)

Odnaleziono bezpośrednio powiązany materiał w repozytorium `jbackk-lang/TIMDR-Concept-Archive`, katalog `Topological-Reduction-Model-TRM/physics/`:

- `element-stability.md` — szkic efektywnego skrętu jądra `τ_nuc=f(Z,N)`, w najprostszym wariancie `α|N−Z|+βZ`; proponuje związek z energią wiązania na nukleon i tempem rozpadu.
- `decay-series.md` — serie uranowa, torowa i neptunowa jako „drabiny redukcji” kończące się stabilnymi izotopami ołowiu.
- `leptons.md` — analogia redukcyjna `τ→μ→e`.
- `cosmic_time_in_particle.md` — hipoteza łączenia czasu życia cząstek z globalnym parametrem τ.
- `examples/particle-to-biology.md` — zestawienie analogii `U-238→Pb-206`, `τ→μ→e` i przemian biologicznych.
- `core/twist-reduction-law.md` oraz `math/reduction-equations.md` — ogólne prawo `R=kτ^n` i szkic dynamiki redukcji informacji.

### 15.1. Dlaczego to może pomóc w badaniu węzła i redukcji

Najbardziej użyteczny trop to nie analogia chemiczna sama w sobie, lecz **jawny łańcuch przejść między stanami**. W szeregu rozpadu każdy nuklid ma stan opisany co najmniej przez ((Z,N)), a przejścia zmieniają te liczby według typu rozpadu. Można więc badać:
- graf stanów i skierowanych przejść;
- węzły rozgałęzień (np. konkurujące kanały rozpadu);
- stany końcowe / stabilne;
- niezmienniki i wielkości monotoniczne;
- warunki brzegowe łańcucha i prawdopodobieństwa przejść.

To może dostarczyć formalnego języka do sprawdzenia, czy „redukcja 4→3” w modelu helikalnym oznacza redukcję liczby niezależnych stanów, kontrakcję grafu, projekcję obserwacji czy rzeczywistą zmianę topologii. Nie dowodzi jednak, że proces jądrowy i postulowana geometria helisy są tym samym mechanizmem.

### 15.2. Krytyczne rozróżnienie: tablica okresowa a szeregi rozpadu

Nie znaleziono w tym przeglądzie odrębnego repozytorium wyprowadzającego układ okresowy pierwiastków jako całość z redukcji TIMDR. Znaleziony materiał dotyczy przede wszystkim **stabilności jąder i szeregów rozpadu**, a nie wyprowadzenia okresowości chemicznej z konfiguracji elektronowych.

W fizyce jądrowej stan nuklidu opisuje ((Z,N)); rozpad α zmienia ((Z,N)	o(Z-2,N-2)), rozpad β⁻ ((Z,N)	o(Z+1,N-1)), a β⁺ / wychwyt elektronu ((Z,N)	o(Z-1,N+1)). Są to reguły bilansu liczby protonów i neutronów. Łańcuch U-238→Pb-206 ma wiele etapów i rozgałęzień, więc nie wolno przedstawiać go jako prostego, jednorodnego skalowania pojedynczego τ bez walidacji.

### 15.3. Status naukowy równań TRM

Równania w `element-stability.md` są hipotezami modelowymi, nie wyprowadzonym prawem jądrowym:
- `τ_nuc=α|N−Z|+βZ` nie uwzględnia samodzielnie parowania nukleonów, efektów powłokowych, deformacji jądra ani szczegółów oddziaływań;
- `τ_nuc∝1/(B/A)` nie jest uniwersalnym prawem fizycznym;
- `λ=λ₀τ^m` wymaga kalibracji osobno dla kanałów rozpadu i nie wynika z samej definicji τ;
- `R=kτ^n` jest postulatem TRM, którego parametry i zdolność predykcyjna wymagają testu na danych izotopowych.

Dodatkowo `cosmic_time_in_particle.md` zawiera mocną hipotezę o globalnym czasie kosmicznym zapisanym w czasie życia cząstek, ale w znalezionym pliku nie ma wyprowadzenia ani testu rozstrzygającego. Nie traktować jej jako ustalonego faktu.

### 15.4. Nowy kierunek eksperymentu — graf redukcji nuklidów

Zalecany test porównawczy:
1. Zbudować graf nuklidów z węzłami ((Z,N)) i skierowanymi krawędziami kanałów α, β⁻, β⁺ / EC oraz rozgałęzień.
2. Oznaczyć stabilne nuklidy jako stany końcowe, a niestabilne jako stany przejściowe.
3. Dodać dane empiryczne: typ rozpadu, energię, okres półtrwania, rozgałęzienia i niepewności.
4. Dopiero potem obliczyć kandydackie `τ_nuc` i `R`, dopasować parametry na zbiorze treningowym i sprawdzić predykcję na odłożonych izotopach.
5. Porównać z prostymi baseline'ami: odległość od doliny stabilności, parzystość Z/N, liczby magiczne i znane modele jądrowe.
6. Zarejestrować, czy redukcja jest monotoniczna, czy występują cykle/rozgałęzienia i ile stanów niezależnych rzeczywiście pozostaje.

**Wniosek:** archiwum zawiera wartościowy trop do formalizacji redukcji jako grafu przejść stanów. To może pomóc w analizie trajektorii trójkąta i hipotezy 4→3, ale analogia musi zostać przetestowana, a nie przyjęta jako dowód.



## 16. Protokół eksperymentu NRG-01

Utworzono prerejestrację `docs/experiments/NRG-01_NUCLEAR_REDUCTION_GRAPH.md`. Dokument określa budowę grafu nuklidów z ocenionych danych, walidację reguł bilansu, pomiary rozgałęzień i stanów końcowych, trzy rozdzielne typy redukcji (iloraz stanów, kontrakcja grafu, projekcja obserwacyjna), test modelu `τ_nuc` względem baseline'ów oraz warunki dopuszczenia porównania z geometrią helisy.

**Status:** protokół zapisany; danych nuklidowych nie pobrano, grafu nie zbudowano, hipotez nie przetestowano. Czterech wierzchołków grafu nie utożsamiamy z czterowęzłem topologicznym.


## 17. NRG-01 — implementacja pobierania danych

W repozytorium dodano skrypt `experiments/nuclear_reduction/NRG-01/src/nrg01_build_graph.py`, testy jednostkowe i README. Skrypt korzysta z IAEA LiveChart API, zachowuje surowe CSV i SHA-256, a niejednoznaczne kanały pozostawia nierozwiązane. Szczegóły i ograniczenia w `docs/experiments/NRG-01_NUCLEAR_REDUCTION_GRAPH.md`.

**Uczciwy status:** implementacja jest zapisana; nie potwierdzono jeszcze jej uruchomienia na danych zdalnych ani przejścia testów. Następny raport musi zawierać rzeczywisty log uruchomienia i artefakty CSV/JSON, zanim zaczniemy interpretować graf.


## 18. Znak skrętu i hipoteza chiralności / antycząstki

Nowa uwaga badawcza: w modelu helisy należy zachowywać **podpisany znak skrętu** (lewy/prawy), nie redukować go do wartości bezwzględnej. Znak może być ważną cechą kardynalną geometrii i kandydatem na obserwablę chiralności.

Nie utożsamiać jednak ręczności geometrycznej z antycząstką. Trzeba rozdzielić torsję geometryczną, chiralność, heliczność, parzystość P i sprzężenie ładunkowe C. Odbicie P odwraca chiralność geometryczną, ale nie zamienia samo z siebie cząstki w antycząstkę. Szczególny związek heliczności neutrin i antyneutrin w oddziaływaniach słabych nie jest ogólną regułą dla wszystkich cząstek.

Szczegółowy protokół, definicję podpisanej torsji, kontrolę konwencji osi/parametryzacji oraz hipotezy falsyfikowalne H-CH0/H-CH1/H-CH2 zapisano w `docs/experiments/NRG-01_NUCLEAR_REDUCTION_GRAPH.md`, sekcja 13.

**Konsekwencja dla modelu helisy:** znak skrętu staje się obowiązkowym polem zapisu geometrii. Nie jest etykietą cząstka/antycząstka, dopóki nie zostanie wykazane niezależne mapowanie do C, P i CP.


## 19. Pierwszy wykonany przebieg NRG-01 i równoległy test ręczności

Raport rzeczywistego przebiegu zapisano w `docs/experiments/NRG-01_RUN_REPORT_2026-11-09.md`. GitHub Actions zakończył powodzeniem testy, pobieranie danych IAEA, analizę grafu i analityczny test podpisanej torsji helisy.

W pierwszym zbiorze: 48 nuklidów, 54 rozpoznane przejścia, 12 kanałów nierozstrzygniętych, 9 punktów rozgałęzienia, maksymalny stopień wyjściowy 2. Graf rozdzielił się na trzy komponenty osiągalne z trzech wybranych jąder startowych (U-238: 20, Th-232: 12, Np-237: 16 węzłów). Ten podział wynika z doboru trzech jąder startowych i nie dowodzi sam w sobie uniwersalnej trójdzielności.

Nie wykazano jeszcze rozgałęzienia trójkanałowego ani naturalnej redukcji 4→3. Dziewięć rozgałęzień binarnych zapisano jako kandydatów do porównania z punktami kardynalnymi na poziomie zdarzeń grafowych, nie jako ich geometryczne odpowiedniki.

Równoległy test idealnej helisy dla (R=1), (h=\pm0.5) uzyskał podpisane torsje (+0.4) i (-0.4). Potwierdza to, że redukcja do (|\tau_g|) usuwa rozróżnienie ręczności. To kontrola analityczna, nie pomiar geometrii TIMDR ani dowód relacji z antycząstkami.

**Nadrzędna reguła:** zachowywać znak torsji i skoku, orientację osi, fazę oraz kolejność punktów kardynalnych podczas każdej redukcji.


## 20. Audyt odpowiedniości 3 komponentów NRG-01 ↔ 3 gałęzie helisy

Wykonano audyt na rzeczywistym artefakcie NRG-01. Szczegóły: `docs/experiments/NRG-01_THREE_STRAND_CORRESPONDENCE_AUDIT_2026-11-09.md`.

Komponenty:
- Np-237: 16 węzłów, 18 krawędzi, 3 rozgałęzienia, 4 ścieżki źródło–terminal, najdłuższa ścieżka 12 krawędzi;
- U-238: 20 węzłów, 24 krawędzie, 5 rozgałęzień, 15 ścieżek, najdłuższa ścieżka 14 krawędzi;
- Th-232: 12 węzłów, 12 krawędzi, 1 rozgałęzienie, 2 ścieżki, najdłuższa ścieżka 10 krawędzi.

Wszystkie są DAG-ami w rozpoznanym podzbiorze, ale ich profile nie są równoważne. Istnieje sześć możliwych przypisań trzech komponentów do trzech nazwanych gałęzi; żadne nie jest wyróżnione, bo graf nie ma współrzędnych 3D, fazy, podpisanej torsji ani etykiet punktów kardynalnych. Każdy komponent ma rozgałęzienia, więc nie odpowiada bezpośrednio pojedynczej gładkiej, nie rozgałęziającej się krzywej.

Istniejący `core/trefoil_frenet_torsion.py` opisuje jedną zamkniętą krzywą z trzema lobami, a nie trzy niezależne helisy. Konstrukcja `Φ_G` z `TIMDR_Geometry_From_EventGraph.md` wymaga pozycji 3D i uporządkowania zdarzeń; nuklidowy graf NRG-01 nie dostarcza pozycji.

**Rozstrzygnięcie:** odpowiedniość 3 komponenty ↔ 3 gałęzie jest obecnie nieidentyfikowalna. Trzy komponenty wynikają z trzech wybranych jąder startowych; nie są niezależnym dowodem trójdzielności. Nie można wyprowadzić osi, punktów kardynalnych ani zachowania ręczności z samego grafu nuklidów. Nie wykazano redukcji 4→3.

Dodano kod audytu `experiments/nuclear_reduction/NRG-01/src/audit_three_strand_correspondence.py` oraz testy. Następny rozstrzygający eksperyment wymaga niezależnie określonych trzech krzywych (H_i(s)), wspólnej osi, faz, podpisanych torsji/skoków i punktów kardynalnych TIMDR oraz prerejestrowanego operatora mapowania bez dopasowywania współrzędnych nuklidów po fakcie.


Audyt odpowiedniości został także uruchomiony w CI: workflow [42563682586](https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42563682586) zakończył wszystkie kroki sukcesem. Artefakt `nrg01-parallel-tracks` (ID `13650283583`, SHA-256 `64ece60415e3768cfd485abb387892d58b3ede9cc272bc789fc355b39acd6068`) zawiera `three_strand_correspondence_audit.json` z profilem 3 komponentów i jawnym wynikiem nieidentyfikowalności mapowania.


## 21. Korekta modelu: operacja cięcia i ponownego łączenia 4→3 na kuli/jaju

Doprecyzowanie autora z 2026-11-09: redukcja nie polega na dopasowaniu trzech komponentów grafu do trzech helis. Należy wyciąć wybrany zamknięty obieg/łuk jednej helisy czterowęzłowej, po dwóch cięciach połączyć końce, a trzy pozostałe przebiegi dopasować do kolistości wspólnej bryły — kuli lub jaja. Formalizacja v0.1 i wyniki: `docs/geometry/FOUR_TO_THREE_HELIX_REDUCTION_ON_SPHERE_OR_EGG_v0.1.md`.

Model referencyjny wykorzystuje powierzchnię obrotową
(S(\theta,\phi)=(R\sin\theta(1+\epsilon\cos\theta)\cos\phi, R\sin\theta(1+\epsilon\cos\theta)\sin\phi, Rc\cos\theta)), gdzie kula ma ((c,\epsilon)=(1,0)), a jajowaty wariant kontrolny ((1.08,0.28)). Po redukcji trzy fazy są rozstawione co (120^\circ), zamiast (90^\circ). Lokalny odstęp zmienia się z promieniem równoleżnika (\rho(\theta)), więc jajowatość wpływa na profil lokalny, nawet gdy średnia po symetrycznym obiegu się znosi.

CI [42564365070](https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42564365070) zaliczył wszystkie testy i oba uruchomienia. W tym modelu mostek-kandydat ma długość 0.949232 na kuli i 0.919649 na jaju; zakres podpisanej torsji jest odpowiednio około ±0.959278 i ±1.619435. Torsja zmienia znak, więc obecna krzywa testowa nie spełnia jeszcze wymogu stałej orientacji skrętu. To jawny wynik negatywny, który musi wejść do następnej wersji modelu.

Ważne ograniczenie: obecny mostek jest interpolacją po parametrach powierzchni, nie geodezyjną; pozostałe trzy krzywe są fazowo przesuniętymi kopiami, a nie rozwiązaniem relaksacji sprężystej. Nie traktować v0.1 jako pełnego dowodu topologicznego ani fizycznego. Następny krok: geodezyjny/energetycznie optymalny mostek, relaksacja trzech krzywych przy warunkach brzegowych i jawny warunek zachowania znaku torsji.


## 22. Korekta zgodna z decyzją autora: ćwiartka fazowa i odpadnięcie całej helisy

Decyzja z 2026-11-09: przyjmujemy obrót fazowy jako miarę podziału kuli; jedna helisa odpada w całości, a nie przez usunięcie łuku. Cztery sektory mają po (90^\circ=2\pi/4); po redukcji trzy ocalałe mają dopasować się do (120^\circ=2\pi/3). Kula jest geometrią bazową. Jajo pozostaje wariantem kontrolnym, w którym porównujemy podział fazowy z podziałem według długości łuku, nie zakładając ich równoważności.

Nowy model v0.2: `experiments/helix_reduction/phase_locked_whole_strand_reduction.py`; specyfikacja: `docs/geometry/PHASE_QUARTER_WHOLE_STRAND_DETACHMENT_4_TO_3_v0.2.md`. Testy w `experiments/helix_reduction/tests/test_phase_locked_whole_strand_reduction.py`. Workflow uruchamia model na kuli i jaju.

**Kontrola krytyczna:** w idealnie symetrycznej kuli z czterema identycznymi helisami i symetrycznymi warunkami brzegowymi wszystkie cztery mają ten sam próg. Samo rozszerzanie/kurczenie nie wybierze jednej helisy. Jednoznaczne odpadnięcie wymaga fizycznego selektora: asymetrii, zaburzenia albo różnego warunku brzegowego. To musi wynikać z danych/teorii, nie z arbitralnego wskazania w kodzie.

Zachowanie ręczności w v0.2 jest kontrolowane przez znak kierunku fazowego (\sigma=\mathrm{sign}(d\phi/du)), osobno od podpisanej torsji Freneta. Model pozostaje kinematyczny: nie rozwiązuje jeszcze mechaniki odłączenia ani relaksacji energii trzech pozostałych helis.


CI v0.2: [run 42565302887](https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42565302887) zakończony sukcesem. Kula i jajo dały fazy 90°→120°, trzy ocalałe krzywe i zachowany znak obiegu. Długości każdej z trzech krzywych: 6.502990 (kula), 6.571573 (jajo). Próg pierwszego odpadnięcia nie jest jednoznaczny w żadnym wariancie, ponieważ model jest symetryczny.

**Istotne zastrzeżenie:** v0.2 usuwa jedną z czterech zamkniętych krzywych, ale nie modeluje jeszcze rzeczywistych połączeń między helisami. Następna wersja musi zbudować połączony graf przestrzenny z węzłami połączeń, łukami helikalnymi oraz dwiema zgodnymi granicami odcięcia określonymi przez globalną ćwiartkę fazy. Bez tego nie można twierdzić, że wykonano topologiczną redukcję czterowęzła do trójwęzła.


## 23. Zasadnicza korekta: redukcja jest indukowana DODANIEM elementu

Doprecyzowanie autora z 2026-11-09: dotychczasowy mechanizm redukcji przebiegał przez dodawanie elementów: trójkąt po dodaniu czwartego elementu staje się czworościanem; próba dodania następnego elementu do czworościanu wywołuje redukcję. To odwraca wcześniejsze założenie, że punktem wyjścia jest odpadnięcie jednej helisy podczas rozszerzania/kurczenia.

Nowa sekwencja robocza:
`triangle(3) -> add element 4 -> tetrahedron(4) -> add element 5 -> boundary violation -> reduction operator`.

Nie zakładamy jeszcze, czy piąty element zostaje odrzucony, czy jego dodanie reorganizuje cały układ do trzech niezależnych gałęzi. Wynik musi wynikać z jawnych warunków brzegowych i operatora redukcji, nie z ręcznego usunięcia helisy. Kula pozostaje geometrią bazową, faza jest miarą podziału; jajo jest wariantem kontrolnym.

Specyfikacja: `docs/geometry/ADDITION_INDUCED_REDUCTION_TRIANGLE_TETRAHEDRON_v0.1.md`. Wyniki wcześniejszego modelu 4→3 (v0.2) pozostają wyłącznie kontrolą kinematycznego rozstawienia faz 90°→120° i nie są dowodem mechanizmu redukcji przez dodanie elementu.


## 24. Sygnał naprzemienny + − + jako kandydat na źródło trójwęzła

Autor wskazał, że sygnał sinusoidalny przebiega kolejno: dodatnio, ujemnie, dodatnio. Hipoteza: trzy kolejne płaty sinusoidy o znakach `(+1,-1,+1)` mogą stanowić źródło konstrukcji trójwęzła. Znak środkowego płata jest informacją o odwróceniu orientacji i nie może zostać utracony przez wartość bezwzględną sygnału.

Nie utożsamiamy znaku płata z torsją Freneta, ręcznością topologiczną ani własnością antycząstki. Trzeba zdefiniować mapę sygnał→trzy gałęzie 3D, punkty przejścia przez zero, styczne, fazę i warunki domknięcia. Dopiero wtedy można stwierdzić, czy powstaje topologiczny trójwęzeł, czy tylko trójpłatowa trajektoria.

Specyfikacja: `docs/geometry/TRIPLE_NODE_FROM_ALTERNATING_SINUSOID_LOBES_v0.1.md`. Kandydatami na punkty kardynalne są ekstrema płatów, przejścia przez zero i punkty zmiany orientacji mapowania; ich status wymaga testu stabilności.


## 25. Wynik badania trzech płatów sinusoidy (+−+)

Wykonano audyt sygnału (s(t)=A\sin(\omega t)) na trzech kolejnych półokresach. Kod: `experiments/helix_reduction/three_lobe_signal_audit.py`; testy: `experiments/helix_reduction/tests/test_three_lobe_signal_audit.py`; raport: `docs/geometry/THREE_LOBE_SINUSOID_SIGNAL_AUDIT_v0.1.md`.

Wynik sygnałowy: znaki płatów (+,-,+), ekstrema (+A,-A,+A), cztery granice zerowe z naprzemiennymi znakami pochodnej (+,-,+,-). Wartość bezwzględna zmienia słowo znaków na (+,+,+), tracąc orientacyjną informację środkowego płata.

**Odkryta pułapka:** słowo (+,-,+) jest palindromiczne, więc samo nie rozróżnia kierunku przejścia. Odwrócenie parametryzacji zmienia znak kierunku/pochodnej, choć sekwencja polaryzacji płatów pozostaje taka sama. Ręczność wymaga dodatkowego kanału orientacji (kierunek parametru, styczna, rama lub faza przestrzenna); nie można jej wywnioskować z samych znaków.

CI [run pending from latest commit] uruchamia testy oraz zapis JSON. Wynik sygnałowy nie dowodzi jeszcze trójwęzła: potrzebny jest jawny operator osadzenia 3D, reguła połączeń i niezmiennik topologiczny. Nie utożsamiać trzech płatów z trzema strunami.


## 26. Krytyczna ocena wartości sygnału +−+: warunek szwu

Samo odzyskanie sekwencji (+,-,+) jest własnością definicyjną trzech półokresów sinusoidy i nie stanowi niezależnego potwierdzenia trójwęzła. Istotniejszy wynik audytu: dla trzech półokresów (s(t)=A\sin(\omega t)), (t\in[0,3\pi/\omega]), położenie skalarne domyka się (C^0), ale styczna nie: (s'(0)=+A\omega), (s'(3\pi/\omega)=-A\omega). To daje konkretną niezgodność warunku brzegowego, którą operator sygnał→helisa musi rozwiązać.

Kod audytu rozszerzono o pomiar zgodności (C^0/C^1); testy CI [42566568596](https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42566568596) przeszły. Warianty do porównania: odcinek przejściowy obracający styczną; sklejenie z odwróceniem orientacji (wraz z ramą); inny zakres fazy; albo trzy płaty jako fragment większego obiegu. Nie wybieramy jeszcze żadnego.

**Wniosek:** +−+ wnosi do analizy dopiero jako wymóg zachowania znaku środkowego płata i jako problem szwu (C^1). Samo słowo znaków nie daje topologii, kierunku obiegu ani ręczności.


## 27. Porównanie +−+ z podpisaną torsją istniejącego trefoila

Wykonano nowy audyt analityczny: `experiments/helix_reduction/trefoil_lobe_correspondence_audit.py`, testy: `experiments/helix_reduction/tests/test_trefoil_lobe_correspondence.py`, raport: `docs/geometry/SINUSOID_LOBES_VS_TREFOIL_TORSION_AUDIT_v0.1.md`.

Dla klasycznej krzywej trefoil z `core/trefoil_frenet_torsion.py` torsję obliczono z pochodnych analitycznych, a parametr podzielono na trzy równe sektory. Każdy sektor ma ten sam rozkład podpisanej torsji (trzykrotna symetria); w każdym występują zarówno wartości dodatnie, jak i ujemne. Średnia w każdym sektorze wynosi ok. +0.05343, udział dodatnich próbek ok. 57.71%, a zakres ok. [-0.22222,+0.35294].

**Wniosek:** nie ma mapowania „ujemny środkowy płat sygnału = ujemna torsja środkowego sektora trefoila”. Środkowy sektor klasycznego trefoila nie jest wyróżniony. To negatywny wynik dla prostego utożsamienia, nie obalenie możliwości mapowania sygnału na orientację ramy/framingu trzech helikalnych gałęzi.

CI dla audytu uruchomiono w [run 42566883725](https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42566883725); w chwili zapisu nadal trwa. Poprzednia próba workflow miała błędne literalne znaki nowej linii w YAML i została naprawiona w kolejnym commicie.


## 28. Korekta progu redukcji: piąty element mieści się, szósty wywołuje przeciążenie

Autor doprecyzował model 2026-11-09: piąty element nadal mieści się w 4-węźle; dopiero szósty rozpycha układ i ma wymusić reorganizację w trójwęzeł. To zastępuje wcześniejszą hipotezę, że już piąty element przekracza warunki brzegowe.

Sekwencja robocza:
`3 (triangle) -> +4 (tetrahedral / four-node state) -> +5 (still admissible in four-node) -> +6 (overload) -> global reorganization -> three-node`.

Warunek do zbadania:
`X5 ∈ A4` oraz `X6* ∉ A4`, gdzie A4 jest zbiorem konfiguracji dopuszczalnych dla 4-węzła. Nie wpisujemy progu 6 jako arbitralnego limitu licznika. Trzeba zdefiniować „element” (wierzchołek, ściana, krawędź, płat sygnału czy gałąź helikalna), metrykę i warunek brzegowy. Liczby wierzchołków, krawędzi, ścian, cykli grafu i gałęzi nie są zamienne.

Specyfikacja: `docs/geometry/SIXTH_ELEMENT_OVERLOAD_FOUR_NODE_TO_TREFOIL_v0.1.md`. Wcześniejszy dokument `ADDITION_INDUCED_REDUCTION_TRIANGLE_TETRAHEDRON_v0.1.md` pozostaje historią hipotezy 5→redukcja, ale jej próg jest superseded przez 6→przeciążenie.


### Doprecyzowanie nazewnictwa progu 5→6

„Pięciościan” i „sześciościan” oznaczają tu bryły o pięciu i sześciu ŚCIANACH (F=5 i F=6), a nie konstrukcje z pięcioma/sześcioma wierzchołkami. Czworościan ma F=4. Liczba ścian nie wyznacza jednoznacznie typu kombinatorycznego bryły: pięciościan i sześciościan mogą mieć różne grafy incydencji. Specyfikację skorygowano odpowiednio w `docs/geometry/SIXTH_ELEMENT_OVERLOAD_FOUR_NODE_TO_TREFOIL_v0.1.md`.

Właściwy test ma zatem porównać konkretny typ pięciościanu z konkretnym typem sześciościanu, zachowując jawne V, E, F i macierze incydencji. Hipoteza brzmi: konfiguracja F=5 mieści się w 4-węźle, a wybrana konfiguracja F=6 wymusza przeciążenie i reorganizację do trójwęzła. Nie wolno sprowadzać tego do samego licznika wierzchołków.


### Korekta semantyki elementu: moduły odbiciowe helisy, nie ściany wielościanu

Autor doprecyzował, że „elementy” to moduły generujące helisę — analogiczne do trójkąta w odbiciu. Interpretacja pięcio- i sześciościanu jako brył o F=5/F=6 ścianach była błędna i zostaje wycofana. W aktualnym modelu liczymy kolejne moduły helikalne: cztery tworzą konfigurację czterowęzłową, piąty nadal mieści się w jej warunkach brzegowych, a szósty ma wywołać konflikt / przeciążenie i reorganizację do trzech gałęzi.

Specyfikację skorygowano w `docs/geometry/SIXTH_ELEMENT_OVERLOAD_FOUR_NODE_TO_TREFOIL_v0.1.md`. Do dalszego modelowania należy jawnie zdefiniować trójkątny moduł bazowy, operator odbicia, orientację przed/po odbiciu, regułę sklejenia sąsiednich modułów, przyrost fazy/obrotu wokół osi oraz znak skrętu. Licznik modułów jest odrębny od liczby ścian, wierzchołków, gałęzi i cykli grafu.


### Nowa interpretacja mechanizmu helisy: obrót modułów, oś wewnętrzna, ograniczenie kuliste

Autor doprecyzował: obrót kolejnych modułów wymusza helisę; jej oś wewnętrzna sama ma przebieg spiralny. Otoczenie kuliste ogranicza geometrię i może wymuszać dodatkową krzywiznę / obrót ramy, przez co helisa może przejść w strukturę węzłową. Kula jest otoczeniem, nie osią.

Rozdzielamy: moduł trójkątny z orientacją odbicia, wewnętrzną oś (A(s)), ramę lokalną osi, fazę obrotu modułu, gałęzie helikalne i kulistą granicę. Obrót modułu, torsja osi, holonomia ramy i twist gałęzi są różnymi wielkościami. Kula nie tworzy węzła automatycznie: potrzebne są warunki domknięcia, sklejenia i test niezmiennika topologicznego.

Specyfikacja: `docs/geometry/ROTATION_INNER_SPIRAL_SPHERICAL_CONFINEMENT_TO_KNOT_v0.1.md`. Plan testów rozdziela helisę bez kuli, tę samą helisę pod ograniczeniem kulistym, próg 5→6 modułów oraz test topologiczny. Jajo pozostaje kontrolą asymetrii.


## 29. Audyt odejścia od źródłowych właściwości helisy — powrót do rdzenia

Audyt `docs/geometry/HELIX_SOURCE_PROPERTIES_DRIFT_AUDIT_2026-11-09.md` wykazał, że ostatnia linia „spiralna oś wewnętrzna + kula wymuszająca skręt + próg 5→6” nie wynika jeszcze z wcześniejszej definicji TIMDR. To hipotezy potomne, bez operatora generującego moduły i bez testu mechanizmu.

Pierwotny porządek z `docs/geometry/TRIANGLE_HELIX_NODE_BOUNDARY_CONDITIONS.md` pozostaje nadrzędny:
`trajektoria trójkąta → redukcja → węzeł trójhelikalny → oś i punkty kardynalne → sygnał`.
Oś jest elementem pierwotnym, ale jej źródłowa parametryzacja oraz punkty kardynalne pozostają nieustalone. Katalog `HELIX_SENSITIVITY_REPRODUCIBILITY.md` definiuje miary krzywej (pozycja, pochodne, krzywizna, torsja Freneta, kandydacka helikalność), lecz wiele wrażliwości pozostaje niezmierzonych.

Aksjomaty G2–G4 wskazują na trójkąt/asymetrię oraz zmianę pola normalnych powierzchni jako obiekty gałęzi geometrycznej; nie ustanawiają kuli jako źródła helisy. Obecne skrypty 4→3 są jawnie kinematycznymi modelami zadanych krzywych: wybierają/wycinają gałąź, budują mostek lub usuwają całą krzywą, a następnie ustawiają trzy pozostałe fazy na 120°. Nie wyprowadzają modułów z odbicia trójkąta, nie wyprowadzają wyboru gałęzi ani nie dowodzą węzła lub progu 5→6.

**Decyzja:** wstrzymać rozbudowę hipotezy „kula generuje spiralną oś i węzeł” do czasu odtworzenia operatora trójkąt→odbicie→obrót→sklejenie. Najpierw odtworzyć moduł źródłowy, z niego wyprowadzić oś i gałęzie, zmierzyć właściwości i dopiero później dodać kulę jako kontrolowany warunek. Zachować znak orientacji, fazę, kolejność zdarzeń i warunki brzegowe w każdej redukcji.


## 30. Dowodowe rozstrzygnięcie kąta czworościan → sześcian (problem otwarty)

Autor skorygował wcześniejsze przypomnienie: nie traktujemy 720° ani fazy 1–0–1 jako ustalonych danych. Kąt skrętu ma zostać rozstrzygnięty dowodem matematycznym.

Punkty odniesienia geometrii klasycznej:
- regularny czworościan: kąt dwuścienny wewnętrzny `acos(1/3) = 70.528779°`;
- kąt między zewnętrznymi normalnymi sąsiednich ścian: `acos(-1/3) = 109.471221°`;
- sześcian: kąt dwuścienny wewnętrzny `90°`;
- różnica wartości bezwzględnej względem 90° wynosi `19.471221°`, ale znak zależy od tego, czy porównujemy kąty wewnętrzne czy normalne zewnętrzne.

Te kąty brył nie są automatycznie kątem obrotu modułu, torsją osi, twistem ramy ani fazą helisy. Aby rozstrzygnąć mechanizm TIMDR, trzeba wyprowadzić zorientowane macierze przejścia moduł→moduł `R_n ∈ SO(3)` z geometrii wspólnej krawędzi, normalnych, odbicia i konwencji znaku, a następnie obliczyć holonomię `R_loop = R_0 R_1 ... R_(m-1)`. Obroty 3D nie muszą komutować, więc suma kątów nie zastępuje iloczynu macierzy.

Zapisana hipoteza autora: punkty kardynalne mogą odpowiadać zdarzeniom, w których kąt skrętu przekracza 90°. To wymaga definicji ciągłej funkcji kąta `theta(s)` i testu stabilności zdarzeń `theta(s)>90°`; nie utożsamiamy tego z kątem dwuściennym sześcianu.

Specyfikacja i plan dowodowy: `docs/geometry/TETRAHEDRON_CUBE_TWIST_ANGLE_PROOF_2026-11-09.md`. Do czasu wyprowadzenia operatora przejścia 90° pozostaje punktem odniesienia, a nie potwierdzonym parametrem helisy TIMDR.


## 31. Druga droga redukcji: π, idealna konstrukcja koła oraz √2 + √3

Autor przypomniał niezależną ścieżkę analizy redukcji przez analogię do π i idealnej konstrukcji koła z udziałem sumy pierwiastków √2 i √3. Ścieżka ta ma być zachowana równolegle do drogi trójkąt→bryły→węzeł; nie łączymy ich bez dowodu wspólnego operatora lub niezmiennika.

Kontrola liczbowa:
- √2 + √3 ≈ 3.1462643699419726;
- π ≈ 3.1415926535897932;
- różnica ≈ 0.0046717163521794 (względnie ok. 0.1487%).

Suma nie jest równa π: √2+√3 jest algebraiczna, a π przestępne. W geometrii koła jednostkowego √2 jest długością cięciwy kąta środkowego 90°, a √3 cięciwy 120°. To interesujące punkty konstrukcyjne, ale nie odtwarzają jeszcze źródłowej konstrukcji autora ani nie dowodzą reguły redukcji.

Dokument roboczy: `docs/geometry/PI_CIRCLE_SQRT2_SQRT3_REDUCTION_PATH_v0.1.md`. W przeszukanym drzewie bieżącego GIA-TIMDR nie odnaleziono jeszcze pierwotnego rysunku/notatki tej konstrukcji. Należy odzyskać dokładną kolejność konstrukcji, normalizację długości, rolę π (wartość, granica czy normalizacja) i operator redukcji. Nie utożsamiać sumy pierwiastków z π i nie zakładać, że to ta sama redukcja co redukcja grafowa.


### Korekta drugiej drogi redukcji: √2 i √3 jako odpowiednik mechanizmu π idealne → π rzeczywiste

Autor doprecyzował, że √2 i √3 nie miały być sumą przybliżającą π ani dwiema cięciwami do dodania. Miały być odpowiednikiem samego mechanizmu redukcji — analogicznie do przejścia od π idealnego (idealny okrąg / dokładna wielkość) do π rzeczywistego rozumianego jako skończona realizacja lub przybliżenie.

Ścieżka ta jest strukturalną analogią, nie równością liczbową. W matematyce π pozostaje jedną dokładną liczbą; „idealne → rzeczywiste” oznacza tu rozróżnienie obiektu idealnego i skończonej realizacji/pomiaru. Rola √2 i √3 jako stanów, parametrów lub elementów operatora redukcji wymaga odtworzenia ze źródłowej konstrukcji. Nie zakładać √2+√3=π (to fałsz).

Skorygowano dokument `docs/geometry/PI_CIRCLE_SQRT2_SQRT3_REDUCTION_PATH_v0.1.md`. Następne zadanie: zdefiniować obiekt idealny, realizowany, operator przejścia i zachowywany niezmiennik, a dopiero potem porównać tę analogię z redukcją helisy.


## 32. Dwa diagonalne poziomy konstrukcji helisy: √2 (2D) i √3 (3D)

Autor doprecyzował model: relacja trójkąt–kwadrat ma odpowiadać diagonalizacji płaskiej z przekątną jednostkowego kwadratu √2; relacja czworościan–sześcian ma odpowiadać diagonalizacji przestrzennej z przekątną jednostkowego sześcianu √3. Złożenie tych dwóch poziomów ma stanowić model konstrukcji helisy TIMDR.

Fakty matematyczne:
- kwadrat o boku a: przekątna (a\sqrt2);
- sześcian o krawędzi a: przekątna ściany (a\sqrt2), przekątna przestrzenna (a\sqrt3).

Ważne: √2 jest przekątną kwadratu, nie trójkąta; √3 jest przekątną przestrzenną sześcianu, nie czworościanu. „Trójkąt→kwadrat” i „czworościan→sześcian” są nazwami postulowanych przejść konstrukcyjnych, których operacje trzeba dopiero zdefiniować. Nie utożsamiać ich z automatyczną transformacją brył ani z samymi długościami.

Nowa specyfikacja: `docs/geometry/HELIX_CONSTRUCTION_SQRT2_SQRT3_DIAGONAL_TRANSITIONS_v0.1.md`. Kluczowym brakującym elementem jest operator składania dwóch poziomów: musi określić kolejność modułów, orientację odbić, fazę, macierze przejścia i regułę sklejenia. Dopiero jeśli z tego operatora wynika krzywa z osią i mierzalnym skrętem, można mówić o konstrukcji helisy. Zachować znak lewo-/prawoskrętny.


## 33. Zmiana priorytetu: tunel osi, warunki brzegowe i zakres skrętu

Autor ocenia, że relacje diagonalne √2/√3 wpływają na właściwości helisy co najwyżej szczątkowo. Pozostają pomocniczym tropem, nie głównym mechanizmem. Priorytet przechodzi na tunel osi i jego warunki brzegowe oraz ustalenie dopuszczalnego zakresu skrętu, ponieważ na granicy tego zakresu może zachodzić redukcja.

Nowa specyfikacja: `docs/geometry/AXIS_TUNNEL_BOUNDARY_CONDITIONS_TWIST_RANGE_REDUCTION_v0.1.md`.

Roboczo tunel osi to otoczenie krzywej osiowej z lokalnym przekrojem i ograniczeniami dopuszczalnych trajektorii. Należy wyprowadzić źródłową oś TIMDR, określić promień/przekrój tunelu, warunki wejścia/wyjścia, domknięcie, zgodność stycznych, ramy, fazy, orientacji i gałęzi. Mierzyć luz poprzeczny, regularność współrzędnych rurowych, krzywiznę osi i minimalne odległości nieprzyległych fragmentów.

Zakres skrętu traktować jako zorientowaną zmienną geometryczną (np. obrót przekroju względem transportowanej ramy), odrębną od torsji Freneta, skrętu powierzchniowego i τ TRM. Redukcja ma być testowana jako zdarzenie na granicy zbioru dopuszczalnych stanów, nie jako z góry zadany próg. Hipoteza 90° pozostaje testem: sprawdzić, czy przy tej wartości niezależnie zanika luz, powstaje kolizja/osobliwość albo naruszenie warunków szwu. Nie zakładać 90° jako aksjomatu.

Kolejność: źródłowa oś → tunel i przekrój → warunki brzegowe → zorientowany skręt i jego zakres → granica dopuszczalności / punkty kardynalne → operator redukcji → dopiero potem wpływ √2/√3, kuli i liczby modułów.


## 34. Wyniki przeszukania repozytoriów koncepcyjnych — tunel osi i granica redukcji

Przejrzano źródła z `TIMDR-Concept-Archive` (TRM-Geometry-Core, Topological-Reduction-Model-TRM, topologia-informacji) oraz `Helix-Lock` (granice parametrów, eksperyment tunelu/chiralności i testy).

Najważniejsze wskazówki:
1. TRM-Geometry-Core opiera się na kole oraz kwadracie wpisanym i opisanym jako dwóch granicach przekroju; archiwalna interpretacja przypisuje im Λ (struktura), τ (przejście) i ρ (defekt/różnica). Dla koła promienia r boki kwadratów wynoszą odpowiednio √2 r i 2r, więc stosunek granic to √2. To użyteczna para obwiedni przekroju, ale sama nie dowodzi skrętu.
2. Kula i wpisany sześcian dają niezależne ograniczenie przestrzenne (a=2r/\sqrt3). Nie jest to przekątna czworościanu.
3. Archiwalne TRM mówi o krytycznym τ, przeciążeniu/nasyceniu ρ i punkcie przejścia J. To sugeruje badać próg jako interakcję skrętu z dostępnym luzem/pojemnością, ale (R=k|τ|^n) i (|τ|>τ_{krit}) pozostają koncepcyjnymi postulatami, nie wyprowadzonym prawem geometrii helisy.
4. Helix-Lock doprecyzowuje: tunel jest geometryczny, sygnał jest mapowany na jego geometrię. Eksperyment syntetyczny wykazuje, że odbicie lustrzane zachowuje κ i odwraca znak torsji; faza sygnału musi respektować handedness. Aktualny G5 używa (|τ|), więc traci chiralność. Nie należy wstawiać ujemnej torsji bezpośrednio jako ujemnej wagi sprężyny.
5. Brak uniwersalnego liczbowego maksimum κ/τ bez skali, promienia i skoku. Obecny warunek dodatniej określoności G5 nie wyznacza górnego limitu (|τ|). Zatem próg redukcji musi wynikać z jawnego warunku geometrycznego/dynamicznego, nie z arbitralnej liczby.

Audyt i plan testów: `docs/geometry/CONCEPT_ARCHIVE_AUDIT_AXIS_TUNNEL_REDUCTION_2026-11-09.md`. Nowy priorytet: modelować przekrój tunelu przez granice wpisaną/opisaną, obwiednię przestrzenną i chiralną ramę; mierzyć luz, kolizje, holonomię, fazę i ρ oddzielnie. Punkt J należy zdefiniować jako wykrywalne zdarzenie przejścia po naruszeniu jawnego warunku brzegowego. Dopiero potem testować, czy występuje reorganizacja 4→3.


## 35. Priorytet nadrzędny: niezależna charakterystyka rzeczywistych właściwości helisy

Po korekcie kierunku badania celem nie jest ustalenie ani zmiana warunków redukcji, lecz poznanie rzeczywistych właściwości, ograniczeń i przydatności helisy. Redukcja, próg 90°, model π–√2–√3 i interpretacje TRM nie mogą być założeniami eksperymentu ani kryteriami sukcesu.

Nowy protokół: `docs/geometry/HELIX_CHARACTERIZATION_PROTOCOL_HC01_v0.1.md`.

Badanie rozdziela rodziny: helisa kołowa HC-01 (analityczny przypadek kontrolny), helisa zmiennoskokowa HC-02, stożkowa HC-03, helisa na zakrzywionej osi HC-04, krzywa zamknięta o lokalnej helikalności HC-05 oraz trefoil HC-06. Wyników trefoila nie wolno przenosić na helisę kołową.

Dla HC-01 punktem odniesienia są dokładne wzory:
`κ=a/(a²+h²)`, `τ_FS=h/(a²+h²)`, `τ_FS/κ=h/a`, `p=2πh`, `L_turn=2π√(a²+h²)`. Badania należy prowadzić również w parametrach bezwymiarowych, aby oddzielić zmianę kształtu od zmiany skali.

Karta pomiarowa obejmuje geometrię lokalną, ramę i tunel, chiralność, domknięcie/topologię oraz odporność numeryczną. Skręt raportować jako odrębne wielkości (torsja Freneta, obrót ramy, twist pasma, writhe/linking, faza), nigdy nie zastępować ich jednym symbolem. Zachowywać znak orientacji i wartości unwrapped.

Kolejność: walidacja wzorów analitycznych → testy niezmienniczości i zbieżności → sweep promienia/skoku/fazy/orientacji → porównanie rodzin → pomiary tunelu i odległości między zwojami → perturbacje i szum → dopiero na końcu ocena potencjalnych zastosowań względem geometrii kontrolnych.

Kryterium sukcesu to rzetelny, odtwarzalny atlas właściwości wraz z zakresem wiarygodności i ograniczeniami. Nie oczekujemy konkretnego progu ani redukcji. Wyniki mogą potwierdzić, zmienić lub obalić hipotezy TIMDR.


## 36. Korekta metodologii: nadrzędny obraz całości helisy TIMDR

Autor zwrócił uwagę, że nadmierne uszczegóławianie pojedynczych pomiarów grozi utratą ogólnego obrazu. Od tej chwili wszystkie eksperymenty HC-01, HC-01-TUBE i kolejne mają być podporządkowane jednej mapie właściwości i pytaniu o przydatność helisy jako całości. Nie mnożyć eksperymentów bez wskazania, jaką część ogólnego obrazu wyjaśniają.

Nadrzędne pytanie: **jakie możliwości i ograniczenia wynikają z geometrii helisy TIMDR jako całości oraz czy daje ona przewagę względem prostszych struktur w określonym zadaniu?**

Mapa badań ma cztery poziomy:
1. **Konstrukcja:** oś, tunel, przebieg helisy, przekrój, geometria przestrzenna i punkty charakterystyczne.
2. **Zachowanie:** skręt, faza, chiralność, ciągłość, stabilność, reakcja na zmianę parametrów i zaburzenia.
3. **Właściwości emergentne:** sprzężenia, synchronizacja, węzły, transport i zachowanie informacji; badać jako wynik, nie założenie.
4. **Przydatność:** konkretne zadania, ograniczenia, koszt geometryczny/obliczeniowy i porównanie z prostszymi geometriami.

Każdy wynik cząstkowy musi być przypisany do jednej z tych warstw oraz opisywać konsekwencję dla całości. Raportować syntetycznie: co ustalono, czego nie ustalono, jaki jest wpływ na model ogólny i jaki następny eksperyment ma największą wartość informacyjną.

Nie traktować redukcji 4→3, progu 90°, √2/√3 ani archiwalnych interpretacji TRM jako osi badań. Pozostają hipotezami wtórnymi, dopóki niezależna charakterystyka nie wykaże ich znaczenia.

**Zasada organizacyjna:** utrzymywać jeden nadrzędny model/diagram helisy i aktualizować go po każdym istotnym wyniku. Szczegółowe pomiary są podporządkowane mapie, nie odwrotnie. Nie tworzyć kolejnych wariantów dokumentów dla drobnych obserwacji, jeśli można je dopisać do wspólnego raportu HC.


## 37. Korekta zasadniczego pytania: wpływ informacji/sygnału na helisę i jej odpowiedź

Autor doprecyzował, że celem nie jest ponowne katalogowanie znanych właściwości helisy (m.in. pamięci, samonaprawy itd.). Przedmiotem badań jest **sprzężenie sygnał → helisa → odpowiedź**, w tym zależność odpowiedzi od historii wcześniejszych sygnałów.

Nadrzędne pytanie: jaki sygnał wprowadzony do helisy zmienia jej stan, jaką obserwowalną odpowiedź generuje helisa i czy identyczny sygnał daje inną odpowiedź zależnie od wcześniejszego pobudzenia?

Audyt istniejących gałęzi:
- G-Rezonans (core/geometric_resonance_operator.py) jest najbliższym istniejącym modelem pobudzenia i odpowiedzi: Mx''+Γx'+Kx=F(t), odpowiedź częstotliwościowa. Jest jednak liniowym modelem mechanicznym na zamkniętej krzywej, pobudzanym siłą harmoniczną; używa |τ|, więc gubi znak chiralności w sprzężeniu, i nie jest pełnym modelem informacji.
- K opisuje modalności (f,φ,A) i ich synchronizację; sam nie określa dynamiki geometrii helisy.
- M/S klasyfikuje sygnały czasowe; jego „rezonans” progowy nie jest ani rezonansem mechanicznym G, ani fazowym K.
- Model T szkicuje pola informacji/modalności/rezonansu/emergencji, ale nie dostarcza jeszcze zwalidowanego prawa sprzężenia sygnał–helisa.

Nowa synteza i program: docs/geometry/HELIX_SIGNAL_RESPONSE_COUPLING_v0.1.md.

Badanie ma ustalić mapę: (sygnał, stan początkowy, historia, geometria) → odpowiedź helisy. Wejście opisujemy amplitudą/energią, widmem, fazą, orientacją/chiralnością, obwiednią, modulacją i sekwencją. Wyjście mierzymy w kanałach geometrycznym, fazowym, widmowym, propagacyjnym i informacyjnym.

Rozdzielić bezwzględnie: reakcję na pobudzenie, pamięć (identyczne wejście → różne wyjście zależnie od historii), adaptację, samonaprawę (powrót do niezależnego stanu odniesienia) i odzyskanie informacji (payload/referencja odtworzona). Powrót częstotliwości nie dowodzi powrotu fazy, przebiegu ani informacji; zachować rygor protokołu PHASE_RECOVERY_VALIDATION_PROTOCOL.md.

Pierwszy test o najwyższej wartości informacyjnej: porównać odpowiedź na identyczny sygnał testowy dla helisy w stanie świeżym i po wcześniejszym kontrolowanym pobudzeniu, przy identycznych warunkach i kontrolach. To rozstrzyga, czy w badanym kanale występuje mierzalna zależność wejście–wyjście od historii.

Od tej chwili pomiary κ, τ, tunelu i chiralności są opisem stanu/zmiennymi objaśniającymi odpowiedź, a nie celem samym w sobie. Nie scalać znaczeń rezonansu G/K/M i nie zmieniać aksjomatów bez jawnego, testowalnego mostu.


## 38. Handoff i zasada wznowienia pracy

Utrwalono punkt wznowienia w `docs/handoffs/HANDOFF_HELIX_SIGNAL_RESPONSE_2026-11-09.md`. Obowiązuje nadrzędny cel: prześledzić rzeczywisty wpływ sygnału/informacji na helisę i jej odpowiedź, w tym zależność odpowiedzi od historii. Następnym krokiem jest audyt istniejącego przepływu sygnału przez moduły G/K/M/T i Helix-Lock — od reprezentacji wejścia, przez miejsce oddziaływania i zmianę stanu, do obserwowalnego wyjścia. Nie rozpoczynać nowych sweepów ani pobocznych analiz przed tym audytem. Wskazać jedną najważniejszą lukę i jeden minimalny test. W raportach rozróżniać kod zapisany, testy CI, eksperyment faktycznie uruchomiony i wniosek z wyniku.


## 39. Audyt przepływu sygnału — wynik i następny krok

Audyt źródeł zapisano w `docs/handoffs/AUDIT_SIGNAL_TO_HELIX_RESPONSE_PATH_2026-11-09.md`. Istniejące komponenty: graf zdarzeń→sygnał M/S (`trm_gia_projections.py`); modalności K (`phase_sync.py`); trzy obwiednie→trajektoria Γ→metryki κ/τ (`chrono_modal_geometry_bridge.py`); mechaniczny pierścień G i harmoniczna odpowiedź ustalona (`geometric_resonance_operator.py`); dopasowanie skalarnej częstotliwości s (`modal_self_repair.py`). Nie tworzą one jednak zintegrowanej pętli sygnał→stan helisy→odpowiedź→kolejny sygnał.

Najważniejsza luka to brak jawnego adaptera wejścia i dynamiki stanu: mapowania sygnału na kanał oddziaływania, aktualizacji stanu helisy i pomiaru odpowiedzi zależnej od historii. G obecnie przyjmuje wektor wymuszenia harmonicznego w dziedzinie częstotliwości i zwraca odpowiedź ustaloną; chrono-modalny most mierzy geometrię trajektorii obwiedni, ale nie zasila nią dynamicznie G. K ma stałe parametry modalności. G używa |τ|, więc nie zachowuje znaku chiralności w sprzężeniu.

Dalszy krok jest pojedynczy: zaprojektować minimalny test integracyjny na jednym istniejącym sygnale, z jawnym kanałem wymuszenia i jednostkami (albo oznaczoną normalizacją abstrakcyjną), porównujący odpowiedź na identyczny sygnał testowy dla stanu odniesienia i stanu po wcześniejszym pobudzeniu. Nie prowadzić teraz pobocznych sweepów geometrii ani redukcji. Nie nazywać testu fizycznym, jeśli mapowanie sygnału na wymuszenie nie ma uzasadnienia jednostkowego.
