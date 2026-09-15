# Pre-rejestracja: homologia perzystentna (β₁) jako most M/S↔topologia

> Status: PRE-REJESTRACJA, zamrożona PRZED uruchomieniem (kod jeszcze
> nie napisany w chwili zapisania tego dokumentu). Data: 2026-09-15.
> Trzecia i ostatnia z trójki kandydatów rozważanych po odrzuceniu
> torsji Freneta-Serreta (`RESULT_TREFOIL_MS_BRIDGE.md`, 0/10) oraz
> winding/crossing number (`RESULT_WINDING_CROSSING_MS_BRIDGE.md`,
> 0/20).

## 0. Dlaczego to inny przypadek, nie trzecia powtórka tego samego

Diagnoza po dwóch poprzednich porażkach (patrz `RESULT_WINDING_
CROSSING_MS_BRIDGE.md`, sekcja „Diagnoza"): trzy różne metryki, trzy
różne rzędy różniczkowania (torsja=3, winding=1, crossing=0) dały ten
sam wzorzec porażki — sam embedding opóźniający tworzy z szumu
trajektorię lokalnie/globalnie „poszarpaną", która wygrywa z genuine
sygnałem w KAŻDEJ dotąd przetestowanej mierze złożoności trajektorii.

Homologia perzystentna różni się mechanizmem, nie tylko nazwą: cecha
topologiczna (tu: pętla H1) liczy się do wyniku tylko jeśli
**przetrwa (persystuje)** przez zakres skali filtracji — krótkotrwałe,
przypadkowe struktury (dokładnie to, co generuje szum w embeddingu)
mają z definicji krótką persystencję i wnoszą mało do sumy, podczas
gdy genuine, stabilna pętla (jeśli istnieje) persystuje przez szeroki
zakres skali. To jest INNY mechanizm odporności na szum niż
„policz coś i zobacz czy szum jest mniejszy" — dlatego uzasadnione jest
przetestowanie tego jako trzeciej, niezależnej próby, nie oczekiwanie
z góry tego samego wyniku.

**Uczciwe zastrzeżenie a priori**: dwie porażki z rzędu to nie dowód, że
trzecia też zawiedzie, ale też nie jest podstawą do optymizmu — dokładnie
jak poprzednio, oczekiwanie neutralne/lekko pesymistyczne, nie
entuzjastyczne.

## 1. Zależność (nowa, jawnie odnotowana)

`ripser` (biblioteka do homologii perzystentnej, filtracja
Vietorisa-Ripsa) zainstalowana w środowisku sandboxa na potrzeby tego
testu (`pip install ripser`) — NIE była wcześniej częścią stosu tego
ekosystemu. To jest nowa zależność, jawnie odnotowana, nie ukryta.

## 2. Konstrukcja obiektu — RÓŻNI SIĘ od poprzednich dwóch (bez rzutu 2D)

Embedding 1D→3D identyczny jak poprzednio (`lag=1`, sygnał znormalizowany
`(x-mean)/std`, `p(t)=(x(t),x(t+lag),x(t+2*lag))`) — reużyty bez zmian
dla porównywalności.

**Bez rzutu PCA do 2D** — w odróżnieniu od winding/crossing, homologia
perzystentna działa natywnie w dowolnym wymiarze (ripser liczy
odległości parami punktów w przestrzeni embeddingu), więc krok
projekcji jest zbędny i pominięty — jeden mniej krok przetwarzania,
jedna mniej okazja do wprowadzenia artefaktu.

Chmura punktów = wszystkie punkty embeddingu, TRAKTOWANE JAKO
NIEUPORZĄDKOWANY zbiór (kolejność czasowa NIE wchodzi do filtracji
Vietorisa-Ripsa — to jest różnica koncepcyjna względem poprzednich
dwóch metryk, które używały kolejności wprost).

## 3. Metryka — β₁ jako suma persystencji (zamrożona)

Filtracja Vietorisa-Ripsa, `maxdim=1` (liczymy H0 i H1), `thresh`
domyślny biblioteki (bez sztucznego ograniczenia promienia — zamrożone;
jeśli wydajność tego wymaga, zmiana zostanie odnotowana jako decyzja
inżynieryjna PRZED pełnym przebiegiem, analogicznie do wektoryzacji
`crossing_metric_fn` w poprzednim moście, nie jako retuning po wyniku).

Metryka skalarna (zamrożona, żeby uniknąć wprowadzania nowego,
niekalibrowanego progu birth/death):

```
metric = SUMA (death - birth) po wszystkich SKOŃCZONYCH parach H1
       = "całkowita persystencja H1"
```

Uzasadnienie wyboru sumy zamiast np. „liczby pętli powyżej progu X":
próg X byłby dokładnie tym rodzajem wolnego, niekalibrowanego
parametru, przed którym ostrzegał punkt 0 `PREREG_WINDING_CROSSING_
MS_BRIDGE.md` (sekcja 0) jako powodem odłożenia tej metody na później.
Suma persystencji jest standardową miarą w literaturze TDA (topological
data analysis), nie wynalazkiem na potrzeby tego testu, i nie wymaga
progu — naturalnie waży cechy krótkotrwałe (szum) blisko zera, a
długotrwałe (strukturalne) z pełną wagą.

`β₂` (pustki 2D) świadomie POMINIĘTE na tym etapie — wymagałoby dużo
gęstszego próbkowania niż nasze okna (64-300 punktów), żeby cokolwiek
sensownego wykryć w wymiarze 2; dodanie tego teraz zwiększałoby ryzyko
niedomocy testu bez jasnego uzasadnienia. Zostaje jawnie odłożone.

## 4. Reszta konstrukcji — bez zmian względem poprzednich dwóch mostów

Te same generatory (pozytywna = `sin(w1*t)+0,5*sin(w2*t+phi)+szum`,
`w1=1,0, w2=2,7`; negatywna A = czysty szum; negatywna B =
`sin(w1*t+phi)+szum`), te same rozmiary okna `{300, 64}`, ta sama
siatka szumu `{0,0; 0,1; 0,3; 0,5; 1,0}`, `n_windows=30`, `alpha=0,05`,
te same kryteria sukcesu z `pipeline.run_controls()`.

## 5. Co pozostaje otwarte

- Czas obliczeń nie jest znany z góry (filtracja VR na chmurach do
  n=300 w 3D) — jeśli okaże się nadmierny, dopuszczalne inżynieryjne
  decyzje (np. ograniczenie `thresh`) będą jawnie odnotowane jako
  podjęte PRZED zobaczeniem wyniku statystycznego, analogicznie do
  wcześniejszej wektoryzacji.
- Real-data — dopiero po tym kroku, tylko jeśli wynik syntetyczny da
  podstawę, jak poprzednio.

## 6. Status

Zamrożone. Następny krok: implementacja, uruchomienie na syntetyce,
uczciwy raport — łącznie z wynikiem negatywnym, bez retuningu po fakcie.
