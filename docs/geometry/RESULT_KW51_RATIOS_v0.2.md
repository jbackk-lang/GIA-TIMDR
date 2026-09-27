# RESULT — KW51: stosunki częstotliwości jako odniesienie z samej stali, v0.2

Pre-rejestracja: `PREREG_KW51_RATIOS_v0_2.md` (commit 1684eea). Jedno uruchomienie. Liczby: `RESULT_KW51_RATIOS_v0_2.json`.
Okres testowy „przed” (1.03–14.05.2019, 1325 pełnych godzin, bez mrozu), „po” wzmocnieniu (959 h).

Rozrzut (MAD, ‰) względnych częstotliwości i |ρ| z temperaturą powierzchni mostu, okres „przed”:

| Mod [Hz] | surowe MAD / ρ | **stosunki** MAD / ρ | termometr (regresja) MAD / ρ |
|---|---|---|---|
| 1,89 | 3,25 / 0,17 | 2,93 / 0,42 | 3,38 / 0,30 |
| 2,57 | 5,02 / 0,04 | 4,25 / 0,12 | 5,05 / 0,09 |
| 2,93 | 1,59 / 0,51 | **0,91 / 0,06** | 1,41 / 0,29 |
| 4,10 | 1,11 / 0,49 | 0,95 / 0,17 | 0,94 / 0,01 |
| 5,34 | 2,32 / 0,46 | **1,25 / 0,15** | 2,18 / 0,39 |
| 6,34 | 2,57 / 0,68 | 1,65 / 0,54 | 2,40 / 0,58 |

- **H1 (temperatura znika): SUPPORTED** — MAD stosunki/surowe mediana 0,74; |ρ(T)| mediana 0,48 → 0,16.
- **H1b (lepiej niż termometr): SUPPORTED** — mniejszy rozrzut niż regresja na temperaturze w 5/6 modów
  (|ρ| termometr 0,29).
- **H3 (wzmocnienie bez fałszywych alarmów): MIXED — sufit.** Wszystkie trzy warianty: 0 fałszywych alarmów, 100% trafień.
  Wzmocnienie jest za duże, żeby rozróżnić metody; ryzyko „skala wchłonie zmianę” się nie spełniło (trafienia 100%).
- Skala s koreluje z temperaturą (ρ −0,51): działa jak termometr ze stali.

## Wniosek
Odniesienie z samej konstrukcji (wspólny czynnik skali częstotliwości) znosi temperaturę lepiej niż regresja na
termometrze — bo reaguje z tą samą bezwładnością co most i nie wymaga czujnika. Warunek fizyczny potwierdzony w obu
mostach: działa przy równym skalowaniu (bez mrozu; Hell Bridge P1), nie przy nierównym (mróz w rozwoju KW51, Hell Bridge P2).
Wykrywanie wzmocnienia nie rozróżnia metod (sufit) — potrzebna mniejsza zmiana konstrukcji (np. Z24, stopniowe uszkodzenia).
