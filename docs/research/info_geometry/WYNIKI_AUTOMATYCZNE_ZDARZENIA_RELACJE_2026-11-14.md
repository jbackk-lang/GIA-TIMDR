# Automatyczna detekcja zdarzeń i relacje czasowe — 2026-11-14

## Cel
Sprawdzić, czy automatycznie wykryte lokalne trójki (MIN, MAX, Δt) odzyskują informację o przyszłym sygnale bez ustalonych ręcznie okien i czy wymagają relacji do osi czasu.

## Protokół
2000 przykładów treningowych, po 1000 testowych dla przesunięć impulsów 0, 4, 10 i 18 próbek. Sygnały 128 próbek, szum Gaussa σ=.12, globalne ekstrema -5 w indeksie 16 i +5 w 112, dwa wewnętrzne impulsy Gaussa o amplitudach +1.5 i -1.5 w (35,48) lub (68,81), przesuwane podczas testu. Przyszłość: AR(1) α=.15 lub .85, 128 próbek; etykieta wyznaczona z autokorelacji przyszłego fragmentu >.5.

Ekstrakcja: lokalne maksima |x| >.7 i <3 z nie-maksymalnym tłumieniem w promieniu 5 próbek; wybór dwóch najwyższych i ich porządkowanie w czasie. Każde zdarzenie reprezentowane przez dokładnie (min, max, (t_max−t_min)/127) z pięciopunktowego otoczenia. Porównania: 6 cech dwóch trójek; + jedna krawędź odległości czasowej między zdarzeniami (7); + środek pary względem początku obserwacji (8); pełne 128 próbek. Model: regresja logistyczna ze standaryzacją, trenowana tylko na nieprzesuniętych danych.

## Rzeczywisty wynik
```text
SHIFT 0 detection_2_events 1.0
triples_only 0.508
triples_plus_gap 0.509
triples_plus_gap_and_center 1.0
full128 1.0
SHIFT 4 detection_2_events 1.0
triples_only 0.51
triples_plus_gap 0.51
triples_plus_gap_and_center 1.0
full128 0.907
SHIFT 10 detection_2_events 1.0
triples_only 0.518
triples_plus_gap 0.515
triples_plus_gap_and_center 1.0
full128 0.01
SHIFT 18 detection_2_events 1.0
triples_only 0.487
triples_plus_gap 0.487
triples_plus_gap_and_center 0.5
full128 0.695
```

## Wniosek
W tym generatorze klasa jest zakodowana przede wszystkim w **położeniu** pary impulsów, nie w ich kształcie ani wzajemnym odstępie. Lokalna trójka i odstęp między trójkami nie wystarczają; potrzebna jest relacja do osi czasu obserwacji. Dla przesunięcia +18 ta relacja nie uogólnia się. Niska trafność pełnego przebiegu przy przesunięciu +10 oznacza błąd generalizacji liniowego klasyfikatora, nie brak informacji w sygnale.

## Ograniczenia
Detektor używa progów .7 i 3 oraz z góry znanej liczby dwóch zdarzeń, mimo że okna nie są ręcznie ustalone. 'Wykryto >=2' nie jest metryką precyzji detekcji. Generator sztucznie wiąże położenie impulsów z przyszłością; nie ma tu dowodu uniwersalności TIMDR. Relacja środka do początku obserwacji nie jest niezmiennicza na translację sygnału. Kod używa sklearn/numpy.

## Następny krok
Zadanie, w którym etykieta zależy od relacji czasowych **między zdarzeniami**, a nie od ich absolutnego położenia. Losować translacje już podczas treningu, mierzyć precyzję/recall detektora i testować odporność na fałszywe zdarzenia.
