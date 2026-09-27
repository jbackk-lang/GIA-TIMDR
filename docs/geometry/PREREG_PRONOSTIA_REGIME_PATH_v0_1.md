# PREREG — PRONOSTIA: droga reżimu wzdłuż życia łożyska (pole → cząsteczka → fala), v0.1

Data: 2026-09-27. Zamrożone PRZED ekstrakcją cech z 11 łożysk Full_Test_Set (pobrane, nieotwierane).
Kod: `core/pronostia_io.py`, `core/pronostia_features.py`, `core/pronostia_eval.py`; parametry: `core/transition_params.py`.

## Dane
IEEE PHM 2012 / FEMTO-ST PRONOSTIA (kopia GitHub `wkzs111/phm-ieee-2012-data-challenge-dataset`). Łożyska do zniszczenia
(próg 20 g), uszkodzenia naturalne i mieszane (dokument: sygnatury częstotliwościowe „nie działają”). 25,6 kHz,
migawka 0,1 s; pobrane co drugie nagranie (co 20 s). Geometria: Z = 13, d = 3,5 mm, Dm = 25,6 mm → BPFO 5,61, BPFI 7,39,
BSF 3,59 × obroty. Rozwój: Learning_set (6 łożysk). Ocena: Full_Test_Set (11 łożysk, pełne życie).

## Reguła wykonalności (przed testem)
N_cyk dla BPFO ≈ 14–17 (okno 0,1 s) — mało; kotwica stała, ale typ uszkodzenia nieznany i mieszany. Przewidywanie:
sito z kotwicą (Q) słabe; droga przez reżim (D, P) ma szansę.

## Cechy (kanał poziomy, mediana ruchoma 15 migawek)
Klasyczne: RMS, kurtoza. TIMDR: P (cząsteczkowość obwiedni 1–12 kHz), D (gęstość zdarzeń η/(1−η)), Q (sito z kotwicą
BPFO/BPFI/BSF, 1×+2×, maks.), K (linie wału 1×+2×). Trend = Spearman ρ(cecha, czas życia).

## Obserwacja z rozwoju
D spada wzdłuż życia (mediana ρ = −0,71): obwiednia przechodzi od tła szumowego („pole”, D ≈ 3,7) do błysków
(cząsteczki). Na końcu D w połowie łożysk wraca w górę (≥ 1,2 × minimum). RMS: ρ = 0,16; kurtoza 0,71; Q 0,36.

## Hipotezy (11 łożysk eval)
- **H1 (pole → cząsteczka):** ρ(D) ≤ −0,3 w ≥ 8/11 łożyskach.
- **H2 (D lepszy trend niż RMS):** mediana(−ρ_D) > mediana(ρ_RMS). Przewidywanie dodatkowe (bez werdyktu): remis z kurtozą
  (|różnica| < 0,1) — D jest miarą impulsowości jak kurtoza.
- **H3 (powrót do fali na końcu):** średnie D z ostatnich 3% życia ≥ 1,2 × minimum D w ≥ 6/11 łożyskach.
- **H4 (reguła wykonalności):** mediana ρ_Q < mediana(−ρ_D) — sito z kotwicą słabsze, jak przewiduje N_cyk ≈ 15.
Jedno uruchomienie; wynik do README niezależnie od werdyktu.
