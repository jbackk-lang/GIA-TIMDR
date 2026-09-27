# PREREG — budynek LANL: kotwica modalna K → sito w reżimie fali, v0.3

Data: 2026-09-27. Kod: `core/real_lanl_modal_anchor.py`. Zamrożone przed liczeniem cech H i D na danych
(poza trzema pomiarami stanu 1 do reguły wykonalności, niżej). Dane użyte już w v0.1 i v0.2 — ujawnione.

## Skąd ten test
v0.2: sito cząsteczkowości wykrywało rzadkie uderzenia zderzaka (szczelina 0,15–0,13 mm), gubiło częste
(0,10–0,05 mm): ciężkość ρ = −0,57. Macierz reżimów: częste uderzenia to reżim fali; tam droga prowadzi przez linie
gałęzi K przy kotwicy modalnej, nie przez błyski. To przesunięcie z pola „fala / kotwica wolna” do „fala / śledzona”.

## Reguła wykonalności (stan 1, pomiary 0–2, przed testem)
N_cyk ≈ 1400–1800 (25 s × mod 55/72 Hz) — dużo cykli. Kotwica: śledzona (mody z danych). D w paśmie 90–160 Hz:
1,7–2,9 (pakiet). L_koh ≈ 560–900 < N_cyk — reguła każe „prostować rurę”, ale tu szerokość linii to tłumienie modu przy
losowym wymuszeniu, nie dryf zegara; nie ma czego prostować. **Ograniczenie reguły:** L_koh nie odróżnia tłumienia od
dryfu. Przewidywanie reguły: sito z kotwicą ma szansę.

## Konstrukcja
Kotwica K: fa = max widma ruchu względnego pięter 3−2 w 45–62 Hz, fb w 64–80 Hz (w każdym pomiarze). H = log(moc przy
2fa, 2fb, fa+fb) − log(moc przy fa, fb). Wynik łączny C = max(z(Q_P z v0.2), z(H)), z-score względem nieuszkodzonych
zbioru uczącego; próg alarmu = 95. percentyl C leave-one-out. Foldy A/B jak v0.1.

## Hipotezy
- **H1 (odwrócenie ciężkości):** stany 10–14: Spearman ρ(H, ciężkość) ≥ 0,5, p < 0,05.
- **H2 (dwa reżimy razem):** AUC(C) ≥ 0,95 w obu foldach i fałszywe alarmy stanów 2–9 ≤ klasyczne B.
- **H3 (D rośnie z gęstością uderzeń):** ρ(D, ciężkość) ≥ 0,5, p < 0,05.
Jedno uruchomienie; wynik do README niezależnie od werdyktu.
