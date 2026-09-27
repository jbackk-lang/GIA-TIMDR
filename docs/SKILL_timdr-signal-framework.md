---
name: timdr-signal-framework
description: Zwięzła ściąga GIA-TIMDR: czym jest TIMDR, gałęzie, drogowskazy budowy analizy, mosty, parametry przejść, protokół testów i aktualny stan wyników. Używaj przy każdej pracy nad teorią, kodem lub testami TIMDR.
---

# TIMDR — ściąga (stan 2026-09-27)

Szczegóły zawsze w repo `jbackk-lang/GIA-TIMDR` (README: tabela wyników; `docs/theory/*`; pary `PREREG_*`/`RESULT_*`
w `docs/geometry/`; kopia tej ściągi: `docs/SKILL_timdr-signal-framework.md`). Autor idei: Jacek Kielich.

## 1. Czym jest TIMDR

**Model do budowania programów analizujących sygnały**: rama opisu + drogowskazy konstrukcji + parametry przejść +
protokół badania. **Nie jest gotowym detektorem** — operatory użyte wprost nie dają przewagi; programy zbudowane według
drogowskazów (sito, kotwica, reżim, przerwa ciągłości) dają. Większość klocków ma znane odpowiedniki; wkład TIMDR to logika
wyboru i kolejności (jaki sygnał → jaka droga → jaka kotwica → jaki zegar → czy test ma sens).

## 2. Gałęzie (każda ma własny obiekt — nie utożsamiać)

- **M/S — sygnał** (13 aksjomatów): anomalia (> próg), defekt (skok), rezonans M (≥3 anomalie naraz — koincydencja,
  nie oscylator), skręt (zmiana znaku nachylenia).
- **G — geometria** (10): krzywizna, dyskretny Weingarten, obwiednia P/Q (G10), G-Rezonans (G5), rura/wstęga, rodzina Γ
  (kanały w przestrzeni, kształt modu).
- **K — modalność** (10): częstotliwość, faza, amplituda; rezonans K = zgodność faz/częstotliwości.
- **META-DYNAMICS** (9): Λ–τ–ρ–J + M = dS/dt; teraz mierzalnie: τ = czas wygaszania zdarzenia, ρ = D = f·τ.
- **Chronoproces Ξ = (T, x, Γ, φ):** wspólny czas; M/S czyta x, G rodzinę Γ, K fazy φ. „Pierwszy trybik” = wybór zegara
  (czas / kąt obrotu / zdarzenie).
- **TRM/GIA:** źródło idei; prawo R = kτⁿ na razie 0/2 (przegrywa z rozpadem wykładniczym wg AIC).

Kolizje symboli: „skręt/τ” ma 8 znaczeń (m.in. 7. = widmo Laplasjanu na wstędze Möbiusa, DOI 10.5281/zenodo.22812269),
„rezonans” 5 — zawsze mów, które (`TIMDR_Twists.md`, `GLOSSARY_EN_PL.md`).

## 3. Idee autora (nie gubić)

Membrana = pole; rezonans = nałożenie pól / dana ustalająca oczka sita; model samokorygujący; zwinięcie pola = sygnał w rurze
(rura może się zginać wzdłuż i w poprzek, skręcać); sygnał zachowuje się jak foton na sicie (cząsteczka / fala);
lokalne uszkodzenie = przerwa na czymś ciągłym. Obserwacja (klocki/trybiki): gałąź użyta sama = minus, most między
gałęziami = plus; o powodzeniu łańcucha decyduje pierwszy trybik (zegar).

## 4. Drogowskazy (`docs/DROGOWSKAZY_TIMDR.md`)

0. **Typ sygnału / reżim:** P (błyski), D = η/(1−η) (η = wypełnienie obwiedni): D < 0,3 cząsteczka, D > 3 fala (szum ≈ 3,7);
   przy szerokopasmowym wymuszeniu licz D względem tła.
1. **Pole** (czas × pasmo, czas × kanał). 2. **Rezonans** (co się powtarza lub zgadza). 3. **Sito** (oczka ustala rezonans).
4. **Samokorekta** wokół **kotwicy z K** (rytm z fizyki). 5. **Geometria** (zwiń pole w rurę; kształt modu z fazą).
6. **Test**: rozwój → zamrożenie → jedno uruchomienie na danych nieoglądanych.
**Droga wg reżimu:** cząsteczka → P / sito z kotwicą; pakiet → sito z kotwicą; fala → linie K przy kotwicy (harmoniczne).
Każdy krok porównuj ze znanym odpowiednikiem (widmo obwiedni, kurtogram, order tracking, PLL, OMA/SSI, AR, wskaźnik harmonicznych).

## 5. Parametry przejść i reguła wykonalności (`docs/theory/TIMDR_Parametry_Przejsc.md`, `core/transition_params.py`)

N_cyk (cykle rytmu w oknie; < 10 → sito bez szans) • kotwica (stała / śledzona / wolna; wolna → porażka) • D (reżim) •
L_koh (koherencja; < N_cyk → wyprostuj rurę, zmień zegar; nie odróżnia tłumienia od dryfu) • koherencja przestrzenna
γ² ≥ 0,8 (dobór kotwic do kształtu modu) • rozstaw czujników = rozdzielczość przestrzenna • środek oczek (lokalizacja).
Licz PRZED testem i zapisz przewidywanie.

## 6. Mosty (kod + testy w GIA-TIMDR)

- **Pole + sito** (`real_paderborn_resonance_sieve.py`): oczka per hipoteza (BPFO/BPFI) wg rezonansu.
- **Kotwica K → sito + prostowanie rury** (`modal_speed_tracking.py`, `wind_lbf_*`): zegar kątowy z tachometru.
- **Reżim D (K → META)** (`transition_params.py`, `pronostia_*`, `real_lanl_modal_anchor.py`): cząsteczka ↔ fala; w fali linie K.
- **K → G → M/S, przerwa ciągłości** (`hbta_modal_curvature.py`, `hbta_discontinuity.py`): faza względem wzbudnika → kształt
  modu → skok w przestrzeni (wzdłuż: gapped smoothing; w poprzek: sąsiednie linie); MAKSIMUM, nie suma.
- **Rura analityczna** (`analytic_tube.py`, `bent_tube.py`), **samonaprawa modalna** (`modal_self_repair.py`): poprawne,
  bez zysku przy stałej prędkości. **Fourier M/S↔K:** ważny tylko dla pojedynczego modu gaussowskiego.

## 7. Stan wyników (pre-rejestrowane)

- **SUPPORTED:** sito Paderborn 3 próby (15 foldów +0,08 vs klasyka 12/15; vs kurtogram tak; vs obwiednia +0,04 — mieszany);
  turbina LBF w osi kątowej (AUC 1,00, swoistość 1,00 vs 0,85); PRONOSTIA 11 łożysk (D spada 9/11, powrót 7/11; D ≈ kurtoza);
  budynek LANL kotwica modalna (ciężkość −0,57 → +0,98); most KW51 (kotwica z 2 kanałów AUC 1,00 = SSI, AR 0,67);
  śruba ORION-AE (linie K ρ −0,85/−0,64; cząsteczkowość max przy średnim luzie); HBTA przerwa ciągłości (uszkodzenia
  pionowe 0,93–0,94, każde ≥ AR; średnio remis 0,80 — dane użyte 4. raz). Też: MC_M/S↔G diagnostyka na łożyskach
  (nie selektor); K: częstotliwość sieci (walidacja potoku).
- **NOT SUPPORTED / bez przewagi:** operatory wprost (LANL, prądy silnika, wideo ρ, MARS DAS, BTC, sejsmika częściowo);
  radar mikro-Doppler (pole 0,76, rura 0,76 vs klasyka 0,90); HBTA sama kotwica 0,65, krzywizna 0,72; niewyważenie turbiny
  (brak 1× — zatrzymane w rozwoju); MC K↔G Möbius (artefakt kratownicy); topologia na uszkodzeniach naturalnych.
- Obraz: TIMDR wygrywa, gdy rytm jest zakotwiczony w fizyce; lokalne uszkodzenia — dopiero z fazą i szukaniem przerwy.

## 8. Narzędzia (zgodne 1:1 z walidacją, testy wzorcowe)

- `TIMDR-Industrial-Predict`: `bearing_resonance_sieve.py analyze | analyze-orders`, `bearing_health_trend.py trend`, wykonalność.
- `TIMDR-Structural-Health`: `timdr_shm.py` (kotwica, linie, reżim, `mode_shapes`, `DiscontinuityBaseline`), dashboard `run.bat`
  (127.0.0.1:8765, zakładka „Jak widzi TIMDR”), `export_view_page.py` → podstrona `jak-widzi-timdr.html` na jbackk-lang.github.io.
- Strona: diagram `timdr-branches-diagram.svg` generuje `docs/rysuj_diagram_galezi.py` (aktualizuj liczby po wynikach).

## 9. Protokół (anty-numerologia)

- Hipoteza, cechy, progi, reguła sufitu i przewidywania w commicie **przed** danymi testowymi; jedno uruchomienie;
  poprawki po zamrożeniu ujawnione; zero strojenia po fakcie.
- Mocny punkt odniesienia z dziedziny (obwiednia, kurtogram, OMA/SSI, AR, kurtoza), nie same statystyki.
- Test na jednostkach spoza uczenia; kontrola negatywna (permutacja) i pozytywna (syntetyka); Mann-Whitney + rozmiar efektu.
- Sprawdzaj ślady akwizycji (dzień, konfiguracja, temperatura), sufit baseline'u, moc testu; ponowne użycie danych ujawnij
  (wynik rozpoznawczy). „Poprawne na syntetyce” ≠ „użyteczne na realnych danych”; selektor ≠ diagnostyka.
- Wynik negatywny jest wynikiem — wszystko do README; twierdzenia sprawdzalne przez `claim_audit` (`TIMDR-AI-Core`).
- Commit lokalnie (Jacek, jbackk@gmail.com), wypycha użytkownik.

## 10. Czego nie robić

Nie ogłaszać TIMDR detektorem; nie stroić po wyniku; nie dopisywać aksjomatów bez testu; nie łączyć gałęzi bez znanej
transformaty (odrzucone: tensor grawitacji, MöbiusCoherence); nie szukać „czy TIMDR wykryje X” na ślepo — najpierw reguła
wykonalności; przy propozycji łamiącej zasadę ramy — nazwać konflikt i zapytać.
