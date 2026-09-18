# Pre-rejestracja: kandydujący (NIE ustalony) most 2-gałęziowy `MC_{M/S↔K}` #2 — tłumienie trybu zerowego (`Z0`) vs pierwsza istotna częstotliwość (`ω1`) na REALNYCH danych (3 domeny)

> **Kolejność, jawnie.** Standardowa kolejność ekosystemu: freeze → run.
> Ten plik zamraża wszystkie parametry PRZED napisaniem
> `core/real_ms_k_zero_mode_bridge.py` i PRZED jakimkolwiek
> uruchomieniem go na realnych danych. Implementacja/uruchomienie nie
> zaczyna się, dopóki ten dokument nie jest zacommitowany osobno,
> PRZED commitem z kodem/wynikiem (ten sam wzorzec co
> `PREREG_MOBIUS_COHERENCE_BRIDGES.md`).

## 0. Kontekst i pochodzenie

**Dlaczego ten most teraz.** Po podniesieniu `MC_{M/S↔G}` #1 do statusu
USTALONY (diagnostyka) (2026-09-18, `TIMDR_Branch_Specification.md`,
"Słownik statusów mostów kandydujących"), ekosystem ma dokładnie JEDEN
stabilny most 2-gałęziowy w rodzinie Möbiusowej i jeden odrzucony
(`MC_{K↔G}`, NIE ustalony). Zasada nieredukowalności gałęzi (punkt 21
skilla, `TIMDR_Gravity_Speculative.md`) dopuszcza rozważenie operatora
3-gałęziowego dopiero, gdy istnieją co najmniej DWA niezależne, stabilne
mosty 2-gałęziowe — obecnie jest jeden. Ten dokument otwiera ścieżkę do
drugiego, wybranego na wyraźną prośbę użytkownika (2026-09-18) z
uzasadnieniem: nie używa gałęzi G ani META, ma już częściowo
zaimplementowaną matematykę (`ω1` z mostu Fouriera, `Z0` z
`zero_mode_topology_bridge.py`), i jest to jedna z dwóch połówek
pierwotnej propozycji `MöbiusCoherence(S)`.

**Ten most JUŻ ISTNIEJE jako nazwany, ale niezaimplementowany kandydat**
— dopisek "Kandydujący (NIE ustalony) most M/S↔K #2: tłumienie trybu
zerowego + pierwsza istotna częstotliwość" w `Axioms_K_TIMDR.md` i
`Axioms_S_TIMDR_Signal.md` (2026-09-17), stwierdzający jawnie: "brak
pre-rejestrowanych progów `θ0`/`θω`, kontroli pozytywnej/negatywnej,
danych realnych". Ten dokument zamraża dokładnie te brakujące elementy.

**Rodowód (dla porządku, nie do powtórzenia tutaj).** Pierwotna
propozycja użytkownika `MöbiusCoherence(S)` łączyła `Z0` (M/S), `ω1`
(K) i `G_i` (G) w JEDNYM operatorze trzy-gałęziowym — odrzucona i
rozbita na trzy niezależne kandydaty 2-gałęziowe: `MC_{K↔G}`
(zrealizowany, odrzucony), `MC_{M/S↔G}` #1 (zrealizowany, USTALONY
diagnostyka) i **`MC_{M/S↔K}` #2 (ten dokument — dotąd tylko nazwany,
teraz operacjonalizowany)**. Żaden z trzech nie jest podzbiorem/
rozszerzeniem innego — dzielą składniki, nie definicje.

**Pytanie testowane:** czy okno sygnału bez trybu stałego (małe `Z0`,
"Möbius-like" w sensie analogii strukturalnej z widmem Laplasjanu
Möbiusa, `λ₁=π²/4>0`, brak trybu zerowego przy Dirichlecie) ma
JEDNOCZEŚNIE wysoką energię skoncentrowaną w pierwszej istotnej
częstotliwości `ω1` — bezpośrednio, bez pośrednictwa żadnej trzeciej
gałęzi.

## 1. Dane (zero nowych plików — reużyte 1:1 z czterech istniejących mostów realnych)

Te same trzy domeny, te same pliki, te same loadery co w
`core/real_{bearing,seismic,btc}_noise_robustness_bridge.py` i w
`core/real_mobius_kg_bridge.py`/`core/real_zero_mode_topology_bridge.py`:

| Domena | Loader (reużyty import) | Klasa pozytywna | Klasa negatywna | fs |
|---|---|---|---|---|
| Łożyska CWRU | `load_real_signals()` | `ir_0021`/`or6_0021`/`b_0021` (defekt) | `normal` | 12000 Hz |
| Sejsmika Ridgecrest | `load_station(name)`, stacje CLC/RIO | `coda` (po `EVENT_IDX`) | `background` (przed) | 100 Hz |
| BTC/USD | `load_log_returns()` + `split_blocks_by_regime()` | `high_vol` bloki | `low_vol` bloki | 1.0 (umowne, patrz §7.1) |

Zero nowego pozyskiwania danych, zero nowych generatorów okien
(`make_real_window_injector`/`make_region_injector`/`make_regime_injector`,
importowane bez zmian).

## 2. Siatka (zero nowych wartości — reużyta 1:1 z `real_mobius_kg_bridge.py`/`real_zero_mode_topology_bridge.py`)

| Domena | `WINDOW_SIZES` | `SIGMAS` | `N_WINDOWS` | `SEED` | `ALPHA` |
|---|---|---|---|---|---|
| Łożyska | (32, 64) | (0.0, 0.1, 0.3, 0.5, 1.0) | 30 | 0 | 0.05 |
| Sejsmika | (64, 128) | (0.0, 0.1, 0.3, 0.5, 1.0) | 30 | 0 | 0.05 |
| BTC | (12, 24) | (0.0, 0.1, 0.3, 0.5, 1.0) | 30 | 0 | 0.05 |

3 domeny × 2 okna × 5 sigm = 30 komórek dla TEGO mostu (jeden most, nie
dwa jak w `PREREG_MOBIUS_COHERENCE_BRIDGES.md` — stąd połowa liczby
komórek tamtego dokumentu).

## 3. Statystyka (zero nowej maszynerii — reużyty 1:1 `run_controls`)

`timdr_formalism.pipeline.run_controls()` (Mann-Whitney U + rank-biserial
`r`, `passed = (positive.pvalue < alpha) and (negative.pvalue >= alpha)`),
identycznie jak we wszystkich sześciu wcześniejszych mostach realnych.

## 4. Składniki (oba już zaimplementowane i przetestowane — zero nowego kodu ekstrakcji)

**`ω1` — pierwsza istotna częstotliwość (gałąź K).** Reużyty
`core.real_mobius_kg_bridge.dominant_omega1(window, fs)` bez zmian —
sam wywołuje `timdr_time.fourier_bridge.fft_modalities` (most Fouriera
M/S↔K, już zweryfikowany 10/10 testów), wybiera modalność o
NAJWIĘKSZEJ amplitudzie `A`, zwraca `ω1=2π·f`.

**`Z0` — tłumienie trybu zerowego (gałąź M/S).** Reużyty
`core.zero_mode_topology_bridge.zero_mode_fraction(window)` bez zmian —
`Z0 = μ²·N/(Σ(S-μ)²+ε)`, już zweryfikowany jako dt/skalo-niezmienniczy
w `tests/test_zero_mode_topology_bridge.py`.

Oba składniki są WIELKOŚCIAMI JUŻ UŻYTYMI w dwóch innych, zrealizowanych
mostach tej rodziny — ten dokument nie wprowadza żadnej nowej ekstrakcji,
tylko nową KOMBINACJĘ dwóch istniejących wielkości.

## 5. Kalibracja (każdy składnik dziedziczy WŁASNĄ, już zamrożoną konwencję ze swojego mostu macierzystego — nie nowy wybór)

**`ω_ref` (dla `ω1`).** Reużyty `core.real_mobius_kg_bridge.calibrate_omega_ref()`
bez zmian: mediana `ω1` na 30 oknach klasy NEGATYWNEJ (tło), `sigma=0.0`,
**seedy 1000–1029** (rozłączne z pulą testową `seed=0..29`) — dokładnie
ta sama konwencja co w `MC_{K↔G}`.

**`θ0` (dla `Z0`).** Mediana `Z0` na POŁĄCZONEJ puli 30 okien klasy
pozytywnej + 30 okien klasy negatywnej, **seedy 1000–1029**, `sigma=0.0`,
`window_size` = MNIEJSZA wartość z `WINDOW_SIZES` danej domeny —
dokładnie ta sama konwencja co `θ0` w `MC_{M/S↔G}` #1
(`core/real_zero_mode_topology_bridge.py::calibrate_domain`).

Rozdzielenie źródeł kalibracji (czysto negatywna dla `ω_ref`, mieszana
dla `θ0`) NIE jest nowym wyborem dla tego mostu — to bierne
odziedziczenie konwencji, którą każda wielkość już ma z WŁASNEGO mostu
macierzystego, celowo NIE ujednolicone tutaj, żeby uniknąć wprowadzenia
jeszcze jednej, nigdzie wcześniej niezweryfikowanej decyzji.

## 6. Operator `MC_{M/S↔K}` #2 — jawna definicja (zamrożona)

**Naprawa znana PRZED dotknięciem danych tego mostu (nie post-hoc).**
`MC_{M/S↔G}` #1 ma udokumentowane, NIENAPRAWIONE zniekształcenie: wersja
ciągła zakłada `Z0∈[0,1]`, ale `Z0` jest z definicji nieograniczone
(rzędu 20–39 na sejsmice) — `Axioms_G_TIMDR_Geometry.md`,
"Ograniczenia" punkt 1. Ta wada jest znana z INNEGO, już ZAKOŃCZONEGO
testu (nie z danych TEGO mostu) — naprawienie jej TERAZ, przed
dotknięciem danych `MC_{M/S↔K}` #2, nie łamie dyscypliny
anty-numerologii (nie jest to dostrojenie po zobaczeniu WYNIKU TEGO
testu). Naprawa: `Z0_norm = Z0/(Z0+1) ∈ [0,1)` — samo-normalizujący
przekształcenie tej samej rodziny co `Λ_dyspersja` w Aksjomacie META-2
(`Axioms_META_TIMDR.md`, `σ/(σ+|μ|+ε)`), bounded z czystej algebry.
`MC_{M/S↔G}` #1 NIE jest tym dokumentem retrospektywnie poprawiany
(jego status i wynik zostają bez zmian) — to jest wyłącznie decyzja
projektowa dla NOWEGO operatora poniżej.

**Wagi `w1`, `w2` — kontynuacja pierwotnej dekompozycji.** Pierwotna,
odrzucona propozycja trzy-gałęziowa miała trzy wagi (`w1` dla `Z0`, `w2`
dla `ω1`, `w3` dla `G_i`) — `MC_{M/S↔G}` #1 użył `w1`,`w3` (usuwając
`w2`/`ω1`). Ten most używa DOKŁADNIE `w1` (ten sam współczynnik/rola co
w moście macierzystym) i `w2` (wcześniej usunięty stamtąd, użyty tu
zamiast `w3`) — pozostaje spójne z oryginalną dekompozycją, nie nowe
nazewnictwo. `w1=w2=0,5` (symetryczne, bez kalibracji, ten sam wybór co
`w1=w3=0,5` w moście macierzystym).

**Operator ciągły (zamrożony):**
```
MC_continuous(S) = w1·(1 - Z0_norm) + w2·(ω1/ω_ref)
                 = 0.5·(1 - Z0/(Z0+1)) + 0.5·(ω1/ω_ref)
```

**Operator binarny (zamrożony), próg `ω1` = `ω_ref` (ta sama wielkość,
bez podwójnego dopasowania):**
```
MC_binary(S) = 1[Z0 < θ0] · 1[ω1 > ω_ref]
```

**Metryka wejściowa do `run_controls`:** `MC_continuous` jako główny
test (większa moc niż binarny na 30 oknach, ten sam wybór co w
`MC_{M/S↔G}` #1); `MC_binary` liczony DODATKOWO i raportowany osobno
jako wartość diagnostyczna, nie jako główny test.

## 7. Zastrzeżenia, jawnie, przed zobaczeniem wyniku

1. **BTC nie ma fizycznej częstotliwości w Hz** — to samo zastrzeżenie
   co w `MC_{K↔G}` (`PREREG_MOBIUS_COHERENCE_BRIDGES.md` §7.1): `ω1`
   dla BTC jest częstotliwością kątową PER PRÓBKA (`dt=1` umowne), nie
   wielkością fizyczną. Wynik na BTC traktowany jako najsłabszy
   dowodowo z trzech domen niezależnie od wyniku.
2. **Konfundacja znana z góry, jawnie nazwana:** zarówno `Z0` (w
   `MC_{M/S↔G}` #1) JAK I metryki oparte na `ω1`/kratownicy (w
   `MC_{K↔G}`) już osobno pokazały TEN SAM wzorzec domenowy — najsilniej
   na łożyskach, częściowo na sejsmice, brak/słabo na BTC. Jeśli
   `MC_{M/S↔K}` #2 powtórzy ten wzorzec, NIE jest to niezależny dowód
   koincydencji `Z0`↔`ω1` specyficznie — może to być artefakt tego, że
   OBIE wielkości z osobna już koreluj z tymi samymi etykietami klas w
   tych samych domenach z niezwiązanych powodów (np. amplituda/SNR
   różna między domenami). Pozytywny wynik na łożyskach w szczególności
   powinien być interpretowany z tym zastrzeżeniem, NIE jako mocny dowód
   specyficznej koincydencji `Z0`-`ω1`.
3. **`Z0_norm` to nowa, wcześniej nieprzetestowana transformacja** —
   mimo że motywowana znanym problemem z innego mostu, sam fakt
   `Z0_norm=Z0/(Z0+1)` bounded nie był dotąd zweryfikowany empirycznie
   na żadnych danych. Traktowany jako świadomy wybór projektowy, nie
   ustalona poprawka.
4. **Oczekiwanie przed testem** (zapisane tutaj, sprawdzalne po fakcie):
   łożyska najsilniejszy efekt, sejsmika częściowy, BTC brak/najsłabszy
   — spójne z WSZYSTKIMI czterema wcześniejszymi mostami realnymi tej
   rodziny (nie nowa hipoteza, powtórzenie już ugruntowanego wzorca
   domenowego w tym ekosystemie).

## 8. Klasyfikacja selektor vs diagnostyka — odroczona do momentu po wyniku

Tak jak w obu poprzednich mostach: klasy pozytywna/negatywna są w
każdej domenie ustalone NIEZALEŻNIE od `Z0`/`ω1`/`MC_{M/S↔K}` (etykiety
CWRU, znacznik czasu mainshocku, podział std bloku BTC) — metryka NIE
będzie użyta do samodzielnego wykrycia/wyboru tych klas. Klasyfikacja
ostateczna (diagnostyka, nie selektor — oczekiwany wynik, zgodnie z
lekcją G-Rezonansu, punkt 11 skilla) zostaje potwierdzona PO zobaczeniu
pełnej siatki 30 komórek, zapisana w `Axioms_K_TIMDR.md` i
`Axioms_S_TIMDR_Signal.md` w osobnym zadaniu, nie w tym dokumencie.

## 9. Status

Zamrożone 2026-09-18, PRZED napisaniem `core/real_ms_k_zero_mode_bridge.py`
i PRZED jakimkolwiek uruchomieniem na realnych danych. Żaden parametr
powyżej nie zostanie zmieniony po zobaczeniu wyniku. Ten plik jest
commitowany OSOBNO, PRZED commitem z kodem/wynikiem — dowód braku
data-snoopingu widoczny w historii git (kolejność commitów), ten sam
wzorzec co `PREREG_MOBIUS_COHERENCE_BRIDGES.md`.

Powiązane: [`PREREG_MOBIUS_COHERENCE_BRIDGES.md`](./PREREG_MOBIUS_COHERENCE_BRIDGES.md)
(bliźniacza pre-rejestracja dla pozostałych dwóch mostów tej rodziny),
[`../theory/Axioms_K_TIMDR.md`](../theory/Axioms_K_TIMDR.md) i
[`../theory/Axioms_S_TIMDR_Signal.md`](../theory/Axioms_S_TIMDR_Signal.md)
(dopiski "most M/S↔K #2", stan sprzed tego dokumentu),
[`../theory/Axioms_META_TIMDR.md`](../theory/Axioms_META_TIMDR.md)
(Aksjomat META-2 — rodzina samo-normalizujących przekształceń, wzór
`Z0_norm` powyżej jest tej samej rodziny), [`../theory/TIMDR_Branch_Specification.md`](../theory/TIMDR_Branch_Specification.md)
("Słownik statusów mostów kandydujących" — status tego mostu zmieni się
najwcześniej po implementacji i wyniku, w osobnym zadaniu).
