# Wynik: most M/S↔topologia/K na REALNYCH danych sejsmicznych (Ridgecrest 2019) + szum syntetyczny

> Streszczenie `PREREG_REAL_SEISMIC_NOISE_ROBUSTNESS.md` — standardowa
> kolejność (freeze→build), w odróżnieniu od mostu łożyskowego. Kod:
> `core/real_seismic_noise_robustness_bridge.py`. `EVENT_IDX=6004`
> (t=60,04s), obliczony z realnego czasu mainshocku, niezależnie od
> danych. Siatka: 2 stacje × 5 metryk × 2 okna × 5 poziomów szumu =
> 100 komórek. Data: 2026-09-15. Czas wykonania: 46,0 s.

## Wynik surowy — **47/100 komórek siatki przeszło (47%)**

Ani powtórka porażki serii syntetycznej (1/50), ani powtórka silnego,
odpornego na szum sukcesu mostu łożyskowego (123/150, 82%) — coś
pomiędzy, wyraźnie słabsze i mniej spójne niż łożyska.

| metryka | CLC | RIO | razem |
|---|---|---|---|
| `winding_number` | 6/10 | 7/10 | 13/20 |
| `crossing_number` | 6/10 | 4/10 | 10/20 |
| `h1_persistence` | 2/10 | 8/10 | 10/20 |
| `phase_winding` | 5/10 | 4/10 | 9/20 |
| `torsion_max\|τ\|` | 0/10 | 5/10 | 5/20 |

**Zgodnie z oczekiwaniem a priori (sekcja 4 pre-rejestracji), efekt
JEST obecny w części komórek, ale w odróżnieniu od mostu łożyskowego —
nie w sposób spójny między dwiema stacjami ani odporny na szum.**

## Znalezisko #1: kierunek efektu ZALEŻY OD STACJI (nie od metryki)

Przy `window=64, σ=0,00`: `winding_number` daje `r=+0,182` (CLC, słaby,
niepassed) vs `r=-0,571` (RIO, silny, passed) — **przeciwny znak** na
tym samym zdarzeniu, dwóch różnych stacjach tej samej sieci sejsmicznej.
`torsion_max|τ|` jest bardziej spójna kierunkowo (dodatnia na obu
stacjach), ale w ogóle nie przechodzi na CLC (0/10) mimo dodatniego,
czasem umiarkowanego `r`. **To jest jakościowo inna, gorsza forma
niespójności niż w moście łożyskowym**, gdzie te same trzy metryki
(`winding`/`crossing`/`phase_winding`) miały identyczny kierunek
efektu we WSZYSTKICH trzech niezależnych typach defektu. Tutaj
"replikacja" (2 stacje, to samo zdarzenie) nie potwierdza spójności
kierunku — sugeruje, że efekt jest silnie zależny od charakterystyki
instrumentu/miejsca (odległość i azymut od epicentrum, lokalna
geologia), nie od wspólnej cechy "sejsmiczności" per se.

## Znalezisko #2: efekt NIE jest odporny na szum (w odróżnieniu od łożysk)

W moście łożyskowym `winding`/`crossing`/`phase_winding` utrzymywały
duży efekt (r≥0,8) aż do σ=1,0. Tutaj większość komórek, które
przechodzą przy σ=0,00–0,10, PRZESTAJE przechodzić przy σ≥0,30–0,50 —
znacznie bliżej wzorca kruchości znanego z serii CZYSTO SYNTETYCZNEJ
(`RESULT_TOPOLOGICAL_BRIDGE_MS_SCOPE.md`) niż wzorca odporności z mostu
łożyskowego. Przykład RIO/`h1_persistence` (najsilniejsza kombinacja
tutaj): `r=-0,76` (σ=0,00, duży) → `r=-0,31` (σ=1,00, średni, ale
`passed=True` cały czas dzięki niskiemu p) — to jedna z niewielu
kombinacji, która trzyma się w całej siatce; większość innych nie.

## Diagnoza — sprawdzona bezpośrednio na danych, nie zgadnięta

Policzono kurtozę CAŁEGO regionu (tła 60s vs kody 300s) ORAZ kurtozę
LOKALNĄ (per okno 64 próbek, tak jak faktycznie widzi ją `metric_fn`):

```
CLC: tło  (cały region) kurt=-0.30   koda (cały region) kurt=5.46
CLC: tło  (mediana lokalna, okno 64) kurt=-0.55   koda (mediana lokalna) kurt=-0.43
RIO: tło  (cały region) kurt=0.21    koda (cały region) kurt=7.41
RIO: tło  (mediana lokalna, okno 64) kurt=-0.63   koda (mediana lokalna) kurt=-0.98
```

**Kluczowa różnica względem mostu łożyskowego**: kurtoza CAŁEGO regionu
kody jest silnie podniesiona (5,5–7,4) — ale to wynika z NIELICZNYCH,
ekstremalnie silnych okien blisko `event_idx` (główny wstrząs/fale P i
S), rozproszonych wśród setek znacznie spokojniejszych okien kody
odległej w czasie (koda zanika przez 5 minut). Kurtoza LOKALNA (per
pojedyncze okno 64 próbek — czyli to, co faktycznie widzi każda
`metric_fn`) jest w rzeczywistości PODOBNA albo NIŻSZA w kodzie niż w
tle (RIO: -0,98 vs -0,63) — **odwrotnie niż w moście łożyskowym**, gdzie
lokalna kurtoza defektu była systematycznie podniesiona względem
zdrowego łożyska w całym regionie.

**Wniosek mechanistyczny**: region "pozytywny" (koda) w tym moście jest
WEWNĘTRZNIE NIEJEDNORODNY — miesza nieliczne okna o ekstremalnej
energii (blisko `event_idx`) z licznymi oknami stopniowo cichnącej kody,
lokalnie niewiele różniącymi się strukturalnie od tła. To zupełnie inna
sytuacja niż łożysko, gdzie CAŁY zdefiniowany region defektu był
jednorodnie inny niż zdrowe. Prawdopodobnie stąd: (a) słabszy, mniej
spójny efekt niż łożyska, (b) brak odporności na szum (bo tylko
nieliczne okna niosą sygnał, łatwo zagłuszane), (c) niespójność
kierunku między stacjami (który dokładnie moment/faza fali trafia w
próbkę zależy od losowania i od różnic w rejestracji między stacjami).

## Ograniczenia — jawnie, nie pominięte

1. **n=1 zdarzenie.** Dwie stacje to NIE dwa niezależne trzęsienia —
   to ten sam mainshock zarejestrowany dwoma instrumentami. Rozbieżność
   kierunku między nimi (Znalezisko #1) jest realną, wartościową
   informacją, ale nie należy jej mylić z "efekt nie replikuje się
   między zdarzeniami" — mamy tylko jedno zdarzenie.
2. **Region pozytywny jest niejednorodny w czasie** — nie została
   podjęta próba oddzielenia fazy silnego wstrząsu od dalszej kody
   (byłoby to nowe, osobne pytanie, wymagające własnej pre-rejestracji
   z podziałem regionu kody na pod-okna czasowe).
3. **150→100 komórek bez korekty Bonferroniego**, ta sama konwencja co
   poprzednie mosty (raportowanie surowe, przebieg eksploracyjny na
   pełnej siatce).

## Porównanie trzech przebiegów "most na realnych danych" do tej pory

| przebieg | przeszło | kierunek | odporność na szum | mechanizm |
|---|---|---|---|---|
| Seria syntetyczna (5 mostów) | 1/50 | niespójny/odwrócony | krucha | entropia szumu w embeddingu (4/5) + maskowanie amplitud (1/5) |
| Łożyska CWRU | 123/150 | spójny (4/5 metryk) | duża (trzyma się do σ=1,0) | częściowo kurtoza lokalna (wykluczona jako JEDYNE wyjaśnienie), region pozytywny jednorodny |
| Sejsmika Ridgecrest | 47/100 | NIESPÓJNY między stacjami | krucha (znika przy σ≥0,3-0,5) | region pozytywny niejednorodny (mieszanka silnego wstrząsu i cichnącej kody), lokalna kurtoza NIE podniesiona |

**Uczciwy wniosek zbiorczy**: "realne dane" nie jest jedną kategorią o
jednolitym zachowaniu — kluczowy czynnik to nie "realność" danych per
se, tylko to, czy zdefiniowany region pozytywny jest WEWNĘTRZNIE
JEDNORODNY (łożyska: tak, defekt jest stały w czasie nagrania) czy
NIEJEDNORODNY (sejsmika: koda zanika, miesza fazy o bardzo różnej
energii). To jest nowa, wartościowa obserwacja metodologiczna,
niewidoczna ani w serii syntetycznej, ani w pierwszym moście na
realnych danych osobno.
