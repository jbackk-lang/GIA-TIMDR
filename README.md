# GIA‑and‑TIMDR / TRM

> **Uwaga: to jest model koncepcyjny / narzędzie do myślenia, nie teoria naukowa ani model empiryczny.**
> Poniższy opis nie przedstawia ustalonej, zweryfikowanej fizyki, biologii ani historii — to autorska metafora
> służąca do analizy struktur. Nie należy tego traktować jako dowodu na to, jak faktycznie zbudowana jest
> rzeczywistość, ani jako publikacji naukowej w rozumieniu peer review.

**Uniwersalny model pola, impulsów i informacji, wyprowadzony z pierwotnej asymetrii geometrycznej Trójkąta.**

TIMDR/TRM (Triangle Information Momentum Dynamics Resonance) to jednolita rama interpretacyjna łącząca geometrię, informację, dynamikę pól oraz topologię w jeden spójny, samoreplikujący się mechanizm. Niniejsze repozytorium stanowi matematyczny i logiczny fundament całego systemu — definiuje operatory, powierzchnie interpolujące, anomalie, rezonanse oraz modele emergencji we wszystkich skalach rzeczywistości.

---

## 📖 Cytowanie

Formalizacja gałęzi sygnałowej TIMDR (operatory progowe, rezonans jako
koincydencja, `Axioms_S_TIMDR_Signal.md`, `Resonance_M_Operator_Empiryczny.md`,
protokół `TIMDR-Math-Formalism` z realną walidacją na danych pogodowych)
ma osobny, wersjonowany zapis na Zenodo:

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22288541.svg)](https://doi.org/10.5281/zenodo.22288541)

> Kielich, J. S. (2026). *TIMDR Signal Formalization: Mathematical
> Operators, Axioms_S, Effect Size, and Reproducible Resonance
> Validation* (Version v1) [Zbiór danych]. Zenodo.
> https://doi.org/10.5281/zenodo.22288541

Zakres tego wydania to wyłącznie gałąź sygnałowa (M, S w `docs/theory/`
+ `TIMDR-Math-Formalism`) — nie obejmuje modelu geometrycznego trójkąta
(sekcje 1-9 poniżej) ani rezonansu modalnego (`Axioms_K_TIMDR.md`).

---

## 🌿 Trzy gałęzie TIMDR — mapa terenu

TIMDR to nie jedna teoria z trzema zastosowaniami — to trzy
**niezależne** konstrukcje matematyczne pod wspólną nazwą, z własnymi
obiektami, operatorami i aksjomatami. Współdzielenie słów ("rezonans",
"skręt") między nimi jest źródłem większości nieporozumień w tym
ekosystemie (pełne rozgraniczenie: `docs/GLOSSARY_EN_PL.md`) — dlatego
rozdzielone tu wprost, jedna gałąź na wiersz, zamiast zakładać, że
czytelnik sam to poskłada.

### 1. Gałąź sygnałowa — TIMDR-Math-Formalism (M, S)

**Obiekt:** `x: T→ℝᵈ`, `x∈ℓ^∞(T,ℝᵈ)`.
**Operatory:** anomalia, defekt, skręt sygnałowy (odwrócenie trendu),
rezonans M (koincydencja progowa + baseline dwumianowy), okno `W_k`/
partycja `P_k`, effect size (rank-biserial `r`), kontrola +/-, test
istotności (Mann-Whitney).
**Pliki:** `TIMDR-Math-Formalism/` (`timdr_formalism/pipeline.py`,
`docs/PROTOCOL.md`), `docs/theory/Axioms_S_TIMDR_Signal.md`,
`docs/theory/Resonance_M_Operator_Empiryczny.md`.
**To NIE jest:** geometria/krzywizna/normalne, rezonans modalny f/φ/A,
model trójkąta.

### 2. Gałąź geometryczna — TIMDR-Geometry (G)

**Obiekt:** powierzchnia `S⊂ℝ³`, normalna `n(p)`.
**Operatory:** skręt powierzchniowy `‖n(p+Δp)−n(p)‖`; krzywizna
dyskretna i operator kształtu (Weingarten) w wersji dyskretnej —
**wskazane jako kierunek, jeszcze niesformalizowane** (patrz
`Axioms_S_TIMDR_Signal.md`, sekcja "Pozostałe braki formalne").
**Pliki:** skręt powierzchniowy jest obecnie opisany w
`Resonance_M_Operator_Empiryczny.md` §6 — osobny katalog
`docs/theory/Geometry/` jeszcze nie istnieje, to raczej cel niż stan
obecny; model trójkąta to sekcje 1-9 tego README.
**To NIE jest:** sygnał czasowy, rezonans M, Axioms_S, rezonans modalny
f/φ/A.

### 3. Gałąź modalna — TIMDR-Modal (K)

**Obiekt:** moduły sygnału `(f, φ, A)`.
**Operatory:** rezonans modalny (wyrównanie częstotliwości i fazy), 10
aksjomatów modalnych.
**Pliki:** `docs/theory/Axioms_K_TIMDR.md`.
**To NIE jest:** sygnał `x:T→ℝᵈ`, testy statystyczne, skręt sygnałowy,
skręt powierzchniowy.

### Tabela porównawcza (kanoniczna)

| Gałąź | Domena | Operator rezonansu | Skręt | Aksjomaty | Status |
|---|---|---|---|---|---|
| Sygnałowa (M, S) | sygnały czasowe | M — progowy, baseline dwumianowy, zwalidowany empirycznie na danych Krakow_Centrum | sygnałowy (odwrócenie trendu) | Axioms_S | sformalizowana, testowana kodem |
| Geometryczna (G) | powierzchnie 3D | brak | powierzchniowy (normalne) | brak | wzór zdefiniowany, powiązanie z Weingartenem otwarte |
| Modalna (K) | moduły f/φ/A | K — modalny (wyrównanie f/φ) | brak | Axioms_K | zdefiniowana aksjomatycznie, bez empirycznej walidacji |

Żadna gałąź nie jest rozszerzeniem innej — każda ma własną domenę
matematyczną. Tam, gdzie dwie gałęzie używają tego samego słowa
("rezonans" w M i K, "skręt" w M i G), oznaczają **różne obiekty** —
nie różne poziomy tej samej rzeczy.

**Czwarty, wcześniejszy szkic (nie osobna gałąź):** sekcja "📘 TIMDR —
Pełny Model Operatora Topologicznej Zmiany Sygnału" dalej w tym README
definiuje własne, mniej sformalizowane `R` i `T` (koherencja
kierunkowa, przejście przez zero) — to poprzednik gałęzi sygnałowej
(M), nie czwarta niezależna konstrukcja. Rozgraniczenie wprost w tamtej
sekcji i w `docs/GLOSSARY_EN_PL.md`.

---

## Appendix: literatura 2021–2026 stosująca podobny wzorzec sygnałowy (zweryfikowane, koniec sierpnia 2026)

> **Metodologia tej sekcji:** każda pozycja poniżej została sprawdzona niezależnie (tytuł, czasopismo,
> data, treść metody) zamiast przyjęta z wcześniejszego zestawienia na wiarę. Z pierwotnej listy sześciu
> pozycji dwie zostały usunięte, bo nie udało się ich potwierdzić jako realnych, konkretnych publikacji
> pod podanym tytułem/czasopismem/datą ("IoT anomaly detection — IEEE IoT Journal, 2025" i "Crystal
> stability latent anomaly — Computational Materials Science, 5 września 2026" — najbliższa realna praca
> o zbliżonej tematyce, zespołu z Nagoya Institute of Technology, ma inny tytuł, inną datę publikacji
> (10 lutego 2026) i nie została potwierdzona jako opublikowana w Computational Materials Science).
> Pozostałe cztery pozycje są prawdziwe i poprawnie zacytowane, ale mapowanie ich metod na
> anomalia/defekt/skręt/rezonans poniżej jest interpretacją nałożoną z zewnątrz — żadna z tych prac
> nie używa ani nie zna terminologii TIMDR.

1. **CHEM-AD** — *Chemical Science* (Royal Society of Chemistry), 2026, tom 17, nr 16, s. 7967–7985,
   opublikowane 24 lutego 2026. Wykrywanie anomalii strukturalnych w MOF-ach (81 cech geometrycznych/
   chemicznych/topologicznych) przez autoencoder + błąd rekonstrukcji, z odległością Mahalanobisa i
   PCA jako dodatkową weryfikacją w przestrzeni embeddingu. Odpowiednik anomalii (błąd rekonstrukcji
   AE) jest tu trafny; odpowiednik "skrętu" dla PCA/Mahalanobisa jest naciągnięty — odległość
   Mahalanobisa to statyczna miara wielowymiarowego odchylenia, nie wielkość kierunkowa/trendowa,
   jaką skręt jest w TIMDR.
2. **Interference Detection** — *Sensors* (MDPI), 14 grudnia 2025, Technical University of Košice.
   Fuzja trzech (nie czterech) sygnałów: błąd rekonstrukcji PCA (globalna anomalia), Local Outlier
   Factor na mapach reszt (lokalna rzadkość/defekt), wariancja Monte Carlo jako niepewność
   epistemiczna modelu. Komponent "korelacja między kanałami → rezonans" NIE jest potwierdzony w
   opisie metody tej pracy — praca fuzuje trzy sygnały, nie cztery.
3. **"Smart anomaly detection in sensor systems: A multi-perspective review"** — *Information Fusion*
   (Elsevier), 2021. To szeroki przegląd metod wykrywania anomalii w systemach sensorowych (nie jedna
   nowa metoda) — mapowanie jego treści na cztery konkretne sygnały TIMDR to interpretacja narzucona
   z zewnątrz na ogólny przegląd, nie coś, co artykuł sam proponuje jako jedną spójną metodę.
4. **"Machine learning for anomaly detection in particle physics"** — *Reviews in Physics*, tom 12, 2024.
   Również przegląd (outlier detection + wykrywanie nadgęstości w danych zderzeń), nie jedna metoda z
   czterema wyraźnie zdefiniowanymi sygnałami — ta sama uwaga co przy pozycji 3.

**Uczciwy wniosek:** techniki użyte w tych pracach — błąd rekonstrukcji autoencodera, PCA (Hotelling,
1933), odległość Mahalanobisa (1936), Local Outlier Factor (Breunig i in., 2000), korelacja
międzykanałowa — są standardowymi, dobrze ugruntowanymi narzędziami statystyki/ML, o dekady starszymi
niż TIMDR jako projekt. Właściwy kierunek zależności jest odwrotny od sugerowanego w poprzedniej wersji
tej sekcji: to anomalia/defekt/skręt/rezonans w TIMDR są przeformułowaniem tych dużo starszych, ogólnych
pojęć zastosowanym do konkretnej domeny (grafu/sieci/pola), a nie odwrotnie — te prace nie "niezależnie
odkrywają wzorzec TIMDR, nie nazywając go", tylko używają narzędzi, które istniały na długo przed TIMDR.
Realna wartość tego zestawienia: pokazuje, że styl "połącz kilka niezależnych sygnałów odchylenia w jeden
werdykt" jest w literaturze uznanym, użytecznym podejściem — nie że TIMDR ma w tym pierwszeństwo.

## 0. Dokumentacja online
Odwiedź pełną dokumentację i interaktywne opisy układu:  
👉 [https://jbackk-lang.github.io/](https://jbackk-lang.github.io/)

![Diagram TRM / GIA / TIMDR](https://github.com/jbackk-lang/GIA-TIMDR/raw/main/diagram.png)

---

## 1. MODEL WYJŚCIOWY: ASYMETRIA TRÓJKĄTA I GENEZA IMPULSU

U podstaw TIMDR leży założenie, że cała dynamika wszechświata bierze się z geometrycznego wymuszenia. Najprostszą możliwą figurą zdolną do wygenerowania trwałej różnicy jest **trójkąt**.

```
[ Koło: Pełna Symetria ]             [ Prosta: Złamanie Symetrii ]
       A = B = C                                A ≠ B ≠ C
          ▲                                        │
          │                                        ▼
   (Stan idealny)                       (Pierwszy Impuls / Skręt)
```

### 1.1 Trójkąt w kole (Stan Idealny)
Trójkąt równoboczny wpisany w okrąg reprezentuje stan doskonałej symetrii:
$$\text{A} = \text{B} = \text{C}$$
W tym układzie nie istnieje żaden wyróżniony kierunek, brak jest gradientu potencjału, brak różnicy i brak skrętu. To stan czystej statyki.

### 1.2 Przeniesienie na prostą (Złamanie Symetrii)
W momencie rzutowania lub przeniesienia trójkąta z przestrzeni koła na prostą, symetria zostaje bezpowrotnie złamana. Środowisko wymusza zmianę: dwa ramiona układu „opadają” w inny sposób niż ramię trzecie.

### 1.3 Składanie i rozkładanie ramion (Mechanizm Impulsu)
Trójkąt w nowym układzie nie jest w stanie utrzymać swojej równoboczności. Przechodzi w trójkąt równoramienny lub różnoboczny, generując **pierwszą wymuszoną różnicę**. Zmiana geometrii rodzi napięcie — jest to **czysty impuls**.

### 1.4 Dynamiczny mechanizm przejścia boków
1. **Symetria pierwotna:** $\text{A} = \text{B} = \text{C}$ (Brak przepływu informacji).
2. **Zmiana układu odniesienia:** Przejście koło $\rightarrow$ prosta.
3. **Geometryczne wymuszenie:** Ramiona geometryczne nie mogą zachować identycznych proporcji.
4. **Impuls:** Pojawienie się minimalnej, mierzalnej różnicy między elementami układu.
5. **Kierunek i Skręt:** Różnica generuje wektor — układ zaczyna dążyć do kompensacji, rodząc ruch obrotowy wokół nowej osi.

> **Trójkąt jest pierwszym i ostatecznym silnikiem różnicy we Wszechświecie.**

### 1.5 Przykłady złamania symetrii w matematyce (analogie, nie dowód)

> **Zastrzeżenie:** poniższe dwanaście przykładów to prawdziwe, ustalone od dawna wyniki matematyczne
> (teoria mnogości, teoria miary, topologia, analiza funkcjonalna, teoria grafów, logika) — nie są to
> instancje mechanizmu TIMDR ani nie zostały wyprowadzone z asymetrii trójkąta. Zestawiam je tu jako
> **analogię ilustrującą wspólny kształt zjawiska**, o którym mówi Sekcja 1: intuicja słuszna w skali
> skończonej/lokalnej często pęka dokładnie na jakiejś granicy (nieskończoności, braku zwartości, braku
> mierzalności, granicy aksjomatów) — i za każdym razem to pęknięcie NIE jest chaosem, tylko punktem,
> w którym trzeba było zbudować precyzyjniejsze pojęcie po drugiej stronie granicy.

1. **Hotel Hilberta.** Symetria: "pełny hotel = brak miejsca". Pęka: hotel o ℵ₀ pokojach, wszystkie
   zajęte, wciąż może przyjąć nowego gościa (przesunięcie n→n+1) albo nieskończenie wielu nowych gości
   naraz (n→2n, zwalniając wszystkie nieparzyste pokoje). **Co z tego wynika:** dla zbiorów
   nieskończonych "rozmiar" nie jest już mierzony przez inkluzję (A⊂B ⇒ A mniejsze), tylko przez
   istnienie bijekcji — to zresztą definicja Dedekinda zbioru nieskończonego: zbiór jest nieskończony
   wtedy i tylko wtedy, gdy istnieje bijekcja między nim a jego właściwym podzbiorem.
2. **Paradoks Banacha–Tarskiego.** Symetria: kula 3D ma określoną objętość, zachowaną przez izometrie.
   Pęka: kulę można rozciąć na (minimalnie 5) kawałków i złożyć z nich dwie identyczne kopie oryginału,
   używając tylko obrotów i przesunięć. **Co z tego wynika:** to nie usterka geometrii, tylko cena
   Aksjomatu Wyboru — kawałki są z konieczności niemierzalne, nie da się ich "zobaczyć" ani skonstruować
   efektywnie. Wynik jest specyficzny dla wymiaru ≥3: na płaszczyźnie (2D) miara addytywna dla
   WSZYSTKICH podzbiorów istnieje (Banach, 1923) — paradoks nie zachodzi w 2D.
3. **Zbiory Vitaliego.** Symetria: "każdy podzbiór prostej ma miarę". Pęka: zbiór skonstruowany przez
   wybór jednego reprezentanta z każdej klasy abstrakcji R/Q (liczby różniące się o wymierną) nie ma
   miary Lebesgue'a — ani zerowej, ani dodatniej. **Co z tego wynika:** mierzalność nie jest
   automatyczna, tylko realnym ograniczeniem, i — co ciekawe — jest to znowu konsekwencja Aksjomatu
   Wyboru: w modelu Solovaya (ZF + DC, bez pełnego AC) WSZYSTKIE podzbiory R są mierzalne.
4. **Zbiór Cantora.** Symetria: "ciągłość/gęstość = brak dziur". Pęka: zbiór Cantora ma miarę zero
   (usuwa się z niego łącznie odcinek o długości 1), a mimo to ma moc continuum (tyle samo punktów co
   cała prosta), jest doskonały (każdy punkt jest punktem skupienia) i nigdzie gęsty. **Co z tego
   wynika:** "miara" (długość) i "moc" (liczność) to niezależne pojęcia rozmiaru — zbiór może być
   jednocześnie "duży" (nieprzeliczalny) i "mały" (miary zero).
5. **Paradoks Russella.** Symetria: "każda określona własność wyznacza zbiór". Pęka: zbiór wszystkich
   zbiorów, które nie zawierają same siebie, prowadzi do sprzeczności (R∈R ⟺ R∉R). **Co z tego
   wynika:** naiwna, nieograniczona abstrakcja zbioru jest sprzeczna — to odkrycie (1901) wymusiło
   przejście na aksjomatyczną teorię mnogości (ZFC), gdzie schemat wyróżniania pozwala wydzielać
   podzbiory tylko z już istniejących zbiorów, blokując samoodnoszące się konstrukcje typu R.
6. **Twierdzenie Banacha o punkcie stałym.** Symetria: "odwzorowanie ciągłe ma punkt stały". Pęka:
   kontrakcja (stała Lipschitza < 1) na przestrzeni zupełnej ma DOKŁADNIE JEDEN punkt stały,
   osiągalny przez iterację z dowolnego punktu startowego — ale izometria (stała Lipschitza = 1,
   dokładnie na granicy) może nie mieć punktu stałego wcale (np. przesunięcie na prostej). **Co z tego
   wynika:** istnienie punktu stałego jest zjawiskiem progowym, nie stopniowym — granica "<1 vs =1"
   jest jakościowa, nie tylko ilościowo słabsza.
7. **Nieskończone drzewa regularne (grafy Cayleya).** Symetria: "lokalna jednorodność = brak
   struktury globalnej". Pęka: nieskończone drzewo 3-regularne jest lokalnie identyczne w każdym
   wierzchołku (ten sam stopień wszędzie), a mimo to nie ma żadnych cykli, rośnie eksponencjalnie i
   ma brzeg w nieskończoności o mocy continuum. **Co z tego wynika:** jednorodność lokalna nie
   implikuje trywialności globalnej — czysto lokalna, jednostajna reguła może generować bogatą,
   nietrywialną strukturę globalną.
8. **Paradoks Galileusza.** Symetria: "część zbioru jest mniejsza niż całość". Pęka: odwzorowanie
   n↦n² jest bijekcją między liczbami naturalnymi a kwadratami — właściwym podzbiorem liczb
   naturalnych. **Co z tego wynika:** to historycznie ten sam fakt co Hotel Hilberta (Galileusz
   opisał go już w 1638 r., na długo przed Cantorem) — Galileusz uznał, że porównania
   większy/mniejszy/równy po prostu "nie stosują się" do nieskończoności; Cantor (XIX w.) nie
   poddał się w tym miejscu, tylko przedefiniował "tę samą liczność" przez istnienie bijekcji,
   zamieniając paradoks w twierdzenie (ℵ₀=ℵ₀).
9. **Miara Haara w przestrzeniach nieskończenie wymiarowych.** Symetria: "każda grupa topologiczna ma
   naturalną miarę niezmienniczą na przesunięcia". Pęka: twierdzenie o istnieniu miary Haara wymaga
   LOKALNEJ ZWARTOŚCI grupy — dla grup, które jej nie mają (np. nieskończenie wymiarowa przestrzeń
   Hilberta jako grupa addytywna), miara niezmiennicza na przesunięcia, przypisująca kulom skończoną,
   niezerową miarę, w ogóle nie istnieje. **Co z tego wynika:** "rozkład jednostajny" w nieskończonym
   wymiarze nie jest spójnym pojęciem — dlatego prawdopodobieństwo na przestrzeniach nieskończenie
   wymiarowych (np. miara Wienera) wymaga zupełnie innego aparatu niż "miara jednostajna".
10. **L² kontra L^∞ (ograniczoność).** Symetria: "całkowalna w kwadracie = ograniczona". Pęka:
    funkcja f(x)=x^(−1/4) na (0,1] jest nieograniczona (rozbiega do nieskończoności przy x→0), a mimo
    to należy do L² — jej całka z kwadratu (∫₀¹x^(−1/2)dx=2) jest skończona. **Co z tego wynika:**
    "rozmiar" funkcji mierzony całką (energia/norma L²) jest z gruntu innym pojęciem niż rozmiar
    mierzony punktowym ograniczeniem (norma L^∞) — funkcja może być lokalnie bardzo duża, a mimo to
    globalnie "mała" w sensie zagregowanym; to dlatego mechanika kwantowa używa L² (skończone
    prawdopodobieństwo całkowite), nie ograniczoności funkcji falowej.
11. **Niezależność hipotezy continuum.** Symetria: "każde pytanie matematyczne ma w danej aksjomatyce
    rozstrzygalną odpowiedź tak/nie". Pęka: Gödel (1940) pokazał, że hipotezy continuum (CH) nie da
    się OBALIĆ z aksjomatów ZFC, a Cohen (1963, metoda forsingu) pokazał, że nie da się jej też
    UDOWODNIĆ — CH jest NIEZALEŻNA od ZFC: istnieją modele ZFC, w których CH zachodzi, i takie, w
    których nie zachodzi. **Co z tego wynika:** nie każde sensowne pytanie matematyczne ma jednoznaczną
    odpowiedź względem danego, skądinąd wystarczającego systemu aksjomatów — "ile jest liczb
    rzeczywistych względem przeliczalnej nieskończoności" jest w ZFC realnie niedookreślone.
12. **Bazy ortonormalne w przestrzeniach Hilberta.** Symetria: "wymiar to jedna liczba". Pęka: w
    skończonym wymiarze każda baza ortonormalna ma tyle samo elementów (n), i to się uogólnia — każda
    dana przestrzeń Hilberta ma wszystkie bazy ortonormalne tej samej mocy — ale RÓŻNE przestrzenie
    Hilberta mogą mieć bazy różnej nieskończonej mocy: przestrzenie ośrodkowe (np. L²[0,1], ℓ²) mają
    bazę przeliczalną, nieośrodkowe wymagają bazy nieprzeliczalnej. **Co z tego wynika:** wymiar
    uogólnia się na nieskończoność jako niezmiennik kardynalny, ale przestaje być "jednym rodzajem
    nieskończoności" — powstaje cała hierarchia możliwych rozmiarów bazy, i właśnie dlatego większość
    praktycznej analizy (mechanika kwantowa, równania różniczkowe, analiza Fouriera) świadomie
    ogranicza się do przypadku ośrodkowego, bo tylko tam baza przeliczalna pozwala pisać rzeczy jako
    zbieżne szeregi.

**Wspólny wątek (analogia, nie wniosek matematyczny):** we wszystkich dwunastu przypadkach złamanie
symetrii nie kończy się chaosem — matematycy za każdym razem precyzyjnie zlokalizowali GDZIE i DLACZEGO
intuicja pęka (nieskończoność, brak zwartości, Aksjomat Wyboru, granica aksjomatyki) i zbudowali
dokładniejsze pojęcie po drugiej stronie tej granicy (moc zamiast inkluzji, miara zamiast "każdego
zbioru", niezależność zamiast jednego rozstrzygnięcia). To jest jedyny sens, w jakim te przykłady
"pasują" do Sekcji 1 — jako ilustracja wzorca "pęknięcie → nowa, precyzyjniejsza struktura", nie jako
formalny dowód mechanizmu trójkąta.

---

## 2. OD ANOMALII DO INFORMACJI

Gdy impuls wygenerowany przez asymetrię trójkąta napotyka barierę i nie ma drogi powrotu do stanu idealnej symetrii, różnica zostaje utrwalona.

* **Anomalia** to zamrożona w strukturze różnica; lokalny defekt topologiczny.
* Stanowi ona punkt nieodwracalny, wymuszający stały kierunek przepływu energii.
* W modelu TIMDR, **anomalia jest pierwotnym źródłem informacji**.

---

## 3. SKRĘT (TWIST) — JEDNOSTKA INFORMACJI

W systemie TIMDR informacja nie jest abstrakcyjnym ciągiem bitów — jest fizycznym **skrętem (Twist M)**, czyli orientacją zmiany geometrycznej, wyprowadzoną z asymetrii trójkąta.

* **Fluktuacja** = Minimalny, pojedynczy krok czasu (drżenie trójkąta).
* **Foton** = Uporządkowana, liniowa sekwencja fluktuacji.
* **Cząstka** = Zamknięty, stabilny geometrycznie skręt.
* **Pole** = Przestrzeń matematyczna zawierająca potencjalne konfiguracje skrętów.
* **Próżnia** = Stan tła posiadający minimalny, niezerowy skręt bazowy.

### 3.1 Hierarchia Emergencji Informacji
$$\text{Twist (M) [Orientacja]} \longrightarrow \text{Relacja } I(t) \text{ [Interakcja]} \longrightarrow \text{Informacja (R/E) [Stabilny wzorzec]}$$

* **Wstęga Möbiusa:** Odpowiada za jednostronność skrętu.
* **Podwójny Möbius ($M^2$):** Sytuacja, w której twist zaczyna oddziaływać na drugi twist. Generuje węzły relacyjne, interferencję, dyfrakcję oraz makroskopową emergencję materii.

---

## 4. STABILIZACJA: HELISA, OBIEGI I BOUNDARY‑MATTER

Utrwalony impuls musi zostać zorganizowany, by nie uległ rozproszeniu. Służą do tego struktury wyższego rzędu, będące bezpośrednią konsekwencją ewolucji asymetrycznego trójkąta.

```
Asymetria Trójkąta ──> Utrwalony Skręt (Twist) ──> Helisa (Zapis) ──> Obiegi (Struktura)
```

### 4.1 Helisa jako czasowy zapis różnicy
Helisa porządkuje i stabilizuje pierwotny impuls. Zamyka asymetrię w powtarzalny, spiralny obieg, tworząc podstawową komórkę strukturalną przestrzeni.

### 4.2 Obiegi wielokomórkowe
Z połączeń poszczególnych helis powstają zorganizowane sieci energetyczno-informacyjne (obiegi):
* Pojedyncze i wielokomórkowe,
* Otwarte, zamknięte oraz sprzężone rezonansowo.
* **Obieg to struktura, która trwale pamięta kierunek nadany przez pierwotną asymetrię.**

### 4.3 Język struktury: Boundary‑Matter
Boundary-Matter to natywny język pola (zastępujący klasyczny opis chemiczny i cząsteczkowy). Opisuje on zachowanie granic, interakcje między obiegami helis, przejścia fazowe oraz zachowanie defektów wewnątrz geometrii pola.

---

## 5. APARAT MATEMATYCZNY I OPERATORY POLA

Transformacja impulsu trójkąta w stabilne struktury opisywana jest przez triadę operatorów: **$\Lambda$ – $\tau$ – $\rho$**.

### 5.1 Główne operatory dynamiczne
* **$\Lambda$ (Struktura):** Bieżąca, statyczna konfiguracja geometryczna układu.
* **$\tau$ (Transformacja):** Ciągły operator zmiany układu odniesienia. Mierzy globalną gęstość skrętu w polu:
$$\tau = \nabla^2 S$$
* **$\rho$ (Defekt / Anomalia):** Operator ujawniający różnicę wyjściową. Wskazuje, gdzie asymetria trójkąta uniemożliwia powrót do stanu $A=B=C$.

### 5.2 Dyskretny operator skrętu ($J$)
Podczas gdy $\tau$ odpowiada za ciągłość pola, operator punktowy $J$ określa precyzyjną lokalizację zmian orientacji:
$$J = \frac{d\tau}{ds}$$

---

## 6. GEOMETRIA TOPOLOGICZNA: MOBIOSOTOURYS I TETROIDA

Model asymetrii operuje na dedykowanych powierzchniach, które bezkonfliktowo interpolują stany braku skrętu ze stanami osobliwymi.

### 6.1 Mobiosotourys
Powierzchnia łącząca właściwości torusa (brak skrętu), wstęgi Möbiusa (jednostronność) oraz tetroidy. Opisują ją równania parametryczne:
$$\begin{aligned}
x &= (R + r\cos(v + \tfrac{1}{2}u))\cos u \\
y &= (R + r\cos(v + \tfrac{1}{2}u))\sin u \\
z &= r\sin(v + \tfrac{1}{2}u)
\end{aligned}$$

### 6.2 Tetroida — Osobliwość Pola $\tau$
Tetroida to geometryczne domknięcie układu. Jest to trójścienna, całkowicie zamknięta warunkami brzegowymi, jednostronna bryła o maksymalnym nasyceniu operatorem $\tau$. Stanowi ona punkt przejścia dla różnicy potencjałów ($\Delta S$).

---

## 7. REZONANS, EMERGENCJA I SKALA CZASU globalnego (TRM)

### 7.1 Model Emergencji i Rezonansu Warstwowego
Emergencja strukturalna ($E$) jest bezpośrednią funkcją rezonansu ($R$) występującego na określonej topologii ($T$):
$$E = \mathcal{E}(R, T)$$
Dla wielowarstwowych układów skrętów $M = \{M_1, M_2, ..., M_k\}$, trwały, stabilny rezonans zachodzi na przecięciu ich zbiorów:
$$R = \bigcap_{j} R_j$$

### 7.2 Uniwersalne Spektrum Rezonansu (2 $\rightarrow$ 24 $\rightarrow$ 118)
Model TRM opisuje ewolucję i skalowanie struktur od elementarnej asymetrii do pełnej tablicy materii:
* **2** — Binarna baza skrętu (asymetria / brak asymetrii).
* **24** — Zamknięty, czysty cykl harmoniczny geometrii pola.
* **118** — Pełne, znane spektrum rezonansu materii (odzwierciedlone m.in. w układzie okresowym pierwiastków).

Współczynniki redukcyjne determinujące stabilność:
* $\frac{1}{12}$ — Stabilny, czysty stan informacyjny układu.
* $\frac{1}{59}$ — Stabilny stan w skali makro/kosmicznej.

### 7.3 Czas lokalny jako projekcja $\tau$ globalnego
Czas mierzony lokalnie w układzie fizycznym ($t_{\text{lokalne}}$) nie jest zmienną niezależną, lecz bezpośrednią projekcją stanu globalnego pola skrętu:
$$t_{\text{lokalne}} = f(\tau_{\text{globalne}})$$
Każda pojedyncza cząstka "wie" o wieku i stanie Wszechświata poprzez interakcję z polem $\tau$. Teza ta prowadzi do bezpośrednio falsyfikowalnych przewidywań w obszarach:
* Anomalii czasu połowicznego rozpadu izotopów.
* Zmian w czasie życia mionów w zależności od geometrii otaczającego pola.
* Dokładnego przebiegu szeregu promieniotwórczego uranu ($U\text{-}238 \rightarrow Pb\text{-}206$).

---

## 8. INTEGRACJA SYSTEMOWA (TIMDER ARCHITECTURE)

W ujęciu technologicznym i algorytmicznym system przetwarza informacje w pętli trzech głównych warstw, zachowując geometryczną kompresję danych:

```
[ S ] Pełny stan wejściowy ──> [ J(S) ] Szkielet logiczny ──> [ S' ] Rekonstrukcja pola
  │
  └───( Zarządzane przez: Λ, τ, ρ, G_J, T_adapt )
```


* **S** — Pełny wejściowy stan układu (dowolne dane fizyczne, sygnał, obraz).
* **J(S)** — Szkielet logiczny wyizolowany przez operator punktowy skrętu.
* **S'** — Bezkolizyjna rekonstrukcja struktury na podstawie uniwersalnej geometrii pola.

Dzięki zastosowaniu operatorów $\Lambda$, $\tau$, $\rho$, grafu przejść $G_J$ oraz adaptacyjnego tensora $T_{\text{adapt}}$, TIMDER dokonuje bezstratnej kompresji struktury argumentacji i danych.

---

## 9. OBSZARY ZASTOSOWAŃ MODELU

Jednolita geometria asymetrii trójkąta pozwala na aplikację ram TIMDR/TRM w skrajnie różnych dziedzinach inżynierii i nauki:

* **WHITE-LASER-MAP (Biały laser 3+1):** Kontrola fazowa i geometryczna emisji fotonowej.
* **ASTRO-MAP & ASTRO-CYCLES:** Mapowanie dynamiki struktur makroskopowych (w tym rezonansu czarnej dziury Sgr A*) za pomocą orientacji lokalnych skrętów.
* **Analizator giełdowy / Synoptyk:** Mapowanie rynkowych i pogodowych punktów zwrotnych jako anomalii informacyjnych w ciągłym polu trendu.
* **EasySound:** Translacja geometrii struktur atomowych i pól bezpośrednio na spektrum fali dźwiękowej (synestezja geometryczna).
* **FAM (Fundamental AI Model):** Silnik sztucznej inteligencji nowej generacji, rezygnujący ze ślepego, wielomiliardowego dopasowywania wag (brute-force) na rzecz odsłaniania gotowych, niskokosztowych ścieżek geometrycznych w polach informacji.

---

## 10. JAK KORZYSTAĆ Z REPOZYTORIUM

1. **Zaimplementuj zasady:** Nakarm lokalne modele AI (LLM/Agent) strukturą TIMDR, ze szczególnym uwzględnieniem modelu asymetrii trójkąta.
2. **Podstaw dane:** Wprowadź własne macierze danych, sygnały dźwiękowe, fizyczne opisy układów lub serie czasowe.
3. **Uruchom walidację:** Wykorzystaj `TIMDR-Math-Formalism` (następca pierwszej wersji `math-validator`, usuniętej z ekosystemu) w celu weryfikacji jednorodności matematycznej i zachowania warunków brzegowych.
4. **Współtwórz:** Wyniki eksperymentów, anomalie obliczeniowe lub propozycje nowych operatorów zgłaszaj poprzez Issues oraz Pull Requests.

---

## 11. REPOZYTORIA POWIĄZANE

Ekosystem uniwersalnej geometrii pola dystrybuowany jest pomiędzy wyspecjalizowane moduły:
* `GIA-and-TIMDR` — Rdzeń geometryczny i definicje operatorów.
* `topologia-informacji` — Przestrzenie metryczne i przekształcenia Möbiusa.
* `TIMDR-Math-Formalism` — Działający protokół odróżniania realnej struktury matematycznej od numerologii (pre-rejestracja, kontrola pozytywna/negatywna, test Manna-Whitneya, effect size, uczciwy wynik negatywny); następca pierwszej wersji `math-validator`.
* `TRM` — Przetwarzanie rezonansów warstwowych i stałych redukcji.
* `FIELDCORE` — Niskopoziomowy silnik obliczeniowy pól dynamicznych.
* `WHITE-LASER-MAP` / `ASTRO-MAP` / `ASTRO-CYCLES` — Mapowanie skalowane (mikro/makro).
* `EasySound` / `Synoptyk` — Praktyczne aplikacje rezonansowe (dźwięk i predykcja złożona).
* `FAM` — Fundamental AI Model wykorzystujący architekturę skrętu.

---

## 12. LICENCJA

Niniejsze repozytorium dystrybuowane jest na licencji **Open Source**. Udostępnione do nieskrępowanych badań naukowych, eksperymentów technologicznych, rozwoju i budowy nowego paradygmatu unifikacji wiedzy.

---

## 📘 TIMDR — Pełny Model Operatora Topologicznej Zmiany Sygnału

TIMDR to operator wykrywający lokalne zmiany topologii sygnału. Nie jest pojedynczą metodą — jest strukturą, która łączy trzy niezależne detektory:

- **skręt** — zmiana znaku pochodnej (zero-crossing)
- **defekt** — lokalna anomalia energetyczna (z-score)
- **rezonans** — zgodność kierunku kilku sygnałów (korelacja kierunkowa)

TIMDR nie jest sumą tych trzech rzeczy. TIMDR jest interpretacją ich wspólnego zachowania.

### 🧩 1. Formalna definicja TIMDR

Dany sygnał `S(t)`, jego pochodna `S'(t)`, oraz okno czasowe `W`:

**Skręt (T) — lokalna zmiana orientacji**

```
T(t) = [ sign(S'(t)) ≠ sign(S'(t − Δt)) ]
```

Interpretacja: punkt, w którym sygnał zmienia kierunek → lokalna zmiana topologii.

**Defekt (D) — lokalna anomalia energetyczna**

```
D(t) = ( S(t) − μ_W ) / σ_W
```

Interpretacja: punkt, w którym sygnał „wychodzi" poza swoją lokalną strukturę (z-score względem okna `W`).

**Rezonans (R) — zgodność kierunku wielu sygnałów**

Dla sygnałów `S_1, S_2, ..., S_n`:

```
R(t) = (1/n) · Σ_{i=1}^{n} sign(S_i'(t))
```

Interpretacja: lokalna koherencja — sygnały „ciągną" w tę samą stronę.

**Operator TIMDR**

```
TIMDR(t) = mean( T(t), D(t), R(t) )
```

To jest operator topologicznej zmiany sygnału.

### 🔥 2. Interpretacja geometryczna TIMDR

TIMDR nie opisuje wartości sygnału. TIMDR opisuje zmianę jego kształtu.

TIMDR wykrywa:
- punkty krytyczne,
- lokalne przejścia fazowe,
- zmiany stabilności,
- miejsca, gdzie sygnał „łamie" swoją strukturę.

### ⚙️ 3. Interpretacja inżynierska TIMDR

TIMDR jest detektorem zmian strukturalnych. Można go użyć do:
- wykrywania anomalii,
- predykcji punktów krytycznych,
- filtrowania szumu strukturalnego,
- analizy trendów,
- detekcji zmian kierunku,
- stabilizacji sygnałów.

W praktyce TIMDR działa jak: „czujnik niestabilności", „miernik deformacji", „wykrywacz punktów przełomowych".

### 🧠 4. TIMDR jako operator predykcyjny

TIMDR można rozszerzyć o:

**TIMDR-Δ — zmiana TIMDR w czasie**

```
ΔTIMDR(t) = TIMDR(t) − TIMDR(t − Δt)
```

To jest detektor nadchodzącej zmiany.

**TIMDR-S — stabilność lokalna**

```
Stab(t) = var( T(t), D(t), R(t) )
```

Niska wariancja → sygnał stabilny. Wysoka wariancja → sygnał w stanie przejściowym.

**TIMDR-P — predykcja punktu krytycznego**

```
P(t) = f( ΔTIMDR(t), Stab(t) )
```

`f` nie jest tu jeszcze zdefiniowaną funkcją — to szkielet operatora predykcyjnego, wymagający konkretnej implementacji (np. progu, regresji albo klasyfikatora), żeby dało się z niego realnie korzystać.

### 🌐 5. TIMDR jako moduł w pipeline

TIMDR można wpiąć w pipeline jako: filtr anomalii, filtr stabilności, filtr kierunku, filtr strukturalny.

W połączeniu z TRM i GIA tworzy:
- TRM → spójność
- GIA → kierunek
- TIMDR → zmiana

### 🧬 6. TIMDR jako element warstwy geometrycznej

TIMDR jest operatorem, który opisuje deformację sygnału, wykrywa zmiany topologii, działa na poziomie kształtu, nie wartości. To jest fundament dla modeli heurystycznych geometrycznych, operatorów stabilności, operatorów trajektorii, operatorów spójności.

### 📌 Podsumowanie

TIMDR to: operator topologicznej zmiany sygnału, detektor punktów krytycznych, miernik lokalnej niestabilności, narzędzie predykcyjne, element warstwy geometrycznej.

> **Nota redakcyjna:** T, D i R odpowiadają wprost trzem klasycznym, dobrze znanym technikom przetwarzania sygnałów — detekcji przejścia przez zero, z-score i korelacji kierunkowej — dokładnie tym samym, które są już realnie zaimplementowane w repozytoriach `topologic` i `Senscore`. Nazwa „operator topologiczny" jest tu warstwą interpretacyjną/metaforyczną, a nie odniesieniem do topologii w sensie matematycznym (homologia, rozmaitości itd.). `TIMDR-P` (sekcja 4) jest szkieletem koncepcyjnym — `f` nie ma tu jeszcze definicji ani implementacji.
>
> **Rozgraniczenie od gałęzi sygnałowej (M) i modalnej (K):** `R` i `T`
> powyżej NIE są tymi samymi operatorami co rezonans M i skręt sygnałowy
> z `docs/theory/Axioms_S_TIMDR_Signal.md` (tam: koincydencja progowa
> `Σ𝔸ᵢ≥K`, nie średnia zgodność kierunku), ani rezonansem modalnym K z
> `docs/theory/Axioms_K_TIMDR.md` (tam: wyrównanie częstotliwość/faza).
> Ta sekcja jest wcześniejszym, mniej sformalizowanym szkicem —
> kanoniczne nazwy ("rezonans kierunkowy" dla `R`, uproszczony
> poprzednik "skrętu sygnałowego" dla `T`) i pełne rozgraniczenie:
> [`docs/GLOSSARY_EN_PL.md`](docs/GLOSSARY_EN_PL.md).

---

## 📘 GIA — Operator Lokalnego Toru Informacji

GIA to operator, który wyznacza dominującą trajektorię sygnału w lokalnym otoczeniu. Nie jest to zwykłe PCA — PCA jest tylko narzędziem do wyciągnięcia wektora własnego. GIA jest interpretacją tego wektora jako toru topologicznego.

### 🧩 1. Formalna definicja GIA

Dany zbiór punktów `P = {p_1, p_2, ..., p_n}` w lokalnym otoczeniu sygnału. Każdy punkt ma: pozycję `x_i`, czas `t_i`, energię `E_i`.

**Macierz kowariancji**

```
C = cov(P)
```

**Największy wektor własny**

```
v = eig_max(C)
```

**Operator GIA**

```
GIA(P) = v
```

To jest lokalny tor informacji.

### 🔥 2. Interpretacja geometryczna GIA

GIA nie mówi „sygnał rośnie" ani „sygnał maleje". GIA mówi: „w tym miejscu sygnał ma dominujący kierunek deformacji".

GIA wykrywa:
- lokalny przepływ informacji,
- dominującą trajektorię,
- kierunek deformacji sygnału,
- stabilny tor struktury.

To jest odpowiednik: gradientu topologicznego, lokalnej ścieżki minimalnej energii, najbardziej stabilnej trajektorii.

### ⚙️ 3. Interpretacja inżynierska GIA

GIA jest detektorem kierunku. Można go użyć do:
- predykcji trajektorii obiektów,
- analizy trendów giełdowych,
- modelowania przepływu energii,
- analizy ruchu w radarach/LIDARach,
- wykrywania kierunku deformacji sygnału.

W praktyce GIA działa jak: „kompas sygnału", „wektor dominującej dynamiki", „lokalny tor struktury".

### 🧠 4. Rozszerzenia GIA

**GIA-S — stabilność kierunku**

```
S = λ_max
```

Im większa wartość własna, tym bardziej stabilny kierunek.

**GIA-Δ — zmiana kierunku**

```
Δv = v(t) − v(t − Δt)
```

To jest detektor zmiany trajektorii.

**GIA-C — koherencja kierunkowa**

```
C = mean( sign(v_i) )
```

To jest zgodność kierunku w wielu sygnałach.

### 🌐 5. GIA w pipeline

GIA jest modułem, który określa kierunek, stabilizuje trajektorię, przewiduje ruch, dostarcza wektor dla TIMDR i TRM.

W połączeniu z TIMDR i TRM tworzy:
- TRM → spójność,
- GIA → kierunek,
- TIMDR → zmiana.

### 🧬 6. GIA jako element warstwy geometrycznej

GIA jest operatorem, który opisuje lokalny tor informacji, działa na poziomie kształtu, nie wartości, jest topologicznym kompasem sygnału. To jest fundament dla predykcji ruchu, analizy trendów, modeli przepływu energii, detekcji kierunku deformacji.

### 📌 Podsumowanie

GIA to: operator lokalnego toru informacji, wektor dominującej dynamiki, kompas topologiczny sygnału, narzędzie predykcyjne, element warstwy geometrycznej.

> **Nota redakcyjna:** `GIA(P)` zdefiniowane powyżej to dokładnie pierwsza składowa główna (first principal component) klasycznego PCA — największy wektor własny macierzy kowariancji lokalnego sąsiedztwa punktów. Ten sam mechanizm (dopasowanie linii metodą PCA i pomiar reszt) jest już realnie zaimplementowany w repozytorium `Senscore` jako "GIA filter". Nazwy „tor topologiczny" i „kompas topologiczny" są warstwą interpretacyjną nad tym klasycznym narzędziem statystycznym, nie odrębną metodą obliczeniową.

---

## 14. STRUKTURA DOKUMENTACJI

Wszystkie dokumenty koncepcyjne repozytorium są uporządkowane pod `docs/`:

- **`docs/theory/`** — pełna, litereowana seria modeli abstrakcyjnych (J, K, L, M, N, O, Q, R, S, T, U, V, X, Y) oraz seria zastosowań domenowych (AA–AK: kosmologia, biologia, technologia, percepcja, AI, język, muzyka), plus `TRM_biology.md` i `TIMDR-T-operator.md`. **M** (`Resonance_M_Operator_Empiryczny.md`) i **S** (`Axioms_S_TIMDR_Signal.md`) to formalizacja gałęzi sygnałowej TIMDR (rezonans jako koincydencja progów, nie rezonans modalny z Axioms_K) — z realną walidacją empiryczną na danych pogodowych, nie tylko definicjami; pełny działający protokół testowy żyje w osobnym repo `TIMDR-Math-Formalism`.
- **`docs/models/`** — konkretne modele geometryczne (emergencja, interferencja, rezonans warstwowy, model topologiczno-modalny, model S 3D).
- **`docs/geometry/`** — konstrukcje geometryczne Möbiusa/torusa (tetroida, mobiosotourys, tourosomobius, domeny Hopfa, eksperymenty domknięcia).
- **`docs/filters/`** — dokumentacja filtrów (liczby pierwsze, stosunek Möbiusa, przewidywania filtra Al).
- **`docs/diagrams/`** — diagramy formalne (F, G, H, P) i diagram struktury topologicznej.
- **`docs/concepts/`** — pojedyncze eseje koncepcyjne (czas, topologia informacji, metodologia dowodu, słownik pojęć rdzeniowych itd.).
- **`docs/`** (poziom główny) — dokumenty referencyjne: pełny dokument teoretyczny PL/EN, słownik EN/PL, przykłady zastosowań, stałe, prompt systemowy AI, kierunki rozwoju.

Ta struktura zastępuje wcześniejszy stan, w którym ponad 30 plików leżało luźno w katalogu głównym repozytorium (część z nich nawet bez rozszerzenia `.md`, np. `MASTER DIAGRAM TIMDR`, `N — Operatory matematyczne TIMDR`). Przy okazji porządkowania usunięto dwa martwe pliki (`constants.md` w katalogu głównym — dokładny duplikat `docs/constants.md`; pusty plik `models`) oraz scalono dwa przypadki zduplikowanej treści (`TIMDR-T-operator.md` miało dwie rozbieżne wersje — zachowano pełniejszą; `Diagram F` istniał jako urwany szkielet w jednym miejscu i pełna treść w drugim — zachowano pełną).

---

## 15. DIAGRAM TOPOLOGII SYGNAŁU

```
SYGNAŁ / DANE
(S(t), S'(t), punkty P)
        │
        ▼
WARSTWA TOPOLOGICZNA
        │
        ├───────────────┬───────────────┐
        ▼               ▼               ▼
      TIMDR            TRM             GIA
     (zmiana)        (spójność)      (kierunek)
        │               │               │
        └───────────────┼───────────────┘
                         ▼
                     GAITIMDR
                   (stabilność)
                         │
                         ▼
              MODEL TOPOLOGICZNY
               (pełna struktura)
```

| Operator | Rola | Kluczowe wielkości | Co wykrywa | Typ topologii |
|---|---|---|---|---|
| **TIMDR** | zmiana | skręt (T), defekt (D), rezonans (R) | zmianę kształtu sygnału | lokalna, w czasie |
| **TRM** | spójność | sąsiedztwo x, sąsiedztwo t, gęstość N(p) | strukturę / prawdziwe zdarzenia | przestrzenno-czasowa (x–t) |
| **GIA** | kierunek | PCA → v_max, tor informacji | dominującą trajektorię | trajektorii |

**GAITIMDR** zbiera wyjścia tych trzech (deformacja funkcji, punkty krytyczne, stabilność lokalna) i podaje je dalej do pełnego modelu topologicznego.

### Interpretacja diagramu — jedno zdanie na warstwę

- **TIMDR** — wykrywa, gdzie sygnał zmienia topologię (skręt, defekt, rezonans).
- **TRM** — wykrywa, czy punkt należy do lokalnej struktury (spójność x–t).
- **GIA** — wykrywa, w którą stronę płynie informacja (trajektoria).
- **GAITIMDR** — wykrywa, jak stabilna jest funkcja i gdzie ma punkty krytyczne.

Razem tworzą pełny model topologiczny sygnału: **zmiana → spójność → kierunek → stabilność**.
