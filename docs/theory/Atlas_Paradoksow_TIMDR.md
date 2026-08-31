# Atlas paradoksów matematycznych pod TIMDR/TRM/GIA

**Status:** narzędzie robocze, nie ustalona teoria. Ten dokument powstał z serii
audytów w rozmowie — każdy kolejny przykład był testowany pod kątem, czy
faktycznie spełnia deklarowany warunek reguły, nie tylko czy "brzmi podobnie".
Kilka rund poprawek (patrz historia commitów) usunęło niejednoznaczności
znalezione po drodze: zniknięcie Galileusza z pierwszej wersji reguł, ukryte
podwójne przypisania (Cantor, drzewa regularne), sztuczkę "ZF vs ZF+AC", która
groziła wchłonięciem połowy teorii miary do jednej reguły. Sekcja 4 na końcu
uczciwie wypisuje to, co zostało niedomknięte.

Powiązane: `README.md` §1.5 (dwanaście przykładów jako luźna analogia — ten
atlas to próba zrobienia z tamtej analogii czegoś sprawdzalnego), §7.2 (skala
TRM 2→24→118), `timdr-signal-framework-ADDENDUM.md` (audyt `core/`, osobny
wątek).

---

## 1. Trzy osie klasyfikacji

Klasyfikacja przykładu to funkcja **(obiekt, wybrana skala, oś modelowa) →
reguła**, nie jedna etykieta na obiekt. Poniższe trzy osie są od siebie
niezależne — żadna nie wynika z pozostałych.

### 1.1 Oś modelowa: jednomodelowe / wielomodelowe

**Kryterium:** czy twierdzenie da się w całości **sformułować i zweryfikować**
w jednym, ustalonym systemie aksjomatów, czy samo jego sensowne postawienie
wymaga odniesienia do co najmniej dwóch różnych modeli.

To nie jest to samo co "czy dowód korzysta z mocnego aksjomatu" — Vitali i
Banach–Tarski korzystają z AC, ale oba są w całości stwierdzeniami **w ZFC**
("w ZFC istnieje zbiór niemierzalny"). AC jest tu narzędziem dowodu, nie
przedmiotem porównania. Dopiero twierdzenie w rodzaju "CH jest niezależna od
ZFC" wymaga **z definicji** co najmniej dwóch modeli (jednego, gdzie CH
zachodzi, drugiego, gdzie nie) — bez tego porównania samo zdanie nie ma
sensu.

- **Jednomodelowe:** Vitali, Banach–Tarski, Banach FP, Miara Haara, dobre
  uporządkowanie, Galileusz, Hotel Hilberta, Cantor, drzewa regularne, bazy
  Hilberta, Gödel-1.
- **Wielomodelowe:** CH, paradoks Skolema, Gödel-2.

### 1.2 Oś skali: lokalnie / globalnie

**Kryterium:** czy patrzysz na mechanizm w małym otoczeniu / na jednym kroku
konstrukcji (lokalnie), czy na pełny obiekt jako całość (globalnie).

Nie każdy przykład ma sensowny split — sprawdzone i **odrzucone** dla:
Vitali, CH, paradoks Skolema, dobre uporządkowanie (to są z natury
jednowarstwowe stwierdzenia, bez wewnętrznego mechanizmu "buduję punkt po
punkcie, potem patrzę na całość"). Tam, gdzie split jest realny, każda skala
dostaje **osobny wiersz w tabeli**, bo może mieć inną regułę i inny TRM — nie
tylko inny opis tej samej reguły.

Osobny podtyp tej osi (nie mylić z lokalnie/globalnie): **skala wymiaru**
(skończone/nieskończone) dla baz Hilberta — tam podział nie dotyczy
fragmentu-vs-całości jednego obiektu, tylko dwóch jakościowo różnych reżimów
wymiaru.

Kolumna "Skala" pozostaje ściśle geometryczna/wymiarowa (lokalnie/globalnie,
z wymiarem jako jej podtypem) — nie mieszamy do niej innych rodzajów podziału.

### 1.3 Oś TRM: 2 / 24 / 118

Niezależna od reguły — mówi, **ile poziomów pęknięcia** faktycznie tu jest,
nie która reguła się aktywowała (empirycznie: 3 z 5 reguł współwystępują z
TRM=118, więc sama liczba TRM nie odróżnia reguł).

- **2 — pojedyncze pęknięcie.** Jeden fakt, bez hierarchii i bez granicy
  reżimu do przekroczenia (Galileusz, Vitali, Hilbert lokalnie, drzewa
  lokalnie, Cantor lokalnie, Banach–Tarski lokalnie, Banach FP lokalnie,
  Gödel-1, dobre uporządkowanie).
- **24 — granica reżimu.** Ciągły parametr przekracza próg między dwiema
  klasami (kontrakcja→izometria, zwarty→niezwarty): Banach FP globalnie,
  Miara Haara, Banach–Tarski globalnie.
- **118 — wielopoziomowa hierarchia.** Więcej niż jedna jakościowo różna
  warstwa struktury naraz (miara zero *i* moc continuum; przeliczalna baza
  *i* nieprzeliczalna; wiele niezależnych modeli): Cantor globalnie, Hilbert
  globalnie, drzewa regularne globalnie, bazy Hilberta (wymiar nieskończony),
  CH, paradoks Skolema, Gödel-2.

### 1.4 Pole dodatkowe (nie oś): Perspektywa

Nie liczy się do trzech osi powyżej. Na razie ma dokładnie jeden przykład —
Gödel-1 (syntaktyczna/semantyczna: teoria dowodu vs teoria modeli nałożone na
ten sam, pojedynczy fakt) — więc nazwanie go "czwartą osią" byłoby
przedwczesne: jeden punkt danych nie ustala wzorca (ta sama zasada co przy
próbce z §4). Trzymany jako osobne pole w tabeli właśnie po to, żeby nie
zaśmiecać kolumny "Skala" wynikiem, który nie jest skalą — dopóki nie
pojawi się drugi, niezależny przykład tego samego kształtu, zostaje
oznaczony jako eksperymentalny, nie równoprawny z pozostałymi trzema osiami.

### 1.5 Zasada ogólna splitu (dlaczego kolumny się nie mieszają)

To, co wydarzyło się z Gödlem-1, jest instancją jednej, powtarzalnej zasady,
którą atlas stosuje od Cantora i Banach–Tarskiego — warto ją nazwać wprost,
bo będzie działać na kolejnych przykładach:

1. **Jeśli jeden obiekt ma dwie poprawne, niezależnie uzasadnione
   interpretacje → dostaje dwa wiersze**, nie jedną etykietę na siłę
   uśredniającą oba odczyty (Cantor, Banach–Tarski, Hilbert, Banach FP,
   Gödel-1).
2. **Jeśli te dwie interpretacje różnią się RODZAJEM podziału, nie tylko
   wartością tej samej osi → dostają osobne pole, nie tę samą kolumnę.**
   Geometryczne fragment-vs-całość (Skala), reżim liczności (Skala/wymiar) i
   język opisu (Perspektywa) to trzy różne mechanizmy — wrzucenie ich do
   jednej kolumny ukryłoby różnicę, którą właśnie ta kolumna miała ujawniać.
3. **Nowe pole nie staje się osią na podstawie jednego przykładu.** Zostaje
   pomocnicze/eksperymentalne, dopóki drugi, niezależny przypadek tego samego
   kształtu nie potwierdzi, że to powtarzalny mechanizm, a nie jednorazowa
   cecha jednego paradoksu.

Test na przyszłość: gdy pojawi się kolejny przykład wymagający splitu, pytanie
brzmi nie "czy da się go opisać w Skali", tylko "czy jego dwie interpretacje
są tego samego RODZAJU co któryś z już istniejących podziałów" — jeśli nie,
dostaje nowe pole, nie naciąganą wartość w starym.

---

## 2. Pięć reguł i ich falsyfikacja

Każda reguła ma warunek aktywacji i — równie ważne — warunek, przy którym
**nie powinna** się aktywować. Bez drugiej połowy reguła nie jest
sprawdzalna, tylko opisowa.

**Defekt (D)** — lokalna miara/norma/rozkład nie istnieje lub jest
sprzeczna; lokalna wartość wychodzi poza μ/σ; lokalna reguła się nie domyka.
*Nie aktywuje się, jeśli lokalna miara/reguła istnieje i domyka się.*

**Rezonans (R)** — lokalne reguły są koherentne, "ciągną" w tę samą stronę
(lokalna jednorodność, zgodność kierunku). Wymaga jawnie wybranej skali
lokalnej. *Nie aktywuje się, jeśli lokalne reguły są chaotyczne/niezgodne.*

**Skręt (T)** — zmienia się **sposób porównywania** obiektów (inkluzja →
bijekcja), ale nie zmienia się klasa obiektów. *Nie aktywuje się, jeśli
sposób porównywania zostaje ten sam.*

**Transition** — zmienia się reguła/reżim **wewnątrz jednego modelu**
(kontrakcja→izometria, zwarty→niezwarty, zmiana definicji przy stałym
zestawie aksjomatów); twierdzenie w całości stawialne w jednym systemie.
*Nie aktywuje się, jeśli nie ma zmiany reżimu w obrębie jednego modelu, albo
jeśli samo postawienie problemu wymaga porównania dwóch modeli (wtedy to
Stabilność, nie Transition).*

**Stabilność (Λ/τ/ρ)** — samo sformułowanie lub weryfikacja twierdzenia
wymaga porównania ≥2 różnych modeli, nie tylko technicznie korzysta z
jednego wybranego aksjomatu. *Nie aktywuje się, jeśli twierdzenie da się w
całości wypowiedzieć i zweryfikować w jednym ustalonym systemie — nawet gdy
ten system zawiera AC czy inny mocny aksjomat.*

**Emergentność** — lokalne/niżej-poziomowe fakty łączą się w stabilną,
jakościowo nową strukturę globalną (nowy wymiar/hierarchia). Wymaga jawnie
wybranej skali globalnej. *Nie aktywuje się, jeśli żadna nowa stabilna
struktura globalna nie powstaje.*

---

## 3. Tabela

| Przykład | Skala | Perspektywa | Oś modelowa | Reguła | TRM |
|---|---|---|---|---|---|
| Galileusz | — (bez splitu) | — | jednomodelowe | Skręt | 2 |
| Hotel Hilberta | lokalnie | — | jednomodelowe | Skręt | 2 |
| Hotel Hilberta | globalnie | — | jednomodelowe | Emergentność | 118 |
| Vitali | — (bez splitu) | — | jednomodelowe | Defekt | 2 |
| Cantor | lokalnie | — | jednomodelowe | Defekt | 2 |
| Cantor | globalnie | — | jednomodelowe | Emergentność | 118 |
| Drzewa regularne | lokalnie | — | jednomodelowe | Rezonans | 2 |
| Drzewa regularne | globalnie | — | jednomodelowe | Emergentność | 118 |
| Banach–Tarski | lokalnie (F₂, algebraicznie) | — | jednomodelowe | Defekt | 2 |
| Banach–Tarski | globalnie (kula w R³) | — | jednomodelowe | Transition | 24 |
| Banach Fixed Point | lokalnie (stabilność w punkcie) | — | jednomodelowe | Rezonans | 2 |
| Banach Fixed Point | globalnie (kontrakcja na całości) | — | jednomodelowe | Transition | 24 |
| Miara Haara | — (bez splitu, niesprawdzone do końca — patrz §4) | — | jednomodelowe | Transition | 24 |
| Dobre uporządkowanie | — (bez splitu) | — | jednomodelowe | Skręt | 2 |
| Bazy Hilberta | skala wymiaru: skończony | — | jednomodelowe | — (brak zjawiska) | — |
| Bazy Hilberta | skala wymiaru: nieskończony | — | jednomodelowe | Emergentność | 118 |
| Gödel-1 | — | syntaktyczna (reguła dowodzenia) | jednomodelowe | Defekt | 2 |
| Gödel-1 | — | semantyczna (prawda vs dowodliwość) | jednomodelowe | Skręt | 2 |
| CH | — (bez splitu) | — | wielomodelowe | Stabilność | 118 |
| Paradoks Skolema | — (bez splitu) | — | wielomodelowe | Stabilność | 118 |
| Gödel-2 (różne modele, różne wartości G) | — (bez splitu) | — | wielomodelowe | Stabilność | 118 |

---

## 4. Niedomknięte — uczciwie, nie zamiecione

- **Miara Haara: lokalnie/globalnie nie zostało domknięte.** Padła hipoteza
  (lokalnie = czy punkt ma zwarte otoczenie; globalnie = czy da się to
  skleić w spójną miarę na całej grupie — problem sklejania typu snopowego),
  ale nigdy nie przetestowana z takim samym rygorem jak Banach–Tarski/Banach
  FP. Obecny wiersz w tabeli to najlepsze dotychczasowe przybliżenie, nie
  wynik audytu.
- **"Skala wymiaru" (skończone/nieskończone) vs "skala geometryczna"
  (lokalnie/globalnie)** — nazwane tu jako podtyp jednej osi (1.2), ale mogą
  być w istocie osią czwartą, nie podtypem trzeciej. Nierozstrzygnięte.
- **Cała tabela testowana na ~19 przykładach, nie na próbie losowej.**
  Wszystkie pochodzą z jednej, niewielkiej puli klasycznych paradoksów teorii
  mnogości/analizy — nie sprawdzono na przykładach z zupełnie innych działów
  (kombinatoryka, teoria liczb, geometria różniczkowa), gdzie osie mogłyby się
  zachować inaczej.
- **Rozwiązane: Transition+TRM=2 (Banach FP lokalnie, Gödel-1, dobre
  uporządkowanie).** Wszystkie trzy przeniesione poza Transition. Sprawdzone
  osobno przeciw definicji Skrętu ("zmienia się sposób porównywania
  obiektów"), nie tylko przeciw "to nie Transition": Gödel-1 (dowodliwość vs
  prawda jako dwa różne sposoby ustalania statusu zdania) i dobre
  uporządkowanie (brak porządku → dobry porządek) trzymają się Skrętu.
  **Banach FP lokalnie nie trzyma się Skrętu** — |f'(x*)|<1 to pojedynczy
  warunek liczbowy w punkcie, nie ma tu dwóch przeciwstawnych sposobów
  porównywania. Pasuje za to do Rezonansu: punkty w otoczeniu x* pod iteracją
  poruszają się w tę samą stronę (do x*) — "lokalna zgodność kierunku" wprost
  z definicji reguły. Przeniesiony do Rezonans/TRM=2, dołączając do drzew
  regularnych lokalnie jako drugi przykład tej pary.
- **Rozwiązane: Gödel-1 rozbity na dwa wiersze (syntaktycznie/Defekt,
  semantycznie/Skręt)**, zamiast wymuszać jeden werdykt między konkurującymi
  odczytami — trzeci obserwowany podtyp splitu, "obiektyw formalny" zamiast
  skali (patrz §1.2). Otwarte pozostaje, czy KAŻDY z tych dwóch wierszy sam
  ma dalszy split lokalnie/globalnie (np. dla konkretnego zdania Gödla vs.
  całego schematu diagonalizacji) — to inne pytanie niż to, które właśnie się
  domknęło, i nie zostało jeszcze sprawdzone.
- **Uzasadnienie "Cantor lokalnie → Defekt" w tabeli jest nieprecyzyjne.**
  Sugeruje analogię do Vitalego ("miara nie istnieje"), ale zbiór Cantora MA
  dobrze określoną miarę (zero) — to nie brak miary, tylko klauzula "lokalna
  reguła się nie domyka" (konstrukcja usuwania nigdy się nie kończy,
  samopodobna na każdej skali). Sama reguła (Defekt) zostaje trafna — to inna
  klauzula tej samej reguły niż u Vitalego, nie błąd klasyfikacji.
