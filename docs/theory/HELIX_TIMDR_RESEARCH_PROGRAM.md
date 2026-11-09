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
