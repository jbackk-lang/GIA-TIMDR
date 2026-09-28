# PREREG MUZ P2 v0.1: odniesienie do zobowiązania (raty) zamiast do dochodu (PKDD'99)

Stan: **zamrożone przed uruchomieniem na części testowej**. Jedno uruchomienie. Kod: `core/muz_p2.py`
(korzysta z `core/muz_berka_p1.py` bez zmian).

## Skąd ten test

P1 (NOT SUPPORTED): odniesienie do dochodu wycięło sygnał, bo przy wypłacalności poziom kwot jest celem, nie
zakłóceniem. Poprawiona zasada: wzorzec ma być **tym, o co pyta decyzja**, z tego samego medium. Pytanie
o kredyt = „czy starczy na ratę”, więc wzorcem jest **miesięczna rata** (kwota znana w chwili przyznania,
kolumna `payments` w fin_loan). Zegar od wypłaty wyznacza dołek salda przed kolejną wypłatą — moment, w którym
rata musi się zmieścić.

## Ujawnienia

- **Ponowne użycie części testowej (2. użycie).** Te same dane i ten sam podział (ziarno 20260928) co P1.
  Po P1 obejrzałem na części testowej pojedyncze AUC cech P1 (post hoc, opisane w RESULT P1): najlepsza była
  „najniższe saldo przed wypłatą / dochód”. Ta obserwacja współkształtowała pomysł dołka salda — przewaga
  z części testowej jest więc możliwa i należy ją odczytywać ostrożnie.
- Rozwój P2 wyłącznie na 1/3 rozwojowej; jedna wersja cech, nic nie strojono.
- Pozostałe ujawnienia jak w P1: prawda = zły kredyt (B/D), historia tylko przed kredytem, ≥ 10 miesięcy,
  daty +20 lat, kwoty /10 (stosunek saldo/rata niezmienny).

## Ramiona

- **C** — klasyka jak w P1 (9 cech, kalendarz, nominalnie).
- **R** (7 cech) — cykle od wypłaty, kwoty względem raty: min i mediana i 25. percentyl (najniższe saldo
  w cyklu / rata), mediana dochód/rata, mediana (dochód − wydatki)/rata, odsetek cykli, w których saldo
  spadło poniżej raty, mediana reżimu D dziennych wydatków.
- **R_cal** — cechy R na miesiącach kalendarzowych.
- **T** — cechy T z P1 (odniesienie do dochodu).
- **C+R**.

Protokół statystyczny bez zmian względem P1 (LDA 0,1; 5-krotna CV × 10 na części testowej; bootstrap
warstwowy 2000×; werdykt: dolna granica CI > 0 SUPPORTED, różnica > 0 MIXED, inaczej NOT SUPPORTED).

## Hipotezy

- **H1 (główna)**: AUC(C+R) > AUC(C) — drogowskaz z właściwym wzorcem dodaje do klasyki.
- **H2**: AUC(R) > AUC(T) — rata jako wzorzec lepsza niż dochód.
- **H3 (zegar)**: AUC(R) > AUC(R_cal).
- **H4**: AUC(R) > AUC(C).

## Wynik rozwojowy (1/3, 15 złych)

AUC: C 0,837, R 0,897, R_cal 0,888, T 0,859, C+R 0,910. H1 +0,073 [+0,016; +0,152], H2 +0,038
[−0,082; +0,156], H3 +0,009 [−0,063; +0,070], H4 +0,060 [−0,049; +0,180].

## Przewidywanie

H1 MIXED lub SUPPORTED (w P1 klasyka na teście była dużo silniejsza niż na rozwoju: 0,935 vs 0,837 — sufit
bliski). H2 dodatnie. H3 bez efektu (jak w P1 — zegar nie ma tu czego porządkować). H4 MIXED/NOT.
