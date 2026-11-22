# 54A.10 — Wieloskalowy predyktor przyczynowy

## Hipoteza
Czy wykorzystanie błędów predykcji z trzech skal historii (16, 64, 256 próbek) poprawia kompresję względem zwykłej adaptacji?

## Protokół
Pięć syntetycznych deterministycznych zbiorów po 32768 bajtów. Predyktory: opóźnienia 1, 3 i 64. Wariant adaptacyjny wybiera najniższy wygładzany błąd. Wariant wieloskalowy wybiera minimum ważonego błędu na oknach 16, 64 i 256. Reszty modulo 256, gzip poziom 9 na całym strumieniu. Dekoder powtarza wybór predyktora wyłącznie z historii zdekodowanych bajtów. Round-trip sprawdzony dla wszystkich wariantów. Bez kosztu nagłówka kodeka.

## Wyniki (bajty)
| Dane | gzip | statyczna | adaptacyjna | wieloskalowa |
|---|---:|---:|---:|---:|
| random | 32796 | 32796 | 32796 | 32796 |
| periodic | 376 | 249 | 172 | 172 |
| drift | 914 | 195 | 167 | 167 |
| regime | 1356 | 1976 | 318 | 318 |
| mixed | 1696 | 299 | 265 | 265 |

## Interpretacja
Wieloskalowość nie poprawiła wyniku na żadnym zbiorze; wszędzie remis z adaptacją. Na danych ustrukturyzowanych obie predykcje pokonały gzip, ale nie dowodzi to przewagi TIMDR. Trzy skale czasowe nie są trzema formalnymi gałęziami TIMDR. Eksperyment nie implementuje Chronoprocesu Ξ=(T,x,Γ,φ) ani dynamiki META.

## Reprodukcja
`python 54A10_MULTISCALE.py` — wyłącznie standardowa biblioteka Pythona.
