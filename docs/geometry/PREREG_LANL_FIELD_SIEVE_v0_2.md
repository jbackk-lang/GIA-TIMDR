# PREREG — budynek LANL jako pole + sito (uderzenia zderzaka = cząsteczki), v0.2

Data: 2026-09-27. Zamrożone przed obliczeniem cech sita na tych danych (poza podglądem niżej).
Kod: `core/real_lanl_field_sieve.py`.

## Ujawnienia
- Dane w całości użyte w v0.1 (stare operatory TIMDR: AUC 0,45 / 0,53 — losowo; klasyczne SHM B: 0,99 — sufit).
  Pytanie o wartość dodaną nad B jest tu nierozstrzygalne (sufit) i **nie jest testowane**.
- Podgląd przed zamrożeniem (stany 1, 5, 12, 14, pomiary parzyste): przy uszkodzeniu rośnie energia > 100 Hz i kurtoza
  na kanale 4 (piętro 3, przy zderzaku); zmiana sztywności (stan 5) przesuwa mody. Na tej podstawie wybrano pasma do 160 Hz.

## Konstrukcja (drogowskazy)
Pole = 4 kanały × 5 pasm (5–40, 40–65, 65–90, 90–120, 120–160 Hz). Krok 0 w każdej komórce: cząsteczkowość P (udział 5%
najsilniejszych próbek energii obwiedni). Mapa dualności: uderzenia zderzaka = cząsteczki; masa/sztywność = przesunięcie fali.
Sito: rezonans = odchylenie komórki od pola wzorcowego (nieuszkodzone, mediana/MAD); oczka tylko przy odchyleniu w górę > 1;
Q = log(1 + suma oczek). Bez uczenia na uszkodzeniach. Foldy A/B jak v0.1. Próg alarmu = 95. percentyl Q leave-one-out.

## Hipotezy
- **H1: sito widzi uszkodzenie.** AUC(Q) ≥ 0,90 w obu foldach (stare operatory TIMDR: losowo).
- **H2: swoistość.** Średni odsetek alarmów dla stanów 2–9 (masa, sztywność) niższy niż dla B (kNN, v0.1), przy wykryciu
  stanów 10–17 ≥ 0,8.
- **H3: ciężkość.** Stany 10–14 (szczelina 0,20 → 0,05 mm): Spearman ρ(Q) ≥ 0,5, p < 0,05.
Jedno uruchomienie; wynik do README niezależnie od werdyktu.
