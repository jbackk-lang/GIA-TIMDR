# RESULT — most Hell Bridge Test Arena: kotwica modalna K + kształt modu, v0.1

Pre-rejestracja: `PREREG_HBTA_MODAL_ANCHOR_v0_1.md` (commit 87303a1). Jedno uruchomienie. Liczby: `RESULT_HBTA_MODAL_ANCHOR_v0_1.json`.

| Stan (typ uszkodzenia) | AUC TIMDR (kotwica K + kształt) | AUC klasyczne AR(5) |
|---|---|---|
| DS1 podłużnica–poprzecznica, 1 | 0,91 | 0,93 |
| DS2 podłużnica–poprzecznica, wiele | 0,81 | 0,92 |
| DS3 poprzeczka podłużnic, 1 | 0,79 | 0,72 |
| DS4 poprzeczki, wiele | 0,75 | 0,73 |
| DS5 stężenie wiatrowe, 1 | 0,33 | 0,64 |
| DS6 stężenia, wiele | 0,36 | 0,68 |
| DS7 stężenia, najwięcej | 0,49 | 0,76 |
| DS8 poprzecznica–dźwigar główny | 0,76 | 0,93 |
| **średnio** | **0,65** | **0,79** |

- **H1 (średnie AUC ≥ 0,90): NOT SUPPORTED** (0,65).
- **H2 (nie gorzej niż AR − 0,02): NOT SUPPORTED** (0,65 vs 0,79).
- **H3 (łatwe DS1, DS2, DS8 > trudne DS3–7, jak w publikacji): SUPPORTED** (0,83 vs 0,54).
- **H4 (fałszywe alarmy UDS_02 ≤ 0,20): formalnie SUPPORTED (0,07), ale test zdegenerowany** — przy 15 oknach uczących próg
  95% leave-one-out jest tak wysoki, że alarmuje tylko jedno okno w każdej rejestracji (także w uszkodzonych: 0,07). Werdykt
  bez wartości informacyjnej.

## Zastrzeżenia
- DS3 i DS4 nagrano przy 21–22 °C, uczenie przy 13 °C, UDS_02 przy 10 °C — ich AUC może częściowo mierzyć temperaturę.
- Uszkodzenia stężeń wiatrowych (DS5–7) działają głównie poprzecznie; pionowe kotwice modalne ich nie widzą (AUC < 0,5),
  AR widzi je słabo (0,64–0,76). Zgodne z publikacją.

## Wniosek
Na prawdziwym moście kotwica modalna z kształtem modu przegrywa z klasycznym AR. Fizyka wyników jest spójna (łatwe i trudne
uszkodzenia jak w literaturze), ale przewagi TIMDR nie ma. Wg reguły decyzji repo konstrukcji wymaga dwóch pozytywnych testów
niezależnych — ten jest negatywny.
