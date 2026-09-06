# Walidacja embeddingu pogodowego na realnych danych — wynik NEGATYWNY, zdiagnozowany

**Status:** przetestowane (4/4 testy przechodzą,
`tests/test_trefoil_weather_embedding_validation.py`). **Wynik: pomysł
"zanurz 3 realne parametry pogodowe jako trajektorię i licz κ/τ" NIE
przechodzi kontroli pozytywnej ani negatywnej na realnych danych
Krakow_Centrum, w obecnej formie.** To jest raport negatywny, zgodnie z
protokołem `timdr-signal-framework` §2 punkt 6 ("zgłoś rzeczywisty
wynik, łącznie z brakiem efektu, bez narracyjnego łagodzenia") —
zdiagnozowany, nie tylko odnotowany.

## 0. Skąd to się wzięło

W rozmowie (`TIMDR_Trefoil_FrenetTorsion.md` był o czymś innym —
syntetycznym trójwęźle) padło pytanie "a teraz praktyka jak to się
ma?". Szybki test na 24 punktach realnej serii prognoz
(`krakow_forecast_snapshots.csv`, Krakow_Centrum, `lead_days=1`)
znalazł 2 dni (2026-08-27/28) oznaczone jako "anomalia geometryczna"
(κ/τ embeddingu 3 znormalizowanych parametrów), nie pokrywające się z
płaską detekcją per-parametr — wyglądało obiecująco. Użytkownik
poprosił o dociągnięcie tego rygorystycznie, z kontrolą na sztucznie
wstrzykniętych dziurach, zanim uzna się to za coś więcej niż
ciekawostkę. Ten dokument to ta rygorystyczna kontrola — i pokazuje, że
wstępny wynik nie przeszedł żadnego z trzech testów, którym go poddano.

## 1. Trzy niezależne problemy znalezione

**1. Artefakt luk w próbkowaniu.** Seria prognoz ma nierówne odstępy
(dziury do 4 dni — pull danych nie działał się codziennie). Na czystym
szumie (skorelowany spacer losowy, BEZ żadnej wstrzykniętej anomalii,
ten sam wzorzec luk co realna seria), próbka zaraz po dużej luce
(≥2 dni) ma **4,1× wyższe** prawdopodobieństwo fałszywej flagi
geometrycznej niż próbka regularna. Korekta na rzeczywisty upływ czasu
(różnice skończone uwzględniające `dt`, nie zakładające jednostkowego
kroku) **nie usuwa** tego efektu — wyższe pochodne (przyspieszenie,
szarpnięcie) pozostają numerycznie niestabilne przy nierównym kroku,
niezależnie od poprawnego skalowania przez `dt`. Odkryte "anomalie"
2026-08-27/28 wypadają dokładnie zaraz po największej luce (4 dni) w
tej serii — dokładnie ten podejrzany wzorzec.

**2. Nierozróżnialność od szumu.** Druga, czystsza seria — realne
OBSERWACJE (nie prognozy) Krakow_Centrum, prawie codzienna (tylko
jedna luka 2-dniowa, 27 dni) — dała inny zestaw "anomalii"
(2026-08-31, 09-03, 09-05), tym razem z dala od jedynej luki. Wyglądało
lepiej. Ale kontrola negatywna (400 syntetycznych realizacji
skorelowanego spaceru losowego, ten sam wzorzec próbkowania, BEZ
żadnej anomalii) pokazała: `P(≥3 fałszywe flagi w jednej realizacji pod
czystym szumem) = 0,60`. **3 flagi zaobserwowane w realnych danych są
statystycznie nieodróżnialne od przypadku** — 60% czystego szumu dałoby
tyle samo lub więcej.

**3. Maskowanie przez małą próbkę.** Test czułości: wstrzyknięto
prawdziwy, jednoczesny skok we wszystkich 3 znormalizowanych
parametrach na losowym (nie post-luka) punkcie, o rosnącej amplitudzie
(3, 6, 10, 20 odchyleń standardowych). **Recall NIE rósł z amplitudą —
nawet lekko malał** (9,2% przy amp=3 → 4,6% przy amp=20). Przyczyna:
próg `mean±2·std` liczony jest z TEJ SAMEJ, małej próbki (n≈24-27),
którą się testuje — pojedynczy, nawet ogromny outlier sam zawyża własne
`std`, maskując się przed własnym progiem wykrywania (znany efekt w
statystyce odpornej: nie-odporne miary rozrzutu liczone z zanieczyszczonej
próbki tracą moc wykrywania właśnie tego zanieczyszczenia).

**Próba naprawy (próg odporny mediana/MAD)** częściowo poprawiła recall
(~20-25%, teraz realnie reaguje na amplitudę), ale kosztem fałszywego
alarmu eksplodującego do `P(≥1 fałszywa flaga na czystym szumie) = 0,997`
— sama dystrybucja κ/τ z potrójnego różniczkowania krótkiego,
nie-gładkiego (podobnego do spaceru losowego) szeregu jest zbyt
ciężko-ogonowa/niestabilna dla JAKIEGOKOLWIEK prostego progu, nie tylko
`mean/std`.

## 2. Dlaczego to działało na syntetycznym trójwęźle, a nie tutaj

`TIMDR_Trefoil_FrenetTorsion.md` testował dokładnie tę samą matematykę
(κ/τ z różnic skończonych) i przechodził wszystkie kontrole bez
zarzutu. Kluczowa różnica: tamta krzywa jest **gładka (C²), analityczna,
gęsto próbkowana (N=300)** — różniczkowanie trzykrotne (v→a→j) gładkiej
funkcji jest numerycznie stabilne. Realna seria pogodowa jest
**krótka (N≈24-27) i z natury szorstka** (bliżej spaceru losowego niż
gładkiej krzywej) — każde kolejne różniczkowanie wzmacnia szum, a przy
tak małej próbce nie ma zapasu danych, żeby to uśrednić. To nie jest
problem kalibracji progu — to fundamentalne ograniczenie metody dla
tego reżimu danych.

## 3. Wniosek

Pomysł embeddingu 3 parametrów pogodowych jako trajektorii i liczenia
κ/τ **nie nadaje się w obecnej formie** do wykrywania anomalii na
krótkich (rzędu dni-tygodni), nieregularnie próbkowanych, realnych
seriach pogodowych — ani jako uzupełnienie, ani jako zamiennik
istniejącej płaskiej detekcji w synoptyku. To dotyczy TEGO KONKRETNEGO
zastosowania (embedding realnych parametrów pogodowych o krótkiej
serii) — nie unieważnia wyniku na syntetycznym trójwęźle
(`TIMDR_Trefoil_FrenetTorsion.md`, gładka krzywa, N=300, gdzie metoda
przeszła wszystkie kontrole) ani modelu rezonansu dynamicznego
(`TIMDR_Trefoil_ResonanceModel.md`, model analityczny, nie oparty na
różniczkowaniu zaszumionych danych).

Żeby to naprawić, potrzeba by co najmniej jednego z: (a) rzędy
wielkości więcej punktów danych (setki-tysiące, nie dziesiątki), (b)
metody różniczkowania odpornej na szum (np. wygładzanie
Savitzky-Golay PRZED liczeniem pochodnych — dokładnie ten sam problem,
który `TIMDR-Earthquake-Core` już rozwiązuje `_trm_savgol()`, choć tam
z innego powodu), (c) progu skalibrowanego na oddzielnym zbiorze
referencyjnym, nie na tej samej, testowanej próbce (usuwa maskowanie
z problemu 3).

## Źródła

- Kod: [`../../core/trefoil_weather_embedding_validation.py`](../../core/trefoil_weather_embedding_validation.py)
- Testy: [`../../tests/test_trefoil_weather_embedding_validation.py`](../../tests/test_trefoil_weather_embedding_validation.py)
- Dane realne: `synoptyk-v2.0/krakow_forecast_snapshots.csv` (stacja Krakow_Centrum,
  źródła `prognoza` dla serii z lukami, `IMGW_real`/`OpenMeteo_real_dailymax`/`web_szukaj`
  dla serii prawie-codziennej)
- Kontrast z wynikiem pozytywnym na danych syntetycznych: [`TIMDR_Trefoil_FrenetTorsion.md`](./TIMDR_Trefoil_FrenetTorsion.md)
- Analogiczne rozwiązanie (wygładzanie przed różniczkowaniem) w innym repo: `TIMDR-Earthquake-Core/timdr_core_earthquake.py::_trm_savgol`
