# PREREG — Paderborn, uszkodzenia naturalne, test na niewidzianych łożyskach: (A) topologia TIMDR jako uzupełnienie,
# (B) membrana jako pole, rezonans jako nałożenie pól (sito), v0.1

Zamrożone PRZED odczytem jakiejkolwiek wartości z nowych archiwów (2026-09-26). Definicja pola/rezonansu/sita
zaakceptowana przez autora idei (J. Kielich) przed zamrożeniem. Kod: `core/real_paderborn_real_damage.py`.

## 1. Dane

Paderborn Bearing Data Center, archiwa pobrane 2026-09-26 do `TIMDR-AI-Core/data/paderborn_candidate/raw/` (SHA-256
w wyniku). **15 łożysk, 5 na klasę:** zdrowe K002, K003, K004, K005, K006; bieżnia zewnętrzna (uszkodzenie z testu
przyspieszonego życia) KA04, KA15, KA16, KA22, KA30; bieżnia wewnętrzna KI04, KI14, KI16, KI18, KI21.
K001/KA01/KI01 (sztuczne) nie biorą udziału. Z każdego łożyska: 4 warunki × pomiary nr 1–5 = 20 pomiarów (300 razem).
Kanały `vibration_1`, `phase_current_1`, `phase_current_2` (64 kHz). Widziane przed zamrożeniem: lista plików w archiwach.

## 2. Przetwarzanie wspólne

Decymacja ×4 (FIR, zero-phase) → 16 kHz. Jeden segment na pomiar: próbki 0–32767 (2,05 s), centrowany.
Prędkość: N15 → 1500 obr/min, N09 → 900 obr/min. Łożysko 6203 (8 kulek, d = 6,75 mm, D = 28,55 mm):
BPFO = 3,054·f_r, BPFI = 4,946·f_r, BSF = 1,997·f_r.

## 3. Test A — topologia TIMDR jako uzupełnienie (kanał drgań)

- **B (7):** std, kurtoza, crest, entropia widmowa (cały segment) + widmo obwiedni (|hilbert|, Hann, cały segment):
  log((A(f) + A(2f)) / mediana) dla BPFO, BPFI, BSF, A = maksimum w paśmie ±3%.
- **T (3):** winding, crossing, phase_winding — mediana z 8 podokien po 512 próbek (próbki 0–4095), funkcje bez zmian.
- Kryterium: g = F1(BT) − F1(B) w każdym z 5 foldów. **SUPPORTED:** średni g ≥ 0,05 i g > 0 w ≥ 4/5.
  **NOT SUPPORTED:** średni g ≤ 0. Inaczej **MIESZANY**. **Sufit:** F1(B) ≥ 0,97 w ≥ 4 foldach → INCONCLUSIVE.

## 4. Test B — pole, rezonans, sito

- **Pole** (osobno drgania, prąd 1, prąd 2): obwiednia e = |hilbert(x)| bez średniej; ramki 4096 próbek, przesunięcie 2048
  (15 ramek), okno Hanna, |rfft|, pasmo 5–500 Hz. Każda komórka zamieniona na percentyl w obrębie swojego pola (0–1).
- **Rezonans:** R = P_drgania · P_prąd1 · P_prąd2 (iloczyn komórka po komórce).
- **Sito:** komórki z R > θ; θ = 95. percentyl R wszystkich komórek zdrowych łożysk **uczących** danego foldu i warunku.
- **Cechy sita S3 (3):** odsetek komórek, które przeszły; średnia częstotliwość komórek przesianych (brak → 250 Hz);
  odsetek przesianych komórek w pasmach ±3% (min. ±1 bin) wokół 1× i 2× BPFO lub BPFI (brak → 0).
- **Sv (3):** te same cechy dla sita z samego pola drgań (R = P_drgania).
- **S1 (czy nałożenie pól coś wnosi):** d = F1(S3) − F1(Sv). **SUPPORTED:** średnie d ≥ 0,05 i d > 0 w ≥ 4/5.
  **NOT SUPPORTED:** średnie d ≤ 0. Inaczej MIESZANY.
- **S2 (uzupełnienie):** g = F1(B + S3) − F1(B), progi jak w teście A.

## 5. Ocena

5 foldów: fold k testuje k-te łożysko każdej klasy (kolejność jak w §1), uczy na pozostałych 4 na klasę — łożyska testowe
nigdy nie są w uczeniu. Każdy warunek standaryzowany własną średnią/std (bez etykiet). LDA z kurczeniem 0,1, równe priory.
Macro-F1 na pomiarach testowych (3 klasy, losowo ≈ 0,33).

## 6. Kontrole (bramka)

- Negatywna: permutacja etykiet uczących (seed 20260926), BT oraz B+S3: średni F1 ≤ 0,45.
- Pozytywna topologii: szum vs szum z impulsami co 64 próbki (segment 4096 dla okien), BT: F1 ≥ 0,9.
- Pozytywna sita: 3 syntetyczne kanały (nośna 1 kHz + modulacja amplitudy 50%): klasa 1 — ta sama modulacja 80 Hz we
  wszystkich; klasa 0 — 60 / 80 / 110 Hz; 20 próbek na klasę; θ z klasy 0: AUC(odsetek przesianych, klasa 1 vs 0) ≥ 0,9.
- Niezaliczona kontrola → INCONCLUSIVE.

## 7. Zasady

Jedno uruchomienie; żadnych zmian po zobaczeniu wyników; wyniki A, S1, S2 trafiają do README GIA-TIMDR niezależnie od werdyktu.
