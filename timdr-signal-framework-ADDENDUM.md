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
