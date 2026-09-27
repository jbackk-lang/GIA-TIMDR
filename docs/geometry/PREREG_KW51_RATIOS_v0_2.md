# PREREG — KW51: stosunki częstotliwości jako odniesienie z samej stali (bez termometru), v0.2

Data: 2026-09-27. Kod: `core/kw51_ratios.py` (`final()`). Zamrożone PRZED liczeniem czegokolwiek na okresach testowych.
Jedno uruchomienie: `python core/kw51_ratios.py`.

## Idea (autor) i fizyka
Temperatura reaguje wolno, a termometr w powietrzu mierzy nie ten obiekt. Odniesienie z samej stali: równa zmiana E
skaluje wszystkie częstotliwości jednym czynnikiem s(t) = mediana_k f_k(t)/f_k,ref; f̃_k = f_k / s znosi ten czynnik
(stereoskopia częstotliwości). Warunek: tylko równe skalowanie — poniżej 0 °C zamarzanie podsypki/gruntu zmienia
sztywność nierówno. Hell Bridge v0.5: działało na P1 (4 °C), nie na P2 (zmiana nierówna).

## Dane
`trackedmodes.mat` (Maes i Lombaert, KW51): częstotliwości 14 modów co godzinę (SSI autorów), X 2018 – I 2020, temperatura
powierzchni mostu `tBD31A`. Wcześniej oglądane: mediany miesięczne częstotliwości i temperatur (v0.1). Mody (braki < 35%):
1,89 / 2,57 / 2,93 / 4,10 / 5,34 / 6,34 Hz.
Okresy: **baza** 1.12.2018–28.02.2019 (rozwój, 131 h mrozu); **przed** 1.03–14.05.2019 (test, bez mrozu);
**po** 28.09.2019–15.01.2020 (po wzmocnieniu, test, bez mrozu). Liczebności godzin i mrozu sprawdzone przed zamrożeniem.

## Ujawnienia z rozwoju (baza)
- T > 0 °C: MAD względnych częstotliwości spada po normalizacji w 5/6 modów (np. 2,93 Hz: 1,79 → 0,95 ‰; 6,34 Hz:
  2,73 → 1,49 ‰); |ρ z T| mediana 0,48 → 0,27. Regresja na termometrze prawie nie zmniejsza rozrzutu (1,79 → 1,67 ‰).
- T ≤ 0 °C: normalizacja pomaga częściowo, ale rozrzut zostaje 2–10 × większy (warunek równego skalowania złamany).
  **Mrozu brak w okresach testowych — warunek zimowy tylko opisowo z rozwoju.**
- Skala s koreluje z temperaturą (ρ −0,63): s działa jak termometr ze stali.

## Hipotezy (test)
- **H1 (temperatura znika, okres „przed”):** mediana po modach MAD(stosunki)/MAD(surowe) < 0,8 ORAZ mediana |ρ(T)|
  stosunki < surowe. Oba → SUPPORTED, jedno → MIXED.
- **H1b:** MAD(stosunki) < MAD(regresja na termometrze) w ≥ 4/6 modów → SUPPORTED.
- **H3 (wzmocnienie widać bez fałszywych alarmów):** nowość kNN (k = 3, mediana/MAD, uczenie: co 3. pełna godzina bazy),
  próg = p99 nowości LOO w bazie. Stosunki: fałszywe alarmy „przed” < surowe ORAZ trafienia „po” ≥ 0,9 → SUPPORTED;
  jedno → MIXED. Ryzyko z góry: jeśli wzmocnienie przesunęło większość modów równo, skala je wchłonie.
- Raport: detekcja dla regresji z termometrem; korelacja s z T w okresie „przed”.
