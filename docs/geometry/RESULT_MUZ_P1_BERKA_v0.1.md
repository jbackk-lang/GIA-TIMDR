# RESULT MUZ P1 v0.1: zegar od wypłaty i odniesienie do dochodu w budżecie (PKDD'99)

Pre-rejestracja: `PREREG_MUZ_P1_BERKA_v0_1.md` (commit c0b84c1). Jedno uruchomienie na części testowej.
Dane publiczne PKDD'99; żadnych danych prywatnych. JSON: `RESULT_MUZ_P1_BERKA_v0_1.json`.

## Wynik (test: 316 kredytów, 32 złe; LDA 0,1, 5-krotna CV × 10)

| Ramię | AUC |
|---|---|
| C — klasyka kalendarzowa, kwoty nominalne | **0,935** |
| T — zegar od wypłaty, względem dochodu, reżim D | 0,872 |
| T_cal — cechy T na miesiącach kalendarzowych | 0,879 |
| T_nom — cechy T od wypłaty, kwoty nominalne | 0,908 |
| C+T | 0,917 |

| Hipoteza | ΔAUC | 95% CI | Werdykt |
|---|---|---|---|
| H1: T > C | −0,063 | [−0,123; −0,014] | **NOT SUPPORTED** (klasyka istotnie lepsza) |
| H2: zegar od wypłaty > kalendarz | −0,007 | [−0,045; +0,029] | **NOT SUPPORTED** (brak efektu) |
| H3: odniesienie do dochodu > nominalne | −0,036 | [−0,080; +0,002] | **NOT SUPPORTED** (raczej szkodzi) |
| H4: C+T > C | −0,019 | [−0,062; +0,019] | **NOT SUPPORTED** |

Przewidywanie przed testem (kierunki dodatnie, MIXED) się nie sprawdziło. Wynik rozwojowy (15 złych) był szumem.

## Interpretacja

- **Odniesienie wycięło sygnał.** Rata kredytu jest kwotą nominalną; zdolność spłaty zależy od poziomu salda
  i dochodu w walucie, nie od ich stosunku. Dzielenie przez dochód usuwa właśnie to, co wspólne — a tu to,
  co wspólne, jest celem, nie zakłóceniem. Doprecyzowanie zasady odniesienia: wzorzec ma znosić
  **zakłócenie** (temperaturę, skalę instrumentu), a nie wielkość, o którą pyta decyzja. Przy KW51/HBTA
  temperatura była zakłóceniem; przy kredycie poziom dochodu jest informacją.
- **Zegar od wypłaty nic nie zmienia.** W tym banku wpływy przychodzą w podobnym dniu, a kryterium (kłopot
  z kredytem) jest wolne wobec przesunięcia cyklu o kilkanaście dni — kotwica nie ma czego porządkować.
- Post hoc (niepre-rejestrowane, z wyborem znaku — optymistyczne): pojedyncze cechy T nie są słabe —
  najniższe saldo przed kolejną wypłatą względem dochodu AUC 0,86 (najlepsza pojedyncza cecha klasyczna 0,77),
  reżim D dziennych wydatków 0,70. Przegrywa zestaw, nie każda cecha. To wskazówka na P2, nie wynik.

## Znaczenie dla MUZ

Dla agenta budżetu: pytania o **wypłacalność** (czy starczy do raty, do końca cyklu) liczyć w kwotach
nominalnych; odniesienie do dochodu i zegar od wypłaty zostawić dla pytań o **zmianę nawyków**, gdzie
wspólna skala (inflacja, podwyżka) jest zakłóceniem. Ten test tego drugiego nie sprawdzał (brak etykiet
„alarmów o wzroście wydatków” w publicznym zbiorze).

## Ograniczenia

Jeden bank, lata 90., 32 złe kredyty w teście; kredyt ≠ alarm wydatkowy; brak CPI.
