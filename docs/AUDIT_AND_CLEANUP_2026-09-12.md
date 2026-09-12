# Audyt struktury GIA-TIMDR (2026-09-12)

Audyt struktury plików repo, wykonany PRZED jakąkolwiek reorganizacją
(`signal_pipeline/` itd. — patrz dyskusja w rozmowie) — żeby decyzje o
przenoszeniu/usuwaniu opierały się na tym, co REALNIE tu jest, nie na
założeniach. Metoda: dla każdego kandydata sprawdzono (1) czy ma test w
`tests/`, (2) czy jest importowany/wspominany gdziekolwiek indziej w
repo, (3) czy jest zduplikowany w innym repo ekosystemu. Nic w tym
audycie nie zostało jeszcze ruszone — to lista rekomendacji do Twojej
decyzji, nie wykonane zmiany.

## Streszczenie

| Kategoria | Liczba | Przykłady |
|---|---|---|
| KEEP (żywe, testowane) | core/ (9 plików), filters/_vendor_senscore_gia_filter.py | sg_background.py, trefoil_*.py, geometric_resonance_operator.py |
| OLD — kandydat do etykiety/archiwum | core/{j_compression,pipeline,timdr_core}.py, core/math/resonance_validator.py, filters/timdr_*.py (6 plików) | zero testów, zero referencji z zewnątrz |
| DELETE — silny kandydat | `I2D/` (caly katalog, 9 plikow) | import nieistniejącej funkcji, wszędzie |
| DELETE — pewny (zero ryzyka) | `do_wgrania_docs_filters/` (caly katalog) | tresc juz zduplikowana w docs/filters/ (4/5 identyczne, 5. drobna roznica) |
| DELETE — pewny (zero ryzyka) | 11x plik `z` (1-bajtowy placeholder) w rożnych katalogach | brak tresci, brak referencji |
| DO PRZENIESIENIA / ZARCHIWIZOWANIA | pliki root: PDF/PNG/docx/html/json/txt zwiazane ze starym GitHub Pages | index.html, robots.txt, sitemap.xml, googlec3ea...html, sequence-manifest.json, timdr_ontology.json, tourosomobius.json, auto.js |
| DELETE — kandydat (orphan scripts) | repaired_timdr_parser.py, timdr_benchmark.py, timdr_entropy_tracker.py, MSGKPlotly_v3.py/.html | zero referencji gdziekolwiek |
| WYMAGA TWOJEJ DECYZJI (cross-repo drift) | filters/prime_spectrum_filter.py vs math-validator-3.0/filters/prime_spectrum_filter.py | dwie NIEZALEZNE linie napraw tego samego pliku w dwoch repo - juz znany problem (skill §10), nie rozwiazany tutaj |

## Szczegóły

### `core/` — w większości ŻYWE

| Plik | Test | Referencje | Werdykt |
|---|---|---|---|
| `constants.py` | pośrednio (`test_operators_wiring.py`) | `diagnostics.py`, `operators.py` | KEEP |
| `diagnostics.py` | pośrednio (`test_operators_wiring.py`) | `operators.py` | KEEP |
| `geometric_resonance_operator.py` | `test_geometric_resonance_operator.py` | — | KEEP |
| `operators.py` | `test_operators_wiring.py` | — | KEEP |
| `sg_background.py` | `test_sg_background.py` | — | KEEP |
| `sg_perturbations.py` | `test_sg_perturbations.py` | — | KEEP |
| `sg_shooting.py` | `test_sg_shooting.py` | — | KEEP |
| `trefoil_frenet_torsion.py` | `test_trefoil_frenet_torsion.py` | — | KEEP |
| `trefoil_missing_coordinate_solver.py` | `test_trefoil_missing_coordinate_solver.py` | — | KEEP |
| `trefoil_resonance_model.py` | `test_trefoil_resonance_model.py` | — | KEEP |
| `trefoil_weather_embedding_validation.py` | `test_trefoil_weather_embedding_validation.py` | — | KEEP |
| `j_compression.py` | brak | tylko `pipeline.py`/`__init__.py` (wzajemnie) | **OLD** |
| `pipeline.py` | brak | tylko `timdr_core.py`/`__init__.py` (wzajemnie) | **OLD** |
| `timdr_core.py` | brak | tylko `pipeline.py`/`__init__.py` (wzajemnie) | **OLD** |
| `math/resonance_validator.py` | brak | ZERO (nawet nie importowany) | **OLD lub DELETE** |

`j_compression.py`/`pipeline.py`/`timdr_core.py` tworzą spójne trio
(inny, wcześniejszy "kompresyjny" pomysł na TIMDR: `T→I→M→I(t)→R→E` na
bajtach) — importują się WZAJEMNIE i przez `core/__init__.py`, ale nic
Z ZEWNĄTRZ ich nie używa i nie testuje. To wygląda na wczesny,
porzucony prototyp równoległy do tego, co repo robi dzisiaj
(analiza sygnałów czasowych, nie kompresja bajtów).

### `I2D/` — cały katalog wygląda na martwy szkielet

Wszystkie 9 plików (`ColorPsychMap.py`, `DefectScanner.py`,
`FrameLoader.py`, `FusionEngine.py`, `LayerSplitter.py`,
`ReportEngine.py`, `RhythmAnalyzer.py`, `SpectralOverlayDetector.py`,
`TwistDetector.py`) ma identyczny wzorzec: `from core import
TIMDR_pipeline_full` — **ale `core/__init__.py` eksportuje
`TIMDR_pipeline`, NIE `TIMDR_pipeline_full`**. Sprawdzone wprost w
`core/__init__.py`. Każdy plik w `I2D/` rzuciłby `ImportError` przy
próbie uruchomienia. Zero testów, zero referencji z zewnątrz. Silny
kandydat do usunięcia (albo etykiety "nigdy nieukończony szkic",
jeśli chcesz zachować jako historyczny ślad pomysłu).

### `filters/` — mieszane

| Plik | Test | Referencje | Werdykt |
|---|---|---|---|
| `_vendor_senscore_gia_filter.py` | `test_vendor_senscore_gia_filter.py` | — | KEEP (poprawnie zwendorowane) |
| `prime_spectrum_filter.py` | brak | `docs/timdr-signal-framework.md`, `TRIGGER.md`, `SKILL.md` (opisowo) | KEEP, ale patrz "cross-repo drift" niżej |
| `timdr_complex_stack.py` | brak | tylko sam siebie | **OLD** |
| `timdr_core_pulse.py` | brak | tylko sam siebie | **OLD** |
| `timdr_field_shear.py` | brak | tylko sam siebie | **OLD** |
| `timdr_filter_gradient_heavy.py` | brak | ZERO (nawet sam siebie nie wspomina) | **OLD/DELETE** |
| `timdr_star_core.py` | brak | tylko sam siebie | **OLD** |
| `timdr_torus_map.py` | brak | tylko sam siebie | **OLD** |

Te 6 plików `timdr_*.py` to male (500B-4KB), nietestowane, nigdzie
niecytowane szkice filtrów — wygladaja na wczesne eksperymenty
sprzed etapu, w ktorym repo zaczelo egzekwowac protokol
preregistracja+kontrola+test (`docs/PROTOCOL.md`-analog dla tego repo).

**Cross-repo drift (nierozwiazane tutaj, tylko odnotowane)**:
`filters/prime_spectrum_filter.py` i
`../math-validator-3.0/filters/prime_spectrum_filter.py` to DWIE
NIEZALEZNE linie napraw tego samego pierwotnego pliku (145 linii roznicy,
kazda strona twierdzi ze ma inna/kolejna naprawe) — to juz znany typ
problemu w tym ekosystemie (`timdr-signal-framework` skill, §10,
"duplication-drift"). Rozstrzygniecie ktora wersja jest "prawdziwa" i
synchronizacja to OSOBNE zadanie, nie czesc tego audytu strukturalnego.

### `do_wgrania_docs_filters/` — bezpieczny DELETE

Nazwa doslownie znaczy "do wgrania" (staging, nigdy niewgrane do
docs/). Porownanie plik-po-pliku z `docs/filters/`:

- `README_filter.md`, `al_filter_predictions.md`,
  `mobius_ratio_filter.md`, `prime_position_filter.md`: **bajt w bajt
  identyczne** z odpowiednikami w `docs/filters/`.
- `prime_spectrum_filter.md`: 9 linii roznicy (docs/filters/ wersja
  wyglada na nowsza/dopracowana).

Cala zawartosc juz istnieje gdzie indziej — ten katalog mozna usunac
bez utraty czegokolwiek.

### 11x plik `z` — bezpieczny DELETE

Jednobajtowe pliki-placeholdery (`core/z`, `core/math/z`, `filters/z`
[juz usuniety wg historii gita — `91c326d Delete filters/z`, ale
odtworzony pozniej?], `docs/z`, `docs/concepts/z`, `docs/diagrams/z`,
`docs/filters/z`, `docs/geometry/z`, `docs/models/z`, `docs/theory/z`,
`I2D/z`, `timdr_visualizer/z`) — najprawdopodobniej sluzyly kiedys do
zachowania pustych katalogow w git (ktory nie sledzi pustych folderow).
Zero tresci, zero funkcji. Bezpieczne do usuniecia hurtowo.

### Top-level clutter (root repo)

Grupa plikow, ktore wygladaja na pozostalosc po hostowaniu tego repo
jako strony (GitHub Pages) — `index.html`, `robots.txt`, `sitemap.xml`,
`googlec3ea479e8d9238d7.html` (weryfikacja Google Search Console),
`sequence-manifest.json`, `timdr_ontology.json`, `tourosomobius.json`,
`auto.js` — ekosystem ma juz dedykowane repo do tego
(`jbackk-lang.github.io`, widoczne w tym samym katalogu nadrzednym), wiec
to prawdopodobnie zdublowane/przestarzale. Rekomendacja: przeniesc do
`archive/` lub usunac po potwierdzeniu, ze `jbackk-lang.github.io` jest
aktualnym zrodlem prawdy dla strony.

Osobne, calkiem osierocone skrypty (zero referencji gdziekolwiek):
`repaired_timdr_parser.py`, `timdr_benchmark.py`,
`timdr_entropy_tracker.py`, `MSGKPlotly_v3.py` (+ jego wygenerowany,
5MB `MSGKPlotly_v3.html`). Kandydaci do `archive/` albo usuniecia.

`_local_diff.txt` (56KB) wyglada na zrzut diffa z jakiejs wczesniejszej
sesji roboczej, nie na czesc repo — kandydat do usuniecia.

## Co NIE zostalo ruszone

Ten audyt jest CZYSTO informacyjny — zaden plik nie zostal przeniesiony
ani usuniety. `docs/theory/` (aksjomaty), `docs/concepts/`,
`docs/diagrams/`, `docs/models/` nie zostaly szczegolowo audytowane
plik-po-pliku (sa to w wiekszosci dokumenty teoretyczne/spekulacyjne,
juz jawnie oznaczone w README jako takie) — jesli chcesz, mozna to
zrobic w kolejnym przebiegu.
