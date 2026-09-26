# PREREG — topologia TIMDR jako uzupełnienie widma obwiedni, na łożyskach niewidzianych w uczeniu (CWRU), v0.1

Zamrożone PRZED obliczeniem cech (2026-09-26). Kod: `core/real_cwru_cross_bearing.py`.

## 0. Po co

Wynik Paderborn (`RESULT_PADERBORN_VIBRATION_COMPLEMENT_v0.1.md`, SUPPORTED) miał dwie słabości: jedno łożysko na klasę
i słaby baseline (4 cechy statystyczne). Tu: (a) test na **innych fizycznych łożyskach** niż uczenie, (b) baseline
z **widmem obwiedni** na częstotliwościach charakterystycznych łożyska — standard diagnostyki.

## 1. Dane

Archiwum `CWRU_Bearing_NumPy_4LUM-main.zip` (dostarczone przez użytkownika), kanał DE, 12 kHz, `ORIGINAL_Data/<RPM> RPM/`.
Zadanie: typ uszkodzenia, 3 klasy — IR (bieżnia wewnętrzna), B (kulka), OR@6 (bieżnia zewnętrzna, godz. 6).
Uczenie: rozmiary 7 i 14 milsów; **test: rozmiar 21 milsów** (fizycznie inne łożyska). Osobno dla każdej prędkości
1797 / 1772 / 1750 / 1730 RPM (warunek). Rozmiar 28 pominięty (brak dla OR@6). Normal nie wchodzi (zadanie = typ usterki).
**Ujawnienie:** z tego archiwum wcześniej liczono wyłącznie widmo korelacji DE/FE (membrana, 8 plików); cech statystycznych,
obwiedni ani topologii na nim nie liczono. Na innej kopii CWRU (1797 RPM) topologia rozróżniała normal vs uszkodzenie.

## 2. Cechy

Na plik 16 kolejnych segmentów po 4096 próbek od początku, centrowanych.
- **B (7):** std, kurtoza, crest, entropia widmowa (funkcje jak wcześniej) + widmo obwiedni: e = |hilbert(x)| bez średniej,
  E = |rfft(e · Hann)|; dla f ∈ {BPFI 5,4152, BPFO 3,5848, BSF 4,7135} × f_r (f_r = RPM/60, geometria łożyska 6205 wg CWRU):
  log((A(f) + A(2f)) / mediana(E)), A(·) = maksimum E w paśmie ±3%.
- **T (3):** winding, crossing, phase_winding — mediana z 4 podokien po 512 próbek (próbki 0–2047 segmentu), funkcje bez zmian.
- **BT (10).**
Każdy warunek (RPM) standaryzowany własną średnią/std (bez etykiet). LDA z kurczeniem 0,1. Macro-F1 (losowo 0,33).

## 3. Kryterium główne

g_c = F1(BT) − F1(B) na rozmiarze 21 dla każdego RPM.
**SUPPORTED:** średni g ≥ 0,05 i g > 0 w ≥ 3 z 4 warunków. **NOT SUPPORTED:** średni g ≤ 0. Inaczej **MIESZANY**.
**Sufit:** F1(B) ≥ 0,97 w ≥ 3 warunkach → **INCONCLUSIVE (sufit)**. Opisowo: F1(T), F1 samych cech obwiedni.

## 4. Kontrole

Negatywna: permutacja etykiet uczących (seed 20260926), BT: średni F1 ≤ 0,45. Pozytywna: szum vs szum z impulsami co 64
próbki w segmencie 4096 (100/klasę, połowa do uczenia), BT: F1 ≥ 0,9. Niezaliczona → INCONCLUSIVE.

## 5. Zasady

Jedno uruchomienie; wynik do README GIA-TIMDR niezależnie od werdyktu.
