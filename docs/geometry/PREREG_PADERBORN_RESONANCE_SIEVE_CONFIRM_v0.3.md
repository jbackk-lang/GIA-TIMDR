# PREREG — trzecie potwierdzenie sita samokorygującego, Paderborn, v0.3

Zamrożone PRZED otwarciem pomiarów 16–20 (2026-09-27). Kod: `core/real_paderborn_resonance_sieve.py` (`final_res`).

## 0. Co się nie zmienia
Sito Q, cechy B, ENV i KURT, 5 foldów łożysk, standaryzacja per warunek, LDA z kurczeniem 0,1 — identyczne jak v0.1 i v0.2.
Zmieniono tylko zbiór (`SETS["res"]`) i dodano funkcję oceny. Żadna stała sita nie jest zmieniana.

## 1. Dane
Te same 15 łożysk (5/klasę, uszkodzenia naturalne), pomiary **nr 16–20** w każdym z 4 warunków (300 pomiarów,
nigdy nieotwierane). To ostatnia rezerwa tych łożysk.

## 2. Kryteria (jak v0.2)
d = F1(Q) − F1(X): **SUPPORTED:** średnie d ≥ 0,05 i d > 0 w ≥ 3/5; **NOT SUPPORTED:** średnie d ≤ 0; inaczej MIESZANY.
- **H1:** X = B (klasyczne + obwiednia). **H2:** X = ENV (obwiednia pełnopasmowa). **H3:** X = KURT (kurtogram).
- Kontrola negatywna: permutacja etykiet, średni F1 ≤ 0,45; inaczej INCONCLUSIVE.

## 3. Ocena łączna (nowe, ustalone przed danymi)
15 foldów z trzech prób (6–10, 11–15, 16–20). SUPPORTED: średnie d ≥ 0,05 i d > 0 w ≥ 9/15; NOT SUPPORTED: średnie
d ≤ 0; inaczej MIESZANY. Dla Q vs B i Q vs ENV. Ujawnienie: wyniki dwóch pierwszych prób są znane (Q vs ENV: +0,075
i +0,033), więc łączny próg jest ustalony ze świadomością, że trzecia próba musi dać około +0,04 lub więcej.

## 4. Zasady
Jedno uruchomienie; wynik do README niezależnie od werdyktu.
