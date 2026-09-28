# PREREG MUZ P1 v0.1: zegar od wypłaty i odniesienie do własnego dochodu w budżecie (dane publiczne PKDD'99)

Stan: **zamrożone przed uruchomieniem na części testowej**. Jedno uruchomienie. Kod: `core/muz_berka_p1.py`
(sha256 przy zamrożeniu podany w commicie PREREG).

## Pytanie

Czy drogowskazy TIMDR przeniesione na budżet domowy (MUZ) — **kotwica = zegar od wypłaty** zamiast miesiąca
kalendarzowego, **odniesienie = własny dochód** zamiast kwot nominalnych, **reżim D** dziennych wydatków — lepiej
wskazują kłopoty finansowe niż klasyczne cechy kalendarzowe w kwotach nominalnych?

## Dane

PKDD'99 Discovery Challenge (Berka, Sochorová; czeski bank, zanonimizowany, publiczny). Kopia w
`DATA/berka/repo` (fin_trans, fin_loan, fin_account). **Żadnych danych prywatnych użytkownika.**
Zbiór ma daty przesunięte o +20 lat (2013–2018) i kwoty podzielone przez 10 — nie wpływa to na testowane stosunki.

## Operacjonalizacja (ujawnienie odstępstw od pierwotnego sformułowania)

1. Pierwotne pytanie brzmiało „mniej fałszywych alarmów o wzroście wydatków”. Zbiór nie ma etykiet alarmów,
   więc **prawdą odniesienia jest status kredytu**: zły = B lub D (niespłacony / zadłużony), dobry = A lub C.
   Cechy liczone **wyłącznie z historii rachunku przed datą przyznania kredytu** — to prognoza, nie opis.
2. Zamiast wskaźnika CPI dla kategorii użyto **odniesienia do własnego dochodu w tym samym cyklu** (E/I,
   saldo/I, kategorie/I). Zasada odniesienia: sygnał nakładany na wzorzec z tego samego medium. CPI dla każdej
   kategorii nie jest dostępne w zbiorze — pominięte.
3. Reguła wykonalności: ≥ 10 miesięcy historii przed kredytem (N_cyk ≥ 10) i ≥ 3 niepuste cykle. Z 682
   kredytów zostaje 472 (47 złych).

## Ramiona

- **C** (klasyka, 9 cech): miesiące kalendarzowe, kwoty nominalne — średnie/min/odchylenie salda, liczba dni
  z ujemnym saldem, średni wpływ, średni wydatek i jego odchylenie, zmiana wydatków (3 ostatnie vs 3 pierwsze
  miesiące), liczba transakcji wydatkowych na miesiąc.
- **T** (TIMDR, 11 cech): cykle od dnia wypłaty (dzień = mediana dnia największego wpływu z innego banku,
  gdy ≥ 60% miesięcy; inaczej największego wpływu; inaczej 1. dzień), wszystko względem dochodu cyklu:
  mediana r = E/I, MAD(r), odsetek cykli z r > 1, trend Spearmana r, min i mediana (saldo minimalne / I),
  gospodarstwo domowe / I, ubezpieczenia / I, wypłaty gotówki / I, mediana D (reżim zdarzeń: η/(1−η) dziennych
  liczebności wydatków), odsetek cykli z ujemnym saldem.
- **T_cal**: te same cechy T, ale cykle = miesiące kalendarzowe (efekt zegara).
- **T_nom**: te same cechy T na cyklach od wypłaty, ale kwoty nominalne zamiast /I (efekt odniesienia).
- **C+T**: połączenie.

Źródło dnia wypłaty (wszystkie 472): wpływ 321, COB 136, kalendarz 15.

## Protokół

- Podział **po rachunkach**, warstwowo wg etykiety, ziarno 20260928: 1/3 rozwój (156 kredytów, 15 złych),
  2/3 test (316, 32 złe). Rozwój użyty tylko do sprawdzenia, że cechy działają; nic nie strojono po nim.
- Na części testowej: LDA ze ściągnięciem 0,1, standaryzacja na foldzie uczącym, 5-krotna warstwowa CV
  powtórzona 10× (wynik out-of-fold uśredniony po powtórzeniach), AUC dla złych kredytów.
- Przedziały: bootstrap warstwowy 2000× różnicy AUC na tych samych wynikach, 95% percentylowe.
- Werdykt: dolna granica CI > 0 → SUPPORTED; różnica > 0 bez tego → MIXED; różnica ≤ 0 → NOT SUPPORTED.

## Hipotezy

- **H1**: AUC(T) > AUC(C) — drogowskazy TIMDR bije klasykę.
- **H2 (zegar)**: AUC(T) > AUC(T_cal).
- **H3 (odniesienie)**: AUC(T) > AUC(T_nom).
- **H4**: AUC(C+T) > AUC(C) — T dodaje coś do klasyki.

## Wynik rozwojowy (1/3, ujawnione przed testem)

AUC: C 0,837, T 0,859, T_cal 0,829, T_nom 0,823, C+T 0,800. Wszystkie różnice w granicach szumu
(15 złych kredytów): H1 +0,022 [−0,057; +0,106], H2 +0,030 [−0,027; +0,094], H3 +0,036 [−0,073; +0,144],
H4 −0,037 [−0,130; +0,046].

## Przewidywanie przed testem

Kierunki H1–H3 dodatnie, ale przy 32 złych kredytach CI prawdopodobnie obejmą 0 → najpewniej MIXED.
Klasyka jest silna, bo saldo minimalne i dni z ujemnym saldem wprost niosą kłopoty. Jeśli T nie przegrywa
z C, to i tak wystarcza MUZ jako warstwa porządkująca (bez kwot nominalnych, bez kalendarza).

## Ograniczenia

Jeden bank, lata 90., mała liczba złych kredytów; kredyt ≠ „alarm o wzroście wydatków”; brak CPI. Wynik
dotyczy przenośności drogowskazów na dane transakcyjne, nie jakości samego agenta MUZ.
