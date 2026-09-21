# Wynik v0.3: chrono_centrifugal_ratio — ZATRZYMANO na etapie Kontroli #0 (RYZYKO): człon odśrodkowy generuje statystycznie istotny, nietrywialny fałszywy "lej" z samego szumu białego, na WSZYSTKICH pięciu rozmiarach okna (2026-09-21)

> Kontynuacja `PREREG_CHRONO_CONE_MS_BRIDGE_v0.3.md` (zamrożonej PRZED
> uruchomieniem realnych danych). Kod: `core/chrono_cone_bridge_v3.py`.
> Zgodnie z PREREG §5.0/§7: jeśli Kontrola #0 (ryzyko fałszywego
> sygnału z czystego szumu) nie przejdzie — ZATRZYMANIE, zgłoszenie na
> etapie kontroli, BEZ Kontroli #1 (strukturalnej) i BEZ realnych
> danych. Dokładnie to się stało. `core/real_chrono_cone_bridge_v3.py`
> **NIE ZOSTAŁ NAPISANY** — realne dane (łożyska/sejsmika/BTC) NIE
> zostały dotknięte w tej sesji.

## 0. Rekapitulacja konstrukcji i kalibracji

`θ_unwrapped(t)` = `core.chrono_cone_bridge_v2.trend_referenced_phase`
bez zmian (kierunek zależny od trendu, wznoszenie/opadanie, PREREG
v0.2). `r_anomalia(t)` = `core.chrono_cone_bridge.anomaly_radius` bez
zmian.

```
r_total(t) = r_anomalia(t) · (1 + k · θ_unwrapped(t)²)
```

`k(w) = A_MAX / M(w)`, `A_MAX=10.0`, `M(w)` = mediana (30 realizacji
kontroli POZYTYWNEJ, seed puli kalibracyjnej `1000`, rozłącznej od puli
testowej) z `max_t θ_unwrapped(t)²` w oknie rozmiaru `w`.

**Wynik kalibracji (wykonanej, zamrożonej, PRZED realnymi danymi)**:

| window_size | M(w) | k(w) |
|---|---|---|
| 48 | 39.4784 | 0.253303 |
| 128 | 39.4784 | 0.253303 |
| 256 | 39.4784 | 0.253303 |
| 512 | 39.4784 | 0.253303 |
| 1024 | 39.4784 | 0.253303 |

**Jedna, identyczna stała `k=0.253303` dla całej siatki** — bo mediana
szczytowego `|θ_unwrapped|` na kontroli pozytywnej wynosi dokładnie
`2π` niezależnie od długości okna (wahadło, nie koło zamachowe —
ilościowe potwierdzenie obserwacji z RESULT v0.2 §2, patrz PREREG v0.3
§3).

## 1. Kontrola #0 (RYZYKO) — NIE PRZESZŁA, na WSZYSTKICH pięciu rozmiarach okna

Test parowy (Wilcoxon signed-rank, PREREG §5.0): na TYCH SAMYCH 30
realizacjach czystego szumu białego (`make_white_noise`, na okno),
porównanie `chrono_pendulum_ratio` (v0.2, bez członu odśrodkowego) vs
`chrono_centrifugal_ratio` (v0.3, z członem), sparowane po realizacji.
`FALSE_SIGNAL` = `p<0.05` i `|r_eff|≥0.3` (te same progi co wszędzie w
tej rodzinie).

| window_size | n_valid | p | r_eff | mediana(pendulum) | mediana(centrifugal) | IQR(pendulum) | IQR(centrifugal) | spread_inflation | FALSE_SIGNAL |
|---|---|---|---|---|---|---|---|---|---|
| 48 | 30/30 | 3.05e-05 | 0.806 (duży) | 0.969 | 1.646 | 0.416 | 1.778 | 4.27× | **TAK** |
| 128 | 30/30 | 5.55e-04 | 0.690 (duży) | 1.003 | 1.190 | 0.312 | 0.383 | 1.23× | **TAK** |
| 256 | 30/30 | 1.70e-04 | 0.742 (duży) | 1.015 | 1.128 | 0.248 | 0.280 | 1.13× | **TAK** |
| 512 | 30/30 | 9.52e-04 | 0.665 (duży) | 0.987 | 1.056 | 0.089 | 0.262 | 2.95× | **TAK** |
| 1024 | 30/30 | 2.37e-03 | 0.617 (duży) | 0.999 | 1.046 | 0.110 | 0.137 | 1.24× | **TAK** |

**5/5 rozmiarów okna dają `FALSE_SIGNAL=True`**, wszystkie z dużym
rozmiarem efektu (`|r_eff|` 0.62–0.81). Kierunek jest spójny i
systematyczny: `chrono_centrifugal_ratio` na czystym szumie jest
**zawsze przesunięte W GÓRĘ** względem `chrono_pendulum_ratio` na
DOKŁADNIE tych samych realizacjach (mediana centrifugal > mediana
pendulum przy wszystkich pięciu `w`), i przy oknach 48/512 dodatkowo
znacząco poszerza rozrzut (`spread_inflation` 4.27×/2.95×).

## 2. Diagnoza mechanizmu (dlaczego, nie tylko że)

`θ_unwrapped(t)²≥0` zawsze, więc `(1+k·θ_unwrapped(t)²)≥1` zawsze —
człon odśrodkowy jest **wyłącznie wzmacniający, nigdy tłumiący**. Na
czystym szumie białym `θ_unwrapped(t)` jest w praktyce błądzeniem
losowym o krokach `±2π` (znak zależny od losowego kierunku każdego
ekstremum) — jego kwadrat w KAŻDYM punkcie okna jest nieujemny i typowo
rośnie w obu kierunkach od zera niezależnie od tego, czy akurat
wypadnie w pierwszych czy ostatnich 20% próbek okna. Ponieważ
`chrono_centrifugal_ratio` to `mean(r_total[koniec])/mean(r_total[start])`,
a mianownik i licznik są NIEZALEŻNIE wzmacniane przez nieujemny,
losowo zmienny czynnik — asymetria między "ile razy koniec okna
przypadkiem miał większe `|θ|` niż start" systematycznie pcha rozkład
`ratio` W GÓRĘ (mediana >1) zamiast pozostawiać go wyśrodkowanym na 1,
jak w czystej metryce promienia (`chrono_pendulum_ratio` na tym samym
szumie: mediana ~0.97–1.02, zgodnie z v0.1/v0.2). To dokładnie
ryzyko zaflagowane w zadaniu PRZED implementacją: **sam człon
odśrodkowy generuje fałszywy "lej" z samego szumu, niezależnie od
jakiegokolwiek prawdziwego wzorca** — potwierdzone tutaj ilościowo, nie
tylko jako obawa teoretyczna.

Ważne: to NIE jest artefakt złej kalibracji `k` w sensie "za duże k" —
`k` było kalibrowane restrykcyjnie (czynnik odśrodkowy ogranicza się do
`≤10×` na SZCZYCIE `|θ|` kontroli pozytywnej, PREREG §3) i mimo to
efekt na szumie jest duży (`|r_eff|` do 0.81). Przyczyna leży w samej
STRUKTURZE wzoru (nieujemny, wyłącznie wzmacniający czynnik
multiplikatywny, korelowany z lokalnie losowym błądzeniem `θ`), nie w
wielkości stałej skalującej.

## 3. Kontrola #1 (strukturalna) i realne dane — NIE URUCHOMIONE

Zgodnie z PREREG §5.0/§7: skoro Kontrola #0 nie przeszła na
ŻADNYM z pięciu rozmiarów okna, sesja zatrzymuje się tutaj.
`run_chrono_centrifugal_controls` (Kontrola #1, a/b/c) i
`core/real_chrono_cone_bridge_v3.py` (łożyska/sejsmika/BTC) **NIE
zostały uruchomione ani napisane** — realne dane pozostają nietknięte
tą konstrukcją.

## 4. Porównanie z v0.1/v0.2 na kotwicach (jak było przewidziane w PREREG §6 — teraz NIEOSIĄGALNE)

PREREG v0.3 §6 zapowiadał bezpośrednie porównanie stabilności znaku na
kotwicach `or6_0021` (256/512), CLC i RIO (512/1024) między v0.1
(niestabilne), v0.2-sekundarną `chrono_pendulum_net_turn` (stabilne na
4/5) i v0.3. **To porównanie jest tu NIEOSIĄGALNE** — v0.3 nie dotarło
do etapu realnych danych. Dla przypomnienia, stan sprzed tej sesji
pozostaje bez zmian:

| konstrukcja | or6_0021 (256→512) | CLC (512→1024) | RIO (512→1024) |
|---|---|---|---|
| v0.1 `chrono_cone_ratio` | NIESTABILNY | NIESTABILNY | NIESTABILNY |
| v0.2 primarna `chrono_pendulum_ratio` | NIESTABILNY (bez zmian) | NIESTABILNY (bez zmian) | NIESTABILNY (bez zmian) |
| v0.2 sekundarna `chrono_pendulum_net_turn` | **stabilny** | **stabilny** | **stabilny** |
| v0.3 `chrono_centrifugal_ratio` | — (niedostępne, zatrzymano na kontroli) | — | — |

## 5. Wniosek

**Hipoteza użytkownika o sile odśrodkowej, w TEJ konkretnej
operacjonalizacji (`r_total = r_anomalia·(1+k·θ_unwrapped²)`), NIE
przeszła nawet etapu kontroli syntetycznej.** Zgodnie z uczciwym
protokołem (PREREG §5.0, skill punkt 3/15): to jest w pełni
prawomocny, negatywny wynik na etapie mechaniki, zaraportowany bez
naginania interpretacji — nie "słaby wynik na realnych danych", tylko
**mechanizm zdyskwalifikowany PRZED dotarciem do realnych danych**,
dokładnie tak, jak przewidywał scenariusz ryzyka zapisany w zadaniu
PRZED implementacją.

**To NIE unieważnia** obiecującego wyniku v0.2-sekundarnej
(`chrono_pendulum_net_turn`, 4/5 stabilnych kotwic) — to jest ODRĘBNA
konstrukcja (θ używane wprost jako netto-obrót, bez kwadratu, bez
członu multiplikatywnie wzmacniającego promień) i pozostaje
niezmieniona, udokumentowana w `RESULT_CHRONO_CONE_MS_BRIDGE_v0.2.md`.

## 6. Status w ekosystemie

NIE dopisywane do `Axioms_G_TIMDR_Geometry.md` ani
`Axioms_S_TIMDR_Signal.md` — konstrukcja eksploracyjna z wynikiem
negatywnym na etapie kontroli syntetycznej (wzorem całej rodziny
mostów M/S↔G).

## 7. Co zostaje otwarte (nieodłożone bez presji wykonania)

- Czy INNA operacjonalizacja "akumulacji obrotu jako wzmocnienia"
  (np. znormalizowana `θ_unwrapped(t)²` przez oczekiwaną wariancję
  błądzenia losowego danej długości — coś w rodzaju "odjęcia tła
  szumu", analogicznie do kalibracji `Q_crit`/`ω_ref` z tła, punkty
  16/22 skilla) usunęłaby systematyczne obciążenie wykazane w §1-2 —
  NIE zbadane tutaj, naturalny następny krok, JEŚLI użytkownik
  zdecyduje się kontynuować tę linię.
- Czy problem zniknąłby, gdyby czynnik odśrodkowy używał ZNAKU netto
  (`sign(θ_unwrapped)·θ_unwrapped²` lub podobne), zamiast czystego
  kwadratu — zmieniłoby to jednak fundamentalnie charakter "wyłącznie
  wzmacniający" z propozycji użytkownika (mogłoby też TŁUMIĆ promień),
  więc wymagałoby osobnego uzgodnienia z użytkownikiem, czy to nadal
  ta sama hipoteza — NIE rozstrzygane tutaj samodzielnie.
- Formalny test Kontroli #0 (parowy Wilcoxon na tych samych realnych
  segmentach, nie tylko syntetycznym szumie) jako dodatkowa, niezależna
  weryfikacja diagnozy z §2 — odłożone, bo Kontrola #0 na syntetyce już
  dała jednoznaczny, spójny na całej siatce wynik uzasadniający
  zatrzymanie.
