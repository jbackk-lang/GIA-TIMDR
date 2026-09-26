# PREREG — sito samokorygujące: rezonans ustala oczka sita (Paderborn, uszkodzenia naturalne), v0.1

Zamrożone po fazie rozwoju, PRZED odczytem pomiarów ewaluacyjnych (2026-09-26). Kod: `core/real_paderborn_resonance_sieve.py`
(funkcja `final`). Zgodne z regułą kalibracji i zamrożenia (`docs/theory/TIMDR_CALIBRATION_FREEZE_RULE.md`).

## 0. Idea (J. Kielich) i konstrukcja

Membrana = pole; rezonans = dana, która ustala oczka sita (samokorekta). Konstrukcja:
- **Pole:** drgania (`vibration_1`, decymacja ×2 → 32 kHz, 2 s) rozłożone na 15 pasm nośnych 1–16 kHz; w każdym paśmie
  obwiednia analityczna.
- **Mapa rezonansu** Rz[pasmo, α]: widmo obwiedni pasma dla α = 5–500 Hz, znormalizowane medianą (tło = 1).
- **Sito Q (osobne oczka dla każdej hipotezy uszkodzenia):** dla k ∈ {BPFO, BPFI}: kolumna j = najsilniejszy rezonans
  w paśmie ±3% wokół 1×k; oczka w_b ∝ max(Rz[b, j] − 1, 0) (normalizowane; zero → równe); przesiane widmo S_k = w·Rz;
  cechy: `Q_k` = log(max S_k przy 1×k + max przy 2×k) i `Q_went_k` = entropia oczek. Razem 4 cechy.

## 1. Faza rozwoju (pomiary 1–5, już oglądane — ujawnienie)

Sprawdzono 3 warianty sita i most geometryczny (krzywizna średnia grzbietu rezonansu, rozciągłość grzbietu).
Macro-F1, 5 foldów łożysk: B (klasyczne + obwiednia) 0,58; ENV (sama obwiednia pełnopasmowa, 3 cechy) 0,64;
wariant 1 (jedno sito, dominująca modulacja) 0,54; geometria sama 0,45 i bez zysku w połączeniach;
**wariant 3 (Q) 0,69** — wybrany. Wybór spośród ~9 zestawów na 300 pomiarach: ryzyko optymizmu, stąd test poniżej.

## 2. Ocena (jednorazowa)

Te same 15 łożysk (5/klasę), pomiary **nr 6–10** w każdym z 4 warunków (300 pomiarów, nigdy nieotwierane).
5 foldów: fold k testuje k-te łożysko każdej klasy. Standaryzacja per warunek (bez etykiet), LDA z kurczeniem 0,1, macro-F1.
B, ENV liczone jak w `PREREG_PADERBORN_REAL_DAMAGE_v0.1.md` (16 kHz, segment 32768).

- **H1 (sito vs klasyczne):** d = F1(Q) − F1(B). **SUPPORTED:** średnie d ≥ 0,05 i d > 0 w ≥ 3/5. **NOT SUPPORTED:**
  średnie d ≤ 0. Inaczej MIESZANY.
- **H2 (czy samokorygujące oczka coś dają ponad zwykłą obwiednię na tych samych częstotliwościach):** d = F1(Q) − F1(ENV),
  progi jak H1.
- Kontrola negatywna: permutacja etykiet uczących (seed 20260926), B+R+G: średni F1 ≤ 0,45. Kontrola pozytywna konstrukcji:
  syntetyczne uderzenia co BPFO w paśmie 5 kHz podnoszą cechę rezonansu BPFO (sprawdzone w rozwoju: 1,1 → 4,6).
- Pozostałe zestawy (R, G, B+Q, …) raportowane opisowo.

## 3. Zasady

Jedno uruchomienie; bez zmian po zobaczeniu wyników; wynik do README GIA-TIMDR niezależnie od werdyktu.
Pomiary 11–20 pozostają nieotwarte jako rezerwa na replikację.
