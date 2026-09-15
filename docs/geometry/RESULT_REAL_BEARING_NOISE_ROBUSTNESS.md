# Wynik: most M/S↔topologia/K na REALNYCH danych (łożyska CWRU) + szum syntetyczny

> Streszczenie `PREREG_REAL_BEARING_NOISE_ROBUSTNESS.md` (napisanej
> post-hoc, patrz zastrzeżenie o kolejności tam). Kod:
> `core/real_bearing_noise_robustness_bridge.py`. Siatka:
> 3 defekty × 5 metryk × 2 okna × 5 poziomów szumu = 150 komórek.
> Data: 2026-09-15. Czas wykonania: 23,7 s.

## Wynik surowy — **123/150 komórek siatki przeszło (82%)**

Diametralnie inny wynik niż seria syntetyczna (1/50 komórek, ta jedna
odrzucona jako niewiarygodna). Pełna tabela w wyjściu skryptu
(`python3 core/real_bearing_noise_robustness_bridge.py`), tu skrót po
metryce (agregacja po 3 defektach × 2 oknach × 5 sigmach = 30 komórek
na metrykę):

| metryka | przeszło | typowy kierunek `r` (pozytywna) | uwagi |
|---|---|---|---|
| `winding_number` | 30/30 | dodatni, zwykle 0,5–1,0 (duży) | brak porażek w całej siatce |
| `crossing_number` | 30/30 | dodatni, prawie zawsze ≥0,9 (duży) | najsilniejszy i najbardziej stabilny |
| `phase_winding` | 30/30 | dodatni, prawie zawsze ≥0,8 (duży) | zaskakujące — w serii syntetycznej ten sam kandydat dał 0/10 |
| `torsion_max\|τ\|` | 21/30 | UJEMNY, zwykle -0,5 do -0,9 (duży) | kierunek odwrotny niż pozostałe 4; porażki głównie przy σ=1,0 i specyficzności przy σ=0 |
| `h1_persistence` | 12/30 | niespójny (raz dodatni, raz ujemny, często pomijalny) | jedyna metryka bliska poprzedniemu wzorcowi porażki |

## Diagnoza — sprawdzona bezpośrednio na surowych danych, nie zgadnięta

Policzono kurtozę nadmiarową (excess kurtosis) surowych sygnałów przed
jakąkolwiek normalizacją/embeddingiem:

```
normal    std=0.0739  kurtoza=-0.06
ir_0021   std=0.5097  kurtoza= 4.05
or6_0021  std=0.5329  kurtoza=12.12
b_0021    std=0.1136  kurtoza= 0.55
```

**Kluczowy, uczciwy wniosek**: dla `ir_0021` i `or6_0021` (2 z 3
defektów) realny sygnał uszkodzenia ma DRASTYCZNIE wyższą kurtozę
(sygnatura impulsowości — klasyczna, dobrze znana cecha uszkodzeń
łożysk w literaturze wibrodiagnostycznej, używana od dekad jako
"kurtosis-based bearing fault detection") niż sygnał zdrowy. Metryki
`metric_fn` w tym repo normalizują `(x-mean)/std` PRZED liczeniem, więc
różnica SKALI amplitudy jest usunięta — ale różnica KSZTAŁTU rozkładu
(impulsowość, grube ogony) NIE jest usuwana przez samą normalizację
odchylenia standardowego, i bardzo prawdopodobnie właśnie to, nie
jakaś specyficznie "topologiczna" struktura, napędza silną separację
dla `ir_0021`/`or6_0021`.

**`b_0021` (defekt kulki) jest bardziej interesującym przypadkiem**:
kurtoza (0,55) jest BLISKA zdrowemu sygnałowi (-0,06) — a mimo to
`winding_number`/`crossing_number`/`phase_winding` nadal dają niemal
pełną separację (r≥0,94 w większości komórek). Tu prosta hipoteza
"metryka mierzy tylko impulsowość/kurtozę" NIE wystarcza jako
wyjaśnienie — defekt kulki tworzy inny rodzaj modulacji okresowej
(mniej impulsowej, bardziej ciągłej), a metryki wciąż go odróżniają.
To jest najsilniejszy kandydat spośród trzech na "coś więcej niż
kurtoza", ale NIE zostało to zweryfikowane niezależną metryką kontrolną
(np. bezpośrednim testem samej kurtozy przez `run_controls` na tych
samych oknach) — patrz "Otwarte" niżej.

## Torsja: kierunek ODWRÓCONY względem pozostałych czterech metryk

`torsion_max|τ|` jest jedyną metryką z UJEMNYM `r` (defekt ma NIŻSZĄ
torsję niż zdrowe tło) we wszystkich trzech defektach — dokładnie
odwrotny kierunek niż `winding`/`crossing`/`phase_winding`. Dodatkowo
przy `window=64, σ=0,0` torsja dała FAŁSZYWY ALARM na kontroli
negatywnej (dwa okna TEGO SAMEGO zdrowego nagrania, `neg_p=0,00093`,
`neg_r=-0,498`) dla wszystkich trzech przebiegów (bo `neg_a`/`neg_b` nie
zależą od defektu) — powtórka wzorca niskiej specyficzności torsji
znanego już z serii syntetycznej (`RESULT_TREFOIL_MS_BRIDGE.md`,
0/10). Nie ma powodu ufać kierunkowi ani stabilności tej konkretnej
metryki na tych danych.

## Odporność na szum — jakościowo INNA niż w serii syntetycznej

W serii syntetycznej efekt (tam, gdzie w ogóle się pojawiał) był
niestabilny i znikał/odwracał się już przy niskim σ. Tutaj
`winding`/`crossing`/`phase_winding` **utrzymują duży efekt aż do
σ=1,0** (szum o odchyleniu standardowym równym całemu std realnego
okna) dla wszystkich trzech defektów — realny sygnał defektu okazuje
się odporny na syntetyczny szum o mocy porównywalnej z jego własną
zmiennością. To jest **jakościowo inna, silniejsza odpowiedź** niż w
serii syntetycznej — zgodnie z pytaniem użytkownika: sygnały NIE
"dublują się" w szumie w tym zakresie σ, przynajmniej dla tych trzech
metryk i tego zakresu szumu.

## Ograniczenia — jawnie, nie pominięte

1. **n=1 nagranie na klasę.** Mamy dokładnie jedno realne nagranie
   zdrowe i po jednym na typ defektu. Test specyficzności (`neg_a` vs
   `neg_b`) sprawdza tylko powtarzalność WEWNĄTRZ jednego nagrania
   (różne okna/szumy), NIE generalizację między różnymi fizycznymi
   łożyskami/nagraniami tej samej klasy — których nie mamy. Wynik może
   nie uogólniać się na inne egzemplarze łożysk.
2. **Kurtoza jako konfundator**, opisana wyżej — dla 2 z 3 defektów
   silna separacja jest prawdopodobnie w dużej mierze (może głównie)
   efektem impulsowości sygnału, nie czegoś specyficznie
   "topologicznego"; nie rozdzielono tych dwóch wyjaśnień ilościowo w
   tym przebiegu.
3. **Brak ilościowej prognozy a priori** (w odróżnieniu od mostu OAM,
   gdzie `47,75` było przewidziane przed uruchomieniem) — sam kierunek
   "duży efekt" był tylko jakościowo oczekiwany po fakcie zbudowania
   generatora, nie ilościowo prognozowany przed.
4. **Dokumentacja post-hoc** — patrz zastrzeżenie na górze
   `PREREG_REAL_BEARING_NOISE_ROBUSTNESS.md`: brak dowodu w historii
   git, że definicje nie zostały dostrojone po zobaczeniu wyniku (poza
   moim słowem, że nie zostały).
5. **150 porównań bez korekty Bonferroniego** — podobnie jak
   poprzednie pięć mostów, ten wynik jest raportowany surowo (bez
   korekty za wielokrotność), zgodnie z konwencją tego repo dla
   przebiegów eksploracyjnych na pełnej siatce, ale warto to mieć na
   uwadze przy porównywaniu z pojedynczym, z góry ustalonym testem.

## Kontrola dodatkowa (zrobiona, nie pozostawiona jako "otwarte"): kurtoza okna jako `metric_fn`

Żeby nie zostawić hipotezy "to tylko kurtoza" jako spekulacji,
policzono SAMĄ kurtozę nadmiarową okna (`scipy.stats.kurtosis`, bez
żadnego embeddingu/fazy) jako `metric_fn`, przepuszczoną przez TĘ SAMĄ
siatkę `run_controls()` (3 defekty × 2 okna × 5 sigm = 30 komórek —
bez `h1_persistence`/`torsion` itd., to jest jedna dodatkowa metryka
kontrolna, nie część zamrożonej piątki).

**Wynik: 22/30 (73%)** — kurtoza SAMA W SOBIE jest realnym,
statystycznie wykrywalnym predyktorem (r zwykle 0,4–0,9, duży/średni),
ale **wyraźnie słabszym i mniej odpornym na szum** niż
`winding`/`crossing`/`phase_winding` (które dały 30/30 z r prawie
zawsze ≥0,8, nawet przy σ=1,0):

- Kurtoza traci istotność przy σ=1,0 dla `ir_0021` i `b_0021` (spada
  do r=0,25/0,13, "mały"); `winding`/`crossing`/`phase_winding`
  utrzymują r≥0,68 na tym samym poziomie szumu dla wszystkich trzech
  defektów.
- Przy σ=0,3 kurtoza ma powtarzalną, ciekawą porażkę specyficzności
  (neg_p<0,05) we WSZYSTKICH trzech defektach jednocześnie —
  prawdopodobnie artefakt konkretnego zestawu seedów przy tym
  poziomie szumu, niezbadany głębiej tutaj.
- **Sprostowanie własnej wcześniejszej hipotezy**: globalna kurtoza
  (na całym nagraniu 1536 próbek) dla `b_0021` była bliska normalnej
  (0,55 vs -0,06), co sugerowało, że wynik `b_0021` NIE da się
  wyjaśnić kurtozą. To okazało się nieprecyzyjne: kurtoza LOKALNA
  (liczona na oknach 32/64 próbek, tak jak faktycznie używana w
  generatorze) DALEJ niesie realny, istotny sygnał dla `b_0021`
  (r=0,13–0,74) — słabszy niż globalna wartość sugerowała, ale
  niezerowy. Właściwy wniosek nie jest "kurtoza nie wyjaśnia
  b_0021", tylko "kurtoza częściowo wyjaśnia b_0021, ale
  `winding`/`crossing`/`phase_winding` niosą wyraźnie WIĘCEJ
  informacji niż sama kurtoza, i to zarówno dla b_0021 (r≈0,94-1,0
  vs kurtoza r≈0,13-0,74), jak i dla pozostałych dwóch defektów".

**Zaktualizowany, ostateczny wniosek**: `winding`/`crossing`/
`phase_winding` NIE są prostym przemalowaniem kurtozy — niosą wyraźnie
więcej i bardziej odporny na szum sygnał niż sam czwarty moment
statystyczny, dla wszystkich trzech typów defektu, nie tylko dla
`b_0021`. To nie dowodzi, że mierzą coś specyficznie "topologicznego"
w sensie TIMDR (mogą równie dobrze mierzyć jakąś inną, nie-kurtozową
cechę kształtu falowego związaną z okresową modulacją defektu — np.
autokorelację/widmo, dobrze znane w klasycznej wibrodiagnostyce) — ale
odrzuca najprostszą, najbardziej redukcyjną hipotezę alternatywną.

## Otwarte, NIE zrobione teraz

- Porównanie z jeszcze prostszymi/klasycznymi cechami wibrodiagnostyki
  (RMS w paśmie, widmo obwiedni/envelope spectrum, crest factor) —
  żeby sprawdzić, czy `winding`/`crossing`/`phase_winding` przewyższają
  też te standardowe narzędzia branżowe, nie tylko gołą kurtozę.
- Powtórzenie na innych plikach CWRU (inne obroty, inne rozmiary
  defektu, inne konfiguracje) do sprawdzenia generalizacji ponad n=1
  nagranie na klasę.
- Wymagałoby to własnej, nowej pre-rejestracji (tym razem — jeśli
  użytkownik zechce — w standardowej kolejności freeze→run).
