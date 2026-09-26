# PREREG — diagnostyka wielokanałowa TIMDR na innym stanowisku niż CWRU (SEU gearbox, bearingset) v0.1

Zamrożone PRZED obliczeniem jakiejkolwiek cechy na tych danych (2026-09-26). Kod:
`core/real_seu_multichannel_bridge.py` (commitowany razem z tym plikiem, przed pierwszym uruchomieniem na danych).

## 0. Pytanie

Czy cechy TIMDR, które zadziałały na łożyskach CWRU (membrana `spectral_concentration` na rodzinie kanałów,
trójka topologiczna winding/crossing/phase_winding), (H1) rozdzielają stan zdrowy od uszkodzeń na innym stanowisku
i (H2) wnoszą informację ponad klasyczne cechy, gdy klasyfikator musi przenieść się na inne warunki pracy?

## 1. Dane

Southeast University (SEU) Drivetrain Dynamics Simulator, `gearbox/bearingset` z repozytorium
`cathysiyu/Mechanical-datasets` (GitHub, gałąź master). 10 plików: `{health, ball, inner, outer, comb}_{20_0, 30_2}.csv`
(klasa × warunek prędkość-obciążenie 20 Hz/0 V i 30 Hz/2 V). Kopia lokalna: `DATA/seu_bearingset/` (poza repo);
SHA-256 plików zapisane w wyniku. Kanały wg README źródła: 1 wibracja silnika, 2-4 wibracja przekładni planetarnej x/y/z,
5 moment silnika, 6-8 wibracja przekładni równoległej x/y/z; README: „kanały 2, 3, 4 są efektywne”.
Częstotliwość próbkowania 5120 Hz (nagłówek: Frequency Limit 2000 Hz, 1600 linii → 2,56 × 2000).

**Co widziałem przed zamrożeniem (ujawnienie):** nagłówek pliku `health_20_0.csv`, README źródła i pierwszy wiersz danych
każdego pliku (sprawdzenie formatu: `ball_20_0` jest rozdzielany przecinkami, pozostałe tabulatorami). Ten pierwszy wiersz
pokazał, że pliki `health_*` i `comb_*` mają duże przesunięcie DC (kanał 1 ≈ −2,5, kanały 2-4 ≈ −0,4), a pozostałe ≈ −0,1 —
ślad innej konfiguracji akwizycji, który trywialnie zdradza klasę. Dlatego każde okno jest centrowane per kanał (§2).
Żadnej cechy ani statystyki poza tym pierwszym wierszem nie liczyłem.

**Ograniczenie z góry:** jedna fizyczna jednostka na klasę. H1/H2 nie dowodzą uogólnienia na inne łożyska; H2 testuje
przeniesienie między warunkami pracy tej samej jednostki.

## 2. Okna

Kanały 2, 3, 4. Okno W = 512 próbek (0,1 s), 100 okien na plik, początki `round(linspace(0, n − W, 100))`
(bez nakładania). W każdym oknie od każdego kanału odejmowana jest jego średnia. Kanał główny dla cech jednokanałowych:
wszystkie trzy (cecha liczona osobno na kanałach 2, 3, 4).

## 3. Cechy

- **T (TIMDR, 10):** `spectral_concentration` macierzy korelacji kanałów 2-4 (`timdr_geometry.spectral_family`,
  bez zmian) + `winding_metric_fn`, `crossing_metric_fn` (`core/winding_crossing_ms_bridge.py`) i `phase_winding_fn`
  (`core/phase_winding_oam_ms_bridge.py`) na każdym z kanałów 2, 3, 4 — funkcje bez zmian.
- **B (klasyczne, 12):** na każdym z kanałów 2, 3, 4: odchylenie standardowe (RMS AC), kurtoza nadwyżkowa,
  crest factor (max|x|/std), entropia widmowa (widmo mocy okna z oknem Hanna, bez składowej DC, znormalizowana do [0,1]).
- **BT:** B ∪ T (22).

## 4. H1 — rozdzielanie (replikacja kierunku z CWRU v0.2)

`spectral_concentration`, zdrowy vs każdy z 4 uszkodzeń, osobno w każdym warunku: 8 komórek, 100 vs 100 okien.
Mann-Whitney dwustronny, α = 0,05/8. r = rank-biserial, dodatni = zdrowy > uszkodzony (kierunek CWRU v0.2).
**SUPPORTED:** ≥ 6/8 komórek istotnych z r ≥ 0,3. **ODWROTNY:** ≥ 6/8 istotnych z r ≤ −0,3. Inaczej **NOT SUPPORTED**.
Trójka topologiczna: ta sama siatka, raport opisowy (kierunek nie był ustalony na CWRU dla tej konfiguracji).

## 5. H2 — wartość dodana przy zmianie warunków (test główny)

Klasyfikacja 5 klas. Kierunek A: uczenie na 20_0, test na 30_2; kierunek B: odwrotnie. Klasyfikator: LDA z kurczeniem
(standaryzacja średnią/std zbioru uczącego; kowariancja wewnątrzklasowa Σ, Σ_s = 0,9 Σ + 0,1 (tr Σ / p) I; równe priory),
czysty numpy, bez strojenia. Miara: macro-F1.
**SUPPORTED:** F1(BT) − F1(B) ≥ 0,05 w obu kierunkach. **NOT SUPPORTED:** < 0,05 w obu. Inaczej **MIESZANY**.
Dodatkowo raportowane: F1(T) vs F1(B) (czy TIMDR sam jest lepszy od klasycznych) i sufit w obrębie warunku
(uczenie na oknach 0-49, test na 50-99 każdego pliku) — opisowo, bez werdyktu.

## 6. Kontrole (bramka przed H1/H2)

- Pozytywna: `run_synthetic_controls()` ze `spectral_family` — wszystkie 6 komórek `passed=True`, jak w RESULT membrany v0.1.
- Negatywna: etykiety zbioru uczącego permutowane (seed 20260926), BT, oba kierunki: macro-F1 ≤ 0,35 (losowo 0,2).
- Jeśli któraś kontrola nie przejdzie: wynik INCONCLUSIVE, H1/H2 nieinterpretowane.

## 7. Dodatkowo (opisowo)

Spearman między `spectral_concentration` a średnim |r| par kanałów — dla N = 3 membrana jest funkcją trzech korelacji,
więc sprawdzamy, czy nie jest po prostu średnią korelacją pod inną nazwą.

## 8. Zasady

Jedno uruchomienie. Żadnej zmiany okna, kanałów, cech, klasyfikatora, progów po zobaczeniu wyników. Wynik negatywny
jest pełnoprawnym wynikiem.
