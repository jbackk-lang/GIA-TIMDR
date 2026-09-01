# TIMDR signal framework — addendum (GIA-TIMDR/core audit)

Uzupełnienie do `timdr-signal-framework-SKILL.md`, nie zamiennik.
Osobny plik, żeby nie rozdymać już dużego (115KB) głównego dokumentu —
scal ręcznie do głównych sekcji (np. jako rozszerzenie §6 i §10), jeśli
wolisz mieć jeden plik. Tylko ustalenia dotyczące samego rdzenia TIMDR
(`core/`) — bez wątków specyficznych dla zewnętrznych źródeł (PDF-y,
transkrypcje wzorów spoza TIMDR). Każdy wpis: Problem → Rozwiązanie →
Uzasadnienie, bez narracji — pełny opis i testy w `GIA-TIMDR/core/` i
`GIA-TIMDR/README.md` (§16).

---

### A. `constants.py` nieużywany + zduplikowane progi (rozszerza §6 "Duplication-drift")

**Problem:** `core/constants.py` definiował progi/wagi, ale nic w `core/`
go nie importowało (`grep -rn "constants" core/` → zero wyników).
`DELTA_S_THRESHOLD=12` istniał tam niezależnie od hardcoded `12` w
`operators.op_deltaS()` i osobnego domyślnego `12` w
`diagnostics.defect_map()` — trzy kopie tej samej liczby, mogące się
rozjechać przy edycji jednej bez pozostałych.

**Rozwiązanie:** `op_deltaS()`/`defect_map()` czytają teraz
`DELTA_S_THRESHOLD` z jednego miejsca; `STAB_*_WEIGHT`, `SPECTRAL_*`,
`PRIME_SENSITIVITY` aktywowane w odpowiadających operatorach (część in
place z wstecznie kompatybilnym defaultem, część jako nowe funkcje
obok starych — patrz `op_stab_weighted`, `op_spectral_filtered`).

**Uzasadnienie:** to dokładnie wzorzec z §6 — dwie/trzy niezależne
kopie tej samej stałej to nie redundancja-jako-bezpieczeństwo, tylko
odroczony bug (jedna kopia się zmieni, inne nie). Test na to: `grep`
za literałami progu w całym module przed uznaniem "jednego źródła
prawdy" za prawdziwe.

---

### B. Stałe-widma-nigdy-nieosiągalne: `RESONANCE_MAX=1e9` (rozszerza §10 "Physical ceilings vs numeric ceilings")

**Problem:** `RESONANCE_MAX=1e9` w `constants.py` miało reprezentować
sufit "nasycenia" rezonansu, ale teoretyczne maksimum
`op_R_local(window=3)` na bajtach (0–255) to ≈442 — sufit był ~2 000 000×
za duży. Warunek `R < RESONANCE_MAX` był więc praktycznie zawsze
prawdziwy; filtr "nazwany", ale nieoperacyjny (`transition_mask ≈
soft_mask` w praktyce).

**Rozwiązanie:** `theoretical_local_resonance_max(window, byte_max)` =
`byte_max·√window` — sufit wyprowadzony ze skali DANYCH, nie
arbitralna liczba. `op_transition()` liczy teraz
`resonance_max = RESONANCE_MAX_K · theoretical_local_resonance_max(rho_window)`
domyślnie (dostosowuje się do `rho_window`, więc nie rozjeżdża się przy
zmianie parametru). Dla prawdziwego sygnału referencyjnego —
`adaptive_resonance_bounds(values, k)` (pasmo mean±k·σ) jest lepszym
wyborem niż teoretyczny zakres bajtów.

**Uzasadnienie:** to jest dokładnie przypadek z §10 — "sufit liczbowy"
(1e9, bo "duża liczba") pomylony z "sufitem fizycznym" (co realnie
osiągalne dla tego typu danych i tego wzoru). Test na to: policzyć
teoretyczne maksimum/minimum wzoru dla realnej dziedziny danych PRZED
wybraniem stałej granicznej, nie po.

---

### C. Nazwany w teorii, brak w kodzie: "Obszary przejściowe" (nowy wzorzec — teoria/implementacja drift)

**Problem:** `docs/TIMDR_Full_Document_PL.md` §2.4 i `docs/GLOSSARY_EN_PL.md`
definiują "Obszary przejściowe" (Transition Regions — granice między
modalnościami, strefy bifurkacji + wzmacniacze rezonansu) jako
koncepcję rdzenia teorii. W całym `core/` nie było ŻADNEJ funkcji ani
operatora, który by je wykrywał — sprawdzone przez grep za
"transition"/"bifurcation"/"boundary" w kodzie: zero wyników.

**Rozwiązanie:** `op_transition(data, delta_s_soft, delta_s_hard,
resonance_min, resonance_max, ...)` — maski `soft`/`hard` (ΔS ponad
progami) i `transition` (soft ORAZ lokalny rezonans w paśmie),
zgodnie z definicją z §2.4.

**Uzasadnienie:** dokumentacja teoretyczna i kod mogą się rozjechać w
obie strony — nie tylko "kod robi coś, czego teoria nie tłumaczy"
(typowy temat głównego dokumentu), ale też "teoria nazywa mechanizm,
kod nigdy go nie zaimplementował". Test na ten drugi kierunek: grep za
kluczowymi terminami z dokumentacji teoretycznej (glosariusz,
"Pełny Dokument") w kodzie źródłowym, nie tylko odwrotnie.

---

### D. Sprzeczność między dwoma polami klasyfikacji, niewidoczna przy sprawdzaniu ich osobno (rozszerza §6 "Duplication-drift")

**Problem:** przy klasyfikatorze z kilkoma niezależnymi polami (np. reguła +
poziom/miara + skala) każde pole z osobna może przejść walidację, a mimo to
PARA pól łamać własną definicję jednego z nich. Znalezione przy budowie
`docs/theory/Atlas_Paradoksow_TIMDR.md`: reguła "Transition" (z definicji:
zmiana reżimu) współwystępowała w dwóch wierszach z poziomem "TRM=2" (z
definicji: "pojedyncze pęknięcie, bez granicy reżimu do przekroczenia") —
sprzeczność wykryta dopiero przy sprawdzeniu PARY (reguła, TRM) razem, nie
przy weryfikacji każdego pola osobno. Osobno oba pola wyglądały poprawnie.

**Rozwiązanie:** po ustaleniu wartości każdego pola z osobna, dodatkowy
przebieg per parę pól, które mają własne warunki brzegowe: sprawdzić, czy
każda faktycznie występująca kombinacja wartości jest zgodna z definicjami
OBU pól naraz, nie tylko z definicją tego, które akurat się ustala. Przy
okazji tego samego audytu wyszedł pokrewny wzorzec: gdy jeden obiekt ma dwie
poprawne interpretacje RÓŻNEGO RODZAJU (nie tylko różną wartość tej samej
osi — np. podział geometryczny fragment/całość vs podział wg języka opisu),
nie wolno ich wciskać w tę samą kolumnę/pole, bo to chowa różnicę, którą pole
miało ujawniać — potrzebne osobne pole, i to dopiero po drugim, niezależnym
przykładzie tego samego kształtu, nie po pierwszym (żeby nie mnożyć pól na
podstawie jednej obserwacji).

**Uzasadnienie:** to inny przypadek niż duplication-drift z §6 (tam problem
to dwie kopie TEJ SAMEJ stałej), ale ten sam mechanizm ryzyka: coś
niewidocznego, gdy patrzysz na elementy osobno, widoczne dopiero po
sprawdzeniu ich razem. W `core/` odpowiednik: przy rozszerzaniu wyjścia
operatora o nowe pole/etykietę (np. rozszerzenie masek `op_transition`
o nowy powód aktywacji) sprawdzić, czy nowa wartość nie łamie założeń już
istniejącego pola (np. progu), nie tylko czy sama ma sens w izolacji.

---

### E. "Nic nie pasuje" / "łamie wszystko" jako sygnał złego obiektu testowego, nie braku reguły (rozszerza D)

**Problem:** przy klasyfikatorze wieloregułowym dwa razy w tej samej sesji
(budowa `docs/theory/Atlas_Paradoksow_Fizycznych.md`, runda druga) test
"żadna reguła nie pasuje" / "łamie wszystkie reguły" wyszedł fałszywie
dodatni z dwóch różnych, ale spokrewnionych powodów: (1) test pominął
część reguł zestawu, sprawdzając tylko te, które wyglądały na oczywiste
kandydatki (kaskada Kołmogorowa — sprawdzone przeciw 4 z 6 reguł, pominięto
Rezonans i Skręt; Rezonans finalnie okazał się trafną odpowiedzią); (2)
test sprawdzał obiekt zbity z kilku niezależnych, różnych KSZTAŁTEM
elementów naraz, zamiast rozbity na części (trzy "warunki Sacharowa"
bariogenezy przetestowane jako jeden checklist przeciw wszystkim regułom
dały "TRM=0, brak reguła"; dopiero rozbicie na dwie role o różnym kształcie
— lokalny fakt strukturalny vs skumulowana wielkość globalna — ujawniło, że
pasują Defekt i Emergentność).

**Rozwiązanie:** zanim wynik "nic nie pasuje" zostanie przyjęty, dwa
osobne sprawdzenia: (a) czy test faktycznie przeszedł przez KAŻDĄ regułę
zestawu z jej warunkiem falsyfikacji, a nie tylko przez te "oczywiste"; (b)
czy testowany obiekt jest jednym spójnym zjawiskiem o jednym kształcie, czy
kilkoma zjawiskami różnego kształtu zbitymi razem — jeśli to drugie, rozbić
najpierw (po RODZAJU mechanizmu, nie po dowolnej granicy), dopiero potem
testować każdą część osobno.

**Uzasadnienie:** "brak dopasowania" ma dwie zupełnie różne przyczyny —
prawdziwy brak struktury (rzadki, wymaga nowej kategorii) i wadliwy test
(częstszy, wymaga poprawki testu, nie nowej kategorii) — a odróżnienie ich
wymaga właśnie (a)+(b), nie przyjęcia wyniku przy pierwszym przejściu. W
`core/` odpowiednik: zanim `diagnostics.py` zgłosi "żaden wzorzec nie
pasuje" dla danego okna sygnału, sprawdzić, czy okno nie miesza dwóch
różnych reżimów sygnału (np. przejścia i szumu tła naraz) i czy sprawdzone
zostały wszystkie zaimplementowane detektory, nie tylko te najczęściej
trafiające.

---

### F. Test "przeniesione czy nowo wytworzone" jako rozstrzygnięcie Transition vs Emergentność

**Problem:** przy własności globalnej połączonej z czymś lokalnym przez
ciągły mechanizm (przepływ, ekspansję, akumulację) łatwo pomylić dwa różne
przypadki, bo powierzchownie wyglądają tak samo ("coś lokalnego prowadzi do
czegoś globalnego"): własność globalna może być tym samym faktem co
lokalny, tylko przeniesionym/rozciągniętym (jednorodność CMB — obecna już
w małej łatce przed inflacją, inflacja tylko ją rozciąga — reguła
Transition, bez Emergentności), albo może być faktycznie nową strukturą,
nieistniejącą w żadnym pojedynczym elemencie lokalnym (asymetria
barionowa η_B — żaden pojedynczy proces nie ma zdefiniowanej "asymetrii
netto", to pojęcie istnieje tylko jako suma po całej populacji procesów —
reguła Emergentność). Bez jawnego testu obie sytuacje wyglądają identycznie
z zewnątrz ("lokalny mechanizm → globalny efekt").

**Rozwiązanie:** jawne pytanie przed wyborem reguły: czy globalna własność
istniała już (w tej samej postaci) na poziomie lokalnym PRZED zadziałaniem
mechanizmu, a mechanizm tylko ją przenosi/skaluje (→ Transition) — czy
globalna własność nie ma odpowiednika na poziomie pojedynczego elementu
lokalnego w ogóle, i mechanizm ją aktywnie wytwarza przez akumulację/
agregację (→ Emergentność). Ten sam test rozstrzygnął w tej sesji dwa
przykłady w przeciwne strony (Kosmologia → Transition; Bariogeneza →
Emergentność) tym samym pytaniem, nie osobną intuicją za każdym razem.

**Uzasadnienie:** to uszczelnia falsyfikowalność reguły Emergentność
("Nie aktywuje się, jeśli żadna nowa stabilna struktura globalna nie
powstaje") konkretnym pytaniem operacyjnym zamiast oceny "na wyczucie". W
`core/` odpowiednik: przy rozróżnianiu w `op_transition`/`diagnostics.py`
między maską realnie NOWEGO wzorca a maską, która tylko powiela/rozciąga
już wykryty lokalnie sygnał na dłuższe okno — to samo pytanie ("czy okno
większe ujawnia coś, czego nie było w żadnym mniejszym oknie, czy tylko
sumuje to samo") stosuje się wprost.
