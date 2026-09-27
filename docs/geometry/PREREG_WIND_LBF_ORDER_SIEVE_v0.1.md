# PREREG — turbina wiatrowa Fraunhofer LBF: sito w osi kątowej (zegar = sygnał modalny) vs stała prędkość, v0.1

Zamrożone PRZED odczytem nagrań ewaluacyjnych (2026-09-27). Kod: `core/wind_lbf_io.py`, `core/wind_lbf_sieve.py`
(`segment_rows`), ocena: `core/wind_lbf_eval.py`. Dane rozwojowe i ich wyniki: `DEV_WIND_LBF_v0.1.json`.

## 0. Idea i zmiana planu (ujawnienie)

Idea (J. Kielich): sygnał modalny ustawia zegar, polowy niesie uszkodzenie; samonaprawa modelu prostuje rurę wzdłuż.
**Pierwotna hipoteza — śledzenie prędkości z samych drgań — odpadła w fazie rozwoju:** na 5 nagraniach błąd względem
tachometru 40–200% (także z globalną ścieżką Viterbiego i liniami odniesienia wybranymi w rozwoju). Wirnik 0,2–0,9 obr/s,
linie obrotowe 2–5× ponad tło, energia głównie w rzędach parzystych (drgania „udają” podwójną prędkość).
Dlatego **zegarem jest tachometr** (108 imp./obr.) — sygnał modalny z czujnika. Test sprawdza sito w osi kątowej
(„rura wyprostowana wzdłuż”) wobec sita przy stałej prędkości.

## 1. Dane

Fraunhofer LBF (Zenodo 10.5281/zenodo.11820598, CC BY 4.0): Healthy.zip, Bearing.zip (Imbalance_Mid.zip nieużywany
w tym teście). Kanał `brng_f_y` (akcelerometr łożyska przedniego, 74 kHz), łożysko 6007 2Z, 11 kulek:
BPFO = 4,593, BPFI = 6,407, BSF = 5,995 rzędu obrotu. **Podział:** w każdej klasie pierwsza trzecia nagrań (kolejność
czasowa) = rozwój (oglądane), reszta = ocena (nieotwierana). Każda klasa nagrana innego dnia — stąd nacisk na
**swoistość** (czy zapala się właściwy rząd) zamiast samej klasyfikacji między dniami.

## 2. Cechy (bez zmian od rozwoju)

Segmenty 60 s (do 5 na plik; plik krótszy = jeden segment), pominięcie segmentów < 10 obrotów. Decymacja ×4 (18,5 kHz),
8 pasm nośnych 1–9 kHz, obwiednie. **QO_k**: mapa rezonansu w rzędach (oś kątowa z tachometru, 64 próbki/obrót,
rzędy 0,5–30), sito z oczkami przy rzędzie k. **QH_k**: to samo w Hz przy stałej prędkości = mediana tachometru w segmencie
(0,2–60 Hz). k ∈ {BPFO, BPFI, 2×BSF}. Klasyczne: kurtoza, RMS segmentu.

## 3. Hipotezy (jednostka: segment ewaluacyjny)

- **H1 (sito kątowe wykrywa uszkodzenie bieżni zewnętrznej):** AUC(QO_BPFO; OuterRace vs Healthy) ≥ 0,90.
- **H2 (oś kątowa daje swoistość, której brak przy stałej prędkości):** AUC_sw(QO_BPFO) − AUC_sw(QH_BPFO) ≥ 0,10, gdzie
  AUC_sw = AUC(Q_BPFO; OuterRace vs wszystkie segmenty nie-OuterRace: Healthy + InnerRace + RollerElement).
- **Kontrola zakłócenia dniem:** AUC(QO_BPFI; OuterRace vs Healthy) w [0,25; 0,75] — niepasujący rząd nie może rozróżniać
  dni; poza zakresem → wynik H1 oznaczony jako podejrzany o zakłócenie.
- Opisowo (bez werdyktu): AUC(QO_BPFI; InnerRace vs Healthy), AUC(QO_BSF2; RollerElement vs Healthy) — w rozwoju brak
  sygnału; klasyczne KURT/RMS: AUC OuterRace vs Healthy i AUC_sw (podatne na dzień); różnica QO_BPFO − QO_BPFI w segmentach OR.

## 4. Zasady

Jedno uruchomienie; bez zmian po zobaczeniu wyników. Ograniczenia z góry: jedna turbina; uszkodzenia wytrawione;
OuterRace ma tylko 2 nagrania ewaluacyjne (5 min + 30 s) → mało segmentów; każda klasa to inny dzień.
