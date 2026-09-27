# RESULT — most kolejowy KW51: kotwica modalna K z surowych drgań vs wzmocnienie, v0.1

Pre-rejestracja: `PREREG_KW51_MODAL_ANCHOR_v0_1.md` (commit 81ccb45). Jedno uruchomienie. Liczby: `RESULT_KW51_MODAL_ANCHOR_v0_1.json`.
Uczenie 71 rekordów (X 2018), test „przed” 72 (X 2018), test „po” 90 (I 2020).

| | TIMDR: kotwica K (2 kanały) | AR(5) | SSI autorów (pełny potok OMA) |
|---|---|---|---|
| AUC przed vs po wzmocnieniu | **1,00** | 0,67 | 1,00 |

Zgodność kotwicy z SSI (mediana błędu względnego): 0,26% / 0,03% / 1,3% / 0,08% / 0,07% (mody 2,58 / 2,92 / 4,30 / 5,32 /
6,31 Hz). Przesunięcie po wzmocnieniu (TIMDR vs SSI): −0,010 vs −0,010; +0,068 vs +0,067; +0,279 vs +0,089; +0,122 vs
+0,119; +0,099 vs +0,107 Hz.

- **H1 (zgodność z OMA ≤ 1% dla ≥ 4/5 modów): SUPPORTED** (4/5; mod 4,30 Hz: 1,3% — kotwica przeskakuje na sąsiedni szczyt).
- **H2 (AUC ≥ 0,90): SUPPORTED** (1,00).
- **H3 (≥ AR − 0,02): SUPPORTED** (1,00 vs 0,67).
- **H4 (≥ SSI − 0,05): SUPPORTED** (remis 1,00).

## Zastrzeżenia
- Zadanie jest łatwe dla metod opartych na częstotliwościach: wzmocnienie przesuwa mody o 0,07–0,12 Hz przy rozrzucie
  kilku setnych. SSI też daje 1,00 — to sufit, nie przewaga TIMDR.
- Kotwica modalna to w istocie wyszukiwanie szczytów wokół znanego modelu modalnego (klasyczna technika); wkład TIMDR to
  droga wskazana przez regułę reżimów i samokorekta kotwicy. Z dwóch kanałów odtworzyła wynik pełnego potoku OMA
  (12 kanałów, SSI).
- Temperatura w październiku 2018 niedostępna; w styczniu 2020 bez mrozu (mediana 7,5 °C), więc duży efekt mrozu
  (powyżej opisany przez autorów) nie wchodzi w grę, ale różnica temperatur X/I mogła dodać część przesunięcia.

## Wniosek
Na prawdziwym moście kotwica modalna TIMDR wykrywa zmianę konstrukcji tak dobrze jak potok OMA autorów i znacznie lepiej niż
model AR. Razem z mostem HBTA obraz jest spójny: kotwica widzi zmiany globalnej sztywności (wzmocnienie), gorzej lokalne
uszkodzenia połączeń (HBTA, AUC 0,65).
