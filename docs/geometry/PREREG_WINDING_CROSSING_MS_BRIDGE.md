# Pre-rejestracja: winding number + crossing number jako most M/S↔topologia

> Status: PRE-REJESTRACJA, zamrożona PRZED dotknięciem jakichkolwiek
> danych (nawet syntetycznych — kod jeszcze nie napisany w chwili
> zapisania tego dokumentu). Data: 2026-09-15. Bezpośrednia kontynuacja
> `PREREG_TREFOIL_MS_BRIDGE.md` / `RESULT_TREFOIL_MS_BRIDGE.md` (most
> przez torsję Freneta-Serreta: 0/10, ODRZUCONY — diagnoza: potrójne
> różnicowanie wzmacnia szum szybciej niż wyłapuje strukturę).

## 0. Dlaczego ten kandydat, nie inny

Po odrzuceniu torsji przeanalizowano trzy alternatywy: winding/crossing
number (zero lub minimalne różniczkowanie), homologia perzystentna
(najbardziej rygorystyczna topologicznie, ale wymaga nowej zależności —
`gudhi`/`ripser`/`persim` NIE są zainstalowane w środowisku — i nowego
wolnego parametru zakresu filtracji), oraz uogólnienie P/Q (Aksjomat
G10) na dowolne trajektorie — odrzucone na tym etapie, bo wymagałoby
NAJPIERW zbudowania nowej definicji obwiedni dla chmury punktów, czyli
osobnego projektu formalizacyjnego przed jakimkolwiek testem.

Wybrano winding+crossing number **wprost dlatego**, że atakuje
zdiagnozowaną przyczynę poprzedniej awarii: liczenie kąta obrotu wymaga
JEDNEJ różnicy (przez `atan2` względem centroidu), nie trzech (v→a→j)
jak torsja. Crossing number nie wymaga różniczkowania wcale — to czysto
kombinatoryczna własność łamanej.

## 1. Konstrukcja — część WSPÓLNA z poprzednim mostem (celowo niezmieniona)

Żeby porównanie było uczciwe (ta sama trajektoria, inna metryka, nie
nowy eksperyment od zera), **embedding jest identyczny** z
`PREREG_TREFOIL_MS_BRIDGE.md` §3.1, bez zmian:

- `lag=1`, sygnał znormalizowany `(x-mean)/std` przed embeddingiem,
  `p(t) = (x(t), x(t+lag), x(t+2*lag))`.
- Te same generatory kontroli (§4-5 tamtego dokumentu, bez zmian):
  pozytywna = `sin(w1*t) + 0.5*sin(w2*t+phi) + szum`, `w1=1.0, w2=2.7`;
  negatywna A = czysty szum; negatywna B = `sin(w1*t+phi) + szum`.
- Te same rozmiary okna `{300, 64}`, siatka szumu
  `{0.0, 0.1, 0.3, 0.5, 1.0}`, `n_windows=30`, `alpha=0.05`.

Zmienia się WYŁĄCZNIE krok „trajektoria 3D → skalar" (poprzednio:
κ/τ Freneta-Serreta → `max(|τ|)`; teraz: rzut 2D → winding/crossing).

## 2. Rzut 3D → 2D (nowy krok, zamrożony)

Metoda: **PCA** — środkuj punkty trajektorii (odejmij ich własną
średnią), policz macierz kowariancji, weź dwa wektory własne o
największych wartościach własnych (`np.linalg.eigh`, deterministyczne
dla macierzy symetrycznej), rzutuj punkty na te dwie osie.

Uzasadnienie wyboru: to jest bezparametrowa, deterministyczna odpowiedź
na pytanie „jak zdefiniować sensowną oś/płaszczyznę rzutu" — nie wymaga
zgadywania osi, nie wprowadza wolnego parametru do strojenia. Zero
różniczkowania (dekompozycja macierzy kowariancji, nie pochodne czasowe).

**Znana niejednoznaczność, jawnie zaakceptowana**: znak wektorów
własnych z `eigh` jest arbitralny (odbicie lustrzane rzutu) — obie
metryki poniżej są zdefiniowane tak, żeby być niezmiennicze względem
odbicia (`|winding|`, `crossing count` — oba nieczułe na znak/kierunek
obrotu), więc ta niejednoznaczność nie wpływa na wynik.

## 3. Metryka A — winding/turning number

Po rzucie: środkuj punkty 2D (odejmij ich średnią — daje centroid w
zerze), policz `theta_i = atan2(y_i, x_i)` dla każdego punktu,
`unwrap(theta)` (`np.unwrap`, standardowa funkcja, nie wynalazek na
potrzeby tego testu), metryka:

```
winding = |unwrap(theta)[-1] - unwrap(theta)[0]| / (2*pi)
```

**Jawnie ujawnione ryzyko numeryczne, NIE łatane progiem wymyślonym na
poczekaniu**: jeśli trajektoria przejdzie bardzo blisko centroidu
(`r≈0`), kąt `theta` jest źle uwarunkowany i `unwrap` może dać skok
niezwiązany z realnym „owinięciem". Nie wprowadzam tu progu
odległości minimalnej — taki próg wymagałby własnej kalibracji, a to
jest dokładnie rodzaj decyzji, którą trzeba by podjąć PRZED danymi, nie
mamy podstaw do jej ustalenia teraz. Zamiast zgadywać próg: to ryzyko
zostanie sprawdzone opisowo w wynikach (czy pojawiają się
ekstremalne/niestabilne wartości) i zaraportowane wprost, jeśli
wystąpi — nie ukryte.

## 4. Metryka B — crossing number

Na tym samym rzucie 2D: policz liczbę par NIESĄSIADUJĄCYCH odcinków
łamanej, które się przecinają. „Niesąsiadujące" = indeksy odcinków
różniące się o ≥2 (czyli nie dzielą wspólnego wierzchołka) — zamrożona
reguła, eliminuje fałszywe „przecięcia" w punkcie wspólnym sąsiednich
odcinków. Test przecięcia dwóch odcinków: standardowy algorytm oparty
na znaku iloczynu wektorowego (orientacja trzech punktów) — NIE
biblioteka zewnętrzna (choć `shapely` jest dostępne w środowisku),
implementacja bezpośrednia, żeby zostać w tym samym stylu co reszta
kodu geometrycznego w tym repo (numpy, bez ciężkich zależności
geometrycznych).

```
crossing = |{(i,j) : j >= i+2, odcinek_i przecina odcinek_j}|
```

Złożoność O(n²) — przy `n≤300` to ~45000 par, pomijalny koszt.

**Jawnie zaakceptowane uproszczenie**: przypadki zdegenerowane
(odcinki kolinearne/nakładające się) NIE są traktowane specjalnie —
standardowy test orientacji je pomija lub liczy niespójnie w
skrajnych przypadkach. To jest znana, zaakceptowana wada tej prostej
implementacji, nie coś do naprawienia po zobaczeniu wyniku.

## 5. Dwa równoległe testy, nie jedna metryka

`pipeline.run_controls()` przyjmuje `metric_fn` zwracającą pojedynczy
float — winding i crossing są dwoma NIEZALEŻNYMI `metric_fn`, każda
przechodzi przez CAŁĄ siatkę osobno (2 rozmiary okna × 5 poziomów
szumu × 2 metryki = 20 komórek łącznie), dokładnie jak kryteria A/B
przy estymatorze kształtu helikalnego — raportowane osobno, nie
uśrednione w jedną liczbę.

## 6. Kryteria sukcesu (niezmienione względem poprzedniego mostu)

Te same co w `PREREG_TREFOIL_MS_BRIDGE.md` §7: `ControlResult.passed`
z pipeline'u (kontrola pozytywna istotna I obie kontrole negatywne
wzajemnie nieistotne), plus raportowany rozmiar efektu
(`rank_biserial_effect_size`) dla każdej komórki.

## 7. Co pozostaje otwarte / jawnie NIE rozstrzygnięte teraz

- Czy okno=300 przy `w1=1.0` (period≈6,28 próbki → ~48 okresów w
  oknie) i okno=64 (~10 okresów) to sensowne reżimy dla winding number
  — zostawione bez zmian względem poprzedniego mostu celowo (żeby
  metryka, nie embedding, była jedyną zmienną), NIE dostrajane teraz,
  nawet jeśli po fakcie okaże się niewygodne.
- Realne dane (sejsmika/łożyska/BTC) — dopiero po tym kroku, i tylko
  jeśli wynik syntetyczny da podstawę, dokładnie jak poprzednio.

## 8. Status

Zamrożone. Następny krok: implementacja dokładnie wg powyższego,
uruchomienie na syntetyce, raport — łącznie z wynikiem negatywnym,
bez retuningu po fakcie.
