# PREREG — orbita prądów silnika (wektor α–β) jako prawdziwa trajektoria dla TIMDR, Paderborn, v0.1

Zamrożone PRZED odczytem jakiejkolwiek wartości prądów (2026-09-26). Kod: `core/real_paderborn_current_orbit.py`.

## 0. Hipoteza (sformułowana po wynikach CWRU/SEU/LANL — ujawnione)

TIMDR „coś widzi” tylko wtedy, gdy sygnał zawiera ruch wirujący. Prądy trójfazowe po transformacji Clarke'a dają fizycznie
wirujący wektor (α, β) — prawdziwą trajektorię 2D zamiast sztucznego osadzenia jednego kanału. Pytania:
(H1) czy cechy TIMDR wnoszą coś ponad klasyczną diagnostykę prądową (metoda wektora Parka + cechy fazowe);
(H2) czy metryki TIMDR na prawdziwej orbicie α–β są lepsze niż te same metryki na osadzeniu pojedynczego kanału.

## 1. Dane

Paderborn Bearing Data Center, archiwa lokalne `TIMDR-AI-Core/data/paderborn_candidate/raw/{K001,KA01,KI01}.rar`
(zdrowe / sztuczne uszkodzenie bieżni zewnętrznej EDM / wewnętrznej EDM; jedno łożysko na klasę — ograniczenie).
Pomiary wyłącznie z zamrożonego podziału `TIMDR-AI-Core/prereg/PADERBORN_MS_REPLICATION_v0.1.json`
(SHA-256 `f72623c68918b48c896c31824ac0c984565dd22b3a0dc7af399aba4228a96cf9`), tylko `train` + `calibration` (192 pomiary, 64/klasę). **Pomiary `holdout` tego
podziału nie są otwierane** (należą do tamtej, niezakończonej pre-rejestracji).
Kanały `phase_current_1`, `phase_current_2` (64 kHz, 4 s). Widziane przed zamrożeniem: nazwy pól i długości tablic jednego
pliku; wartości prądów — nie. Wcześniejsze prace w AI-Core czytały z tych pomiarów wyłącznie `vibration_1`.

## 2. Przetwarzanie

i3 = −(i1 + i2). Clarke (niezmiennik amplitudy): α = i1, β = (i1 + 2·i2)/√3. Decymacja ×16 (dwa kroki ×4,
`scipy.signal.decimate`, FIR, zero-phase) → 4 kHz. Okna 512 próbek (128 ms), 4 kolejne okna od początku zapisu na pomiar
(768 okien). W oknie od α, β, i1, i2 odejmowana jest średnia.

## 3. Cechy (na okno)

- **B (klasyczne, 12):** metoda wektora Parka: moduł |i| = √(α²+β²) — std/średnia, kurtoza modułu, entropia widmowa modułu;
  stosunek osi elipsy (√(λ_min/λ_max) kowariancji α–β, miara składowej przeciwnej). Na i1 i i2: RMS, kurtoza, crest factor,
  entropia widmowa.
- **T_orbit (2):** winding orbity α–β (|Δ kąta po rozwinięciu|/2π) i crossing number orbity α–β (ten sam algorytm
  przecięć niesąsiednich odcinków co `crossing_metric_fn`, ale na prawdziwej trajektorii 2D, bez osadzenia i PCA).
- **T_1D (6):** `winding_metric_fn`, `crossing_metric_fn`, `phase_winding_fn` na i1 i na i2 (bez zmian).
- **T = T_orbit ∪ T_1D (8), BT = B ∪ T (20).**

## 4. Ocena

Warunki pracy: N15_M07_F10, N09_M07_F10, N15_M01_F10, N15_M07_F04. Leave-one-condition-out: uczenie na 3 warunkach,
test na czwartym (4 foldy). Każdy warunek standaryzowany własną średnią/std (bez etykiet — lekcja z SEU). Klasyfikator:
LDA z kurczeniem 0,1 (jak SEU v0.1), klasy z równymi priorami. Miara: macro-F1 (losowo ≈ 0,33).

- **H1 (wartość dodana):** Δ = F1(BT) − F1(B). **SUPPORTED:** średnia Δ ≥ 0,05 i Δ > 0 w ≥ 3/4 foldów.
  **NOT SUPPORTED:** średnia Δ ≤ 0. Inaczej **MIESZANY**. **Sufit:** jeśli F1(B) ≥ 0,97 w ≥ 3 foldach → **INCONCLUSIVE**.
- **H2 (orbita vs osadzenie):** **SUPPORTED:** średni F1(T_orbit) ≥ średni F1(T_1D) + 0,05. **NOT SUPPORTED:** ≤ F1(T_1D).
  Inaczej **MIESZANY**. Opisowo: F1(T) vs F1(B), F1(B ∪ T_orbit).

## 5. Kontrole (bramka)

- Pozytywna (syntetyczna): prądy trójfazowe 50 Hz przy 4 kHz + szum 5%, klasa 0 zrównoważone, klasa 1 z 10% składowej
  przeciwnej; 100 okien/klasę, uczenie na połowie, BT: macro-F1 ≥ 0,9; winding orbity zrównoważonej = 6,4 ± 0,2
  (50 Hz × 0,128 s).
- Negatywna: permutacja etykiet uczących (seed 20260926), BT, wszystkie foldy: średni F1 ≤ 0,45.
- Niezaliczona kontrola → INCONCLUSIVE.

## 6. Zasady

Jedno uruchomienie, bez zmian po zobaczeniu wyników. Metoda wektora Parka jest znana od lat 90.; TIMDR ma ją pobić lub
uzupełnić, a nie zastąpić nazwą.
