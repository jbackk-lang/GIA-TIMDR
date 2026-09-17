# Wynik: dwa kandydujące mosty `MC_{K↔G}` i `MC_{M/S↔G}` #1 na REALNYCH danych (3 domeny)

> Streszczenie `PREREG_MOBIUS_COHERENCE_BRIDGES.md` (zamrożonej PRZED
> tym uruchomieniem — patrz commit `bacea57`, poprzedzający commit z
> kodem/wynikiem). Kod: `core/real_mobius_kg_bridge.py`,
> `core/real_zero_mode_topology_bridge.py`. Data: 2026-09-17.
> Oba mosty **pozostają kandydatami, NIE ustalonymi mostami** — ten
> dokument raportuje wynik, klasyfikacja selektor/diagnostyka jest
> odroczona do zadania #65.

## `MC_{K↔G}` — wynik surowy: **36/60 komórek przeszło**, ale patrz diagnoza niżej — wynik NIE jest wiarygodnym dowodem struktury Möbiusa

Siatka: (3 przypadki łożysk + 2 stacje sejsmiczne + 1 BTC) × 2 okna ×
5 sigm = 60 komórek. Podział po domenie: **łożyska 24/30, sejsmika
12/20, BTC 0/10**.

**Diagnoza — sprawdzona bezpośrednio, nie zgadnięta.** Zanim ten wynik
zostanie odczytany jako "realne dane modalne czasem zachowują się
Möbiusowo", sprawdzono GEOMETRIĘ samej kratownicy `(k,n)` niezależnie
od jakichkolwiek danych:

```
K_RANGE=(-6..6), N_RANGE=(1..7): 46 par dopuszczalnych, 45 zabronionych
x jednostajnie losowe w [0,12] -> 54,7% trafia w najbliższy punkt dopuszczalny
x jednostajnie losowe w [0,3]  -> 78,5% trafia w najbliższy punkt dopuszczalny
```

Punkt podstawowy (`k=0,n=1`, `ω=π/2≈1,571`, stan podstawowy widma) jest
dopuszczalny i geometrycznie "przyciąga" szeroki zakres `x` blisko
niego — więc dla `x=ω1/ω_ref` skupionego blisko 1 (co jest OCZEKIWANE
z definicji `ω_ref` = mediana `ω1` z tła, patrz PREREG §5), baza
losowa BEZ ŻADNEGO związku z sygnałem daje już ~79% trafień w
dopuszczalny punkt — nie 50%, jak naiwnie można by oczekiwać z 46/91
par dopuszczalnych. To wyjaśnia, dlaczego prawie wszystkie komórki
siatki (łącznie z tymi, które "przeszły") mają `frac_test≈frac_bg≈1,000`
(mediana obu grup przy suficie) — statystyczna istotność Manna-Whitneya
w tych komórkach pochodzi z drobnych różnic w RZADKICH oknach lądujących
poza punktem podstawowym, nie z wyraźnej różnicy "defekt/normalne w
większości okien".

**Uczciwy wniosek**: `MC_{K↔G}` w obecnej postaci (kratownica
`K_RANGE=(-6..6)×N_RANGE=(1..7)`, `ω_ref`=mediana tła) ma wysoki,
w dużej mierze GEOMETRYCZNY (nie sygnałowy) próg bazowy trafień. Wynik
36/60 NIE jest interpretowany jako dowód, że realne dane "zachowują się
Möbiusowo" — jest interpretowany jako **niediagnostyczny na tej
konfiguracji kratownicy**, wymagający albo innej kalibracji `ω_ref`/
zakresu `(k,n)` (co złamałoby dyscyplinę anty-numerologii, gdyby zrobione
teraz, po zobaczeniu wyniku), albo porzucenia tego mostu w obecnej
formie. Zero prób do dostrojenia w tej sesji — to jest zaraportowane
jako ograniczenie konstrukcji operatora, nie naprawione.

## `MC_{M/S↔G}` #1 — wynik surowy: **140/240 komórek przeszło**, wzorzec zgodny z oczekiwaniem sprzed testu

Siatka: (3 defekty łożysk + 2 stacje sejsmiczne + 1 BTC) × 4 metryki
(`Z0`, `Gi`, `MC_continuous`, `MC_binary`) × 2 okna × 5 sigm = 240
komórek. Podział po domenie i metryce:

| domena | `Z0` | `Gi` | `MC_continuous` | `MC_binary` |
|---|---|---|---|---|
| łożyska | 21/30 | **30/30** | **30/30** | 23/30 |
| sejsmika | 12/20 | 10/20 | 9/20 | 5/20 |
| BTC | 0/10 | 0/10 | 0/10 | 0/10 |

**To dokładnie potwierdza oczekiwanie użytkownika zapisane w PREREG §0
PRZED uruchomieniem** ("łożyska bo tam `G_i` jest silny, sejsmika bo
tam `G_i` jest częściowy, BTC bo tam `G_i` jest słaby") — `Gi` na
łożyskach osiąga PEŁNĄ separację (30/30, efekt zawsze "duży",
`r`≈0,7–1,0), na sejsmice separuje częściowo (10/20, mieszany kierunek
między stacjami CLC/RIO), na BTC nie separuje wcale (0/40 we
WSZYSTKICH czterech metrykach, `r` konsekwentnie pomijalny/mały).

**Zgodność z punktem 19 skilla**: `Gi` na łożyskach (30/30, 100%) jest
NAWET SILNIEJSZY niż oryginalny wynik winding/crossing/phase_winding z
punktu 19 (123/150, 82%) — spójne, bo `Gi` jest znormalizowaną
kombinacją tych samych trzech metryk, a kalibracja `GiRanges` z tła
mogła dodatkowo wyostrzyć separację względem surowych metryk.

**Znane, odziedziczone zastrzeżenie zniekształcenia `MC_continuous`**:
formuła `w1·(1-Z0)+w3·(Gi/gref)` zakłada `Z0∈[0,1]`, ale `Z0` NIE jest
ograniczone (może być rzędu dziesiątek dla sygnałów zdominowanych
składową stałą — zweryfikowane w `test_z0_large_for_strong_dc`).
Na realnych danych `Z0` sejsmiki osiąga wartości 20–39 (kolumna
`med_bg` dla stacji CLC), więc `(1-Z0)` bywa silnie ujemne — `MC_continuous`
na sejsmice jest w praktyce zdominowany członem `Z0`, nie zbalansowaną
kombinacją. Mimo to `MC_continuous` na łożyskach osiąga 30/30 (bo tam
`Z0` jest w rozsądnym zakresie) — efekt zniekształcenia jest więc
DOMENOWO ZALEŻNY, nie naprawiony tutaj (naprawa po zobaczeniu wyniku
złamałaby dyscyplinę anty-numerologii), tylko jawnie odnotowany jako
ograniczenie konstrukcji formuły, dziedziczone z pierwotnej propozycji
użytkownika.

**`Z0` sam w sobie** separuje częściowo wszędzie poza BTC (21/30
łożyska, 12/20 sejsmika, 0/10 BTC) — kierunek `r` NIESPÓJNY między
domenami (dodatni na sejsmice, ujemny na łożyskach), co oznacza, że
"tłumienie trybu zerowego" nie ma jednego uniwersalnego kierunku efektu
między domenami — kolejne zastrzeżenie przeciw traktowaniu `Z0` jako
uniwersalnego, kierunkowego wskaźnika bez kontekstu domeny.

## Zero prób dostrajania po zobaczeniu wyniku

Żaden próg (`ω_ref`, `θ0`, `θG`, `K_RANGE`, `N_RANGE`, `w1`, `w3`,
`gref`) nie został zmieniony po uruchomieniu powyższej siatki. Diagnoza
geometrii `MC_{K↔G}` (sekcja wyżej) została policzona PO zobaczeniu
wyniku siatki, ale NIE zmienia żadnego zamrożonego parametru — jest
niezależnym sprawdzeniem, DLACZEGO wynik wygląda tak, jak wygląda, nie
próbą poprawy go.

## Otwarte, do zadania #65

1. Klasyfikacja selektor vs diagnostyka (lekcja G-Rezonansu, punkt 11
   skilla) dla `MC_{M/S↔G}` #1 (obiecujący kandydat na łożyskach/
   częściowo sejsmice) i osobno dla `MC_{K↔G}` (odrzucony w obecnej
   formie na podstawie diagnozy geometrycznej powyżej).
2. Czy `Gi` samodzielnie (bez `Z0`) byłby czystszym, jednogałęziowym
   dodatkiem do istniejącego zestawu winding/crossing/phase_winding
   zamiast pełnego 2-gałęziowego `MC_{M/S↔G}` — pytanie otwarte, nie
   rozstrzygnięte tutaj.
3. Zapis wyników (w tym odrzucenia `MC_{K↔G}` w obecnej formie) do
   `Axioms_K_TIMDR.md`/`Axioms_G_TIMDR_Geometry.md`/
   `Axioms_S_TIMDR_Signal.md` i aktualizacja skilla.
