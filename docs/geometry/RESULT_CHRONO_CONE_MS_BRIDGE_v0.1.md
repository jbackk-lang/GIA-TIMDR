# Wynik: chrono_cone_ratio — kontrole syntetyczne PRZESZŁY czysto, realne dane dają NIESPÓJNY, niewiarygodny sygnał (2026-09-21)

> Kontynuacja `PREREG_CHRONO_CONE_MS_BRIDGE_v0.1.md` (zamrożonej PRZED
> uruchomieniem czegokolwiek). Kod: `core/chrono_cone_bridge.py`
> (konstrukcja + kontrole syntetyczne), `core/real_chrono_cone_bridge.py`
> (test na trzech realnych domenach). Nic w obu plikach nie zostało
> zmienione po zobaczeniu któregokolwiek z wyników poniżej.

## 0. Rekapitulacja konstrukcji

`θ(t)` — faza rosnąca o `2π` między kolejnymi szczytami wygładzonego
(`smooth_window=5`) sygnału (peak-referenced phase). `r(t) =
|x(t)-mean|/std` — ciągła wersja istniejącej `anomalia_flags()`. `z(t)=t`
— Chronoproces, JAWNIE uproszczony do rodziny jednoelementowej (nie
pełna kongruencja `Γ:T×I→ℝ³`). Krzywa `(r·cosθ, r·sinθ, t)`.
`chrono_cone_ratio` = średni `r` w ostatnich 20% próbek okna / średni
`r` w pierwszych 20% — NOWA nazwa (audyt PREREG §1), koncepcyjnie
inspirowana, ale NIEZWIĄZANA kodowo z `funnel_ratio` (TIMDR-fusion-tools,
plazma TCABR).

## 1. Kontrole syntetyczne — PRZESZŁY, zgodnie z przewidywaniem PRZED uruchomieniem

| window_size | pozytywna (a vs b) | negatywna (b vs c) | PASSED |
|---|---|---|---|
| 128 | p=3.02e-11, r=1.000 (duży), mediana(a)=4.235 vs mediana(b)=1.003 | p=0.348, r=-0.142, mediana(b)=1.003 vs mediana(c)=1.030 | **TAK** |
| 256 | p=3.02e-11, r=1.000 (duży), mediana(a)=5.341 vs mediana(b)=1.015 | p=0.600, r=0.080, mediana(b)=1.015 vs mediana(c)=0.994 | **TAK** |

Wszystkie trzy grupy w 100% ważne (`0/30 NaN`) przy obu rozmiarach
okna — wystarczająco dużo pełnych okresów oscylacji (§7 PREREG), żeby
liczenie szczytów było stabilne. Wyniki dokładnie zgodne z
przewidywaniem zapisanym PRZED uruchomieniem (PREREG §6): (a) rosnąca
amplituda → `ratio` istotnie WYŻSZY (mediana 4.2–5.3, pełna separacja
`r=1.000`), (b) biały szum i (c) stała amplituda → oba blisko `ratio≈1`
(cylinder), BEZ istotnej różnicy między nimi (kontrola negatywna nie
dała fałszywego alarmu). Mechanizm robi dokładnie to, co ma robić, na
syntetyce.

## 2. Realne dane — WYNIK NIESPÓJNY, NIE potwierdzający stabilnej struktury leja

Test główny: `chrono_cone_ratio` na realnym segmencie (+ szum
syntetyczny addytywny, `sigma∈{0,0.1,0.3,0.5,1.0}` na wierzch, jak w
trzech poprzednich mostach realnych) vs Mann-Whitney U + rank-biserial
`r`. `SUPPORTED` = `p<0.05` i `|r|≥0.3` (średni/duży efekt).

### 2.1 Łożyska CWRU (3 typy defektu × 2 okna × 5 sigm = 30 komórek)

**11/30 (37%) formalnie SUPPORTED.** Przy `sigma=0.0` (najczystszy
wiersz):

| defekt | okno | r | p | status |
|---|---|---|---|---|
| ir_0021 | 256 | −0.338 | 0.0245 | SUPPORTED |
| ir_0021 | 512 | −0.093 | 0.533 | NOT_SUPPORTED |
| or6_0021 | 256 | −0.189 | 0.210 | NOT_SUPPORTED |
| or6_0021 | 512 | +0.267 | 0.073 | NOT_SUPPORTED |
| b_0021 | 256 | +0.031 | 0.841 | NOT_SUPPORTED |
| b_0021 | 512 | +0.707 | 1.85e-6 | SUPPORTED |

**Kluczowa obserwacja, decydująca o klasyfikacji**: kierunek efektu
(znak `r`) **ZMIENIA SIĘ ze zmianą samego rozmiaru okna, dla TEGO
SAMEGO typu defektu** — `or6_0021` idzie z `r=−0.189` (okno 256) na
`r=+0.267` (okno 512); `ir_0021` i `b_0021` trzymają znak, ale
`ir_0021` jest ujemny a `b_0021` dodatni — więc NAWET wśród komórek
formalnie `SUPPORTED` przy `sigma=0` dwa różne typy defektu dają
PRZECIWNE kierunki (`ir_0021: −0.338`, `b_0021: +0.707`). Na całej
siatce 30 komórek: 16 dodatnich, 14 ujemnych — praktycznie 50/50, brak
dominującego, fizycznie spójnego kierunku "leja".

### 2.2 Sejsmika Ridgecrest (2 stacje × 2 okna × 5 sigm = 20 komórek)

**5/20 (25%) SUPPORTED — wyłącznie stacja RIO, wyłącznie okno=512**
(wszystkie 5 poziomów szumu). Stacja CLC: **zero** komórek istotnych
przy żadnym oknie/szumie. Przy `sigma=0.0`:

| stacja | okno | r | p | status |
|---|---|---|---|---|
| CLC | 512 | +0.271 | 0.072 | NOT_SUPPORTED |
| CLC | 1024 | −0.164 | 0.276 | NOT_SUPPORTED |
| RIO | 512 | +0.393 | 0.0096 | SUPPORTED |
| RIO | 1024 | −0.216 | 0.153 | NOT_SUPPORTED |

Ten sam mainshock, ta sama zasada podziału tło/koda (`event_idx=6004`)
— ale kierunek ZNOWU zmienia się między oknem 512 a 1024 dla OBU
stacji (`CLC: +0.271→−0.164`, `RIO: +0.393→−0.216`). Ten wzorzec
(niespójność między stacjami I między rozmiarami okna) jest tym samym
zjawiskiem co w moście winding/crossing (punkt 19 skilla: "kierunek
NIESPÓJNY między stacjami") — powtórzone tu na innej, nowej
konstrukcji.

### 2.3 BTC/USD (1 okno=48 × 5 sigm = 5 komórek, `BLOCK_SIZE=48h`)

**2/5 (40%) SUPPORTED, tylko przy najniższym szumie** (`sigma=0.0:
p=0.0165, r=0.360`; `sigma=0.1: p=0.0224, r=0.344`) — efekt **zanika
monotonicznie** ze wzrostem szumu (`sigma=0.3: p=0.115`; `sigma=1.0:
p=0.674, r=0.064` pomijalny). Tylko 7 bloków wysokiej i 7 niskiej
zmienności dostępnych (`n=14` z 719 zwrotów godzinowych przy
`BLOCK_SIZE=48h`) — silne reużycie przy `N_WINDOWS=30`, słaba
replikacja niezależna od kierunku wyniku.

### 2.4 Podsumowanie kierunku na wszystkich 55 komórkach realnych

`r>0`: 31 komórek, `r<0`: 24 komórki — **56%/44%, blisko rozkładu
losowego (chance level)**, nie ma jednego, dominującego,
interpretowalnego kierunku "leja" w żadnej z trzech domen jako całości.

## 3. Wniosek

**Mechanizm zweryfikowany i działa poprawnie** (kontrole syntetyczne,
§1) — `chrono_cone_ratio` poprawnie odróżnia oscylację o rosnącej
amplitudzie od białego szumu i od oscylacji o stałej amplitudzie,
dokładnie zgodnie z przewidywaniem zapisanym przed uruchomieniem.

**Na trzech realnych domenach (łożyska/sejsmika/BTC) — te same, co w
poprzednich pięciu mostach tej rodziny — wynik jest NEGATYWNY/
NIEJEDNOZNACZNY, nie potwierdzający stabilnej struktury geometrycznej.**
Formalny odsetek `SUPPORTED` (11/30, 5/20, 2/5) jest wyraźnie niższy niż
w silnym wyniku łożyskowym z punktu 19 skilla (winding/crossing/
phase_winding: 123/150, 82%, efekt zawsze "duży", KIEROWANY tym samym
znakiem) — a co ważniejsze, **kierunek efektu w tej konstrukcji nie
jest stabilny**: zmienia się ze zmianą samego rozmiaru okna dla tego
samego realnego sygnału (łożyska: `or6_0021` zmienia znak między oknem
256/512; sejsmika: OBIE stacje zmieniają znak między oknem 512/1024),
a globalnie (55 komórek) kierunki rozkładają się niemal 50/50. To jest
zdiagnozowana PRZYCZYNA klasyfikacji negatywnej — nie sama liczba
`SUPPORTED`, którą samą w sobie (37%/25%/40%) dałoby się błędnie
odczytać jako "częściowy sukces", gdyby nie sprawdzić kierunku.

**Klasyfikacja końcowa (zgodnie z PREREG §9, kryterium stabilności
kierunku dodane jako uczciwa kontrola interpretacyjna, NIE jako
retroaktywna zmiana progu `SUPPORTED`/`NOT_SUPPORTED` per komórka)**:
`chrono_cone_bridge` — **NIE POTWIERDZONY jako diagnostyka geometryczna
na realnych danych M/S**, we WSZYSTKICH trzech domenach. Zgodnie z
protokołem (punkt 3/15 skilla): to jest pełnoprawna, negatywna
odpowiedź — mechanizm (peak-referenced phase + ciągła anomalia +
trywialny Chronoproces `z=t`) NIE jest tym samym, co uprzednio silny
sygnał geometryczny (embedding opóźniający + winding/crossing/phase
Hilberta) na tych samych trzech domenach, mimo współdzielonej
motywacji "lej vs cylinder".

**Status w ekosystemie**: NIE dopisywane do `Axioms_G_TIMDR_Geometry.md`
ani `Axioms_S_TIMDR_Signal.md` — eksploracyjna konstrukcja,
świadomie NIEaksjomatyzowana (wzorem całej rodziny mostów M/S↔G z
punktu 19 skilla), z jawnie negatywnym wynikiem na realnych danych
udokumentowanym tutaj.

## 4. Co zostaje otwarte (nieodłożone bez presji wykonania)

- Czy niestabilność kierunku ze zmianą okna wynika z samej definicji
  `chrono_cone_ratio` (proporcja brzeg/brzeg jest wrażliwa na to, ile
  pełnych okresów mieści się w oknie i gdzie akurat wypadają granice
  20%) czy z czegoś głębszego w konstrukcji `θ(t)`/`r(t)` — NIE
  zdiagnozowane tutaj, zostawione jako otwarte pytanie, nie
  rozstrzygane retroaktywnie po zobaczeniu wyniku.
- Korelacja Spearmana `chrono_cone_ratio` z istniejącą trójką
  (`winding_number`/`crossing_number`/`phase_winding`, punkt 19 skilla)
  na tych samych segmentach — czy to niezależne źródło (niska
  korelacja mimo podobnej/słabszej mocy) czy redundantne — NIE
  policzone w tej sesji, naturalny następny krok, jeśli konstrukcja
  miałaby być kontynuowana.
