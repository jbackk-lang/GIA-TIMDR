# Pre-rejestracja: most P/Q → torsja trójwęzła → pipeline (M/S)

> Status: PRE-REJESTRACJA, zamrożona PRZED dotknięciem jakichkolwiek
> realnych danych M/S. Kod jeszcze nie napisany — to jest wersja
> papierowa (zgodnie z ustaloną dyscypliną: najpierw jawnie nowa
> konstrukcja na papierze, potem dopiero implementacja). Data: 2026-09-15.

## 0. Skąd to się bierze i czym NIE jest

Punktem wyjścia jest rozmowa o tym, że **P/Q obwiedni trójkąta (Aksjomat
G10, `timdr_geometry/envelope.py`)** to najtwardszy, faktycznie dowiedziony
kawałek geometrii w całym ekosystemie — dokładna tożsamość
`R_max(Δ)=r_in(Δ)`, 65/65 testów, realny błąd znaleziony i naprawiony.
Padła propozycja, żeby wziąć to jako punkt startowy i „wyprowadzić" z
niego topologię.

**Trzeba to od razu uczciwie skorygować, zanim pójdziemy dalej**: `P(R)`
i `Q(R)` z G10 są ściśle monotoniczne (`Q: [0,1]→[0,1]`, rosnące) —
nie ma tam żadnego naturalnego miejsca na „skręt" (oscylację, zmianę
znaku, zawijanie). Sprawdzone bezpośrednio w kodzie: `envelope.py` nie
zawiera niczego, co dawałoby się interpretować jako topologiczny skręt.
**Ta konstrukcja NIE jest matematycznym rozszerzeniem G10.** G10 służy
tu wyłącznie jako wzorzec rygoru (dokładna definicja + kod + testy +
zero tuningu po fakcie) — nie jako wejście matematyczne. To jest, jak
most Fouriera M/S↔K i sprzężenie helikalne K↔Θ_bif wcześniej, **nowa,
jawnie oznaczona konstrukcja**, nie wyprowadzenie z istniejącej
struktury.

Obiektem, który faktycznie ma jakikolwiek kod w tym ekosystemie i mówi
o „skręcie" w sensie topologicznym, jest **torsja Freneta-Serreta
trójwęzła** (`GIA-TIMDR/core/trefoil_frenet_torsion.py`) — piąte,
formalnie odrębne znaczenie słowa „skręt" wg `TIMDR_Twists.md`,
świadomie NIE utożsamione ani ze skrętem topologicznym
torus→Möbius→tetroida (sprawdzone i odrzucone jako tożsame), ani ze
skrętem sygnałowym M/S. To jedyny istniejący kandydat na „pojedynczy,
skalarny parametr topologiczny" — reszta (liczba przejść klasy
kształtu, zmiana typu obwiedni) nie ma dziś definicji ani kodu.

## 1. Jawne ostrzeżenie a priori (disclosure przed hipotezą)

Zanim sformułuję hipotezę: **dwie niezależne wcześniejsze próby w tym
ekosystemie już zawiodły z dokładnie tego samego powodu**, którym
ryzykuje ta konstrukcja:

1. `trefoil_weather_embedding_validation.py` — ta sama matematyka
   (`v→a→j`, potrójne różnicowanie) zastosowana do krótkiego (N~24-27),
   nieregularnie próbkowanego, zaszumionego szeregu pogodowego dała
   fałszywe flagi 4,1× częstsze po lukach w danych i wynik
   nieodróżnialny statystycznie od czystego szumu (p=0,60).
2. Estymator DMD/delay-embedding w `GS_Matrix_Helical_Coupling_DRAFT.md`
   (punkt 18 skilla) — embedding opóźniający krótkiego, zaszumionego
   sygnału dawał błędy 700-3000% z powodu strukturalnej
   niemal-osobliwości macierzy regresji.

Oba przypadki to ten sam mechanizm: **kolejne różnicowanie/embedding
krótkiego, zaszumionego, rzeczywistego szeregu wzmacnia szum szybciej,
niż dokłada informacji.** Torsja Freneta-Serreta wymaga TRZECH
kolejnych różnic (v, a, j) — to jest strukturalnie ten sam rodzaj
operacji, która już dwukrotnie zawiodła. **Uczciwe oczekiwanie a priori
jest więc pesymistyczne, nie optymistyczne** — ten test ma sprawdzić,
czy tym razem jest inaczej, a nie potwierdzić założenie, że będzie
inaczej. Jeśli wynik będzie negatywny, to NIE będzie zaskoczeniem i
zostanie tak właśnie zaraportowany.

## 2. Pytanie badawcze

Czy skalarna metryka wyprowadzona z torsji Freneta-Serreta trajektorii
zbudowanej metodą embeddingu opóźniającego z okna sygnału M/S niesie
odtwarzalną treść — tzn. odróżnia syntetyczne okna z genuine
nieplanarnością (torsją) od (a) czystego szumu i (b) okien planarnych
(sam ruch/krzywizna, ale zero torsji) — gdy oceniona rygorystycznie
przez istniejący pipeline anty-numerologiczny (`timdr_formalism.pipeline`:
Mann-Whitney U, rozmiar efektu, kontrola +/- bramkująca wynik)?

Real-data (M/S event windows: sejsmika/łożyska/BTC z
`PREREG_MS_K_EVENTS.md`) dotykamy DOPIERO po przejściu (lub jawnie
opisanym nie-przejściu) tego etapu syntetycznego — dokładnie ten sam
porządek co przy moście Fouriera i sprzężeniu helikalnym.

## 3. Konstrukcja (zamrożona przed danymi)

### 3.1 Embedding: sygnał 1D → trajektoria 3D

Sygnał M/S to pojedynczy szereg skalarny `x(t)`, nie gotowa trajektoria
3D — trzeba go osadzić. Wybór (zamrożony, nie tuningowany po wyniku):
**embedding opóźniający** (delay embedding), dokładnie ta sama rodzina
konstrukcji co wcześniej w estymatorze DMD (punkt 18 skilla), tym razem
z opóźnieniem 2-krokowym zamiast 1-krokowego, żeby dać 3 współrzędne:

```
p(t) = (x(t), x(t+lag), x(t+2*lag))
```

- `lag = 1` próbka (wartość domyślna, zamrożona — NIE strojona po
  zobaczeniu wyników; uzasadnienie: najprostszy możliwy wybór, brak
  dodatkowego wolnego parametru do przeszukania).
- **Jawnie ODRZUCONA alternatywa**: embedding przez pochodne
  `(x, dx/dt, d²x/dt²)` — to dokładnie ścieżka, która już zawiodła w
  `trefoil_weather_embedding_validation.py` (tam liczono `v/a/j` z
  POZYCJI, tu liczylibyśmy je z JUŻ RÓŻNICZKOWANYCH współrzędnych —
  jeszcze więcej różnicowania, jeszcze gorzej). Delay embedding różnicuje
  raz mniej niż ta alternatywa.
- Sygnał normalizowany `(x-mean)/std` PRZED embeddingiem (ten sam
  amendment co przy estymatorze kształtu helikalnego — potrzebny, bo
  realne domeny mają skale różniące się o rzędy wielkości).

### 3.2 Krzywizna/torsja wzdłuż trajektorii

Reużyty wprost, bez modyfikacji, `kappa_tau_time_aware()` z
`core/trefoil_weather_embedding_validation.py` (wersja uwzględniająca
rzeczywisty odstęp czasu między próbkami — właściwa dla domen o różnym
`fs`, jak sejsmika 100Hz vs łożyska 12kHz) z domyślnymi progami
`DEFAULT_MIN_SPEED=1e-6`, `DEFAULT_MIN_CURVATURE=1e-4` z
`trefoil_frenet_torsion.py` — te same stałe co w oryginalnym, już
istniejącym kodzie, NIE nowe/zgadnięte.

### 3.3 Redukcja do jednego skalara na okno

`metric_fn(window) -> float` wymagane przez `pipeline.run_controls()`.
Zamrożony wybór: **`max(|tau(t)|)`** po próbkach niezbramkowanych
(`kappa >= min_curvature`) w oknie. Jeśli wszystkie próbki
zbramkowane (trajektoria zdegenerowana/płaska w granicach progu) →
`metric = 0.0`.

Uzasadnienie wyboru `max` zamiast `mean`: torsja jest lokalną
własnością punktową — genuine nieplanarny fragment krzywej może być
krótki; uśrednianie po całym oknie rozcieńcza sygnał zerami z
bramkowanych/płaskich fragmentów. To jest decyzja podjęta PRZED
zobaczeniem jakiegokolwiek wyniku (świadomie różna od wcześniejszego,
zawodnego podejścia progowego mean±2σ z `adaptive_thresholds.py`,
które w walidacji pogodowej samo się psuło przez małą próbkę).

### 3.4 Rozmiar okna

Dwa reżimy, oba zamrożone:

- **Reżim A (gęsty/syntetyczny-analogiczny)**: `window_size=300`,
  ten sam co domyślny `trefoil_points(n=300)` — sprawdza, czy metryka
  działa w ogóle, w warunkach zbliżonych do już zwalidowanego
  syntetycznego trójwęzła.
- **Reżim B (rzadki/realistyczny)**: `window_size=64`, dopasowany do
  rzeczywistego rozmiaru okien łożysk CWRU z `PREREG_MS_K_EVENTS.md`
  (bliżej skali, która faktycznie zawiodła w walidacji pogodowej,
  N~25-27).

Jeśli metryka przechodzi w reżimie A, ale nie w B, to jest **wynik
zawężający zakres** (analogicznie do mostu Fouriera) — dokładna
paralela do znanego już problemu: „gładka, gęsta syntetyka działa;
krótki, rzadki realny szereg nie" — i zostanie tak opisany, nie
zamazany.

## 4. Kontrola pozytywna (syntetyczna)

Generator sygnału 1D o **genuine nieplanarnej** trajektorii w
embeddingu opóźniającym — potrzebna suma NIEZALEŻNYCH częstotliwości
(analogicznie do parametryzacji trójwęzła `sin(t)+2sin(2t)`, która sama
jest sumą harmonicznych):

```
x(t) = sin(w1*t) + 0.5*sin(w2*t + phi) + szum(sigma)
```

z `w1, w2` w stosunku niewymiernym/niezharmonizowanym (np. `w1=1.0,
w2=2.7`, zamrożone), `phi` losowe per okno. Uzasadnienie: pojedyncza
częstotliwość daje w delay-embeddingu elipsę — krzywą PŁASKĄ (torsja
≡0 z definicji, niezależnie od amplitudy) — więc żeby dostać genuine
torsję, potrzeba co najmniej dwóch niewspółmiernych częstotliwości,
dokładnie jak w oryginalnym trójwęźle.

## 5. Kontrole negatywne (dwie, różne mechanizmy)

- **Negatywna A — szum**: `x(t) = szum biały/AR(1)` bez żadnej
  wstrzykniętej struktury. Testuje: czy metryka daje false positive na
  czystej przypadkowości (dokładnie test, który poprzednio wypadł źle
  na danych pogodowych, p=0,60).
- **Negatywna B — planarna (specyficzna dla torsji, NIE ogólny szum)**:
  `x(t) = sin(w1*t) + szum(sigma)` — POJEDYNCZA częstotliwość plus szum.
  Ma normalny ruch i normalną krzywiznę (embedding nie jest zdegenerowany
  do punktu), ale z definicji zerową genuine torsję. To jest test
  SPECYFICZNOŚCI: czy metryka odróżnia „coś się dzieje" od „genuine
  skręt w 3D", czy tylko wykrywa dowolną nietrywialną dynamikę
  (dokładnie błąd, którego chcemy uniknąć — metryka reagująca na
  cokolwiek nie mówi nic o topologii).

`pipeline.run_controls()` wymaga DWÓCH generatorów negatywnych
(`negative_generator_a`, `negative_generator_b`) — kontrole A i B
wypełniają to od razu, bez potrzeby modyfikacji pipeline'u.

## 6. Siatka szumu i liczba powtórzeń

Zamrożone przed danymi: `sigma ∈ {0.0, 0.1, 0.3, 0.5, 1.0}` (względem
amplitudy jednostkowej sygnału pozytywnego), `n_windows=30` (wartość
domyślna `pipeline.run_controls`, niezmieniona), `seed` iterowany
0..N dla powtarzalności, `alpha=0.05` (domyślne).

## 7. Kryteria sukcesu (zamrożone, binarne — z run_controls)

`ControlResult.passed` z pipeline'u już koduje to poprawnie: test
przechodzi, gdy **kontrola pozytywna jest istotna statystycznie
(p<alpha) z odpowiednim kierunkiem**, ORAZ **obie kontrole negatywne
(A i B) NIE są istotne** (p≥alpha) — czyli metryka odróżnia genuine
torsję od szumu I od planarnego ruchu, nie tylko od jednego z nich.
Dodatkowo raportowany (nie bramkujący) rozmiar efektu
(`rank_biserial_effect_size`) dla kontroli pozytywnej — istotność bez
dużego efektu to wynik słaby, nie mocny (ten sam standard co wszędzie
indziej w tym ekosystemie).

Wynik czytany per (reżim rozmiaru okna) × (poziom szumu) — 2×5=10
komórek, bez agregowania w jedną liczbę, żeby nie zgubić ewentualnego
zawężenia zakresu (np. „działa przy gęstym oknie i niskim szumie,
zawodzi gdzie indziej").

## 8. Co NIE jest tu jeszcze rozstrzygnięte (jawnie otwarte)

- Czy `lag=1` to dobry wybór dla wszystkich domen M/S (sejsmika 100Hz
  vs łożyska 12kHz mają bardzo różną gęstość próbkowania względem
  charakterystycznej skali czasowej zjawiska) — jeśli test syntetyczny
  przejdzie, TO dopiero pytanie do rozstrzygnięcia przed realnymi
  danymi, nie teraz.
- Czy `max(|tau|)` jest najlepszym wyborem redukcji — alternatywy
  (mediana z progiem odpornym, udział zbramkowanych próbek) świadomie
  odłożone, żeby nie przeszukiwać wielu wariantów metryki na tym samym
  teście (dokładnie ryzyko, przed którym ostrzega `bonferroni_correct`
  w pipeline).
- To NIE jest test na realnych danych — real-data (sejsmika/łożyska/BTC)
  dopiero po tym kroku, i tylko jeśli wynik syntetyczny da podstawę do
  kontynuacji (a jeśli da wynik negatywny, real-data może zostać
  świadomie pominięte, tak jak katalog transjentów przy moście Fouriera
  — decyzja do podjęcia PO zobaczeniu tego wyniku, nie teraz).

## 9. Status

Niniejszy dokument jest zamrożoną pre-rejestracją. Następny krok:
implementacja dokładnie wg powyższego (bez odstępstw niezanotowanych
tutaj), uruchomienie na syntetyce, uczciwe zaraportowanie wyniku —
łącznie z negatywnym, biorąc pod uwagę pesymistyczny prior z sekcji 1.
