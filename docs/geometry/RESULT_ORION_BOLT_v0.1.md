# RESULT — ORION-AE: luzowanie śruby, droga reżimów, v0.1

Pre-rejestracja: `PREREG_ORION_BOLT_v0_1.md` (commit bda9414). Jedno uruchomienie. Liczby: `RESULT_ORION_BOLT_v0_1.json`.
Test na seriach D i E (inne kampanie niż rozwój B), po 84 odcinki na serię.

- **H1 (linie K przy kotwicy wymuszenia rosną przy luzowaniu): SUPPORTED** — ρ = −0,85 (D), −0,64 (E).
- **H2 (7 klas, TIMDR > klasyka): formalnie SUPPORTED** — macro-F1 0,18 vs 0,04 (średnio D, E), **ale obie wartości są
  przy poziomie losowym (1/7 = 0,14) lub poniżej**: dokładny poziom dokręcenia nie przenosi się między kampaniami
  (inny montaż). Realny sygnał to trend (H1), nie klasyfikacja.
- **H3 (reżim cząsteczki pośrodku, nie przy najluźniejszym): SUPPORTED** — maksimum cząsteczkowości emisji akustycznej
  przy 10 cNm w obu seriach (D: 0,57; E: 0,30; tło 0,21–0,23), w rozwoju (B) przy 20 cNm. Przy 5 cNm P wraca do tła.

## Wniosek
Dwie drogi reguły reżimów działają na połączeniu śrubowym: linie K przy kotwicy wymuszenia śledzą luzowanie (jak zderzak
w ramie LANL), a emisja akustyczna przechodzi przez reżim cząsteczki przy średnim luzie — mikropoślizgi są rzadkie i ostre,
przy pełnym luzie przestają „trzaskać”. To ten sam wzór co w budynku (rzadkie uderzenia = cząsteczki) i w łożyskach
PRONOSTIA (pole → cząsteczka → powrót).
