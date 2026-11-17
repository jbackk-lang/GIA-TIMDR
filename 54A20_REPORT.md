# 54A.20 — Dynamiczne dopasowanie pętli/okna

## Faktyczny test
Uruchomiono lokalnie `python 54A20_ADAPT.py` dla 32768 rekordów (360448 B) w trzech zbiorach: stable, mixed (zmiana co 2048 rekordów), random. Porównano cztery stałe okna 64, 256, 1024, 4096 i dwa adaptacyjne (variance i timdr_proxy) zaczynające od 256. Po zakończeniu każdego bloku adaptacja wybiera długość następnego (podwaja przy stabilności, dzieli przez dwa przy niestabilności, ograniczenie 64–4096). Kodek używa byte-shuffle + zlib 1; długości bloków zapisane w strumieniu. Każda kombinacja przeszła pełny round-trip.

## Rozmiary w bajtach
| Zbiór | fixed64 | fixed256 | fixed1024 | fixed4096 | variance | timdr_proxy |
|---|---:|---:|---:|---:|---:|---:|
| stable | 101405 | 60994 | 20369 | **8907** | 10708 | 10708 |
| mixed | 209605 | 169509 | 131230 | **123195** | 142466 | 142466 |
| random | 286997 | 271537 | 240681 | **233192** | 286868 | 286868 |

## Przepustowość kompresji (MiB/s)
| Zbiór | fixed4096 | variance | timdr_proxy |
|---|---:|---:|---:|
| stable | 551.57 | 75.03 | 6.15 |
| mixed | 168.21 | 38.26 | 21.67 |
| random | 99.58 | 15.55 | 11.65 |

Wszystkie wyniki adaptacji są gorsze od fixed4096 na tych danych. Na random algorytm kurczy okna do 64 i generuje 508 bloków zamiast 8, zwiększając narzut i spowalniając kompresję. Proxy czasowo-przestrzenne liczy cechy przez pętle Pythona i jest dodatkowo wolne.

**Ważne:** `timdr_proxy` nie jest pełnym stanem TIMDR `(Lambda,tau,rho,J)` z formalnego modelu. Używa jedynie dwóch heurystycznych cech (aktywności i wyrównania zmian). Nie można wyciągać wniosków o formalnym trójwęźle TIMDR. Wynik testuje tylko tę konkretną politykę regulacji. Dodatkowo zmiana bloku w środku mieszanej sekwencji nie daje zysku, ponieważ kodek nie zmienia predyktora.

## Co dalej
54A.21: decyzje o długości bloku oparte na zmierzonym zysku kompresji na poprzednich blokach i kosztach nagłówków; histereza i limit zmian, a także osobna decyzja o wyborze kodeka. Weryfikacja na rzeczywistych danych i wielokrotne pomiary czasu. Reprodukcja: `python 54A20_ADAPT.py --records 32768 --output 54A20_RESULTS.json`.
