# Torsja Freneta-Serreta trójwęzła — piąte znaczenie "skrętu", empirycznie przetestowane

**Status:** zaimplementowane i przetestowane (4/4 testy przechodzą,
`tests/test_trefoil_frenet_torsion.py`). Odrębne od pozostałych czterech
znaczeń "skrętu" w tym ekosystemie — patrz `TIMDR_Twists.md` punkt 5 dla
formalnej specyfikacji domeny/przeciwdziedziny/definicji i tabeli
rozdzielenia.

## 0. Skąd to się wzięło

Użytkownik zaproponował model: *"cała idea badania sygnału opiera się
na trójwęźle helikalnym — oś wzdłuż figury reprezentuje skręt,
odstępstwa/deformacje pierwszego węzła to defekty, całość powinna być
rewidowana rezonansem — tylko nie wiem co do czego"*.

Dokładnie ta figura — **trójwęzeł helikalny** — już istnieje w tym
repo, w `docs/geometry/tourosomobius.md` ("Potrójny Tourosomobius"),
jako część hybrydy torus+Möbius+helisa. Ale tamten dokument jest
**wyłącznie notacją pojęciową**: brak dziedziny/przeciwdziedziny, brak
dowodu, brak kodu, brak testów — inny poziom rygoru niż `Axioms_G/S/K`.

Ten dokument bierze jeden, konkretnie nazwany kawałek tej idei — "oś
wzdłuż figury reprezentuje skręt" — i sprawdza go na policzalnym
modelu, zamiast zostawiać jako metaforę.

## 1. Ważne rozgraniczenie PRZED jakąkolwiek matematyką

`TIMDR_Twists.md` już dokumentuje, że słowo "skręt" ma cztery
wcześniej istniejące, formalnie odrębne znaczenia w tym ekosystemie —
i jedno z nich, **skręt topologiczny (τ)** z `Operators_N_TIMDR.md`,
zostało jawnie **sprawdzone i odrzucone** jako tożsame z torsją
Freneta-Serreta krzywej (`timdr-signal-framework` §20 macierzystego
skilla).

Dlatego to, co liczy ten dokument, **nigdzie nie jest nazywane "skręt
TIMDR"** — nazywane jest wprost: **torsja Freneta-Serreta wzdłuż osi
trójwęzła**. To piąte, jawnie odrębne znaczenie (patrz `TIMDR_Twists.md`
punkt 5 i tabela T2) — nie rozszerzenie ani szczególny przypadek
żadnego z poprzednich czterech, mimo współdzielonego symbolu τ ze
skrętem topologicznym.

## 2. Model geometryczny

**Trójwęzeł (trefoil knot)** — klasyczna krzywa zamknięta w 3D o
naturalnej symetrii 3-krotnej:

```
x(t) = sin(t) + 2*sin(2t)
y(t) = cos(t) - 2*cos(2t)
z(t) = -sin(3t)          t ∈ [0, 2π)
```

Trzy "węzły"/loby przy `t = 0, 2π/3, 4π/3` — naturalny kandydat na to,
co użytkownik nazwał "pierwszym węzłem" i jego odpowiednikami.

**Krzywizna i torsja** liczone z prędkości/przyspieszenia/szarpnięcia
(`v, a, j`) wyznaczonych różnicami skończonymi z 4 kolejnych próbek —
**dokładnie ten sam wzór**, co już zwalidowany (błąd <0,001% względem
analitycznej helisy) w `THE_TIMDR_Hyperflow_Engine/the_geo_pro_4d.py`:

```
κ(t) = ‖v × a‖ / ‖v‖³
τ(t) = det(v, a, j) / ‖v × a‖²
```

z tym samym bramkowaniem szumu co G8-G9: `κ(t) < κ_min ⇒ τ(t) = 0`
(dzielenie przez `‖v×a‖²` wzmacnia szum na niemal-prostoliniowym
odcinku, dokładnie ten wzorzec błędu, co przy `cross_norm==0` opisanym
w `the_geo_pro_4d.py`).

Kod powielony (nie zaimportowany) w `core/trefoil_frenet_torsion.py` —
GIA-TIMDR i THE_TIMDR_Hyperflow_Engine to osobne repo bez wspólnej
zależności pakietowej, ten sam wzorzec, co `the_geo_pro_4d.py` samo
stosuje wobec `FLIGHT-TRACKING-TIMDR/core/curvature_detector_3d.py`.

## 3. Trzy hipotezy do przetestowania (zdefiniowane PRZED uruchomieniem)

Zgodnie z protokołem `timdr-signal-framework` §2 (definicja obiektu/
metryki/modelu null PRZED zobaczeniem wyniku, kontrola pozytywna +
negatywna):

- **H1** — "oś wzdłuż figury reprezentuje skręt": torsja Freneta-Serreta
  wzdłuż krzywej niesie sensowny, nie-losowy sygnał geometryczny.
- **H2** — "deformacja pierwszego węzła to defekt": lokalne odkształcenie
  jednego węzła/lobu da się wykryć jako anomalię/skok na sygnale
  krzywizny/torsji, zlokalizowany dokładnie w tym miejscu.
- **H3** — "całość rewidowana rezonansem": koincydencja (≥K kanałów
  jednocześnie anomalnych — krzywizna, torsja, odchylenie pozycji od
  centroidu) lokalizuje deformację trafniej (mniej szumu) niż
  pojedynczy kanał osobno.

Progi anomalii/defektu **celowo identyczne** z
`synoptyk-v2.0/analyzer/adaptive_thresholds.py` (`mean±2·std` dla
anomalii, `0.3·(p90−p10)` dla skoku) — już używany w ekosystemie wzorzec,
nie nowa, niezależnie wymyślona metryka. Rezonans — koincydencja `≥K`
z `N` kanałów — ta sama logika K-z-N co rezonans-M w synoptyku
(tam `DEFAULT_RESONANCE_K=3` z 5 parametrów pogodowych; tu `K=2` z 3
kanałów geometrycznych, bo tylko 3 są zdefiniowane w tym modelu).

## 4. Wyniki (4 testy, `tests/test_trefoil_frenet_torsion.py`)

**Kontrola negatywna** — czysty, niezdeformowany trójwęzeł: **zero**
fałszywych alarmów na jakimkolwiek kanale (krzywizna, torsja,
odchylenie pozycji) i w rezonansie.

**Kontrola pozytywna, węzeł na granicy tablicy próbek** (`t0=0`):
lokalne odkształcenie (gaussowski "bump" w osi z) wykryte przez
rezonans, zlokalizowane w promieniu ≤6 próbek z 300 (≈2% okresu) od
prawdziwego węzła. Torsja reaguje silnie, ale rozmyto (31 punktów
rozrzuconych wokół węzła); krzywizna reaguje słabiej, ale precyzyjniej
(6 punktów); odchylenie pozycji od centroidu — zupełnie ślepe (0
wykryć, słaby kanał). **Rezonans (koincydencja ≥2 z 3) redukuje 31
zaszumionych punktów torsji do 4 ciasno zlokalizowanych** — to
bezpośrednie potwierdzenie H3: koincydencja odszumia, nie tylko
"podbija pewność".

**Kontrola pozytywna, węzeł wewnętrzny** (`t0=2π/3`, z dala od granicy
tablicy — sprawdza, że lokalizacja nie jest artefaktem brzegowym
liczenia różnic skończonych): wykrycie w promieniu ≤6 próbek od
oczekiwanego węzła, zero fałszywych alarmów przy dwóch pozostałych,
nietkniętych węzłach.

**Dwie jednoczesne deformacje różnej siły** (węzeł `t=0`, amp=1,5 i
węzeł `t=4π/3`, amp=0,8), trzeci węzeł nietknięty: obie deformacje
wykryte **osobno i poprawnie zlokalizowane**, zero trzeciego,
fałszywego wykrycia przy nietkniętym węźle — nawet gdy jedna
deformacja jest prawie dwukrotnie słabsza od drugiej.

## 5. Wniosek

Intuicja użytkownika trzyma się na konkretnym, policzalnym modelu:
oś niesie sygnał torsji (H1), punktowa deformacja węzła daje lokalny
"defekt" wykrywalny tymi samymi progami co reszta ekosystemu (H2), a
rezonans jako koincydencja kanałów realnie odszumia i precyzuje
lokalizację zamiast tylko zwiększać pewność (H3) — potwierdzone także
pod obciążeniem (dwie jednoczesne deformacje różnej siły, bez
wzajemnej interferencji wykryć).

**Warunek, którego nie wolno zgubić:** to działa dla torsji
Freneta-Serreta TEJ KONKRETNEJ krzywej (trójwęzła) — nie dla już
zdefiniowanego skrętu topologicznego τ (rodzina powierzchni) ani
skrętu sygnałowego (szereg czasowy 1D). Te zostają formalnie odrębne,
zgodnie z zasadą nadrzędną tego ekosystemu: jedno słowo, różne obiekty
matematyczne w różnych domenach, nie różne poziomy jednej teorii.

## 6. Co NIE zostało zrobione (uczciwe ograniczenia zakresu)

- Model testowany wyłącznie na syntetycznej krzywej analitycznej —
  brak testu na realnej trajektorii 3D z szumem pomiarowym (patrz też
  ograniczenie `FLIGHT-TRACKING-TIMDR`: brak walidacji na realnych
  danych ADS-B/FDR w całym ekosystemie na razie).
- `K=2` (próg rezonansu) i `width=0,15` (szerokość wstrzykiwanej
  deformacji) to punkty startowe dobrane do tego eksperymentu, NIE
  skalibrowane na żadnym realnym rozkładzie — analogicznie do
  `min_curvature=1e-4` w `the_geo_pro_4d.py`, wymagają kalibracji, gdy
  pojawią się realne dane.
- Kanał "odchylenie pozycji od centroidu" okazał się ślepy na tego
  rodzaju deformację — zostawiony w kodzie dla kompletności (3 kanały
  to naturalny odpowiednik 3 węzłów), ale nie wnosi nic do wykrycia w
  tym eksperymencie; nie usunięto go, żeby nie zakładać z góry, że
  będzie równie bezużyteczny dla innych typów deformacji.
- Nie zbadano, czy inne parametryzacje trójwęzła (inny stosunek
  częstotliwości niż 1:2:3) albo inne krzywe węzłowe (węzeł
  torusowy `T(p,q)` ogólnie) dają jakościowo te same wyniki — to
  jeden, konkretny reprezentant, nie dowód dla całej klasy krzywych
  węzłowych.

## Źródła

- Kod: [`../../core/trefoil_frenet_torsion.py`](../../core/trefoil_frenet_torsion.py)
- Testy: [`../../tests/test_trefoil_frenet_torsion.py`](../../tests/test_trefoil_frenet_torsion.py)
- Inspiracja (notacja pojęciowa, nieformalizowana): [`tourosomobius.md`](./tourosomobius.md)
- Formalne rozgraniczenie od pozostałych czterech znaczeń "skrętu": [`../theory/TIMDR_Twists.md`](../theory/TIMDR_Twists.md)
- Matematyka źródłowa (już zwalidowana na helisie analitycznej): `THE_TIMDR_Hyperflow_Engine/the_geo_pro_4d.py`
- Progi anomalia/defekt/rezonans wzorowane na: `synoptyk-v2.0/analyzer/adaptive_thresholds.py`
