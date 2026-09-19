# Wynik na realnych danych: `MC_{M/S↔K}` #2 (tłumienie trybu zerowego `Z0` vs pierwsza istotna częstotliwość `ω1`)

Pre-rejestracja: [`PREREG_MS_K_BRIDGE_2.md`](./PREREG_MS_K_BRIDGE_2.md)
(zamrożona 2026-09-18, PRZED napisaniem `core/real_ms_k_zero_mode_bridge.py`).
Kod: `core/real_ms_k_zero_mode_bridge.py`. Uruchomione 2026-09-19, zero
zmian parametrów po zobaczeniu wyniku.

## Wynik surowy

`MC_continuous` (główny test): **43/60**. `MC_binary` (dodatkowy,
diagnostyczny): **38/60**.

**Sprostowanie liczby komórek względem PREREG §2**: PREREG zapisał
"3 domeny × 2 okna × 5 sigm = 30 komórek dla TEGO mostu" — to niedoszacowanie,
bo traktowało "domeny" jako płaski mnożnik ×3, ignorując że łożyska mają
TRZY niezależne przypadki uszkodzenia (`ir_0021`/`or6_0021`/`b_0021`) a
sejsmika DWIE stacje (CLC/RIO), dokładnie jak w bliźniaczych mostach
`MC_{K↔G}`/`MC_{M/S↔G}` #1 (tam poprawnie liczone: 60 komórek per
metryka = 30 łożyska + 20 sejsmika + 10 BTC). Faktyczna liczba komórek
per metrykę w tym uruchomieniu to **60, nie 30** — sam wynik/kod jest
poprawny (zgodny z konwencją sióstr), tylko opis w PREREG §2 był
niedokładny arytmetycznie. Odnotowane tu jawnie, nie ukryte.

| Domena | `MC_continuous` | `MC_binary` |
|---|---|---|
| Łożyska CWRU (ir_0021/or6_0021/b_0021) | 30/30 | 30/30 |
| Sejsmika Ridgecrest (CLC/RIO) | 10/20 | 5/20 |
| BTC/USD | 3/10 | 3/10 |

## Zgodność z przewidywaniem sprzed testu

PREREG §7.4 przewidywał: "łożyska najsilniejszy efekt, sejsmika
częściowy, BTC brak/najsłabszy". **Wynik dokładnie to potwierdza** —
identyczny porządek jak we wszystkich czterech wcześniejszych mostach
tej rodziny (`MC_K↔G`, `MC_M/S↔G` #1, oryginalny most
winding/crossing/phase_winding).

## Szczegóły, jawnie

**Łożyska — pełna separacja.** Wszystkie 30/30 komórek `MC_continuous`
i 30/30 `MC_binary` przeszły, efekt `r` w większości "duży"
(0.5–1.0), kierunek spójny między trzema typami defektu (`ir_0021`,
`or6_0021`, `b_0021`) i obydwoma oknami (32, 64).

**Sejsmika — kierunek NIESPÓJNY między stacjami**, dokładnie ten sam
wzorzec co w `MC_M/S↔G` #1 i w moście winding/crossing/phase_winding
(punkt 19 skilla): stacja **CLC** przechodzi 10/10 na obu oknach
(`r` średni–duży, 0.38–0.58, kierunek dodatni — `MC_continuous` wyższe
w kodzie niż w tle), stacja **RIO** przechodzi **0/10** na obu oknach
(`r` mały i UJEMNY, -0.13 do -0.31, `passed=False` na każdej komórce —
efekt nieistotny statystycznie i skierowany przeciwnie). To ten sam
mainshock obserwowany z dwóch stacji, dający jakościowo różną
odpowiedź — nie da się tego uśrednić do jednej liczby "sejsmika
działa/nie działa".

**BTC — najsłabszy, częściowo w kierunku PRZECIWNYM.** 3/10 komórek
`MC_continuous` przeszło (okno 12: σ=0.0, σ=0.3; okno 24: σ=0.3), we
wszystkich trzech `r` jest UJEMNY (-0.32 do -0.35, "średni") — czyli
tam gdzie efekt jest istotny, `MC_continuous` jest NIŻSZE w reżimie
wysokiej zmienności niż niskiej, przeciwny kierunek niż na łożyskach.
Pozostałe 7/10 komórek nieistotne.

## Zastrzeżenie z PREREG §7.2, potwierdzone tym wynikiem — NIE dowód specyficznej koincydencji Z0-ω1

PREREG jawnie ostrzegał PRZED zobaczeniem wyniku: obie składowe (`Z0` w
`MC_M/S↔G` #1, metryki oparte na `ω1`/kratownicy w `MC_K↔G`) już
OSOBNO pokazały ten sam wzorzec domenowy (łożyska silny, sejsmika
częściowy, BTC brak/słaby) z niezwiązanych powodów. **Ten wynik
dokładnie powtarza ten wzorzec** — co jest zgodne z przewidywaniem, ale
**NIE stanowi niezależnego dowodu koincydencji `Z0`↔`ω1` specyficznie**.
Równie prawdopodobnym wyjaśnieniem jest, że obie składowe osobno
korelują z tymi samymi etykietami klas (amplituda/SNR/kontrast
sygnał-tło różny między domenami), a ich kombinacja dziedziczy tę
korelację bez dodawania nowej informacji o współwystępowaniu. Odróżnienie
tych dwóch hipotez wymagałoby dodatkowej kontroli (np. sprawdzenia,
czy `MC_continuous` przewyższa lepszy z dwóch pojedynczych składników
osobno — NIE zrobione w tym zadaniu, otwarty punkt).

## Klasyfikacja: diagnostyka, nie selektor

Ten sam wzorzec co wszystkie poprzednie mosty tej rodziny (lekcja
G-Rezonansu, punkt 11 skilla): klasy pozytywna/negatywna w każdej
domenie ustalone NIEZALEŻNIE od `Z0`/`ω1`/`MC` (etykiety CWRU, znacznik
czasu mainshocku, podział std bloku BTC) — metryka nigdy nie użyta do
samodzielnego wykrycia/wyboru tych klas z nieoznakowanych danych.

## Status: częściowo ustalony (NIE "USTALONY (diagnostyka)")

Ważne rozróżnienie względem `MC_{M/S↔G}` #1: ten most **NIE spełnia**
jeszcze wszystkich sześciu kryteriów tieru "USTALONY (diagnostyka)"
(`TIMDR_Branch_Specification.md`, "Słownik statusów mostów
kandydujących") — konkretnie brakuje **kryterium (2): kontrola
pozytywna i negatywna na danych SYNTETYCZNYCH**. `dominant_omega1` i
`zero_mode_fraction` mają własne testy syntetyczne (odziedziczone z
mostów macierzystych), ale sama KOMBINACJA `z0_norm`/`mc_continuous`/
`mc_binary` (nowy kod w `core/real_ms_k_zero_mode_bridge.py`) nie
przeszła przez osobny plik testów syntetycznych analogiczny do
`tests/test_mobius_kg_bridge.py` czy
`tests/test_zero_mode_topology_bridge.py` — PREREG tego nie
przewidywał (przeszedł od razu do danych realnych, reużywając
składniki uznane za już zweryfikowane osobno). To jest świadomie
nazwana, nienaprawiona luka, nie przeoczenie: podnoszenie statusu bez
spełnienia własnego, wcześniej ustalonego kryterium złamałoby
dyscyplinę tego samego "Słownika statusów", który to kryterium
wprowadził.

Pozostaje: **częściowo ustalony** — realny, powtarzalny, zgodny z
przewidywaniem efekt na 2 z 3 domen (silny łożyska, częściowy/
niespójny sejsmika), słaby/przeciwny kierunkowo na trzeciej (BTC), plus
jawnie nazwana konfundacja (§7.2) i brakujące testy syntetyczne.

## Otwarte

1. Napisać `tests/test_ms_k_zero_mode_bridge.py` (kontrola
   syntetyczna pozytywna/negatywna dla `z0_norm`/`mc_continuous`/
   `mc_binary`) — dopiero to domyka kryterium (2) tieru "USTALONY
   (diagnostyka)".
2. Test odróżniający "kombinacja dodaje informację" od "kombinacja
   dziedziczy korelację składników" (§7.2 wyżej) — nie zrobiony.
3. Diagnoza kierunku RIO (ujemny, nieistotny) vs CLC (dodatni, istotny)
   — ten sam otwarty punkt co w `MC_M/S↔G` #1, nie rozwiązany tu ani
   tam.

Powiązane: [`PREREG_MS_K_BRIDGE_2.md`](./PREREG_MS_K_BRIDGE_2.md),
[`RESULT_MOBIUS_COHERENCE_BRIDGES_REAL_DATA.md`](./RESULT_MOBIUS_COHERENCE_BRIDGES_REAL_DATA.md)
(bliźniacze wyniki dla pozostałych dwóch mostów tej rodziny),
[`../theory/Axioms_K_TIMDR.md`](../theory/Axioms_K_TIMDR.md),
[`../theory/Axioms_S_TIMDR_Signal.md`](../theory/Axioms_S_TIMDR_Signal.md),
[`../theory/TIMDR_Branch_Specification.md`](../theory/TIMDR_Branch_Specification.md).
