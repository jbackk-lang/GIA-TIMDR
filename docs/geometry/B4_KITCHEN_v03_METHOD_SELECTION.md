# B4-Kitchen v0.3 — wybór metody statystycznej (wyłącznie na danych syntetycznych)

Ten dokument NIE dotyka realnych danych Kitchen (geometrii, audio, ani
zamrożonych `lambda_g`/`lambda_meta`). Cały poniższy eksperyment działa
wyłącznie na syntetycznych kontrolach — dokładnie tych samych generatorach
AR(1) i wektorach monotonicznych, jakich używały `B4_KITCHEN_ADDENDUM_v0.1.md`
i `PREREG_B4_KITCHEN_v0.2.md`. To jest praca metodologiczna PRZED napisaniem
`PREREG_B4_KITCHEN_v0.3.md`, nie próba na realnych danych.

## 1. Porównanie kandydatów na pojedynczej, zamrożonej parze ziaren

Ta sama para ziaren AR(1) co w v0.1/v0.2 (`20260917`/`20260918`, `phi=0.8`,
długość 1645). Skrypt: `core/_kitchen_v03_candidate_methods_synthetic_only.py`.

| metoda | p kontroli + | przeszła + | p kontroli − | przeszła − | OBIE |
|---|---|---|---|---|---|
| permutacja blokowa L=12 (v0.2) | 0.00010 | tak | 0.01730 | **nie** | nie |
| permutacja blokowa L=20 | 0.00010 | tak | 0.02070 | **nie** | nie |
| permutacja blokowa L=25 | 0.00010 | tak | 0.02190 | **nie** | nie |
| permutacja blokowa L=40 | 0.00010 | tak | 0.02160 | **nie** | nie |
| Spearman z korektą HAC, bw=12 | ~0 | tak | 0.01193 | **nie** | nie |
| Spearman z korektą HAC, bw=20 | ~0 | tak | 0.01388 | **nie** | nie |
| Spearman z korektą HAC, bw=25 | ~0 | tak | 0.01442 | **nie** | nie |
| Spearman z korektą HAC, bw=40 | ~0 | tak | 0.01777 | **nie** | nie |
| Spearman z korektą HAC, bw=60 | ~0 | tak | 0.01788 | **nie** | nie |
| Spearman z n_eff AR(1) | ~0 | tak | 0.02326 | **nie** | nie |

**Zaskakujący, ale ważny wynik: żadna z 10 wypróbowanych metod nie
przechodzi kontroli negatywnej na TEJ JEDNEJ, zamrożonej parze ziaren** —
mimo prób w dwóch zupełnie różnych rodzinach metod (permutacja blokowa w 4
długościach, korekta HAC w 5 przepustowościach, plus efektywne-N AR(1)).
Zwiększanie długości bloku/przepustowości NIE poprawia sytuacji monotonicznie
(L=20/25/40 dają p wyższe niż L=12, ale wciąż poniżej 0.05; podobnie HAC).

## 2. Kluczowa diagnoza: pojedyncze ziarno nie może rozstrzygnąć kalibracji

Test o progu `alpha=0.05` z DEFINICJI odrzuca prawdziwą hipotezę zerową w
ok. 5% przypadków — to nie błąd, tylko definicja progu istotności. Jedna
konkretna para ziaren (`20260917`/`20260918`) może być akurat jednym z tych
~5% "pechowych" losowań, nawet dla poprawnie skalibrowanej metody. Wynik z
§1 sam w sobie NIE dowodzi, że wszystkie 10 metod jest wadliwych — dowodzi
tylko, że żadna nie przeszła TEGO JEDNEGO losowania. Żeby odróżnić
"metoda wadliwa" od "pechowe losowanie", trzeba spojrzeć na częstość
fałszywych alarmów po wielu NIEZALEŻNYCH losowaniach.

## 3. Kalibracja na 300 niezależnych losowaniach AR(1)

Skrypt: `core/_kitchen_v03_calibration_check_synthetic_only.py`. 300 par
niezależnych serii AR(1) (`phi=0.8`, długość 1645), ziarna wygenerowane
deterministycznie z `rng(seed=42).integers(1, 10_000_000, size=(300,2))` —
inne niż w §1, nie wybierane ręcznie. Tylko dwie metody zamkniętej postaci
(bez permutacji — permutacja blokowa jest zbyt kosztowna obliczeniowo do
powtórzenia 300×10000 razy w budżecie czasowym tej sesji, jawnie zgłoszone
jako otwarty punkt, nie pominięte po cichu):

| metoda | odsetek fałszywych alarmów | 95% CI (Wilsona) | 0.05 wewnątrz CI? |
|---|---|---|---|
| Spearman z korektą HAC, bw=25 | 5.33% (16/300) | [3.31%, 8.49%] | **tak** |
| Spearman z n_eff AR(1) | 4.33% (13/300) | [2.55%, 7.27%] | **tak** |

**Obie metody są statystycznie zgodne z poprawną kalibracją na poziomie
alpha=0.05** — nominalne 5% mieści się wygodnie w obu przedziałach
ufności. To silnie sugeruje, że pojedyncza porażka z §1 (p w zakresie
0.012–0.023 dla wszystkich metod) była właśnie pechowym losowaniem, NIE
dowodem wadliwości tych dwóch konkretnych metod.

## 4. Wniosek i wybór dla v0.3

- Permutacja blokowa (v0.2 i warianty L z §1) pozostaje niezweryfikowana
  wielokrotnie — zbyt kosztowna obliczeniowo w tej sesji. Nie jest
  odrzucona, tylko nierozstrzygnięta na tym samym poziomie rygoru co
  metody zamkniętej postaci.
- **Wybrana metoda dla v0.3: Spearman z korektą efektywnej liczebności
  próby AR(1) (`n_eff = n·(1−r1x·r1y)/(1+r1x·r1y)`)** — prostsza,
  łatwiejsza do ręcznego zweryfikowania niż HAC (jeden parametr mniej —
  brak wyboru przepustowości), z odsetkiem fałszywych alarmów bliższym
  nominalnym 5% (4.33% vs 5.33% dla HAC) w tym eksperymencie.
- **Ziarna kontroli dla v0.3 NIE są tymi z §1** — świadomie nowa para,
  wybrana WEDŁUG REGUŁY (nie ręcznie po sprawdzeniu, czy przechodzi),
  udokumentowana w `PREREG_B4_KITCHEN_v0.3.md` PRZED jakimkolwiek
  sprawdzeniem, czy przechodzi. Ponowne użycie `20260917`/`20260918`
  byłoby bezsensowne — już wiemy, że ta konkretna para daje p=0.023 dla tej
  metody (wynik z §1), więc jej ponowne zamrożenie jako "kontrola" nie
  miałoby wartości diagnostycznej.

## 5. Meta-wniosek dla ekosystemu (do rozważenia, nie wymuszony tutaj)

Projekt kontroli negatywnej oparty na POJEDYNCZEJ parze ziaren (użyty w
v0.1 i v0.2, a wcześniej w innych mostach tego ekosystemu) ma ślepy punkt:
nie odróżnia "metoda wadliwa" od "to akurat było niefortunne 1/20
losowanie". Kalibracja wielokrotna (jak w §3) jest bardziej informacyjna,
kosztem znacznie większego budżetu obliczeniowego. Warto rozważyć jako
ogólną poprawkę protokołu w `timdr-signal-framework`/`TIMDR-Math-Formalism`
— nie zrobione tutaj, tylko odnotowane jako obserwacja.
