# Pre-rejestracja: chrono_sphere_bridge v0.2 — powtarzający się profil kontroli pozytywnej (cykliczne "kopnięcia" kierunku)

> Status: PRE-REJESTRACJA, zamrożona PRZED zmianą kodu (nowy generator
> jeszcze nie napisany w chwili zapisania tego dokumentu). Data:
> 2026-09-22. Druga wersja `chrono_sphere_bridge` — v0.1 ODRZUCONY na
> etapie kontroli syntetycznej (`RESULT_CHRONO_SPHERE_BRIDGE_v0.1.md`):
> kontrola pozytywna (pojedynczy skok kierunku + "zamrożenie") dała
> wynik ODWROTNY do przewidywanego (`r=-1.000`, stabilne na wszystkich
> rozmiarach okna). Diagnoza: `Ω_win` mierzy CIĄGŁE drganie kierunku
> ważone chwilową siłą sygnału, nie pojedynczy skok po którym następuje
> stabilizacja. v0.2 NIE zmienia metryki ani konstrukcji T_G/bramki —
> zmienia WYŁĄCZNIE profil kontroli pozytywnej, żeby pasował do tego,
> co metryka faktycznie wykrywa, i do fizyki realnego uszkodzenia
> łożyska (powtarzające się uderzenia, nie jednorazowy step).

## 0. Co jest dziedziczone z v0.1 bez zmian

Wszystko z `PREREG_CHRONO_SPHERE_BRIDGE_v0.1.md` §2 (dane), §3
(bramka niezależności, transformacja `T_G`, maskowanie `r(t)`), §4
(definicja `Ω_win`, zakres `Δt`), §6 (plan testu real-data: trzy pary
fault-vs-fault, korekta Bonferroniego), §7 (klasyfikacja końcowa) —
**bez zmian**. Zmienia się WYŁĄCZNIE generator kontroli pozytywnej
(a) w §5 i interpretacja, co `Ω_win` ma wykrywać (zapisana explicite
poniżej, nie tylko w komentarzu kodu).

**Reinterpretacja celu metryki (zapisana wprost, jak ustalono)**:
`Ω_win` w v0.2 ma wykrywać "ciągłe lub powtarzające się drganie
kierunku", nie pojedynczy incydent. Kontrola negatywna (b) i bramka
sanity (c) pozostają identyczne jak w v0.1.

## 1. Nowy profil kontroli pozytywnej (a) — cykliczne "kopnięcia"

Zamiast jednego trwałego skoku w połowie okna: **periodyczne,
KRÓTKIE, trójkątne impulsy** dodane do jednego kanału (`c_x`, ten sam
kanał przez cały czas — uzasadnienie fizyczne: uderzenie od
uszkodzenia łożyska konsekwentnie najsilniej pobudza czujnik
najbliższy miejscu uszkodzenia, nie losowy kanał za każdym razem),
na tle niezależnego szumu identycznego jak w kontroli negatywnej (b)
— jedyna różnica między (a) i (b) to OBECNOŚĆ kopnięć, nic więcej.

**Parametry zamrożone PRZED implementacją**:

```
N_KICKS = 8                          # liczba kopnięć w oknie, niezależnie od window_size
kick_period = window_size // N_KICKS
kick_width  = kick_period // 5       # krótki impuls względem odstępu między kopnięciami
K = 8.0                              # amplituda szczytowa (ta sama stała co v0.1, SYN_JUMP_K -> SYN_KICK_K)
```

Kształt impulsu: **trójkątny** (liniowe narastanie do szczytu w
środku `kick_width`, liniowy spadek z powrotem do zera), NIE
prostokątny — celowo, żeby uniknąć płaskiego "szczytu" (fragmentu o
stałej wartości = zerowa prędkość kątowa w środku impulsu), czyli
dokładnie tego mechanizmu, który zawiódł w v0.1. Przy trójkącie
kierunek `u(t)` zmienia się CIĄGLE przez cały czas trwania impulsu —
narastanie i opadanie to dwie osobne, ciągłe fazy ruchu kątowego.

```
dla i = 0..N_KICKS-1:
    center_i = i * kick_period + kick_period // 2
    dla t w [center_i - kick_width//2, center_i + kick_width//2]:
        odleglosc = |t - center_i|
        wklad(t) = K * (1 - odleglosc / (kick_width/2))     # trójkąt, 0 na krawędziach, K w środku
        c_x[t] += max(0, wklad(t))
```

Między kopnięciami (`kick_period - kick_width` próbek z każdego
okresu, czyli większość okna): `c_x`, `c_y`, `c_z` to CZYSTY niezależny
szum, identyczny mechanizm jak (b) — więc (a) = (b) + nałożone
kopnięcia, nie inny proces od zera. To gwarantuje uczciwe porównanie:
jeśli (a) i (b) się nie różnią, to WYŁĄCZNIE dlatego, że kopnięcia
nie mają efektu, nie dlatego, że tło samo w sobie jest inne.

## 2. Przewidywanie (zapisane PRZED uruchomieniem)

`median(Ω_win(a)) > median(Ω_win(b))` — bo (a) zawiera WSZYSTKO, co ma
(b) (ten sam ciągły szum tła), PLUS dodatkowe, powtarzające się,
wysoko ważone (bo `r(t)` rośnie podczas kopnięcia) przejścia kątowe.
W przeciwieństwie do v0.1, tu NIE MA długiego odcinka "zamrożenia" —
większość okna to nadal szum tła identyczny z (b), więc jeśli
kopnięcia w ogóle coś dodają do średniej ważonej, powinny podnosić ją
W GÓRĘ, nie w dół. Mann-Whitney U + rank-biserial `r`, oczekiwane
`p<0.05`, `|r|≥0.3`, ten sam `Δt=1` co w kontrolach v0.1 (stabilność
między `Δt` sprawdzana dopiero na danych realnych, §4/§6 v0.1,
niezmienione).

**Ryzyko odnotowane wprost, nie ukryte**: jeśli kopnięcia są zbyt
rzadkie (tylko 8 na okno) względem gęstego szumu tła (zmiana kierunku
na KAŻDEJ próbce w (b)), efekt może być rozcieńczony przez dużą liczbę
"zwykłych" próbek szumu między kopnięciami — to jest dokładnie to, co
kontrola ma sprawdzić, nie założenie z góry.

## 3. Bramka sanity (c) i kontrola negatywna (b)

Bez zmian względem v0.1 — `make_gate_should_reject`,
`make_independent_noise_3`, te same stałe (`SYN_GATE_NOISE_EPS=0.05`,
`SYN_NOISE_STD=1.0`), ta sama kolejność wykonania (najpierw bramka
sanity, dopiero potem test główny, zatrzymanie jeśli bramka nie
przejdzie).

## 4. Status

Zamrożone. Kolejność: (1) nowy generator `make_periodic_kicks` w
`core/chrono_sphere_bridge.py`, zastępujący (nie kasujący —
`make_direction_jump` v0.1 zostaje w kodzie jako udokumentowany,
odrzucony wariant) poprzedni profil kontroli pozytywnej; (2)
uruchomienie kontroli na tych samych trzech rozmiarach okna
(500,1000,2000); (3) jeśli PASSED: dopiero wtedy `core/
real_chrono_sphere_bridge.py` na danych CWRU, plan real-data
niezmieniony z v0.1 §6; (4)
`docs/geometry/RESULT_CHRONO_SPHERE_BRIDGE_v0.2.md` z pełnym wynikiem,
łącznie z ponownym odrzuceniem, jeśli do niego dojdzie.
