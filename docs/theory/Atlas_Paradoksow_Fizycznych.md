# Atlas paradoksów fizycznych pod TIMDR/TRM/GIA — rozszerzenie eksperymentalne

**Status:** eksperymentalne, w większości NIESPRAWDZONE. To jest pierwsza próba
przeniesienia `Atlas_Paradoksow_TIMDR.md` (osie, reguły, falsyfikacja — nie
powtarzane tutaj, patrz tamten plik) do domeny spoza teorii mnogości/logiki.
Pierwsza runda sześciu przykładów fizycznych złamała własne zasady atlasu w
sześciu miejscach na sześć — nie dlatego, że reguły są złe, tylko dlatego, że
kluczowe pojęcie ("lokalnie/globalnie") ma w fizyce **inne, precyzyjne
znaczenia techniczne**, różne między sobą i różne od znaczenia matematycznego,
którego atlas używał do tej pory. Ten dokument najpierw ustala te znaczenia,
dopiero potem wraca do klasyfikacji.

---

## 1. "Lokalnie/globalnie": cztery różne rzeczy pod jedną nazwą

### 1.1 Sens matematyczny (ustalony w atlasie głównym)

Strukturalny, bez obserwatora: lokalnie = jeden krok/mały fragment konstrukcji
obiektu (usunięcie jednego odcinka w Cantorze, jeden wierzchołek drzewa);
globalnie = obiekt jako ukończona całość. Nie ma tu żadnego "punktu widzenia"
— to własność samego obiektu matematycznego, niezależna od tego, kto patrzy.

### 1.2 Sens GR (ogólna teoria względności)

**Lokalnie** ma tu ścisłe, ugruntowane znaczenie: mała okolica PUNKTU
czasoprzestrzeni, gdzie z zasady równoważności geometria jest w przybliżeniu
płaska (lokalna rama inercjalna). Fakty lokalne są **niezmiennicze** —
krzywizna (np. skalar Kretschmanna), czas własny wzdłuż linii świata, to co
mierzy swobodnie spadający obserwator w swoim bezpośrednim otoczeniu — nie
zależą od wyboru układu współrzędnych.

**Globalnie** = własność CAŁEJ rozmaitości albo całego regionu: topologia,
istnienie globalnej funkcji czasu, struktura przyczynowa (horyzonty,
powierzchnie Cauchy'ego), zachowanie asymptotyczne, oraz — kluczowe —
**konkretny wybór układu współrzędnych jako całości** (np. współrzędne
Schwarzschilda pokrywające cały zewnętrzny region).

**Pułapka, która zepsuła klasyfikację Horyzontu GR w poprzedniej rundzie:**
"obserwator" nie jest tym samym co "lokalnie". Obserwator swobodnie spadający
opisuje fizykę w swojej lokalnej ramie inercjalnej — to faktycznie lokalne, w
sensie GR, i jest tam gładkie (krzywizna skończona, "no drama at the
horizon" — ustalony wynik GR). Obserwator zewnętrzny/statyczny opisuje
fizykę we współrzędnych Schwarzschilda — ale to jest opis w
**globalnym** układzie współrzędnych obejmującym cały region zewnętrzny, i
to ten globalny wybór ma osobliwość przy r=2GM, nie żadna lokalna
geometria. "Który obserwator" ≠ "jaka skala" — to dwie różne osie, które
łatwo pomylić.

### 1.3 Sens mechaniki statystycznej (Loschmidt)

Inny, ale realny odpowiednik "mały fragment / całość": **pojedyncza
trajektoria mikroskopowa** w przestrzeni fazowej (jedna krzywa, analogiczna
do jednego kroku konstrukcji) vs **objętość zbioru mikrostanów** zgodnych z
ograniczeniami makroskopowymi (cały obiekt, z którego dopiero definiuje się
entropię S = k ln Ω). To mapuje się na sens matematyczny (1.1) dość dobrze —
problemem w poprzedniej rundzie nie była sama skala, tylko to, że etykieta
"Transition" (opisująca relację MIĘDZY mikro a makro) została przypisana do
jednej strony (lokalnie) tej relacji, zamiast do samej relacji albo do obu
stron osobno. To do rozstrzygnięcia niżej — realnie sporne w podstawach
fizyki statystycznej, nie tylko kwestia nazewnictwa.

### 1.4 Sens EPR/Bell (lokalność przyczynowa)

To jest **czwarte, jakościowo inne** znaczenie: "lokalność" w EPR/Bell
znaczy brak nadświetlnego wpływu przyczynowego między zdarzeniami
oddzielonymi przestrzennie (rozdzielenie w sensie relatywistycznym) — to
jest sam **przedmiot** paradoksu (założenie testowane przez nierówności
Bella), nie wybór skali opisu jednego, ustalonego obiektu. Nie ma tu
naturalnego "małego fragmentu" i "całości" tego samego obiektu — jest
hipoteza fizyczna (lokalny realizm) kontra przewidywanie innej teorii (QM).
Wymuszanie na tym rozbicia lokalnie/globalnie w sensie 1.1 może być
kategorialnym błędem, nie doprecyzowaniem.

**Wniosek:** cztery różne rzeczy, jedna nazwa. 1.1 i 1.3 mapują się na
siebie nieźle (obiekt bez obserwatora, fragment/całość). 1.2 wymaga
odróżnienia "lokalne=niezmiennicze" od "który obserwator". 1.4 może w ogóle
nie być instancją tej samej osi.

---

## 2. Gdzie kończy się jednomodelowość

Kryterium z atlasu głównego: czy **sformułowanie i weryfikacja** twierdzenia
wymaga ≥2 modeli (formalnych systemów), nie czy dwie fizyczne teorie dają
różne liczby. Test: czy dowód/wynik daje się w całości przeprowadzić
wewnątrz JEDNEGO nadrzędnego aparatu matematycznego, nawet jeśli motywacją są
dwie konkurencyjne teorie fizyczne.

- **Twierdzenie Bella** (EPR): dowodzone w całości wewnątrz jednego aparatu
  (rachunek prawdopodobieństwa + założenie lokalności + formalizm
  kwantowy jako jedna, spójna struktura matematyczna) — **jednomodelowe**,
  tak jak Vitali. Sam fakt, że wynik "koliduje" z intuicją realizmu, nie
  czyni tego wielomodelowym — Vitali też koliduje z intuicją mierzalności,
  a zostaje jednomodelowy.
- **Renormalizacja**: różne schematy (minimal subtraction, on-shell, cutoff)
  dają różne liczby pośrednie dla tych samych, fizycznie mierzalnych
  wielkości — to zmiana parametryzacji WEWNĄTRZ jednej teorii (QFT), bliżej
  zmiany układu współrzędnych niż porównania modeli — **jednomodelowe**.
- **Informacja BH**: GR (semiklasyczna) i unitarna QM dają **różne,
  nieuzgodnione przewidywania** dla tej samej sytuacji fizycznej, bez
  wspólnego, ukończonego aparatu, w którym dałoby się to rozstrzygnąć jednym
  dowodem — to jedyny z sześciu przykładów, gdzie "wielomodelowe" broni się
  bez naciągania, bo aktualnie **nie istnieje** jedna teoria kwantowej
  grawitacji, w obrębie której dałoby się to policzyć jednoznacznie.

---

## 3. Ustalone

| Przykład | Skala | Oś modelowa | Reguła | TRM |
|---|---|---|---|---|
| Paradoks bliźniąt | — | jednomodelowe | Skręt | 2 |
| Paradoks bliźniąt | — | jednomodelowe | Transition | 24 |
| Loschmidt | lokalnie (pojedyncza trajektoria) | jednomodelowe | — (brak zjawiska) | — |
| Loschmidt | globalnie (objętość zbioru mikrostanów) | jednomodelowe | Emergentność | 118 |
| Renormalizacja | lokalnie (gołe parametry, UV) | jednomodelowe | Defekt | 2 |
| Renormalizacja | globalnie (uniwersalna teoria efektywna, IR) | jednomodelowe | Emergentność | 118 |
| Horyzont GR | lokalnie (rama swobodnie spadająca) | jednomodelowe | — (brak zjawiska) | — |
| Horyzont GR | globalnie (współrzędne Schwarzschilda jako całość) | jednomodelowe | Defekt | 2 |
| EPR | lokalnie (statystyki brzegowe jednej cząstki) | jednomodelowe | — (brak zjawiska) | — |
| EPR | globalnie (stan łączny, korelacje łamiące Bella) | jednomodelowe | Emergentność | 118 |
| Informacja BH | — (bez splitu) | wielomodelowe | Stabilność | 118 |
| Izolator topologiczny | lokalnie (cechowanie w punkcie k) | jednomodelowe | Defekt | 2 |
| Izolator topologiczny | globalnie (całka po strefie Brillouina) | jednomodelowe | Emergentność | 118 |

**Loschmidt — rozstrzygnięcie.** Pojedyncza trajektoria nie ma zdefiniowanej
entropii w ogóle (entropia = S=k ln Ω wymaga objętości Ω zbioru mikrostanów,
nie jednej trajektorii) — to nie jest defekt (dynamika Newtona dla jednej
trajektorii jest w pełni określona i domyka się, nic tam się nie psuje), tylko
brak przedmiotu, do którego którakolwiek reguła miałaby się odnosić. Stąd
lokalnie = brak zjawiska, dokładnie jak wymiar skończony u baz Hilberta —
ten sam kształt w niezależnej dziedzinie, dobry sygnał, nie zbieg
okoliczności (obie sytuacje: własność wymaga agregacji po wielu elementach,
żeby w ogóle być zdefiniowana; dla jednego elementu jest pusta).
Nie potrzeba trzeciego wiersza na "Transition" (relację mikro→makro) — to
dokładnie to, co już znaczy Emergentność z definicji ("lokalne fakty łączą
się w stabilną, jakościowo nową strukturę globalną"): reguła wzrostu
entropii to nie osobny mechanizm obok lokalnego i globalnego opisu, tylko
STATYSTYCZNA prawidłowość wynikająca z dysproporcji objętości między
makrostanami (twierdzenie Liouville'a: trajektorie nie preferują żadnego
regionu, ale regiony wysokoentropijne są przytłaczająco większe) —
"Transition" sugerowałoby próg ciągłego parametru do przekroczenia, a tu nie
ma progu, jest tylko przewaga liczebna, którą Emergentność już opisuje.

**Renormalizacja — rozstrzygnięcie.** Ani "skala wymiarowa", ani nowa oś
energetyczna — obie opcje z pytania były błędnym punktem wyjścia. "Skala
wymiarowa" pasowała do baz Hilberta, bo TAM zmienną, na której coś się
łamało, był wymiar (skończony/nieskończony). W renormalizacji zmienną, która
faktycznie się zmienia między "lokalnie" a "globalnie", jest **skala
energii**, nie liczba stopni swobody — nieskończenie wiele stopni swobody
jest obecnych na KAŻDEJ skali energii, więc "skończone/nieskończone" nie
dzieli niczego w tym przykładzie; to była zaimportowana etykieta z innego
przykładu, nie faktyczna zmienna tego. Nowa oś też nie jest potrzebna: UV
(gołe parametry, wysoka energia — pojedynczy, krótkodystansowy opis) mapuje
się na "lokalnie", IR (obserwowalna teoria efektywna, długi dystans,
agregat) na "globalnie" — dokładnie ta sama para ról co trajektoria/zespół u
Loschmidta czy fragment/całość u Cantora, tylko innego typu obiekt fizyczny.

Reguły: lokalnie (UV) = **Defekt** — gołe parametry dosłownie divergują bez
regularyzacji, lokalna reguła się nie domyka (ten sam mechanizm co
Banach–Tarski lokalnie, inny przedmiot). Globalnie (IR) = **Emergentność** —
kluczowy wynik grupy renormalizacji to uniwersalność: bardzo różne teorie UV
spływają do TEJ SAMEJ efektywnej teorii IR, więc szczegóły mikroskopowe
"wymywają się" w stabilną strukturę globalną, TRM=118 (wiele możliwych
UV-uzupełnień zapadających się w jedną strukturę — realna wielopoziomowa
hierarchia, nie tylko duża liczba). Ciągły przepływ sprzężeń ze skalą
(funkcje β) jest tu MECHANIZMEM, przez który emergencja zachodzi — nie
osobnym, trzecim zjawiskiem wymagającym własnego wiersza, dokładnie tak jak
przy Loschmidcie mechanizm (twierdzenie Liouville'a) nie dostał osobnego
wiersza obok samej Emergentności.

**Horyzont GR — rozstrzygnięcie.** Odpowiedź na pytanie "czy 'lokalnie' w
GR sprowadza się do atlasowego 'małe otoczenie'?" — tak, pod warunkiem że
"lokalnie" kotwiczy się w faktach PUNKTOWYCH/niezmienniczych (krzywizna w
punkcie, doświadczenie swobodnie spadającego obserwatora w jego
bezpośrednim otoczeniu), nie w tym, "który obserwator opowiada". Skalar
Kretschmanna K=48G²M²/c⁴r⁶ jest skończony przy r=2GM (rozbiega dopiero przy
r=0, prawdziwej osobliwości) — to niezmiennicze potwierdzenie, że lokalnie
nic się nie psuje ("no drama at the horizon", ustalony wynik GR). Stąd
lokalnie = brak zjawiska (trzeci niezależny przypadek tego kształtu obok
Loschmidta i baz Hilberta — choć tu z innego powodu: nie "pojęcie
niezdefiniowane", tylko "pojęcie zdefiniowane i regularne", więc żadna
reguła nie ma się do czego odnieść).

Globalnie: współrzędne Schwarzschilda jako JEDNA całościowa karta
zewnętrznego regionu mają osobliwość współrzędnych przy r=2GM (g_tt→0,
g_rr→∞) — karta się nie domyka, trzeba innej (Kruskal, Eddington-
Finkelstein), żeby przejść przez horyzont. To Defekt, ale na wierszu
globalnym, nie lokalnym — pierwszy taki przypadek w obu atlasach (dotąd
Defekt siedział zawsze lokalnie: Vitali, Cantor, Banach–Tarski,
renormalizacja). Nic w definicji reguły tego nie zabrania (definicja mówi
"reguła się nie domyka", nie "lokalna reguła" w sensie skali), ale warto
odnotować jako pierwszy wyłom we wzorcu, nie przemilczeć.

Cztery ustalone: bliźniacy przeszli bez poprawek, Loschmidt, renormalizacja
i Horyzont GR wymagały rozstrzygnięcia po jednym otwartym pytaniu każdy —
wszystkie cztery teraz bez otwartych zastrzeżeń.

**EPR — rozstrzygnięcie.** Oś modelowa: bez zmian, jednomodelowe (§2).
"Lokalność przyczynowa" (brak wpływu nadświetlnego) NIE jest podtypem osi
Skala — to hipoteza testowana przez nierówność Bella, czyli treść samego
paradoksu, nie sposób jego oglądania; nie dostaje własnego pola, bo to nie
jest w ogóle ten rodzaj rzeczy, do którego "sposób oglądania" się stosuje.
Właściwy split lokalnie/globalnie jest inny, dotąd niezauważony: statystyki
BRZEGOWE pojedynczej cząstki (lokalnie) — zawsze maksymalnie zmieszane,
nieodróżnialne od czystego szumu — vs stan ŁĄCZNY dwóch cząstek
(globalnie), niosący korelacje łamiące nierówność Bella, nieredukowalne do
żadnych lokalnych zmiennych ukrytych. Lokalnie = brak zjawiska (czwarty
niezależny przypadek tego kształtu, po bazach Hilberta, Loschmidcie i
Horyzoncie GR — rozważony i odrzucony alternatywny odczyt przez Rezonans:
wymaga zgodności KIERUNKU wielu lokalnych reguł, a pojedyncza cząstka nie ma
z czym się zgadzać). Globalnie = Emergentność/118 — dosłownie standardowe
sformułowanie fizyczne entanglementu: "całość nie jest sumą (lokalnych)
części". To usuwa też starą niespójność z TRM: nie ma już wiersza
"lokalnie" z TRM=118 łamiącego wzorzec — problem znika, bo lokalny wiersz
w ogóle nie ma TRM.

Pięć ustalonych na sześć. Uczciwe zastrzeżenie: cztery z pięciu rozwiązanych
przykładów (Loschmidt, renormalizacja, Horyzont GR, EPR) wylądowały na tym
samym wzorcu "brak zjawiska + Emergentność/118" — może to być prawdziwa,
powtarzalna struktura fizycznych paradoksów tego typu, ale warto to
traktować jako hipotezę do sprawdzenia na kolejnych, niezależnych
przykładach, nie jako potwierdzone prawo — zanim ten wzorzec zostanie użyty
jako domyślne założenie przy klasyfikowaniu czegokolwiek nowego.

**Informacja BH — rozstrzygnięcie.** Oba otwarte pytania znikają razem, bo
mają wspólną przyczynę: przykład był nadmiernie rozbudowany (3 wiersze),
zamiast sprawdzony pod kątem tego, ile struktury faktycznie potrzebuje.
Kluczowa obserwacja: **żaden dotychczasowy przykład wielomodelowy (CH,
Skolem, Gödel-2) nigdy nie miał splitu lokalnie/globalnie** — zawsze "Skala:
—". To nie zbieg okoliczności: oś Skala z definicji dzieli JEDEN obiekt
wewnątrz JEDNEGO modelu na fragment i całość; przykład wielomodelowy nie ma
takiego pojedynczego obiektu — paradoks polega na samym porównaniu modeli
(tu: GR semiklasycznej i unitarnej QM), nie na czymś dziejącym się wewnątrz
jednego z nich. Informacja BH jest wielomodelowa (jedyny z sześciu, gdzie to
się broni bez naciągania — §2), więc zgodnie z tym wzorcem strukturalnym w
ogóle nie powinna mieć splitu Skala — nie dlatego, że "lokalnie" było źle
przypisane (jak w Horyzoncie GR), tylko dlatego, że sama skala tam nie
występuje. Ten sam argument ekonomii usuwa "Perspektywę operatorowa/
semantyczna": skoro CH/Skolem/Gödel-2 to zawsze jeden czysty wiersz bez
dodatkowych pól, trzecia oś tu też była nadmiarowa — tego samego rodzaju
nadmiar co odrzucony trzeci wiersz "Transition" przy Loschmidcie. Wynik:
jeden wiersz, wielomodelowe/Stabilność/118, zgodny z każdym innym
przykładem wielomodelowym w obu atlasach.

Sześć na sześć. To jedyny z sześciu przykładów, który NIE wylądował na
wzorcu "brak zjawiska + Emergentność" — dobry znak, że poprzednie cztery
trafienia w ten wzorzec nie były bezmyślnym powielaniem szablonu, tylko
faktycznym wynikiem sprawdzania każdego przykładu od nowa.

---

## 5. Podsumowanie pierwszej rundy i zakres

Pierwsza runda (sześć przykładów) jest zamknięta. Rozkład reguł: trzy
przykłady dają "brak zjawiska (lokalnie) + Emergentność/118 (globalnie)"
(Loschmidt, Horyzont GR, EPR), dwa łączą Defekt (lokalnie) z drugą regułą
(globalnie) przez split Skala (renormalizacja: Defekt+Emergentność;
bliźniacy: Skręt+Transition, bez splitu Skala), jeden bez splitu Skala
wcale (Informacja BH, jedyny wielomodelowy). Żaden nie wymagał nowej osi
ani nowego podtypu Skali — obie hipotezy
robocze z początku dokumentu (§1, cztery znaczenia "lokalnie/globalnie";
§2, granica jednomodelowości) okazały się wystarczające do rozstrzygnięcia
wszystkich sześciu, po poprawnym zidentyfikowaniu, KTÓRE z czterech znaczeń
stosuje się w danej dziedzinie.

To NIE dowodzi, że fizyka ogólnie mieści się w trzech osiach atlasu
matematycznego — sześć przykładów z czterech działów (SR, GR, mechanika
statystyczna, QFT, podstawy QM) to wciąż mała, ręcznie dobrana próbka.
Naturalne kolejne kroki, żadien nie pilny: (a) druga, niezależna runda
przykładów z tych samych działów, żeby sprawdzić, czy "brak zjawiska +
Emergentność" nadal dominuje, czy to był artefakt akurat tej szóstki; (b)
przykład z działu jeszcze nietestowanego (np. termodynamika nierównowagowa,
teoria informacji, chemia kwantowa), żeby sprawdzić, czy potrzebna będzie
piąta interpretacja "lokalnie/globalnie" obok już znalezionych czterech.

---

## 6. Runda druga — nowy dział: fizyka fazy skondensowanej

**Przykład:** paradoks izolatora topologicznego (bulk-boundary
correspondence) — dlaczego układ izolujący w całej objętości ma na brzegu
przewodzące, topologicznie chronione stany, odporne na lokalne zaburzenia?

**Czy ujawnia piąte znaczenie "lokalnie/globalnie"?** Nie. Sprawdzone i
odrzucone: to instancja sensu MATEMATYCZNEGO (§1.1, fragment/całość
ustalonego obiektu), nie nowa, fizyczna odmiana — "obiektem" jest tu wiązka
Blocha nad strefą Brillouina, a lokalna krzywizna Berry'ego/globalna liczba
Cherna to dokładnie ta sama para ról co lokalny krok konstrukcji/pełny
obiekt u Cantora, tylko realizowana przez matematykę wiązek włóknistych
zamiast teorii mnogości. Fizyka fazy skondensowanej sięga tu po tę samą
matematykę, którą atlas już miał skatalogowaną — nie generuje własnej.

**Klasyfikacja.** Lokalnie: w jednym punkcie k krzywizna Berry'ego jest
dobrze zdefiniowana punktowo, ale gdy liczba Cherna ≠ 0, nie istnieje
gładki, jednowartościowy wybór cechowania funkcji falowych obejmujący całą
strefę Brillouina naraz (przeszkoda topologiczna, ten sam mechanizm co
twierdzenie o uczesanej kuli) — lokalna reguła (gładkie cechowanie) nie
domyka się globalnie mimo że działa na każdym małym fragmencie osobno —
**Defekt**, TRM=2 (ten sam mechanizm co Banach–Tarski lokalnie i
renormalizacja lokalnie, inny przedmiot). Globalnie: całka krzywizny
Berry'ego po całej, zwartej strefie Brillouina daje skwantowaną liczbę
całkowitą (liczbę Cherna), odporną na dowolne lokalne zaburzenia dopóki
przerwa energetyczna się nie zamknie, wyznaczającą liczbę chronionych
stanów brzegowych — **Emergentność**, TRM=118. Oś modelowa: jednomodelowe
(jeden aparat teorii pasmowej/geometrii kwantowej, bez porównania modeli).

**Wynik dla wzorca z §5.** To pierwszy przykład w rundzie fizycznej, gdzie
lokalnie NIE wychodzi "brak zjawiska" — Berry'ego krzywizna jest lokalnie
zdefiniowana (w przeciwieństwie do entropii jednej trajektorii czy
statystyk brzegowych pojedynczej cząstki), więc lokalnie jest coś
konkretnego, tylko nie ta własność (kwantyzacja), która liczy się globalnie.
Przełamuje serię pięciu z rzędu "brak zjawiska + Emergentność" z dobrego,
niezależnego powodu, nie na siłę — wzmacnia wiarygodność wcześniejszych
pięciu trafień (gdyby każdy nowy przykład automatycznie lądował w tym samym
kształcie, byłby to sygnał ostrzegawczy, nie potwierdzenie).

---

## 4. Niesprawdzone / robocze — nie wchodzi do tabeli jako ustalone

Brak — wszystkie sześć przykładów pierwszej rundy jest teraz ustalonych.
Patrz §5 na temat zakresu tego atlasu i naturalnych kolejnych kroków.
