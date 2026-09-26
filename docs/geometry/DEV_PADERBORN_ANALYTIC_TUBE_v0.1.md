# Rozwój (nie test formalny) — geometria rury analitycznej ponad sito Q, Paderborn, 2026-09-26

Kod: `core/real_paderborn_tube.py`. Dane rozwojowe: pomiary 1–5 (już oglądane), 15 łożysk, 5 foldów łożysk, jak w teście sita.
Cechy rury (per hipoteza BPFO/BPFI, ważone oczkami sita): widmo skrętu rury przy częstotliwości uszkodzenia (FM),
głębokość oddechu std(A)/mean(A), kurtoza promienia.

| Zestaw | macro-F1 |
|---|---|
| sito Q | 0,687 |
| same cechy rury | 0,422 |
| Q + cechy rury | 0,657 |
| Q + skręt rury | 0,678 |

**Wniosek rozwojowy:** w tej postaci geometria rury nie dodaje informacji ponad sito (które już czyta oddech rury).
Zgodnie z zasadą opłacalności **nie** wydajemy na tę hipotezę ostatniej rezerwy (pomiary 16–20) — nie przeszła
nawet fazy rozwoju. Rura pozostaje poprawnym, odwracalnym mostem opisu (`docs/theory/TIMDR_Analytic_Tube.md`),
ale jej dodatkowe wielkości nie są tu nowym źródłem sygnału.

## Druga próba rozwojowa: synchroniczność oddechu wiązki rur (rezonans jako nałożenie pól)

Kod: `core/real_paderborn_tube_sync.py`. Dla częstotliwości uszkodzenia f* (szczyt przesianego widma): zespolona amplituda
oddechu każdej rury C_b; PLV = zgodność fazy oddechu we wszystkich pasmach, COH = zgodność w pasmach przepuszczonych
przez sito. Kontrola syntetyczna: uderzenia dzwoniące w 3 pasmach → PLV 0,07 → 0,96 (mechanizm działa).

| Zestaw | macro-F1 (pomiary 1–5) |
|---|---|
| sito Q | 0,687 |
| sama synchroniczność rur | 0,547 |
| Q + synchroniczność | 0,639 |

Synchroniczność sama niesie sygnał (0,55 — poziom klasycznych cech), ale niczego nie dodaje do sita. Rezerwa 16–20
nadal nieużyta.
