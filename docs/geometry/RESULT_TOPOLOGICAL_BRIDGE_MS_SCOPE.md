# Wynik: most M/S↔topologia — zamknięcie serii pięciu prób

> Streszczenie pięciu pełnych cykli pre-rejestracja→implementacja→wynik
> przeprowadzonych 2026-09-15, po propozycji wzięcia P/Q obwiedni
> trójkąta (Aksjomat G10) jako punktu startowego dla mostu M/S↔topologia,
> rozszerzonej o piąty, jakościowo inny kandydat inspirowany orbitalnym
> momentem pędu (OAM) fotonu. Pełna metodologia w poszczególnych
> `PREREG_*`/`RESULT_*`. Ten plik to wniosek zbiorczy i decyzja co dalej.

## Co przetestowano, w kolejności

| # | Metryka | Mechanizm | Wynik | Dokument |
|---|---|---|---|---|
| 1 | Torsja Freneta-Serreta, `max\|τ\|` | różniczkowanie rzędu 3 (v→a→j) na embeddingu opóźniającym | **0/10**, kierunek odwrócony | `RESULT_TREFOIL_MS_BRIDGE.md` |
| 2a | Winding number (rzut PCA 2D) | różniczkowanie rzędu 1 (Δθ) na embeddingu opóźniającym | **0/10 z 20**, poprawny kierunek ale brak specyficzności | `RESULT_WINDING_CROSSING_MS_BRIDGE.md` |
| 2b | Crossing number (rzut PCA 2D) | zero różniczkowania, kombinatoryka na embeddingu opóźniającym | **0/10 z 20**, kierunek odwrócony przy sigma≥0,3 | jw. |
| 3 | Homologia perzystentna, suma persystencji H1 | zero różniczkowania, filtracja VR na embeddingu opóźniającym | **1/10**, niestabilne (cienki margines, brak replikacji, odwrócony kierunek przy innym oknie) | `RESULT_PERSISTENT_HOMOLOGY_MS_BRIDGE.md` |
| 5 | Winding fazy (Hilbert, inspirowane OAM fotonu) | akumulacja fazy w czasie, BEZ embeddingu opóźniającego | **0/10**, zerowa rozróżnialność — zdominowane przez częstotliwość podstawową | `RESULT_PHASE_WINDING_OAM_MS_BRIDGE.md` |

Łącznie: **1/50 komórek siatki** w całej serii formalnie spełniło
zamrożone kryterium `pipeline.run_controls()` — i ta jedna komórka jest
jawnie odrzucona jako wiarygodna (sekcja "Wniosek" w dokumencie #3).

## Wniosek zbiorczy

**Pięć niezależnych konstrukcji, cztery różne mechanizmy porażki —
żaden most M/S↔topologia/K przez pojedynczy skalar ekstrahowany z okna
sygnału nie zadziałał w sposób odtwarzalny.**

Dla czterech pierwszych (torsja, winding-trajektorii, crossing,
homologia) wspólnym mianownikiem był **embedding opóźniający**: różne
rzędy różniczkowania (3, 1, 0) i różne mechanizmy odporności na szum
(redukcja przez max, kombinatoryka, persystencja topologiczna) dały ten
sam ostateczny wzorzec — szum zaszyty w embedding opóźniający generuje
strukturę (lokalną i globalną) porównywalną lub większą niż genuine
sygnał periodyczny.

**Piąty kandydat (winding fazy) obalił hipotezę, że TO WYŁĄCZNIE
embedding jest źródłem problemu** — ta metoda w ogóle nie używała
embeddingu opóźniającego (działała wprost na sygnale 1D przez
transformatę Hilberta) i TEŻ zawiodła, ale z zupełnie innego,
zdiagnozowanego wprost powodu: dominująca amplitudowo składowa
częstotliwości maskowała obecność drugiej, słabszej składowej w
sumarycznej akumulacji fazy — problem matematyczny specyficzny dla tej
metody, nie powtórka „szum wygrywa entropią".

**Uczciwy wniosek zbiorczy jest więc słabszy, ale bardziej precyzyjny
niż po czterech próbach**: to nie jest jeden, uniwersalny defekt do
naprawienia (jak wydawało się po czterech próbach) — każda z pięciu
metod zawiodła z własnego, odrębnego powodu. Cztery na pięć dzieliły
wspólny mechanizm (entropia szumu w embeddingu), ale to nie jest
`n=5/5` ani nie jest to jedna przyczyna do usunięcia i „naprawienia
wszystkiego naraz".

## Co to oznacza dla dalszej pracy

- **Pięciu kandydatów (torsja, winding/crossing, homologia perzystentna,
  winding fazy) jest wyczerpanych** w swoich przetestowanych postaciach.
  Dalsze próby nowych metryk NA TYM SAMYM embeddingu opóźniającym mają
  niski a priori sens (4/4 embedding-based prób zawiodło tym samym
  mechanizmem). Próba embedding-free (winding fazy) pokazała, że
  porzucenie embeddingu też nie gwarantuje sukcesu — każda konkretna
  metoda ma własne, osobne ograniczenia do sprawdzenia, nie jest to
  gwarantowany „bezpieczny" kierunek.
- Otwarta, NIE podjęta ścieżka dla rodziny embeddingowej: zmiana
  samego embeddingu (np. wygładzenie sygnału przed osadzeniem, inny
  sposób budowy trajektorii z 1D niż opóźnienie).
- Otwarta, NIE podjęta ścieżka dla rodziny fazowej: winding fazy
  liczony OSOBNO per pasmo częstotliwości (filtracja pasmowoprzepustowa
  przed Hilbertem) zamiast dla całego sygnału naraz.
  Obie ścieżki wymagałyby własnej, nowej pre-rejestracji, nie są
  kontynuacją tej serii.
- **P/Q obwiedni trójkąta (Aksjomat G10) pozostaje tym, czym było**:
  najtwardszym, dowiedzionym kawałkiem geometrii w ekosystemie. Ta
  seria prób rozszerzenia go w stronę mostu M/S↔topologia (przez
  torsję trójwęzła jako łącznik, nie przez samo G10 matematycznie —
  patrz zastrzeżenie w `PREREG_TREFOIL_MS_BRIDGE.md` §0) zakończyła się
  negatywnie, ale nie osłabia to samego G10.
- **Status w ekosystemie**: cała ta seria pozostaje eksploracyjna,
  udokumentowana w `docs/geometry/`, NIE promowana do `Axioms_G_TIMDR_
  Geometry.md` — dokładnie ten sam wzorzec co sprzężenie helikalne
  K↔Θ_bif (`GS_Matrix_Helical_Coupling_DRAFT.md`) w TIMDR-Math-
  Formalism: nowa, jawnie oznaczona konstrukcja, nie wyprowadzenie z
  istniejącej struktury, więc jej porażka (lub przyszły sukces) nie
  zmienia statusu aksjomatów.
- Zgodnie ze standardowym wzorcem tego ekosystemu (most Fouriera,
  sprzężenie helikalne): wynik negatywny jest pełnoprawną, wartościową
  odpowiedzią — zawęża przestrzeń poszukiwań (wiemy teraz, że embedding
  opóźniający jest podejrzanym punktem, nie metryka) i jest zapisany
  uczciwie, nie ukryty.
