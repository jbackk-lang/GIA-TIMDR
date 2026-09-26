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
