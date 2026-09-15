# Wynik: most P/Q → torsja trójwęzła → pipeline (M/S), test syntetyczny

> Streszczenie `PREREG_TREFOIL_MS_BRIDGE.md` (pełna metodologia,
> uzasadnienia wyborów i jawny pesymistyczny prior a priori tam). Ten
> plik to sam wynik uruchomienia siatki zamrożonej w sekcjach 3-7 tamtego
> dokumentu, bez żadnej modyfikacji parametrów po zobaczeniu wyniku.
> Kod: `core/trefoil_ms_bridge.py`. Data: 2026-09-15.

## Wynik surowy (10 komórek siatki: 2 rozmiary okna × 5 poziomów szumu)

```
 okno  sigma  passed      pos_p    pos_r  pos_r_lbl      neg_p    neg_r  degen
  300   0.00   False  1.212e-12    1.000       duży  1.212e-12   -1.000    TAK
  300   0.10   False   0.002891   -0.449     średni   3.02e-11    1.000
  300   0.30   False    0.02151   -0.347     średni  3.094e-06    0.702
  300   0.50   False   0.001174   -0.489     średni    0.02151    0.347
  300   1.00   False     0.7062   -0.058  pomijalny     0.1087    0.242
   64   0.00   False  1.212e-12    1.000       duży  1.212e-12   -1.000    TAK
   64   0.10   False      0.126   -0.231       mały   3.02e-11    1.000
   64   0.30   False     0.4553   -0.113       mały   0.001174    0.489
   64   0.50   False      0.429   -0.120       mały     0.1087    0.242
   64   1.00   False     0.8534   -0.029  pomijalny     0.7618    0.047

PRZESZŁO: 0/10 komórek siatki.
```

`passed` = `pipeline.run_controls()` (kontrola pozytywna istotna I obie
kontrole negatywne wzajemnie nieistotne) — kryterium zamrożone w
pre-rejestracji, sekcja 7, bez modyfikacji.

## Wniosek

**0/10. Konstrukcja nie przeszła kontroli syntetycznej w żadnej komórce
siatki — real-data (sejsmika/łożyska/BTC) jest świadomie pomijane,
zgodnie z sekcją 8 pre-rejestracji, która to dopuszczała.**

Dwa wiersze `sigma=0.00` są zdegenerowane (oznaczone `degen=TAK` — tak
jak przewidziano w kodzie PRZED uruchomieniem, nie post-hoc): kontrola
negatywna A (czysty szum) przy `sigma=0` to dosłownie stały, zerowy
sygnał, więc `metric_fn` zwraca `0.0` dla wszystkich 30 okien —
porównanie z czymkolwiek daje sztucznie idealną separację. Te dwa
wiersze są wyłączone z interpretacji.

**Dla pozostałych 8 komórek (sigma>0, realny szum) wynik jest gorszy niż
zwykłe "brak sygnału" — jest odwrócony i dodatkowo niestabilny:**

- Tam gdzie kontrola pozytywna wyszła istotna statystycznie (okno=300,
  sigma∈{0.1,0.3,0.5}, p<0.05), rozmiar efektu `r` jest **UJEMNY**
  (-0.35 do -0.49, średni) — oznacza to, że genuine sygnał
  dwuczęstotliwościowy (kontrola pozytywna) ma SYSTEMATYCZNIE NIŻSZĄ
  wartość `max(|τ|)` niż czysty szum tła, nie wyższą. Kierunek jest
  odwrotny do zakładanego w konstrukcji metryki.
- Niezależnie od tego, kontrola negatywna (`neg_a` czysty szum vs
  `neg_b` pojedyncza częstotliwość+szum, które POWINNY dawać podobny,
  bliski zeru wynik torsji) wychodzi silnie istotna w większości
  komórek (p od 3×10⁻¹¹ do 0,02, r do 1,000 — pełna separacja) — sam
  szum tła (`neg_a`) systematycznie różni się od planarnego sygnału z
  szumem (`neg_b`), co oznacza, że metryka nie jest nawet wewnętrznie
  stabilna między dwoma wariantami "braku genuine torsji".
- Przy najwyższym przetestowanym szumie (`sigma=1.0`) oba efekty
  zanikają do poziomu pomijalnego (r=-0.058/-0.029) — czyli przy
  bardzo dużym szumie różnica w ogóle znika, zamiast się ustabilizować.

## Diagnoza (spójna z zastrzeżeniem a priori z sekcji 1 pre-rejestracji)

Mechanizm jest wytłumaczalny i spójny z dwoma wcześniejszymi
niezależnymi awariami tego samego typu (`trefoil_weather_embedding_
validation.py`, estymator DMD sprzężenia helikalnego): `kappa_tau_time_
aware` liczy `τ` z POTRÓJNEJ różnicy skończonej (`v→a→j`). Dla czystego
szumu białego kolejne próbki są z definicji nieskorelowane — lokalny
"szarpnięcie" (`j`) między sąsiednimi punktami jest DUŻE względem
gładkiego, wolnozmiennego sygnału dwuczęstotliwościowego. Innymi słowy:
**potrójne różnicowanie samo w sobie generuje większe `|τ|` z szumu niż
z genuine geometrycznej struktury** — dokładnie odwrotnie niż zakładała
konstrukcja metryki. To nie jest kwestia złego strojenia progu czy
`lag` — to strukturalna własność liczenia torsji przez różnice
skończone na krótkich, zaszumionych szeregach, trzeci raz z rzędu w
tym ekosystemie.

## Co to oznacza dla dalszej pracy

- **Ta konkretna konstrukcja (embedding opóźniający `lag=1` + surowa
  torsja przez różnice skończone + redukcja `max(|τ|)`) jest odrzucona
  jako most M/S↔topologia.** Zgodnie z ustaloną dyscypliną, progi/`lag`/
  wybór redukcji NIE są retuningowane po zobaczeniu tego wyniku.
- To NIE unieważnia torsji Freneta-Serreta jako obiektu w ogóle — na
  gładkiej, gęsto próbkowanej, syntetycznej krzywej (oryginalny
  `trefoil_frenet_torsion.py`, N=300, C² gładkość) nadal działa
  poprawnie (4/4 testy). Problem jest specyficzny dla zastosowania tej
  matematyki do krótkich/zaszumionych szeregów przez embedding
  opóźniający — trzeci potwierdzony przypadek tego samego mechanizmu.
- **Most P/Q (G10) pozostaje tym, czym był**: najtwardszym, dowiedzionym
  kawałkiem geometrii w ekosystemie — ta próba rozszerzenia go w stronę
  topologii/M-S nie powiodła się, ale nie osłabia to samego G10.
- Możliwe future work, świadomie NIE podjęte teraz (analogicznie do
  „opcji 1B" mostu Fouriera): metryka odporna na szum inna niż surowe
  różnice skończone (np. dopasowanie gładkiej krzywej/wygładzenie przed
  różnicowaniem, jak w estymatorze kształtu helikalnego, który
  faktycznie poprawił wynik przez dopasowanie całego okna zamiast
  różnicowania próbka-po-próbce) — ale to byłaby KOLEJNA nowa
  konstrukcja, wymagająca własnej pre-rejestracji, nie retuning tej.
