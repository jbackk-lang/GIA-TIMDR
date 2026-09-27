# PREREG — most K↔G: kształt modu z fazą + krzywizna, Hell Bridge Test Arena, v0.2

Data: 2026-09-27. Kod: `core/hbta_modal_curvature.py`. Zamrożone przed liczeniem cech na UDS_02 i DS1–DS8.

## Skąd ten test
v0.1 (kotwica K + kształt modu z samych amplitud): AUC 0,65 vs AR 0,79 — NOT SUPPORTED. Brakowało fazy: to ona łączy K z G
(które punkty drgają razem w górę, a które w dół). Most K↔G: K daje częstotliwość kotwicy i fazę względem wibratora,
przejście K→G tworzy rzeczywisty kształt ψ_k na siatce czujników, G liczy jego krzywiznę. Klasyczny odpowiednik:
krzywizna kształtu modu (Pandey i in. 1991), energia odkształcenia modu.

## Ujawnienia
- Dane użyte trzeci raz (v0.1 + widma uczenia). Oglądane przed zamrożeniem: położenia czujników, koherencja kanałów AL
  z wibratorem (AS) na rejestracji uczącej UDS_01.
- Reguła wykonalności (koherencja γ² ≥ 0,8, mediana i 10. percentyl, na UDS_01): zostają kotwice 6,86 / 7,42 / 17,26 /
  24,12 / 30,08 / 32,32 Hz; odpadają 9,40 (0,51) i 12,79 (p10 0,50). Siatka: 4 linie podłużnic × 10 punktów, rozstaw 3,5 m.

## Cechy i detektor
H_i = S_iA / S_AA przy f_k (samokorekta ±4%); ψ = Re(H e^{−iθ}); znak względem średniej uczenia; κ = druga różnica wzdłuż
podłużnicy / h². CDI_k = Σ|κ_k − κ0_k| / Σ|κ0_k|. Detektor kNN (k = 3), okna 60 s, uczenie UDS_01, test UDS_02 vs DS1–DS8
(jak v0.1). Odniesienia w tym samym przebiegu: AR(5) (jak v0.1) i kształt z fazą bez krzywizny (1 − MAC).

## Hipotezy
- **H1:** średnie AUC(krzywizna) po DS1–DS8 > średnie AUC(AR).
- **H2:** średnie AUC(krzywizna) ≥ 0,75 (v0.1 kotwica 0,65 + 0,10).
- **H3:** średnie AUC(krzywizna) dla uszkodzeń pionowych (DS1–4, DS8) > dla stężeń (DS5–7).
- Rozpoznawczo (bez werdyktu): położenie x maksimum zmiany krzywizny dla każdego DS.
Jedno uruchomienie; wynik do README niezależnie od werdyktu.
