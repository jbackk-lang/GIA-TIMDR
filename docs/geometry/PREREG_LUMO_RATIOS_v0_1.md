# PREREG — LUMO: stosunki częstotliwości w różnych porach roku + wykrywanie usuniętych stężeń, v0.1

Data: 2026-09-27. Kod: `core/lumo_io.py`, `core/lumo_ratios.py` (`final()`). Jedno uruchomienie: `python core/lumo_ratios.py`.

## Dane
LUMO (Leibniz University Test Structure for Monitoring, wieża kratowa 9 m, CC-BY 3.0), sześć paczek przykładowych:
DAM3/DAM4/DAM6 × {111 = cały poziom stężeń usunięty, 010 = jeden pręt}; w każdej 5 bloków 10-min zdrowych przed
uszkodzeniem i 5 z uszkodzeniem (X 2020 – VI 2021). 18 kanałów przyspieszeń, temperatura stali temp01 (−3,7 … 40,4 °C).
**Rozwój:** dam6_111 (X 2020, 7–15 °C). **Test:** pozostałe 50 bloków (25 zdrowych z XI, III, V, VI; 25 uszkodzonych).

## Ujawnienia z rozwoju
1. Kotwice ze średniego widma zdrowych bloków rozwoju (prominencja ≥ 2, odstęp ≥ 8%): 2,82 / 13,41 / 16,33 / 39,62 /
   71,42 / 92,29 / 101,01 / 117,39 Hz; samokorekta ±4%.
2. **Podejrzane przed zamrożeniem (ujawnione):** korelacja częstotliwości z temperaturą na WSZYSTKICH zdrowych blokach,
   także testowych: ρ po modach −0,54 … +0,31 (różne znaki), ρ(czynnik skali s, T) = −0,19. To znaczy, że zmiana
   temperaturowa tej wieży NIE jest równym skalowaniem — warunek stosunków może być złamany.
3. Rozwój: DAM6_111 przesuwa mody silnie (13,41 → 13,82; 71,55 → 68,72 Hz) — łatwe.

## Metoda i hipotezy
Warianty: surowe (f/f_ref − 1), **stosunki** (podzielone przez wspólny czynnik skali = mediana f/f_ref), termometr
(regresja liniowa na temp01 dopasowana na 5 zdrowych blokach rozwoju — ekstrapolacja poza 7–15 °C, tak jak w praktyce
przy krótkim okresie bazowym). Detektor: nowość kNN (k = 3, mediana/MAD bazy = zdrowe bloki rozwoju).
- **H1 (odporność na porę roku):** AUC uszkodzone vs zdrowe (cały test): stosunki − surowe > +0,02 → SUPPORTED;
  −0,02 … +0,02 MIXED; niżej NOT.
- **H2 (pojedynczy pręt, przypadki 010):** stosunki > surowe w AUC w ≥ 2/3 przypadków → SUPPORTED.
- Opisowo: ρ(s, T) na zdrowych blokach testu; fałszywe alarmy przy progu p95 nowości bazy.

## Przewidywanie
Z ujawnienia 2: **H1 NOT SUPPORTED lub MIXED** (nierówne skalowanie). Wynik trafia do README niezależnie od werdyktu.
