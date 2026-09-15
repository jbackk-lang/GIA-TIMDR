# Pre-rejestracja (napisana PO fakcie, na wyraźną prośbę użytkownika): most M/S↔topologia/K na REALNYCH danych + szum syntetyczny

> **ZASTRZEŻENIE O KOLEJNOŚCI, na samej górze, nie ukryte.** Ten
> dokument, w odróżnieniu od wszystkich pięciu poprzednich
> `PREREG_*.md` w tym repo, został napisany **PO** implementacji i
> uruchomieniu kodu (`core/real_bearing_noise_robustness_bridge.py`),
> nie przed. Użytkownik poprosił o to wprost: *"zróbmy odwrotnie
> przygotujemy na koniec zbuduj teraz"*. To jest jawne odejście od
> standardowej kolejności tego ekosystemu (freeze→run, nie run→freeze
> opisany post-hoc).
>
> **Co to zmienia, a co nie.** Nie zmienia to najważniejszej własności:
> parametry (dobór plików, definicja generatora okna+szumu, siatka
> `WINDOW_SIZES`/`SIGMAS`, `N_WINDOWS`/`SEED`/`ALPHA`) zostały zapisane
> w kodzie i **nie były zmienione po zobaczeniu wyniku** — kod i wynik
> trafiły do repo jednym commitem, bez iteracji "spróbuj, zobacz,
> popraw". Zmienia to natomiast **weryfikowalność z zewnątrz**: przy
> standardowej kolejności ktoś czytający historię commitów widzi PREREG
> zacommitowany PRZED wynikiem (dowód braku data-snoopingu widoczny w
> samej historii git). Tutaj tego dowodu w historii git nie ma — jest
> tylko moje słowo, że nic nie zmieniłem po fakcie. To jest realna,
> słabsza forma dowodu niż w poprzednich pięciu próbach, i użytkownik
> powinien to wiedzieć wprost, nie tylko przeczytać wynik.

## 0. Kontekst i pytanie

Poprzednia seria pięciu mostów (`RESULT_TOPOLOGICAL_BRIDGE_MS_SCOPE.md`)
testowała wyłącznie na **syntetycznym** sygnale (dwie niewspółmierne
częstotliwości + szum). Użytkownik zapytał: *"jesli znamy dobre dane to
mozna zaszumic nimi i obserwowac czy sie dubluja czy cos innego"*.

Operacjonalizacja (ustalona w rozmowie, przed uruchomieniem kodu):
"dobre dane" = realne, oznakowane nagrania przyspieszeniomierza łożysk
CWRU (zdrowe vs trzy typy defektu — patrz §1). "Zaszumić" = dodać
syntetyczny szum gaussowski o rosnącej mocy NA WIERZCH realnego
sygnału. "Czy się dublują" = czy przy rosnącym szumie realny defekt
staje się nieodróżnialny (statystycznie) od realnego stanu zdrowego —
i czy krzywa degradacji przypomina tę z syntetycznej serii (nagłe
załamanie przy niskim σ) czy jest jakościowo inna.

## 1. Dane (zamrożone)

Cztery pliki CWRU (`TIMDR-Industrial-Predict/data/cwru_bearing/`), po
1536 próbek, 1797 RPM, uszkodzenie 0.021":
`normal_1797_de_first1536.csv` (zdrowe, klasa negatywna),
`ir_0021_1797_de_first1536.csv` (bieżnia wewnętrzna),
`or6_0021_1797_de_first1536.csv` (bieżnia zewnętrzna),
`b_0021_1797_de_first1536.csv` (kulka). Trzy niezależne przebiegi
(każdy defekt osobno vs zdrowe), nie mieszane.

## 2. Metryki (bez zmian względem poprzednich pięciu mostów)

Reużyte 1:1, kod niezmieniony: `torsion_max|tau|`, `winding_number`,
`crossing_number`, `h1_persistence`, `phase_winding` — patrz odnośne
`core/*_ms_bridge.py`.

## 3. Generator: okno realnego sygnału + szum (zamrożone)

Segmentacja na NIEZACHODZĄCE bloki `window_size` próbek (zgodnie z
operatorem okna partycji `P_k(x)` z protokołu — patrz skill §2).
Segment wybierany deterministycznie z `seed` (modulo liczba dostępnych
segmentów). Szum gaussowski `N(0, sigma_frac·std(segment))` dodany PO
wyborze segmentu, własnym `rng` zaseedowanym tym samym `seed`.

**Ważna różnica względem poprzednich pięciu mostów**: tam `sigma=0`
było zdegenerowanym wierszem siatki (kontrola negatywna = czysty szum
= stała zerowa). Tutaj `sigma=0` to NAJCZYSTSZY wiersz — czy metryka w
ogóle odróżnia realny defekt od realnego zdrowia bez żadnego dodanego
szumu.

## 4. Siatka (zamrożona)

`WINDOW_SIZES=(32,64)` → 48 / 24 dostępnych segmentów (1536/32, 1536/64).
`SIGMAS=(0.0,0.1,0.3,0.5,1.0)` — ułamek własnego std segmentu, identyczna
siatka nominalna co w poprzednich pięciu mostach. `N_WINDOWS=30`,
`SEED=0`, `ALPHA=0.05` — bez zmian względem poprzednich mostów.

**Jawnie odnotowane ograniczenie**: przy `window_size=64` dostępnych
jest tylko 24 segmenty < `N_WINDOWS=30` → część z 30 losowań MUSI
ponownie użyć tego samego realnego segmentu (z innym, świeżym szumem).
Oznaczone w wyniku kolumną `reuse`. Przy `window_size=32` (48 segmentów)
reużycie nie jest potrzebne.

**Kontrola negatywna A vs B**: mamy tylko JEDNO realne nagranie zdrowego
łożyska (1536 próbek) — `negative_generator_a` i `negative_generator_b`
to funkcjonalnie IDENTYCZNY generator (oba losują z tego samego pliku
`normal`), a jedyne źródło niezależności między nimi to przesunięcie
seeda o +1, które `run_controls()` robi wewnętrznie. To jest słabszy
test specyficzności niż w poprzednich mostach (gdzie neg_a i neg_b były
dwoma RÓŻNYMI procesami generującymi) — test tutaj sprawdza "czy
metryka fałszywie różnicuje dwa różne okna/szumy TEGO SAMEGO realnego
nagrania zdrowego łożyska", nie "czy różnicuje dwa NIEZALEŻNE realne
nagrania zdrowych łożysk" (tych drugich nie mamy).

## 5. Oczekiwania a priori (formułowane retrospektywnie, patrz zastrzeżenie na górze)

Ponieważ ten dokument powstał po zobaczeniu wyniku, oczekiwania a
priori NIE mogą być tu przedstawione jako niezależny dowód — byłoby to
nieuczciwe. To, co można uczciwie powiedzieć: przed uruchomieniem kodu,
w rozmowie z użytkownikiem, hipoteza robocza była NEUTRALNA co do
kierunku ("zobaczmy, czy realne dane zachowują się jak syntetyczne
[załamanie przy niskim σ] czy inaczej"), bez konkretnej ilościowej
prognozy — w przeciwieństwie do mostu OAM (gdzie konkretna wartość
`w1·N/(2π)=47.75` była przewidziana przed uruchomieniem i faktycznie
zaobserwowana). Ten brak ilościowej prognozy a priori jest kolejnym,
odrębnym ograniczeniem tego mostu względem poprzednich pięciu — patrz
`RESULT_REAL_BEARING_NOISE_ROBUSTNESS.md` po pełny wynik i uczciwą
diagnozę mechanizmu.
