# GIA-TIMDR

GIA-TIMDR gromadzi formalizmy, kod i eksperymenty dotyczące zmiany sygnału. Obejmuje cztery odrębne gałęzie: **M/S** (sygnał), **G** (geometria), **K** (modalność) i **META-DYNAMICS** (agregat Λ–τ–ρ–J). Chronoproces daje trzem pierwszym wspólny nośnik czasu, ale nie utożsamia ich operatorów. Projekt zawiera również starszą warstwę koncepcyjną TRM; nie należy jej traktować jako potwierdzonej teorii fizycznej.

## Zacznij tutaj

- [Mapa repozytorium](REPOZYTORIUM.md) — gdzie znajduje się kod, dokumentacja, prerejestracje i wyniki.
- [Pełne podsumowanie całego ekosystemu na 23 września 2026 r.](PODSUMOWANIE_PROJEKTU_2026-09-23.md) — formalizmy, mosty, wyniki z domen aplikacyjnych, porażki i granice dowodów.
- [Specyfikacja czterech gałęzi](docs/theory/TIMDR_Branch_Specification.md) i [słownik](docs/GLOSSARY_EN_PL.md) — właściwe definicje oraz granice między obiektami.
- [Reguła kalibracji, zamrożenia i testu końcowego](docs/theory/TIMDR_CALIBRATION_FREEZE_RULE.md) — rozwój na train/calibration jest dopuszczony, tuning do wyniku holdoutu nie.
- [Pełny katalog ekosystemu](https://github.com/jbackk-lang/jbackk-lang.github.io/blob/main/KATEGORIE.md) — lista repozytoriów aplikacyjnych i koncepcyjnych; poniżej wymieniono tylko najbliższe temu repo.
- [Historia dawnego README](HISTORIA_README.md) — pełny, zachowany opis koncepcyjny i kronika wcześniejszych prac. Nie jest aktualnym skrótem statusów.

## Formalizmy i kod

| Część | Główne miejsce | Zakres |
|---|---|---|
| M/S | [TIMDR-Math-Formalism](TIMDR-Math-Formalism/) | Operatory sygnałowe i protokół testowania |
| G | [TIMDR-Geometry-Formalism](TIMDR-Geometry-Formalism/) | Krzywizna i dyskretny operator Weingartena |
| K | [TIMDR-Modal-Formalism](TIMDR-Modal-Formalism/) | Częstotliwość, faza, modalność |
| Chronoproces | [TIMDR-Time-Formalism](TIMDR-Time-Formalism/) | Wspólny czas i jawnie ograniczony most Fouriera |
| META-DYNAMICS | [Aksjomaty META-1–META-9](docs/theory/Axioms_META_TIMDR.md), [kod źródłowy](https://github.com/jbackk-lang/TIMDR-META-DYNAMICS) | Wektor stanu Λ–τ–ρ–J i operator ewolucji; implementacje domenowe żyją także w innych repozytoriach |

Cztery katalogi `TIMDR-*-Formalism` zostały włączone przez `git subtree` z zachowaniem historii. Katalog [MAGE-IN-IMAGE-DECODER](MAGE-IN-IMAGE-DECODER/) jest jedynie kopią trzech modułów aplikacyjnych; pełne testy, dane i wyniki tego projektu są w jego własnym repozytorium.

## Jak interpretować wyniki

Test syntetyczny pokazuje, czy implementacja realizuje definicję. Nie dowodzi przydatności na realnych danych. Wynik realnego testu dotyczy konkretnej domeny, danych, wersji operatora i zamrożonych kryteriów. **SUPPORTED**, **NOT SUPPORTED** i **INCONCLUSIVE** są odrębnymi werdyktami; efekt o przeciwnym znaku nie staje się potwierdzeniem po zmianie hipotezy.

Na łożyskach CWRU część mostów dała mocny sygnał diagnostyczny, ale nie uogólniła się w ten sam sposób na sejsmikę i BTC. Wielokanałowa chronomembrana wykazała częściową replikację na nowych obrotach i typach uszkodzeń, nie pełne przejście wszystkich kryteriów. B4-Kitchen ma wynik ograniczony do jednego uczestnika; B4-Bearing bez zsynchronizowanej geometrii pozostaje nierozstrzygnięty. Szczegóły i dokładne liczby są w [datowanym podsumowaniu](PODSUMOWANIE_PROJEKTU_2026-09-23.md) oraz odpowiednich parach `PREREG_*` / `RESULT_*` w [docs/geometry](docs/geometry/).

W osobnym projekcie aplikacyjnym [TIMDR-fusion-tools](https://github.com/jbackk-lang/TIMDR-fusion-tools) klasyfikator czasu zaniku prądu `is_fast_quench()` poprawnie rozpoznał 19/19 nowych strzałów tokamaka TCABR. Metryka portretu fazowego `phasespace_funnel_ratio()` osiągnęła na tych samych danych czułość 12/14 i swoistość 5/5. To konkretne wyniki dla TCABR, nie walidacja wszystkich gałęzi TIMDR ani dowód skuteczności na innym tokamaku: próby MAST bez etykiet pozwoliły opisać rozkład sygnału, lecz nie ocenić trafności klasyfikacji. Lej fazowy z fusion-tools był inspiracją dla późniejszych konstrukcji chronogeometrycznych, ale nie jest tym samym operatorem.

## Powiązane zastosowania

To osobne projekty, nie kolejne gałęzie formalne. Ich wyniki, dane i ograniczenia opisują ich własne repozytoria:

| Projekt | Rola i obecna granica |
|---|---|
| [synoptyk-v2.0](https://github.com/jbackk-lang/synoptyk-v2.0) | Korekta prognozy Open-Meteo, filtr falkowy i lokalny bias; nie tworzy własnego modelu pogody |
| [SYNOPTYK-ARCTIC](https://github.com/jbackk-lang/SYNOPTYK-ARCTIC) | Stacje polarne, backtest i pomiar bias/MAE; test proxy „rezonansu” nie miał jeszcze dostatecznej liczby zdarzeń |
| [Synoptyk-v3](https://github.com/jbackk-lang/Synoptyk-v3) | Pogoda jako pole przestrzenne z wektorami wiatru; wstępny pomiar bias/MAE opiera się na krótkim oknie i małej próbie |
| [TIMDR-fusion-tools](https://github.com/jbackk-lang/TIMDR-fusion-tools) | Diagnostyka sygnałów tokamaka; wyniki TCABR opisane wyżej, transfer klasyfikatora na MAST niezweryfikowany etykietami |
| [TIMDR-Industrial-Predict](https://github.com/jbackk-lang/TIMDR-Industrial-Predict) | Sygnały maszyn i demo łożysk CWRU; nie zastępuje pomiaru geometrii wymaganego przez B4-Bearing |
| [TIMDR-Grid-Monitor](https://github.com/jbackk-lang/TIMDR-Grid-Monitor) | Monitoring sygnałów sieci energetycznej i przykłady PROTECT-90 |
| [TIMDR-Earthquake-Core](https://github.com/jbackk-lang/TIMDR-Earthquake-Core) | Analiza sejsmiczna; wyniki pozytywne i negatywne dokumentowane w repo domenowym |
| [MAGE-IN-IMAGE-DECODER](https://github.com/jbackk-lang/MAGE-IN-IMAGE-DECODER) | Obraz i wideo; trzy moduły skopiowano tu pomocniczo, pełny projekt pozostaje osobno |
| [TIMDR-AI-Core](https://github.com/jbackk-lang/TIMDR-AI-Core) | Protokół epistemiczny i eksperymenty aktywacji; linia HARTH zamknięta bez przyrostu nad baseline'em w badanym ustawieniu |

Pełniejszy spis, także projektów koncepcyjnych, jest w [katalogu ekosystemu](https://github.com/jbackk-lang/jbackk-lang.github.io/blob/main/KATEGORIE.md). Tabela nie rości sobie prawa do wyliczenia wszystkich repozytoriów.

Kod i dokumentacja są materiałem badawczym, nie certyfikowanym narzędziem diagnostycznym. Każda deklaracja przewagi wymaga niezależnych danych i porównania z metodami bazowymi.

## Cytowanie i licencja

Wersjonowane prace autora są dostępne pod DOI: [gałąź sygnałowa](https://doi.org/10.5281/zenodo.22288541), [przegląd ekosystemu](https://doi.org/10.5281/zenodo.22788266), [widmo Laplasjanu na wstędze Möbiusa](https://doi.org/10.5281/zenodo.22812269). Zakres każdego wydania jest różny. Warunki korzystania z kodu określa [LICENSE](LICENSE).
