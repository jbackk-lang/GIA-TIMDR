# RESULT MUZ P2 v0.1: odniesienie do raty zamiast dochodu (PKDD'99)

Pre-rejestracja: `PREREG_MUZ_P2_BERKA_v0_1.md` (commit 5a20031). Jedno uruchomienie; **2. użycie części
testowej** (ujawnione). JSON: `RESULT_MUZ_P2_BERKA_v0_1.json`.

## Wynik (test: 316 kredytów, 32 złe)

| Ramię | AUC |
|---|---|
| C — klasyka (9 cech, kalendarz, nominalnie) | 0,935 |
| R — cykle od wypłaty, względem raty (7 cech) | 0,913 |
| R_cal — cechy R na miesiącach kalendarzowych | **0,945** |
| T — P1, względem dochodu | 0,872 |
| C+R | 0,934 |

| Hipoteza | ΔAUC | 95% CI | Werdykt |
|---|---|---|---|
| H1: C+R > C | −0,001 | [−0,049; +0,046] | **NOT SUPPORTED** (nic nie dodaje) |
| H2: rata > dochód jako wzorzec | +0,041 | [−0,033; +0,124] | **MIXED** (kierunek zgodny) |
| H3: zegar od wypłaty > kalendarz | −0,032 | [−0,088; +0,010] | **NOT SUPPORTED** (raczej szkodzi) |
| H4: R > C | −0,022 | [−0,085; +0,035] | **NOT SUPPORTED** (remis) |

Przewidywanie: H1 MIXED/SUPPORTED — nie sprawdziło się; H2 dodatnie — tak; H3 bez efektu — ujemne;
H4 MIXED/NOT — zgodne. Rozwój (15 złych) znów przeszacował zysk.

## Interpretacja

- **Poprawka wzorca działa częściowo.** Zmiana odniesienia z dochodu na ratę podniosła AUC z 0,87 do 0,91,
  a 7 cech względem raty daje remis z 9 cechami klasyki. Zasada „wzorzec = to, o co pyta decyzja” trzyma
  kierunek, ale nie daje przewagi: obie reprezentacje niosą tę samą informację (poziom salda wobec
  zobowiązań), więc połączenie nic nie dodaje. Sufit tych danych ≈ 0,94.
- **Zegar od wypłaty szkodzi drugi raz** (P1 −0,007, P2 −0,032). R_cal (0,945) nie był hipotezą i jest
  liczbą opisową, nie wynikiem. Wyjaśnienie do sprawdzenia, nie przyjęte: raty i zlecenia stałe w banku
  schodzą według kalendarza, więc rytmem zobowiązania jest kalendarz, a kotwica powinna być zegarem tego,
  o co pyta decyzja — tak samo jak wzorzec.
- Dalsze próby na tym zbiorze nie mają sensu: część testowa użyta 2×, sufit osiągnięty, 32 złe kredyty.

## Znaczenie dla MUZ

Wypłacalność: saldo wobec zobowiązań (rata, stałe opłaty) w ich własnym kalendarzu — to wystarcza i jest
tak dobre jak klasyka. Zegar od wypłaty i odniesienie do dochodu nie mają na tych danych wsparcia; zostają
jako hipoteza tylko dla wykrywania zmian nawyków (niesprawdzalne tu — brak etykiet).
