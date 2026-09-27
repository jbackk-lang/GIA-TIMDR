# PREREG — most kolejowy KW51: kotwica modalna K z surowych drgań vs wzmocnienie, v0.1

Data: 2026-09-27. Kod: `core/kw51_modal_anchor.py`. Zamrożone przed ekstrakcją cech z rekordów otoczenia.
Oglądane przed zamrożeniem: readme, skrypty MATLAB autorów, `trackedmodes.mat` (mediany częstotliwości i temperatur
miesięcznych), dostępność kanałów w rekordach.

## Dane
Maes i Lombaert, KW51 (Leuven), Zenodo 10.5281/zenodo.3745914, CC BY-NC-SA. Rekordy drgań otoczenia 300 s, 825,8 Hz:
październik 2018 (przed wzmocnieniem, 143 rekordy) i styczeń 2020 (po wzmocnieniu, 90 rekordów). Wzmocnienie
połączeń przekątnych: 15.05–27.09.2019. Kanały wspólne dla obu miesięcy: pionowe przyspieszenia pomostu aBD11Az, aBD17Az.
Na moście nie ma uszkodzenia — zmiana konstrukcji to wzmocnienie; wg `trackedmodes` przesuwa ono mod 2,93 Hz o ok. +0,06 Hz.

## Reguła wykonalności
Drgania otoczenia = reżim pola; droga przez linie K przy kotwicy. N_cyk (300 s, mody 2,6–6,3 Hz): 770–1900. Kotwica stała
z modelu modalnego (5 modów pionowych z `trackedmodes`, mediana października 2018), samokorekta ±4% w każdym rekordzie.

## Podział i miary
Uczenie: pierwsza połowa rekordów z października 2018. Test „przed”: druga połowa października 2018. Test „po”: styczeń 2020.
AUC (nowość kNN, k = 3): test „przed” vs „po”. Zestawy: T (5 częstotliwości TIMDR), AR(5) na obu kanałach,
SSI (częstotliwości autorów z `trackedmodes`, najbliższa godzina — potok OMA z publikacji).

## Hipotezy
- **H1 (kotwica zgadza się z OMA):** mediana |f_TIMDR − f_SSI| / f_SSI ≤ 1% dla ≥ 4 z 5 modów.
- **H2:** AUC(T) ≥ 0,90 (wykrycie wzmocnienia).
- **H3:** AUC(T) ≥ AUC(AR) − 0,02.
- **H4:** AUC(T) ≥ AUC(SSI) − 0,05 (tak dobrze jak potok OMA autorów).
Ograniczenie: temperatura w październiku 2018 niedostępna (czujnik bez danych); styczeń 2020 bez mrozu (p5 = 2,7 °C).
Jedno uruchomienie; wynik do README niezależnie od werdyktu.
