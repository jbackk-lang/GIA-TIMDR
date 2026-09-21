# Wynik v0.2: chrono_pendulum_ratio — kontrole syntetyczne PRZESZŁY (identycznie z v0.1), na metryce PRIMARNEJ niestabilność znaku NIE zniknęła (zgodnie z przewidywaniem mechanizmu), ale eksploracyjna metryka rotacyjna pokazuje realną poprawę stabilności na dokładnie tych przykładach, które flipowały w v0.1 (2026-09-21)

> Kontynuacja `PREREG_CHRONO_CONE_MS_BRIDGE_v0.2.md` (zamrożonej PRZED
> uruchomieniem czegokolwiek). Kod: `core/chrono_cone_bridge_v2.py`
> (konstrukcja + kontrole syntetyczne), `core/real_chrono_cone_bridge_v2.py`
> (test na trzech realnych domenach, te same pliki/okna co v0.1). Nic w
> obu plikach nie zostało zmienione po zobaczeniu któregokolwiek z
> wyników poniżej.

## 0. Finalny wzór θ_v2 i uzasadnienie wyboru

Między kolejnymi ekstremami sygnału (szczyt LUB dolina, nie tylko
szczyty jak w v0.1) faza rośnie o dokładnie `+2π` jeśli segment jest
WZNOSZĄCY (`xs[e_{k+1}] > xs[e_k]`) i maleje o `-2π` jeśli OPADAJĄCY —
stała "prędkość kątowa" w obrębie segmentu (liniowa rampa), znak
WYŁĄCZNIE z kierunku trendu, niezależnie od tempa/amplitudy zmiany
(**Opcja A**, PREREG §3). **Opcja B** (`|dθ/dt|∝|dx/dt|`, ciągła
akumulacja proporcjonalna do nachylenia) ODRZUCONA PRZED implementacją:
wymagałaby nowej, dowolnej stałej normalizującej (dodatkowy wolny
parametr, łamiący zasadę "jedna zmienna na raz" — jedyna zmienna
różniąca v0.1/v0.2 miała być KIERUNEK, nie skala), a matematycznie
zredukowałaby embedding `(r·cosθ, r·sinθ)` do reparametryzacji surowego
`x(t)` (bo `θ(t)≈c·x(t)+const`), tracąc ideę "jeden pełny obrót = jeden
pełny cykl", która jest sednem konstrukcji.

## 1. Kluczowe odkrycie mechanizmu, ZAPISANE PRZED uruchomieniem realnych danych (PREREG §1)

Audyt wzoru `chrono_cone_ratio`/`chrono_pendulum_ratio` PRZED
implementacją v0.2 ujawnił: `θ` wchodzi do wzoru WYŁĄCZNIE jako **brama
istnienia** (czy jest ≥2 ekstrema) — sama WARTOŚĆ `ratio` jest funkcją
WYŁĄCZNIE `r(t)`, niezależną od kierunku/wartości `θ`. Zarejestrowana
PRZED danymi przewidywana konsekwencja: dla okna, które przechodzi
bramkę w OBU wersjach, `chrono_pendulum_ratio` MUSI zwrócić dokładnie tę
samą liczbę co `chrono_cone_ratio` — zmiana kierunku θ może wpłynąć na
wynik testu WYŁĄCZNIE pośrednio, przez zmianę SKŁADU zbioru okien
przechodzących bramkę (v0.2 liczy też doliny, bramka bardziej
permisywna). **To odkrycie okazało się kluczowe dla interpretacji
wyniku poniżej — potwierdzone empirycznie niemal dokładnie.**

## 2. Kontrole syntetyczne — PRZESZŁY, wartości IDENTYCZNE z v0.1

| window_size | pozytywna (a vs b) | negatywna (b vs c) | sanity net_turn(c) | PASSED |
|---|---|---|---|---|
| 128 | p=3.02e-11, r=1.000, mediana(a)=4.235 mediana(b)=1.003 | p=0.348, r=-0.142 | mediana=0.0000 MAD=0.0000 | **TAK** |
| 256 | p=3.02e-11, r=1.000, mediana(a)=5.341 mediana(b)=1.015 | p=0.600, r=0.080 | mediana=-1.0000 MAD=0.0000 | **TAK** |

Wartości `p`/`r`/median dla kontroli pozytywnej i negatywnej są
DOKŁADNIE identyczne z v0.1 (§1 RESULT v0.1) — potwierdza to §1
wprost: dla generatorów syntetycznych (a)/(b)/(c), praktycznie wszystkie
okna mają ≥2 szczyty (v0.1) I ≥2 ekstrema łącznie (v0.2) jednocześnie,
więc bramka nie zmienia składu próby. **Dodatkowa kontrola sanity
(fizyczny test "wahadło vs koło zamachowe", PREREG §3/§6)**: na
kontroli (c) — stała amplituda, symetryczna oscylacja —
`chrono_pendulum_net_turn` ma medianę **0.0000 / -1.0000** (bliską
zeru, ograniczoną), MAD=0 (bardzo spójne między seedami). Dla
porównania, `θ_v1` na tym samym sygnale rosłaby bez ograniczeń z liczbą
szczytów (przy oknie=256, okres≈15 próbek, to ~16-17 szczytów →
`θ_v1_final/(2π)≈16`). **Fizyczna różnica "wahadło (ograniczone) vs
koło zamachowe (monotoniczne)" potwierdzona ilościowo na syntetyce,
zgodnie z przewidywaniem PRZED uruchomieniem.**

## 3. Realne dane — metryka PRIMARNA `chrono_pendulum_ratio`: PRAWIE IDENTYCZNA z v0.1, niestabilność znaku NIE zniknęła

Te same 3 domeny, te same pliki, te same rozmiary okien co v0.1.

**Ogólne liczby SUPPORTED**: łożyska 11/30, sejsmika 5/20, BTC 2/5 —
**IDENTYCZNE co do liczby** z v0.1. **Globalny rozkład znaku efektu na
wszystkich 55 komórkach**: `r>0`: 31, `r<0`: 24 — **DOKŁADNIE
IDENTYCZNY** z v0.1 (56%/44%, ten sam rozkład blisko losowego).

### 3.1 Stabilność znaku na przykładach-kotwicach z v0.1 (sigma=0.0)

| sygnał | okno A | r (v0.1) | r (v0.2) | okno B | r (v0.1) | r (v0.2) | stabilny? (v0.1→v0.2) |
|---|---|---|---|---|---|---|---|
| bearing ir_0021 | 256 | -0.338 | -0.338 | 512 | -0.093 | -0.093 | stabilny → **stabilny (bez zmian)** |
| bearing or6_0021 | 256 | -0.189 | -0.189 | 512 | +0.267 | +0.267 | **NIESTABILNY → NIESTABILNY (bez zmian)** |
| bearing b_0021 | 256 | +0.031 | +0.031 | 512 | +0.707 | +0.707 | stabilny → **stabilny (bez zmian)** |
| seismic CLC | 512 | +0.271 | +0.271 | 1024 | -0.164 | -0.164 | **NIESTABILNY → NIESTABILNY (bez zmian)** |
| seismic RIO | 512 | +0.393 | +0.413 | 1024 | -0.216 | -0.216 | **NIESTABILNY → NIESTABILNY (bez zmian)** |

Wartości `r` dla `chrono_pendulum_ratio` są DOKŁADNIE identyczne z v0.1
w 4/5 przypadków (bo bramka v0.1/v0.2 wybiera identyczny skład próby —
sygnały wibracyjne/sejsmiczne mają mnóstwo ekstremów, gate rzadko coś
zmienia), lekko różne w 1/5 (RIO okno 512: `+0.393→+0.413` — inny skład
próby, kilka dodatkowych okien przeszło bramkę v0.2, ale ZNAK i rząd
wielkości bez zmian). **Wniosek: na PRIMARNEJ, pre-rejestrowanej
metryce (ta sama formuła promienia co v0.1) niestabilność znaku
zaobserwowana w v0.1 (or6_0021 między oknami, obie stacje sejsmiczne
między oknami) NIE ZNIKNĘŁA w v0.2 — dokładnie zgodnie z przewidywaniem
mechanizmu zapisanym w PREREG §1 PRZED uruchomieniem realnych danych.**
To jest silne potwierdzenie, że przyczyna niestabilności leży w samym
zachowaniu `r(t)` na krawędziach okna (niezmienionym między v0.1/v0.2),
NIE w kierunku θ per se — w zakresie, w jakim testowała to metryka
promienia.

## 4. Metryka SEKUNDARNA, eksploracyjna `chrono_pendulum_net_turn`: realna poprawa stabilności na DOKŁADNIE tych przykładach, które flipowały

Ta metryka FAKTYCZNIE używa wartości θ (nie tylko bramki istnienia) —
`(θ[-1]-θ[0])/(2π)`, netto liczba obrotów w oknie. NIE była częścią
klasyfikacji SUPPORTED/NOT_SUPPORTED (PREREG §5, jawnie eksploracyjna),
ale rejestrowana właśnie po to, żeby dać hipotezie rotacji uczciwą
szansę zadziałać przez sam mechanizm geometryczny.

| sygnał | okno A | turn_r | okno B | turn_r | stabilny? |
|---|---|---|---|---|---|
| bearing ir_0021 | 256 | +0.051 | 512 | +0.060 | stabilny (oba pomijalne) |
| bearing or6_0021 | 256 | -0.173 | 512 | -0.480 | **stabilny — w v0.1/ratio ten sygnał FLIPOWAŁ** |
| bearing b_0021 | 256 | +0.182 | 512 | -0.020 | niestabilny (ale 512 ~zero, pomijalny) |
| seismic CLC | 512 | -0.353 | 1024 | -0.167 | **stabilny — w v0.1/ratio ten sygnał FLIPOWAŁ** |
| seismic RIO | 512 | +0.322 | 1024 | +0.400 | **stabilny — w v0.1/ratio ten sygnał FLIPOWAŁ** |

**4/5 przykładów stabilnych** (w porównaniu do 2/5 na metryce
primarnej, zarówno w v0.1 jak i v0.2) — i co ważniejsze, stabilność
pojawiła się DOKŁADNIE na trzech przykładach, które v0.1 jawnie
zaflagował jako niestabilne (or6_0021, CLC, RIO). Jedyny przypadek bez
poprawy (b_0021) ma przy oknie 512 efekt praktycznie zerowy
(`turn_r=-0.020`), więc "flip" jest tam kosmetyczny.

**Ograniczenia tego wyniku, zapisane uczciwie**: (1) to jest metryka
EKSPLORACYJNA — nie była pre-rejestrowana jako główny test klasyfikacji,
więc ten wynik NIE jest formalnym potwierdzeniem hipotezy w sensie
protokołu, tylko obiecującym sygnałem do dalszej, osobnej
pre-rejestracji; (2) globalna moc klasyfikacyjna `turn_r` jest NIŻSZA
niż `ratio` (SUPPORTED: 7/55 łącznie vs 18/55 dla ratio — łożyska 3/30,
sejsmika 4/20, BTC 0/5) — mniej okien osiąga formalną istotność, mimo
lepszej stabilności ZNAKU tam, gdzie jest mierzalny efekt; (3) test na
n=5 anchorach to mała próba, nie formalny test statystyczny stabilności
znaku (byłoby to kolejnym krokiem, gdyby ta metryka miała być
kontynuowana).

## 5. Odpowiedź na GŁÓWNE pytanie (PREREG §7-8)

**Czy zmiana kierunku θ naprawia niestabilność znaku z v0.1?**

- **Na PRIMARNEJ, pre-rejestrowanej metryce `chrono_pendulum_ratio`
  (identyczny wzór promienia co v0.1) — NIE.** Dokładnie zgodnie z
  przewidywaniem zapisanym w PREREG §1/§7 PRZED uruchomieniem: metryka
  ta jest matematycznie nieczuła na kierunek θ (poza bramką istnienia),
  więc niestabilność, która w v0.1 pochodziła z zachowania `r(t)` na
  krawędziach okna, pozostaje niezmieniona. Globalne liczby
  (SUPPORTED, rozkład znaku) są PRAKTYCZNIE IDENTYCZNE z v0.1.
- **Na SEKUNDARNEJ, eksploracyjnej metryce `chrono_pendulum_net_turn`
  (faktycznie używającej wartości θ) — CZĘŚCIOWO TAK**, w sensie
  opisowym: 4/5 przykładów-kotwic jest stabilnych, w tym WSZYSTKIE 3
  przypadki jawnie zaflagowane jako niestabilne w v0.1. To NIE jest
  formalnie potwierdzony wynik (metryka eksploracyjna, mała próba
  anchorów, niższa ogólna moc klasyfikacyjna), ale jest konkretnym,
  nietrywialnym sygnałem zgodnym z fizyczną intuicją użytkownika —
  wart osobnej pre-rejestracji jako kontynuacja, nie odkładany bez
  komentarza.

**Uczciwy wniosek całościowy**: hipoteza użytkownika w wersji
"zastąp tę samą metrykę promienia nowym θ" — **NIEPOTWIERDZONA**
(zgodnie z kryterium PREREG §8: odsetek stabilnych znaków na primarnej
metryce jest identyczny z v0.1, nie wyższy). Ale mechanizm, który
faktycznie testuje rotację (nie tylko bramkę), pokazuje wyraźnie
odmienny, bardziej obiecujący obraz — sugerując, że gdyby continuować
tę linię, WŁAŚCIWĄ metryką do budowania byłaby jedna z rodziny
opartych na `θ` bezpośrednio (jak `net_turn`), nie na promieniu `r(t)`
niezmienionym względem v0.1.

## 6. Status w ekosystemie

NIE dopisywane do `Axioms_G_TIMDR_Geometry.md` ani
`Axioms_S_TIMDR_Signal.md` — eksploracyjna konstrukcja (wzorem całej
rodziny mostów M/S↔G, punkt 19 skilla), z wynikiem NEGATYWNYM na
metryce primarnej i eksploracyjnie obiecującym, ale nieformalnym,
wynikiem na metryce sekundarnej, oba udokumentowane tutaj w pełni.

## 7. Co zostaje otwarte

- Formalna pre-rejestracja `chrono_pendulum_net_turn` (albo pokrewnej
  metryki opartej wprost na wartości θ, nie tylko jej istnieniu) jako
  GŁÓWNEJ metryki nowego mostu — z własną siatką kontroli syntetycznych
  i realnych, testowana z tą samą dyscypliną co v0.1/v0.2 — naturalny
  następny krok, jeśli użytkownik zdecyduje się kontynuować.
- Czy stabilność znaku `net_turn` na 4/5 anchorach przetrwa formalny
  test na całej siatce 55 komórek (nie tylko `sigma=0.0`) i na
  niezależnie wybranej czwartej domenie — NIE sprawdzone tutaj.
