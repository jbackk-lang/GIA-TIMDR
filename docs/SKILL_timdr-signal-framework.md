---
name: timdr-signal-framework
description: Zwięzła ściąga GIA-TIMDR: czym jest TIMDR, gałęzie, drogowskazy budowy analizy, mosty, zasada odniesienia, parametry przejść, protokół testów i aktualny stan wyników. Używaj przy każdej pracy nad teorią, kodem lub testami TIMDR.
---

# TIMDR — ściąga (stan 2026-09-28)

Szczegóły zawsze w repo `jbackk-lang/GIA-TIMDR` (README: tabela wyników; `docs/theory/*`; pary `PREREG_*`/`RESULT_*`
w `docs/geometry/`; notatki `docs/NOTATKI_2026-09-27.md`; kopia tej ściągi: `docs/SKILL_timdr-signal-framework.md`).
Autor idei: Jacek Kielich.

## 1. Czym jest TIMDR

**Model do budowania programów analizujących sygnały**: rama opisu + drogowskazy konstrukcji + parametry przejść +
protokół badania. **Nie jest gotowym detektorem** — operatory użyte wprost nie dają przewagi; programy zbudowane według
drogowskazów (sito, kotwica, reżim, przerwa ciągłości, lustro, stosunki) dają. Większość klocków ma znane odpowiedniki;
wkład TIMDR to logika wyboru i kolejności (jaki sygnał → jaka droga → jaka kotwica → jaki zegar → jakie odniesienie →
czy test ma sens).

## 2. Gałęzie (każda ma własny obiekt — nie utożsamiać)

- **M/S — sygnał** (13 aksjomatów): anomalia (> próg), defekt (skok), rezonans M (≥3 anomalie naraz — koincydencja,
  nie oscylator), skręt (zmiana znaku nachylenia).
- **G — geometria** (10): krzywizna, dyskretny Weingarten, obwiednia P/Q (G10), G-Rezonans (G5), rura/wstęga, rodzina Γ
  (kanały w przestrzeni, kształt modu).
- **K — modalność** (10): częstotliwość, faza, amplituda; rezonans K = zgodność faz/częstotliwości.
- **META-DYNAMICS** (9): Λ–τ–ρ–J + M = dS/dt; mierzalne: τ = czas wygaszania zdarzenia, ρ = D (gęstość zdarzeń);
  Λ i J bez definicji pomiarowej.
- **Chronoproces Ξ = (T, x, Γ, φ):** wspólny czas; M/S czyta x, G rodzinę Γ, K fazy φ. „Pierwszy trybik” = wybór zegara
  (czas / kąt obrotu / zdarzenie).
- **TRM/GIA:** źródło idei; prawo R = kτⁿ na razie 0/2 (przegrywa z rozpadem wykładniczym wg AIC).

Kolizje symboli: „skręt/τ” ma 8 znaczeń (m.in. 7. = widmo Laplasjanu na wstędze Möbiusa, DOI 10.5281/zenodo.22812269),
„rezonans” 5 — zawsze mów, które (`TIMDR_Twists.md`, `GLOSSARY_EN_PL.md`).

## 3. Idee autora (nie gubić)

Membrana = pole; rezonans = nałożenie pól / dana ustalająca oczka sita; model samokorygujący; zwinięcie pola = sygnał w rurze
(rura może się zginać wzdłuż i w poprzek, skręcać); sygnał jak foton na sicie (cząsteczka / fala); lokalne uszkodzenie =
przerwa na czymś ciągłym; odbicie odwraca skręt → **lustro i cień** (nałożenie lustrzanych połówek znosi część wspólną,
zostaje cień); temperatura za wolna → **odniesienie z samej konstrukcji** (stosunki częstotliwości). Obserwacja
(klocki/trybiki): gałąź użyta sama = minus, most między gałęziami = plus; o powodzeniu łańcucha decyduje pierwszy trybik.

## 4. Zasada odniesienia (wzór wspólny wszystkich udanych mostów)

Nałóż sygnał na **odniesienie z tego samego ośrodka**, znieś to, co wspólne, czytaj resztę (bezwymiarowy stosunek):
sito (kinematyka → szum poza oczkami), zegar kątowy (tachometr → prędkość), kotwica (model modów → dryf), linie K (f₀ w
mianowniku → amplituda wymuszenia), D względem tła (maszyna), faza względem wzbudnika (nieznane wymuszenie), lustro
(część wspólna połówek → falowanie całego celu), stosunki częstotliwości (wspólny czynnik skali → temperatura).
Porażka = odniesienie nie zniosło zakłócenia dominującego. Znane odpowiedniki: tłumienie składowej wspólnej, transmisyjność.

## 5. Drogowskazy (`docs/DROGOWSKAZY_TIMDR.md`)

0. **Typ sygnału / reżim:** P (błyski), D = η/(1−η) (η = wypełnienie obwiedni): D < 0,3 cząsteczka, D > 3 fala (szum ≈ 3,7);
   przy szerokopasmowym wymuszeniu licz D względem tła.
1. **Pole** (czas × pasmo, czas × kanał). 2. **Rezonans**. 3. **Sito** (oczka ustala rezonans).
4. **Samokorekta** wokół **kotwicy z K** (rytm z fizyki). 5. **Geometria** (zwiń pole w rurę; kształt modu z fazą;
   lustro wokół linii ciała). 6. **Odniesienie** dla każdego zakłócenia (sekcja 4). 7. **Test**: rozwój → zamrożenie →
   jedno uruchomienie na danych nieoglądanych.
**Droga wg reżimu:** cząsteczka → P / sito z kotwicą; pakiet → sito z kotwicą; fala → linie K przy kotwicy.
**Skala:** zmiana globalna → wielkość globalna (biegun); lokalna → lokalna (kształt modu + przerwa ciągłości); zera FRF
lokalne, ale czułe na wszystko. Każdy krok porównuj ze znanym odpowiednikiem (widmo obwiedni, kurtogram, order tracking,
PLL, OMA/SSI, AR, CVD, regresja temperaturowa).

## 6. Parametry przejść i reguła wykonalności (`docs/theory/TIMDR_Parametry_Przejsc.md`, `core/transition_params.py`)

N_cyk ≥ 10 (cykle rytmu w oknie; **liczyć także na danych testowych przed testem**) • kotwica (stała / śledzona / wolna;
wolna → porażka) • D (reżim) • L_koh (< N_cyk → wyprostuj rurę, zmień zegar) • koherencja kanałów z kotwicą γ² ≥ 0,8
(mediana i p10) • rozstaw czujników = rozdzielczość przestrzenna • **stosunki częstotliwości tylko przy równym skalowaniu:
sprawdź znaki ρ(f_k, T) na danych bazowych** (różne znaki / mróz / przeskok bliskiego modu → nie działają).
Licz PRZED testem i zapisz przewidywanie.

## 7. Mosty (kod + testy w GIA-TIMDR)

- **Pole + sito** (`real_paderborn_resonance_sieve.py`): oczka per hipoteza (BPFO/BPFI) wg rezonansu.
- **Kotwica K → zegar kątowy** (`modal_speed_tracking.py`, `wind_lbf_*`): prostowanie rury tachometrem.
- **Reżim D (K → META)** (`transition_params.py`, `pronostia_*`).
- **K → G → M/S, przerwa ciągłości** (`hbta_modal_curvature.py`, `hbta_discontinuity.py`): faza → kształt modu → skok
  w przestrzeni (wzdłuż: gapped smoothing; w poprzek: sąsiednie linie); MAKSIMUM, nie suma.
- **Lustro i cień** (`radar_or_mirror*.py`, `mmwave_*.py`): połówki ±d wokół linii ciała, S = (E₊+E₋)/2, A = cień.
- **Stosunki częstotliwości** (`hbta_lateral.py`, `kw51_ratios.py`, `lumo_ratios.py`): f / (mediana f/f_ref).
- Bez zysku: rura analityczna (`analytic_tube.py`, `bent_tube.py`) i samonaprawa modalna przy stałej prędkości, antyrezonanse
  surowe (`hbta_antiresonance.py`). **Fourier M/S↔K:** ważny tylko dla pojedynczego modu gaussowskiego.

## 8. Stan wyników (pre-rejestrowane)

- **SUPPORTED:** sito Paderborn (15 foldów +0,08 vs klasyka 12/15; vs obwiednia mieszany); turbina LBF w osi kątowej
  (AUC 1,00); PRONOSTIA (D spada 9/11, powrót 7/11; ≈ kurtoza); LANL kotwica (ρ −0,57 → +0,98); KW51 kotwica (AUC 1,00 = SSI);
  ORION-AE linie K; HBTA przerwa ciągłości (pionowe 0,93–0,94); **radar mmWave lustro/cień** (stereoskopia 3/3, rytm
  utykania; macro-F1 0,89 vs klasyka 0,81, most +0,11 MIXED; możliwy przeciek osób); **stosunki częstotliwości**
  (KW51 15 mies.: |ρ z T| 0,48 → 0,16, lepiej niż termometr 5/6; HBTA P1: null ↓ 4/4, zera 0/8 → 7/8). Też: MC_M/S↔G
  diagnostyka na łożyskach (nie selektor); K: częstotliwość sieci (walidacja potoku).
- **NOT SUPPORTED / bez przewagi:** operatory wprost (LANL, prądy silnika, wideo ρ, MARS DAS, BTC, sejsmika częściowo); Open Radar (pole, rura, lustro — za krótkie ślady); HBTA sama kotwica
  0,65, krzywizna 0,72, antyrezonanse surowe 0/8; LUMO stosunki (mody idą z temperaturą w różne strony — przewidziane);
  kierunek pomiaru HBTA (MIXED); niewyważenie turbiny; MC K↔G Möbius; topologia na uszkodzeniach naturalnych.
- Obraz: TIMDR wygrywa, gdy rytm jest zakotwiczony w fizyce, reguła wykonalności spełniona, a każde zakłócenie ma
  odniesienie z tego samego ośrodka.
- Otwarte: lustro na niezależnych osobach; stosunki z regułą znaków przewidującą z góry (Z24: mróz + stopniowe
  uszkodzenia); przerwa ciągłości na drugim obiekcie; Λ i J w META.

## 9. Narzędzia (zgodne 1:1 z walidacją, testy wzorcowe)

- `TIMDR-Industrial-Predict`: `bearing_resonance_sieve.py analyze | analyze-orders`, `bearing_health_trend.py trend`.
- `TIMDR-Structural-Health`: `timdr_shm.py` (kotwica, linie, reżim, `mode_shapes`, `DiscontinuityBaseline`), dashboard
  `run.bat` (127.0.0.1:8765, zakładka „Jak widzi TIMDR”), `export_view_page.py` → podstrona `jak-widzi-timdr.html`.
- `TIMDR-Modal-Formalism`: `timdr_modal/modal_anchor.py` (kotwica, K→G, `anchor_coherence`, wykonalność).
- `TIMDR-META-DYNAMICS`: `analysis/meta_measure.py` (τ, ρ = D, reżim, `measured_state`, `feasibility`).
- Strona: diagram `timdr-branches-diagram.svg` generuje `docs/rysuj_diagram_galezi.py` (aktualizuj po wynikach).

## 10. Protokół (anty-numerologia)

- Hipoteza, cechy, progi, przewidywania w commicie **przed** danymi testowymi; jedno uruchomienie; poprawki po zamrożeniu
  i wszystko obejrzane przed zamrożeniem — ujawnione; zero strojenia po fakcie.
- Mocny punkt odniesienia z dziedziny, nie same statystyki; test na jednostkach spoza uczenia; kontrola negatywna
  (permutacja) i pozytywna (syntetyka); Mann-Whitney + rozmiar efektu.
- Sprawdzaj ślady akwizycji, sufit, moc testu, **duplikaty i wady zbioru** (rozmiary plików, identyczne nagrania);
  ponowne użycie danych ujawnij (wynik rozpoznawczy). „Poprawne na syntetyce” ≠ „użyteczne”; selektor ≠ diagnostyka.
- Wynik negatywny jest wynikiem — wszystko do README; dla usuniętych danych surowych zapisz instrukcję odtworzenia;
  twierdzenia sprawdzalne przez `claim_audit` (`TIMDR-AI-Core`).
- Commit lokalnie (Jacek, jbackk@gmail.com), wypycha użytkownik.

## 11. Czego nie robić

Nie ogłaszać TIMDR detektorem; nie stroić po wyniku; nie dopisywać aksjomatów bez testu; nie łączyć gałęzi bez znanej
transformaty (odrzucone: tensor grawitacji, MöbiusCoherence); nie szukać „czy TIMDR wykryje X” na ślepo — najpierw reguła wykonalności; przy propozycji łamiącej zasadę
ramy — nazwać konflikt i zapytać.
