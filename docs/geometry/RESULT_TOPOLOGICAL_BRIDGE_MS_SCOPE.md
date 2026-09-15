# Wynik: most M/S↔topologia — zamknięcie serii trzech prób

> Streszczenie trzech pełnych cykli pre-rejestracja→implementacja→wynik
> przeprowadzonych 2026-09-15, po propozycji wzięcia P/Q obwiedni
> trójkąta (Aksjomat G10) jako punktu startowego dla mostu M/S↔topologia.
> Pełna metodologia w poszczególnych `PREREG_*`/`RESULT_*`. Ten plik to
> wniosek zbiorczy i decyzja co dalej.

## Co przetestowano, w kolejności

| # | Metryka | Rząd różniczkowania | Wynik | Dokument |
|---|---|---|---|---|
| 1 | Torsja Freneta-Serreta, `max\|τ\|` | 3 (v→a→j) | **0/10**, kierunek odwrócony | `RESULT_TREFOIL_MS_BRIDGE.md` |
| 2a | Winding number (rzut PCA 2D) | 1 (Δθ) | **0/10 z 20**, poprawny kierunek ale brak specyficzności | `RESULT_WINDING_CROSSING_MS_BRIDGE.md` |
| 2b | Crossing number (rzut PCA 2D) | 0 | **0/10 z 20**, kierunek odwrócony przy sigma≥0,3 | jw. |
| 3 | Homologia perzystentna, suma persystencji H1 | 0 | **1/10**, niestabilne (cienki margines, brak replikacji, odwrócony kierunek przy innym oknie) | `RESULT_PERSISTENT_HOMOLOGY_MS_BRIDGE.md` |

Łącznie: **1/40 komórek siatki** w całej serii formalnie spełniło
zamrożone kryterium `pipeline.run_controls()` — i ta jedna komórka jest
jawnie odrzucona jako wiarygodna (sekcja "Wniosek" w dokumencie #3).

## Wniosek zbiorczy

**Most M/S↔topologia przez embedding opóźniający (delay embedding)
sygnału 1D w przestrzeń 3D — z żadną z trzech przetestowanych metryk
ekstrakcji skalara — nie działa w sposób odtwarzalny.** To NIE jest
wniosek o pojedynczej nieudanej metryce, tylko o samej konstrukcji
pośredniczącej (embedding), wspólnej dla wszystkich trzech prób —
zgodnie z diagnozą w dokumencie #2: różne rzędy różniczkowania (3, 1,
0) i różne mechanizmy odporności na szum (redukcja przez max,
kombinatoryka, persystencja topologiczna) dały ten sam ostateczny
wzorzec: szum zaszyty w embedding opóźniający generuje strukturę
(lokalną i globalną) porównywalną lub większą niż genuine sygnał
periodyczny, niezależnie jak się tę strukturę mierzy.

## Co to oznacza dla dalszej pracy

- **Trzy kandydaci z pierwotnej listy (torsja, winding/crossing,
  homologia perzystentna) są wyczerpane** dla TEJ konstrukcji
  embeddingu. Dalsze próby nowych metryk na tym samym embeddingu mają
  niski a priori sens — problem najpewniej leży w embeddingu, nie w
  wyborze metryki (patrz diagnoza wyżej).
- Otwarta, NIE podjęta ścieżka: zmiana samego embeddingu (np.
  wygładzenie sygnału przed osadzeniem, inny sposób budowy trajektorii
  z 1D niż opóźnienie, użycie realnych wielowymiarowych danych zamiast
  sztucznego zanurzenia jednowymiarowego sygnału) — to byłby ZUPEŁNIE
  nowy punkt startowy, wymagający własnej pre-rejestracji, nie
  kontynuacja tej serii.
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
