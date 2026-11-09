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
