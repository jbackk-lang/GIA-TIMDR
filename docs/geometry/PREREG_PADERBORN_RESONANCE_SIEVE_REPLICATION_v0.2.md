# PREREG — replikacja sita samokorygującego + porównanie z kurtogramem, Paderborn, v0.2

Zamrożone PRZED otwarciem pomiarów 11–15 (2026-09-26). Kod: `core/real_paderborn_resonance_sieve.py` (`final_rep`).

## 0. Co się nie zmienia

Sito Q, cechy B i ENV, podział na 5 foldów łożysk, standaryzacja per warunek, LDA z kurczeniem 0,1 — **identyczne jak v0.1**
(`PREREG_PADERBORN_RESONANCE_SIEVE_v0.1.md`, wynik SUPPORTED). Żadna stała sita nie jest zmieniana.

## 1. Dane

Te same 15 łożysk (5/klasę), pomiary **nr 11–15** w każdym z 4 warunków (300 pomiarów, nigdy nieotwierane).
Pomiary 16–20 zostają jako dalsza rezerwa.

## 2. Nowy punkt odniesienia: kurtogram (uproszczony)

Spośród tych samych 15 pasm nośnych wybierane jest pasmo o największej kurtozie widmowej K = E|z|⁴ / (E|z|²)² − 2
(z — sygnał analityczny pasma); z jego obwiedni widmo przy BPFO, BPFI, BSF (log(1× + 2×), ±3%, normalizacja medianą)
+ wartość K. Razem 4 cechy (KURT). To klasyczna zasada wyboru pasma (Antoni), bez pełnego drzewa pasm.

## 3. Kryteria (progi jak v0.1)

d = F1(Q) − F1(X): **SUPPORTED:** średnie d ≥ 0,05 i d > 0 w ≥ 3/5; **NOT SUPPORTED:** średnie d ≤ 0; inaczej MIESZANY.
- **H1:** X = B (klasyczne + obwiednia). **H2:** X = ENV (obwiednia pełnopasmowa). **H3 (nowe):** X = KURT (kurtogram).
- Kontrola negatywna: permutacja etykiet (seed 20260926), średni F1 ≤ 0,45; inaczej INCONCLUSIVE.
- Replikacja uznana za udaną, jeśli H1 i H2 są SUPPORTED. H3 rozstrzyga, czy sito wnosi coś ponad znaną metodę wyboru pasma.

## 4. Zasady

Jedno uruchomienie; wynik do README GIA-TIMDR niezależnie od werdyktu.
