# PREREG — potwierdzenie „klasyczne + topologia TIMDR” na świeżych danych SEU gearset, v0.2

Zamrożone PRZED pobraniem danych (2026-09-26). Kod: `core/real_seu_gearset_confirm.py`.

## 0. Skąd hipoteza

W SEU bearingset v0.1 (`RESULT_SEU_MULTICHANNEL_DIAGNOSTIC_v0.1.md`) analiza **po fakcie** pokazała, że przy standaryzacji
każdego warunku pracy jego własnymi statystykami połączenie klasycznych cech z TIMDR (BT) dało macro-F1 0,95 / 0,81 wobec
0,66 / 0,79 samych klasycznych (B). To jest wynik podejrzany o dopasowanie do danych; tu sprawdzamy go na danych, których
nie oglądaliśmy.

## 1. Dane

SEU `gearbox/gearset` (`cathysiyu/Mechanical-datasets`): `{Health, Chipped, Miss, Root, Surface}_{20_0, 30_2}.csv`
— zdrowe koło i 4 uszkodzenia zęba, dwa warunki pracy. Ta sama przekładnia co bearingset, inne uszkodzenia, pliki nigdy
nieotwierane. Jedna jednostka na klasę (ograniczenie jak w v0.1). SHA-256 plików w wyniku.

## 2. Metoda — identyczna jak v0.1, z jedną zmianą ustaloną w v0.1 po fakcie

Kanały 2–4, okno 512, 100 okien/plik (`round(linspace(0, n − 512, 100))`), centrowanie okien, cechy B (12) i T (10)
dokładnie jak v0.1 (ta sama funkcja `window_features`). LDA z kurczeniem 0,1. **Zmiana:** każdy warunek pracy
standaryzowany własną średnią/std (bez etykiet), dla wszystkich zestawów cech. Kierunki: 20_0→30_2 i 30_2→20_0.

## 3. Kryterium

Zysk g = F1(BT) − F1(B) w każdym kierunku.
**SUPPORTED:** średni g ≥ 0,05 i g > 0 w obu kierunkach. **NOT SUPPORTED:** średni g ≤ 0. Inaczej **MIESZANY**.
**Sufit:** F1(B) ≥ 0,97 w obu kierunkach → **INCONCLUSIVE**.
Opisowo: F1(T), F1(B + topologia bez membrany), F1 w obrębie warunku.

## 4. Kontrole

Negatywna: permutacja etykiet uczących (seed 20260926), BT, oba kierunki: F1 ≤ 0,35. Pozytywna: bramka syntetyczna
membrany (6/6), jak v0.1. Niezaliczona → INCONCLUSIVE.

## 5. Zasady

Jedno uruchomienie. Wynik — jakikolwiek — trafia do README GIA-TIMDR.
