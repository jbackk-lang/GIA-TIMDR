# Wynik — sito samokorygujące (rezonans ustala oczka sita), Paderborn, uszkodzenia naturalne, v0.1 (2026-09-26): SUPPORTED

Pre-rejestracja: `PREREG_PADERBORN_RESONANCE_SIEVE_v0.1.md` (commit dfad20b; zamrożone po fazie rozwoju na pomiarach 1–5,
przed otwarciem pomiarów 6–10). Liczby: `RESULT_PADERBORN_RESONANCE_SIEVE_v0.1.json`. Jedno uruchomienie, bez zmian.
Kontrola negatywna 0,25 — przeszła. 15 łożysk (5/klasę), łożyska testowe nigdy w uczeniu, pomiary 6–10 nigdy wcześniej nieotwierane.

| Zestaw (macro-F1, losowo ≈ 0,33) | średnio | foldy |
|---|---|---|
| klasyczne + obwiednia (B) | 0,56 | 0,73 / 0,31 / 0,72 / 0,46 / 0,60 |
| sama obwiednia pełnopasmowa (ENV) | 0,61 | 0,93 / 0,26 / 0,95 / 0,56 / 0,34 |
| **sito Q (rezonans ustala oczka)** | **0,68** | 0,91 / 0,45 / 0,80 / 0,72 / 0,53 |
| opisowo: B + sito jednego przejścia (R) | 0,71 | 0,95 / 0,65 / 0,90 / 0,61 / 0,42 |
| opisowo: geometria grzbietu (G) | 0,45 | — |

- **H1 (sito vs klasyczne): SUPPORTED** — średnio +0,12, lepsze w 4/5 foldach.
- **H2 (samokorygujące oczka vs zwykła obwiednia na tych samych częstotliwościach): SUPPORTED** — średnio +0,075, lepsze w 3/5;
  sito jest przy tym stabilniejsze między łożyskami (najgorszy fold 0,45 wobec 0,26).

**Co to znaczy.** Na najtrudniejszym zbiorze (uszkodzenia naturalne, niewidziane łożyska i niewidziane pomiary) konstrukcja
z idei „membrana = pole, rezonans = dana dla oczek sita” rozpoznaje stan łożyska lepiej niż klasyczne cechy i lepiej niż
zwykłe widmo obwiedni. Mechanizm jest pokrewny znanej analizie cyklostacjonarnej / wyborowi pasma (kurtogram): sito wybiera
pasma nośne, w których konstrukcja rezonuje z częstotliwością uszkodzenia. Most geometryczny w tej postaci (krzywizna grzbietu)
nic nie dodał.

**Granice:** 5 łożysk na klasę z jednego stanowiska; faza rozwoju na tych samych łożyskach (inne pomiary); porównanie nie
obejmuje pełnego kurtogramu ani widma korelacji spektralnej. Replikacja: pomiary 11–20 (nieotwarte) i inne stanowisko.
