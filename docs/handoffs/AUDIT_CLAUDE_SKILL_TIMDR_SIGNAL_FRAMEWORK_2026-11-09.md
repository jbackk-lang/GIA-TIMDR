# AUDYT SKILLA CLAUDE: TIMDR SIGNAL FRAMEWORK

**Data:** 2026-11-09  
**Źródło:** `timdr-signal-framework-SKILL.md` w repozytorium GIA-TIMDR  
**Zakres:** wskazówki istotne dla geometrii helisy, torsji, sygnału, sprzężenia, pamięci, falsyfikacji i ciągłości badań.  
**Status:** przeczytano pełny plik (29 sekcji); poniżej zapisano wnioski mające bezpośrednie znaczenie dla aktualnego programu helisy.

## 1. Najważniejszy wniosek

Skill nie jest tylko instrukcją implementacyjną. Zawiera pamięć wcześniejszych eksperymentów, wyników negatywnych, pułapek metodologicznych i decyzji, których nie wolno odtwarzać od zera. Dla helisy najważniejsze są sekcje 6, 9, 12, 13, 14, 20, 21 i 23–29. Trzeba je traktować jako źródło kontekstu badawczego, ale każdą liczbę/tezę przenoszoną do nowego eksperymentu należy sprawdzić w źródłowym kodzie/raporcie wskazanym przez skill.

## 2. Najważniejsze wskazówki geometryczne

### 2.1. Boerdijk–Coxeter: istnieje dokładna konstrukcja tetrahelisy

Sekcja 12 opisuje klasyczną tetrahelisę Boerdijka–Coxetera: dołączanie kolejnych przystających czworościanów foremnych przez stałą operację odbicia. Skill raportuje, że dokładna arytmetyka symboliczna wykazała stałość długości krawędzi, kąta wiązania i kąta torsji; istnieje jedna sztywna transformacja śrubowa S, wyznaczona z pierwszych czterech wierzchołków, która przewiduje kolejne wierzchołki i mapuje kolejne czworościany. Zatem wierzchołki leżą na dokładnej helisie kołowej.

**Znaczenie dla GIA:** to jest istniejący, matematycznie ścisły wzorzec konstrukcji modułowej „czworościan → helisa”. Nie jest jednak automatycznie tym samym co:
- helisa osiowa HC-01;
- postulowany moduł trójkątny TIMDR;
- model czterech/trzech gałęzi na kuli;
- redukcja 4→3;
- helisa z osią wewnętrzną lub zmiennym skokiem.

Nie wolno przenosić wyniku z tetrahelisy na te obiekty bez jawnej mapy konstrukcyjnej. Skill wyraźnie zaznacza, że analogiczna konstrukcja 4-gona i odwrotna rekonstrukcja helisa→czworościan nie zostały formalnie skonstruowane. To potencjalnie ważny kierunek, ale wymaga oddzielnej prerejestracji i dowodu.

### 2.2. Torsja Freneta jest poprawna, ale numerycznie krucha

Sekcja 20 podaje testy, w których wzór Freneta–Serreta
`τ=((r'×r'')·r''')/||r'×r''||²`
jest poprawny analitycznie na helisie, linii prostej i krzywej planarnej, ale na zaszumionych syntetycznych danych defektowych nie wnosił kontrastu: prosty baseline oparty o resztę od płaszczyzny osiągał 3.91×, a torsja około 1.0×; nawet przy 30× mniejszym szumie torsja pozostawała słabsza (2.98×).

**Konsekwencja:** nie używać surowej trzeciej pochodnej jako głównego kanału sygnałowego bez porównania z pozycją, resztą, krzywizną i pierwszą pochodną. W HC-01 pochodne analityczne są świetnym baseline'em; dla danych pomiarowych potrzebne są testy zbieżności, szumu, nieregularnego próbkowania i wygładzania. Znak torsji trzeba zachować w analizie chiralności, ale nie oznacza to, że surowy estymator torsji jest odpornym detektorem.

### 2.3. Nie utożsamiać różnych obiektów i symboli

Skill przypomina, że `τ` w różnych repozytoriach może oznaczać różne rzeczy. W GIA obowiązuje rozdzielenie co najmniej: torsji Freneta–Serreta krzywej, skrętu pasma (twist), writhe, linking, skrętu powierzchniowego, fazowego obrotu modalnego i skalarnego pola `MetaState.tau`. Sama zgodność nazwy nie ustanawia mapy między nimi.

## 3. Najważniejsze wskazówki eksperymentalne

### 3.1. Prerejestracja i null model przed testem

Sekcja 13 wymaga:
1. zdefiniować dokładne obiekty i mapowanie przed obliczeniami;
2. zamrozić metrykę i null model przed zobaczeniem wyniku;
3. nie skanować wielu okien/parametrów i nie wybierać najlepszego wyniku bez korekty wielokrotnych porównań;
4. raportować wynik negatywny bez narracyjnego ratowania hipotezy;
5. przy negatywnym wyniku sprawdzić, czy istnieje właściwy, uznany model dziedzinowy — porażka własnej metryki nie dowodzi braku zjawiska.

Dla helisy oznacza to: przed testem sprzężenia zamrozić sygnał, stan początkowy, kanał wejścia, kanał wyjścia, metrykę efektu, kontrolę pozytywną, kontrolę negatywną i prosty baseline. Nie wybierać po fakcie najkorzystniejszego progu ani fragmentu sygnału.

### 3.2. Kontrole muszą być nie-degenerujące

Sekcja 9 zaleca dodatnią kontrolę z wstrzykniętym efektem i negatywną kontrolę z autokorelacyjnym tłem (np. AR(1)), a nie tylko biały szum, który może być zbyt łatwym/degenerującym przypadkiem. Dla eksperymentu helisy trzeba testować zarówno sytuację, w której sprzężenie powinno dać mierzalną odpowiedź, jak i podobne tło, które nie powinno jej dać.

### 3.3. Prostszy baseline zawsze obok operatora złożonego

Sekcje 19, 20 i 23 pokazują, że poprawna matematycznie, wyższego rzędu lub przeniesiona z innej dziedziny miara może przegrać z prostszym baseline'em. Każdy kanał `κ`, `τ`, faza, rezonans lub „defekt” ma być porównany z prostym pomiarem pozycji/reszty/amplitudy/energii/pochodnej pierwszego rzędu. Null model i kalibracja muszą być właściwe dla badanego obiektu, a nie przeniesione tylko dlatego, że kod działał w innym repo.

### 3.4. Nie kalibrować progu na tym samym efekcie, który chcemy wykryć

Sekcje 2, 3, 24 i 25 dokumentują samoodniesienie baseline'u: okno zawierające cały defekt/degradację może uznać defekt za normę; zmienny mianownik może dać fałszywą zbieżność. Dla helisy należy mieć osobny, jawnie oznaczony stan odniesienia albo kontrolowany baseline. Jeżeli stan zdrowy/niezaburzony nie jest dostępny, trzeba to zgłosić jako ograniczenie identyfikowalności.

## 4. Pamięć, odpowiedź i sprzężenie

Skill wspiera zasadę oddzielania:
- reakcji na bieżący sygnał;
- zależności od stanu pozostawionego przez wcześniejsze pobudzenie;
- trwałej pamięci informacyjnej;
- adaptacji;
- samonaprawy i odzyskania payloadu.

Dla identycznego sygnału testowego porównanie stanu świeżego i stanu po historii może wykazać zależność od historii stanu. Nie dowodzi jednak samo w sobie pamięci informacyjnej ani samonaprawy. Resztkowe `(x,v)` w modelu mechanicznym jest zwykłym stanem dynamicznym, dopóki nie zostanie pokazane przechowywanie/odtworzenie informacji i odróżnione od relaksacji.

## 5. Wskazówki dla architektury i kodu

- **Duplication-drift (§6):** wyszukać powielone implementacje tych samych wzorów; preferować jeden moduł źródłowy i re-export, a regresję sprawdzać przez tożsamość obiektu, nie tylko równość wyników.
- **Typowanie operatorów (§13, case 5):** przed złożeniem operatora z samym sobą sprawdzić dziedzinę, przeciwdziedzinę i jednostki. Wynik torsji nie jest automatycznie indeksem próbki/czasem.
- **Znaczenia rezonansu (§1, §7, §8):** koincydencja alarmów, ringdown oscylatora i rezonans rozpraszania to trzy różne pojęcia.
- **Transfer między dziedzinami (§19):** null model jest częścią założeń statystycznych; nie przenosić go z innego procesu bez ponownego sprawdzenia.
- **Wielomodułowość (§21, §28):** jeden adaptacyjny detektor nie rozwiązuje wszystkich klas defektów; przy agregacji nie wolno ukrywać słabego krytycznego kanału przez średnią.

## 6. Nowe istotne ustalenie po zestawieniu skilla z aktualnym repo

W repo istnieją już:
- `docs/geometry/HELIX_SIGNAL_RESPONSE_COUPLING_v0.1.md` — właściwe pytanie badawcze i rozdzielenie reakcji, pamięci, adaptacji, samonaprawy i odzyskiwania informacji;
- `docs/handoffs/AUDIT_SIGNAL_TO_HELIX_RESPONSE_PATH_2026-11-09.md` — audyt ścieżek M/S, K, projekcji geometrycznej i G;
- `experiments/helix_signal_response/minimal_coupling_probe.py` oraz `RESULT_MINIMAL_SIGNAL_HELIX_RESPONSE_PROBE_2026-11-09.md` — działający syntetyczny test `u(t) → z(t) → y(t)`, CI PASS, trzy testy.

To koryguje wcześniejsze skrótowe sformułowanie „brak sprzężenia”: **abstrakcyjny tor czasowy sygnał→stan pierścienia G→odpowiedź już istnieje i przeszedł test integracyjny**. Brakuje natomiast fizycznie uzasadnionego kanału wejścia (jednostek i mapowania sygnału na siłę/naprężenie/modalność), aktualizacji geometrii helisy na podstawie stanu oraz sprzężenia odpowiedzi z następnym sygnałem. Obecny wynik pokazuje zależność odpowiedzi od resztkowego stanu mechanicznego, nie fizyczną pamięć helisy.

## 7. Kwestia redakcyjna pliku skill

Plik `timdr-signal-framework-SKILL.md` zawiera zdublowany blok front matter `--- name/description ---` na początku. Nie zmieniano go w ramach audytu, aby nie naruszyć źródłowej instrukcji bez decyzji autora. Warto później poprawić format pliku w osobnym, czysto redakcyjnym commicie.

## 8. Decyzja dla dalszej pracy

Nie wracać do ogólnego katalogowania geometrii ani nie tworzyć kolejnego niezależnego modelu. Następny krok ma być kontynuacją istniejącego minimalnego testu sprzężenia:

1. zamrozić kontrakt sygnału `u(t)` (źródło, jednostki albo jawna normalizacja, amplituda, faza);
2. wybrać istniejący stan geometryczny i mechaniczny, nie wymyślać nowego;
3. porównać co najmniej prosty baseline z kanałem `κ` i podpisanym `τ`, z kontrolą szumu;
4. zachować dodatnią i niedegenerującą negatywną kontrolę oraz prerejestrację;
5. wykonać test odbicia lustrzanego, sprawdzając czy znak torsji rzeczywiście zmienia odpowiedź, bez arbitralnego usuwania znaku;
6. odróżnić odpowiedź resztkową od pamięci informacji.

**Zasada anty-zapętlenia:** przed każdym nowym zadaniem helikalnym czytać ten audyt, `HANDOFF_HELIX_SIGNAL_RESPONSE_2026-11-09.md` i `HELIX_TIMDR_RESEARCH_PROGRAM.md`; po zadaniu aktualizować handoff, rejestr wyników i wskazany następny krok. Nie powtarzać testu, który ma już raport, chyba że jawnie sprawdzamy jego replikację lub rozszerzenie.


## 9. Weryfikacja §12 na dokładnym generatorze BC (2026-11-09)

Wskazówka z §12 została odtworzona niezależnie w `core/boerdijk_coxeter_tetrahelix.py` z arytmetyką wymierną i 6 testami CI (run 42588917531, SUCCESS). Dla wybranej konwencji współrzędnych uzyskano jedną macierz śrubową `R` i translację `t`, które przewidują 60 kolejnych wierzchołków i przenoszą centroidy tetraedrów. Raport: `docs/geometry/BOERDIJK_COXETER_EXACT_REFERENCE_2026-11-09.md`.

**Doprecyzowanie terminologiczne do §12:** zapis skilla `cos(τ)=1/3` odpowiada wartości cosinusa wewnętrznego kąta dwuściennego regularnego czworościanu (≈70.5288°). Kąt obrotu dokładnej transformacji śrubowej BC dla tej konwencji ma `cos(θ)=-2/3` (≈131.8103°). Żadnego z tych kątów nie należy nazywać ciągłą torsją Freneta–Serreta. To ważne, bo w repo TIMDR `τ_FS` ma jednostkę odwrotności długości, a inne `τ` są odrębnymi obiektami.

**Nowa obserwacja:** ściany BC są równoboczne, ale sekwencja tetraedrów mimo to wykonuje niezerowy obrót śrubowy. Zatem lokalna asymetria modułu i globalna holonomia wynikająca z reguły sklejenia są odrębnymi możliwymi źródłami skrętu. To nie obala G2 TIMDR, lecz wymaga rozdzielenia obiektów i testowania ich niezależnie.

Dodatkowo odnaleziono i zweryfikowano istniejący test chiralności w repozytorium `jbackk-lang/Helix-Lock`: run 42559444225, Python 3.11 i 3.12, po 148 testów PASS. Wynik jest już opisany w `docs/geometry/COMPARISON_BC_HC01_TIMDR_2026-11-09.md`; nie należy kopiować go ponownie do GIA-TIMDR.
