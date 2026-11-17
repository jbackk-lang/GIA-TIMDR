# 54A.14 — Sterowanie kodekiem z uwzględnieniem kosztu selektorów

## Cel
Sprawdzić, czy wybór predyktora lag 1/3/64 per blok daje zysk po doliczeniu informacji sterującej. Porównać wybór przyczynowy (najlepszy model w poprzednim bloku) i oracle (najlepszy model bieżącego bloku, przekazany selektorem).

## Dane i protokół
Pięć syntetycznych strumieni po 32768 bajtów. Przełączanie lag co 256, 512 albo 1024 bajtów, z 2% zakłóceń; dodatkowo losowy i odcinkowo stały. Bloki kodowania 256/512/1024 bajtów. Błąd predykcji modulo 256, gzip level 9. Selekcje kodowane po 2 bity, osobny gzip; 20-bajtowy nagłówek dla wariantów przełączanych. Gzip i adaptacyjny: 12-bajtowy nagłówek. Wszystkie roundtripy sprawdzone. Format testowy zna długość wejścia z kontekstu; nie jest samowystarczalnym formatem produkcyjnym.

## Wyniki (bajty, wliczone nagłówki i selektory)
| Dane | gzip | adaptacyjny | przyczynowy 256/512/1024 | oracle 256/512/1024 |
|---|---:|---:|---|---|
| random | 32808 | 32808 | 32869 / 32852 / 32844 | 32868 / 32852 / 32844 |
| lag_switch_256 | 4833 | 5744 | 8730 / 6297 / 6165 | 5183 / 6233 / 6193 |
| lag_switch_512 | 3309 | 3883 | 5533 / 5951 / 4662 | 3619 / 3618 / 4828 |
| lag_switch_1024 | 2561 | 2972 | 3836 / 4081 / 4509 | 2854 / 2853 / 2853 |
| constant | 197 | 145 | 176 / 176 / 176 | 176 / 176 / 176 |

## Wniosek
Brak przewagi nad gzip dla zmiennych reżimów, nawet dla oracle. Przyczynowy selektor dodatkowo pogarsza kompresję. Dla stałych odcinków adaptacyjny predyktor osiąga 145 B wobec 197 B gzip, ale to nie jest zysk z dynamiki TIMDR. Wynik negatywny, bez poszukiwania pozytywnych przykładów post hoc.

## Ograniczenia
Syntetyczne dane, mała rodzina predyktorów, blokowe przełączanie; to nie jest formalna implementacja trzech gałęzi TIMDR. Potrzebny test na rzeczywistym korpusie i rozdzielenie zysku predykcji od entropii reszt.
