# HELIX–TIMDR: katalog właściwości, wrażliwości i odtwarzalności

**Status:** specyfikacja pomiarów i rejestr właściwości; część wpisów ma wyniki, część pozostaje niezmierzona.  
**Wersja:** 0.1  
**Repozytorium nadrzędne:** GIA-TIMDR  
**Powiązany program:** [HELIX_TIMDR_RESEARCH_PROGRAM.md](../theory/HELIX_TIMDR_RESEARCH_PROGRAM.md)

## 0. Cel i zasada

Celem jest możliwość odtworzenia nie tylko kształtu helisy, lecz także warunków, w których obliczone właściwości są stabilne, zmieniają się, zanikają albo stają się niewiarygodne.

**Nie wpisujemy niezmierzonych cech jako faktów.** Każdy wpis ma status:
- `MEASURED` — wynik istnieje i wskazuje kod, test oraz warunki;
- `DEFINED` — wielkość ma definicję, ale nie zbadano jej wrażliwości;
- `HYPOTHESIS` — przewidywanie do sprawdzenia;
- `UNKNOWN` — brak danych;
- `NOT_APPLICABLE` — własność nie ma sensu dla danego obiektu.

Każdy eksperyment musi zachować: definicję obiektu, parametry wejściowe, jednostki, parametry próbkowania, transformacje, wersje zależności, ziarno RNG, wynik surowy, metryki, commit i komendę uruchomienia.

## 1. Rozdzielenie obiektów — warunek poprawnej rekonstrukcji

Nie wolno łączyć poniższych obiektów tylko dlatego, że w kodzie pojawia się słowo helisa lub symbol tau.

| ID | Obiekt | Definicja / źródło | Status |
|---|---|---|---|
| H-GEO-01 | Krzywa helikalna 3D | Krzywa parametryczna; konkretna postać zależy od modelu | DEFINED, wymaga katalogu wariantów |
| H-KNOT-01 | Trefoil | (x=\sin t+2\sin 2t, y=\cos t-2\cos 2t, z=-\sin 3t), (t\in[0,2\pi)) | MEASURED syntetycznie |
| H-FS-01 | Torsja Freneta-Serreta | Wielkość krzywej wyznaczana z pochodnych 1–3 | DEFINED; wrażliwa numerycznie |
| H-META-01 | Trajektoria meta | (r(t)=(\Lambda(t),\tau_{input}(t),\rho(t))\) | DEFINED |
| H-FIELD-01 | Pole TIMDR | Kandydackie pola (I,M,R,E) w Model T | DEFINED szkicowo; mapowanie helisy UNKNOWN |
| H-TOURO-01 | Potrójny Tourosomobius | Notacja ( (T\times M\times H)_{\Lambda,\tau,\rho}\) | HYPOTHESIS / wymaga dowodu |
| H-STRING-01 | Struna TIMDR | Obiekt z dodatkowymi stopniami swobody do zdefiniowania | UNKNOWN |

Symbol `τ` w MetaState, torsja Freneta-Serreta i skręt topologiczny są różnymi wielkościami. Należy zawsze zapisywać pełną nazwę i domenę.

## 2. Karta geometrii i właściwości

Dla każdej konkretnej krzywej należy zapisać poniższy wektor cech. Nie każda cecha będzie niezmiennikiem i nie każda będzie zdefiniowana w punktach osobliwych.

| Własność | Symbol / definicja | Co może na nią wpływać | Status obecny |
|---|---|---|---|
| Pozycja | (r(t)=(x,y,z)) | translacja, obrót, skala, parametryzacja | DEFINED |
| Prędkość | (v=r'(t)) | skala parametru i czasu | DEFINED |
| Przyspieszenie | (a=r''(t)) | skala parametru, szum | DEFINED |
| Szarpnięcie | (j=r'''(t)) | silnie szum i rozdzielczość próbek | DEFINED |
| Szybkość | (|v|) | parametryzacja, skala | DEFINED |
| Krzywizna | (kappa=\|v\times a\|/\|v\|^3) | geometria, szum, różniczkowanie | DEFINED |
| Torsja | (\tau_{FS}=((v\times a)\cdot j)/\|v\times a\|^2) | geometria, szum, mała krzywizna | DEFINED |
| Helikalność w Hyperflow | (H=\sqrt{\kappa^2+\tau_{FS}^2}) | krzywizna, torsja, jednostki | DEFINED |
| Długość łuku | (L=\int\|r'(t)\|dt) | skala przestrzenna, domena | UNKNOWN dla katalogu helis |
| Skręt całkowity | (\int\tau_{FS}\,ds) | geometria i orientacja | UNKNOWN |
| Liczba/linking/topologia | zależna od obiektu zamkniętego | deformacje i przecięcia | UNKNOWN poza konkretnymi definicjami |
| Widmo / mody | zależne od operatora i warunków brzegowych | próbkowanie, okno, szum | DEFINED tylko w odrębnych narzędziach |

**Uwaga:** (H=\sqrt{\kappa^2+\tau^2}) jest nazwą używaną w THE-GEO PRO 4D. Nie zakładamy, że jest niezmiennikiem geometrycznym ani uniwersalną miarą helikalności bez osobnego dowodu.

## 3. Rejestr wrażliwości

Każdy wiersz to osobny test. Dla wielkości wyjściowej (y) i parametru wejściowego (p) zapisujemy lokalną wrażliwość:
[
S_p(y)=\frac{p}{y}\frac{\partial y}{\partial p}
]
gdy (p,y\ne0). W pobliżu zera raportujemy pochodną bezwzględną i przedział, nie względną wrażliwość.

| ID | Zmieniany czynnik | Oczekiwany wpływ / ryzyko | Minimalny pomiar | Status |
|---|---|---|---|---|
| S-01 | skala przestrzenna r → c·r | Dla tej definicji przy stałym parametrze: κ, τ_FS i H skalują się jak 1/c; długość łuku L jak c | c ∈ {0.25, 0.5, 1, 2, 4}; test numeryczny względem przewidywania | Prawo analityczne wyprowadzone; test implementacji UNKNOWN |
| S-02 | promień helisy | zmienia krzywiznę i relację krzywizna–torsja | siatka promienia, stały skok | UNKNOWN |
| S-03 | skok / pitch | zmienia torsję i kształt | siatka pitch, stały promień | UNKNOWN |
| S-04 | częstotliwość / liczba zwojów | wpływ na długość, lokalną krzywiznę i próbkowanie | siatka częstotliwości | UNKNOWN |
| S-05 | faza początkowa | dla idealnej symetrii może być przesunięciem parametru; dyskretyzacja może wprowadzić różnice | faza w pełnym okresie | UNKNOWN |
| S-06 | obrót sztywny | (kappa,	au) powinny zachować wartości przy obrocie właściwym | macierz obrotu, porównanie tolerancji | HYPOTHESIS |
| S-07 | translacja | pochodne i (kappa,	au) powinny pozostać niezmienione | wektory przesunięcia | HYPOTHESIS |
| S-08 | zmiana parametryzacji | (kappa,	au) geometryczne powinny być niezmiennicze przy regularnej, zgodnej orientacji parametryzacji; implementacja dyskretna może nie | monotoniczne mapy (t\mapsto u) | UNKNOWN |
| S-09 | odwrócenie orientacji | znak torsji może zależeć od konwencji parametryzacji; sprawdzić dokładnie | (t\mapsto -t) | UNKNOWN |
| S-10 | liczba próbek N | błąd różnic skończonych i lokalizacja defektu | (N=50,100,150,300,600,1200) | częściowo MEASURED: N=300 |
| S-11 | szum pozycji | trzecia pochodna może wzmacniać szum bardzo silnie | szum gaussowski i impulsowy, wiele seedów | ryzyko opisane; krzywa degradacji UNKNOWN |
| S-12 | braki / nieregularny krok | różnice skończone zakładają poprawne odstępy | dropout i jitter czasu | UNKNOWN |
| S-13 | próg (kappa_{min}) | bramkuje (	au); może usuwać rzeczywiste odcinki o małej krzywiźnie | siatka logarytmiczna wokół (10^{-4}) | punkt startowy (10^{-4}), nie skalibrowany |
| S-14 | wygładzanie i okno Savitzky–Golay | kompromis bias–variance; może wygasić lokalny defekt | poly, window, porównanie bez filtra | częściowo DEFINED; czułość UNKNOWN |
| S-15 | szerokość deformacji | wpływa na rozmycie i wykrywalność defektu | width sweep | jeden punkt: 0.15 |
| S-16 | amplituda deformacji | próg detekcji i interferencja kilku defektów | amp sweep, w tym znak ± | dwa punkty w teście: 1.5 i 0.8 |
| S-17 | położenie deformacji | brzeg cykliczny vs wnętrze tablicy | wszystkie fazy / trzy loby | dwa położenia i przypadek podwójny MEASURED |
| S-18 | próg rezonansu K/N | precyzja–czułość detekcji | pełna macierz K i kanałów | K=2 z 3 użyte w teście |
| S-19 | definicja kanału / normalizacja | może zmieniać fałszywe alarmy | ablacja każdego kanału | część zmierzona dla jednego defektu |
| S-20 | arytmetyka / tolerancje | małe mianowniki i degeneracje generują niestabilność | float64, tolerancje, przypadki bliskie prostym | ryzyko potwierdzone w dokumentacji |

## 4. Znane parametry i wyniki — nie rozszerzać ich ponad zakres

### 4.1. Trefoil w GIA-TIMDR

Źródła: `core/trefoil_frenet_torsion.py`, `tests/test_trefoil_frenet_torsion.py`, `docs/geometry/TIMDR_Trefoil_FrenetTorsion.md`.

- Parametryzacja:
  [
  x(t)=\sin t+2\sin(2t),\quad
  y(t)=\cos t-2\cos(2t),\quad
  z(t)=-\sin(3t)
  ]
- Domena: (t\in[0,2\pi)), próbki równomierne, endpoint wyłączony.
- Liczba próbek w testach: (N=300).
- Węzły/loby: (t_0=0,2\pi/3,4\pi/3).
- Deformacja: Gaussowski bump w osi z; (amp=1.5), (width=0.15).
- Test podwójny: ((t_0,amp)=(0,1.5)) oraz ((4\pi/3,0.8)).
- Detekcja: trzy kanały (krzywizna, torsja, odchylenie od centroidu); rezonans (K=2).
- Tolerancja lokalizacji: 6 próbek na 300 (około 2% okresu).
- Wynik w zadanym syntetycznym teście: czysty trefoil — zero fałszywych alarmów; deformacje pozytywne wykryte; dwie deformacje rozdzielone, brak alarmu przy nietkniętym trzecim lobie.
- Kanał odchylenia od centroidu był ślepy na testowany typ deformacji; nie wolno uogólniać tego na wszystkie deformacje.
- Nie testowano pełnej siatki amplitud, szerokości, szumu, liczby próbek ani innych rodzin węzłów.

### 4.2. Geometria różnicowa — ostrzeżenia

- Wzory (kappa,	au_{FS}) z (v,a,j) są użyteczne dla gładkich, odpowiednio próbkowanych krzywych.
- Torsja ma mianownik (|v\times a|^2); przy prawie prostoliniowych fragmentach szum może zostać wzmocniony.
- W THE-GEO PRO 4D stosowane jest bramkowanie (kappa<10^{-4}\Rightarrow\tau=0). To punkt startowy, a nie uniwersalna stała.
- Dokumentacja Hyperflow i GIA opisuje porażkę surowego potrójnego różniczkowania na krótkich, zaszumionych danych oraz potrzebę wygładzania. Nie przenosić wyniku testu gładkiej helisy na realne dane.
- W META-DYNAMICS `field_torsion` wygładza serię filtrem Savitzky–Golay, domyślnie `poly=3`, okno do 9 próbek, zakłada stały `dt`; przy zbyt krótkiej serii zwraca zera. Bez SciPy przechodzi na gorsze różnice numeryczne. Te ścieżki muszą być raportowane osobno.

### 4.3. Estymator GS-Matrix

Źródło: `TIMDR-Math-Formalism/docs/theory/PREREG_HELICAL_SHAPE_ESTIMATOR.md`.

- Model: (x(t)=[\exp(Kt)V_0]_0), (K=[ [\mu_{down},\omega_0],[-\omega_0,\mu_{up}] ]).
- (N=64), (dt=0.01), (V_0\sim Uniform(0.5,1.5)^2), 30 prób na kombinację.
- Szum: (sigma\in\{0,0.02,0.05,0.10,0.20\}).
- Wynik: klasyfikacja obecności rotacji przeszła w zakresie testowym, lecz dokładność (Re(\lambda)) nie przeszła; nie jest to dowód stabilnej estymacji wszystkich parametrów helisy.

## 5. Protokół pełnego odtworzenia eksperymentu

Każdy eksperyment helikalny ma osobny katalog wynikowy i manifest JSON/CSV zawierający co najmniej:

1. `experiment_id`, hipotezę, status prerejestracji i datę.
2. Repozytorium, ścieżki plików, commit SHA i czystość drzewa roboczego.
3. Definicję krzywej/pola/struny, wzory, domenę, przeciwdziedzinę, konwencję orientacji.
4. Wszystkie parametry z jednostkami, również domyślne i progi.
5. Generator danych, liczbę próbek, zakres, endpoint, krok i sposób obsługi cykliczności.
6. Szum: rozkład, sigma, korelację, miejsce dodania, seed i liczbę powtórzeń.
7. Transformacje: filtr, okno, rząd wielomianu, normalizację, interpolację, kolejność operacji.
8. Wersje Python, NumPy, SciPy i systemu; precyzję float.
9. Polecenie uruchomienia, log stdout/stderr i status testów.
10. Wyniki surowe (nie tylko średnie), metryki, przedziały ufności, wykresy i hash plików danych.

Przy zmianie jednego parametru nie zmieniać równocześnie innych. Dla testów losowych używać jawnych, niezależnych seedów i zapisać je w manifeście. Prerejestracja musi zostać zamrożona przed uruchomieniem testu potwierdzającego.

## 6. Macierz wymaganych badań wrażliwości

Kolejność minimalna:

**P0 — wiarygodność numeryczna**
- test niezmienniczości względem translacji i obrotu;
- test skalowania przestrzeni i parametryzacji;
- zbieżność względem N na analitycznej krzywej;
- porównanie różnic skończonych z pochodnymi analitycznymi;
- degeneracje: (|v|\to0), (|v\times a|\to0).

**P1 — odporność na zakłócenia**
- krzywa degradacji względem szumu pozycji;
- nieregularny czas, dropout, outliery i kwantyzacja;
- wpływ wygładzania na amplitudę i lokalizację defektu;
- stabilność progów (kappa_{min}), anomalii i K/N.

**P2 — zakres geometryczny**
- promień, pitch, liczba zwojów, faza, orientacja i skala;
- helisa kołowa, stożkowa, zmiennoskokowa i trefoil — oddzielne klasy;
- zamknięte i otwarte krzywe; przypadki samoprzecięć;
- lokalne i globalne deformacje, pojedyncze i nakładające się defekty.

**P3 — pole i struna**
- jawna przestrzeń wartości, jednostki, warunki brzegowe i równania;
- mapa helisa→pole / helisa→struna wraz z dziedziną i przeciwdziedziną;
- test jednoznaczności, stabilności i rekonstrukcji odwrotnej;
- ilościowy pomiar utraty informacji i zachowania niezmienników.

Nie przechodzić do P3, dopóki P0 nie wykaże, że bazowa geometria jest poprawnie odtwarzana.

## 7. Format raportu dla każdej właściwości

Każdy wynik należy zapisać w następującym formacie:

- **Nazwa / ID:**
- **Obiekt i definicja:**
- **Hipoteza:**
- **Parametry bazowe i jednostki:**
- **Parametr zmieniany / zakres:**
- **Metoda i liczba powtórzeń:**
- **Metryka wrażliwości:**
- **Wynik surowy i niepewność:**
- **Kontrola pozytywna / negatywna:**
- **Warunki, w których własność zanika lub staje się niestabilna:**
- **Kod / test / commit / manifest:**
- **Status i ograniczenia:**

## 8. Otwarte luki — jawny stan na 2026-11-09

Nie ma jeszcze pełnego katalogu zmierzonych wrażliwości. W szczególności UNKNOWN pozostają:
- krzywe degradacji (kappa,	au,H) względem szumu i liczby próbek;
- wpływ skali, promienia, pitch, fazy i reparametryzacji;
- stabilność wobec nieregularnego próbkowania i braków;
- czułość na `min_curvature`, okno i rząd filtra;
- granice wykrywalności deformacji względem amplitudy i szerokości;
- zachowanie przy deformacjach o przeciwnych znakach i nakładających się;
- niezmienniki i mapy rekonstrukcyjne pola/struny;
- wszystkie własności kryptograficzne.

## 9. Dziennik zmian

- **2026-11-09 / v0.1:** utworzono katalog właściwości i rejestr wrażliwości; zapisano parametry istniejącego testu trefoil i GS-Matrix; oddzielono wyniki zmierzone od hipotez i luk; określono manifest oraz kolejność badań P0–P3.


## 14. Rozszerzenie rejestru wrażliwości: węzeł trójhelikalny i trajektoria trójkąta

Nowy zestaw obowiązkowych czynników do testowania znajduje się w [TRIANGLE_HELIX_NODE_BOUNDARY_CONDITIONS.md](TRIANGLE_HELIX_NODE_BOUNDARY_CONDITIONS.md): domknięcie osi i fazy na szwie, ciągłość stycznej i ramy, permutacja trzech gałęzi, warunki jednostronne w punktach kardynalnych, naroża trajektorii trójkąta, orientacja obiegu oraz różne modele redukcji 4→3. Wrażliwości te pozostają UNKNOWN do czasu wykonania testów; nie są przedstawiane jako zmierzone.
