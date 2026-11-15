# TIMDR — dekompozycja błędów detekcji i zegara (2026-11-14)

## Pytanie
Czy trudności z odczytem relacji pomiędzy lokalnymi trójkami MIN–MAX–CZAS wynikają przede wszystkim z nieliniowego zegara, czy z wyboru fałszywych zdarzeń?

## Protokół
1000 syntetycznych przebiegów po 256 próbek. Dwa układy trzech prawdziwych zdarzeń o odstępach czasu źródłowego (30,60) i (60,30), klasy zrównoważone. Każde zdarzenie to para impulsów Gaussa (-2,+2) z opóźnieniem 8 próbek. Dodatkowo trzy fałszywe pary o amplitudzie 1.6..2.3, szum sygnału σ=.18, jeden brakujący blok 10..24 próbek. Zegar f(t)=255(t/255)^p, p=exp(U(-1.6,1.6)); 12 znaczników czasu w [5,250] z szumem σ=0,1.5,4; regresja izotoniczna + odwrotna interpolacja. Detektor ekstremów, wybór najlepiej dopasowanej trójki spośród kandydatów. Kryterium wyboru zna odstępy 30/60, zatem wynik nie stanowi dowodu uogólnienia na nieznane procesy.

Wariant *oracle*: prawdziwe czasy trzech zdarzeń podane algorytmowi (po przekształceniu zegarem), co izoluje błąd kalibracji. Wariant automatyczny: czasy estymowane przez detektor. Trafność automatyczna liczona **warunkowo** dla 912/1000 przykładów, w których detektor zwrócił co najmniej trzy kandydaty.

## Faktyczne wyniki
```
clock_noise 0 usable 912 detected_all_three_within3 410 detection_precision 0.4496
oracle_raw 1000 910 0.91
oracle_calibrated 1000 1000 1.0
detected_raw 912 605 0.6634
detected_calibrated 912 629 0.6897
clock_noise 1.5 usable 912 detected_all_three_within3 370 detection_precision 0.4057
oracle_raw 1000 910 0.91
oracle_calibrated 1000 990 0.99
detected_raw 912 581 0.6371
detected_calibrated 912 593 0.6502
clock_noise 4 usable 912 detected_all_three_within3 274 detection_precision 0.3004
oracle_raw 1000 910 0.91
oracle_calibrated 1000 969 0.969
detected_raw 912 529 0.58
detected_calibrated 912 529 0.58
```

## Wniosek
Po podaniu prawdziwych zdarzeń korekcja czasu osiąga 96.9–100% trafności, lecz po automatycznej identyfikacji zdarzeń spada do 58–69%. W tym generatorze **błędny dobór zdarzeń ogranicza system bardziej niż sam zegar**. Odsetek przebiegów z wszystkimi trzema właściwymi zdarzeniami wśród przypadków z ≥3 kandydatami wynosi 30–45%, zależnie od jakości kalibracji.

## Ograniczenia
Ocena dotyczy syntetycznego generatora i etykiety układu odstępów, nie przewidywania przyszłości. Detektor jest heurystyczny; wybór zdarzeń korzysta z wiedzy o możliwych odstępach. Wskaźnik 'detection_precision' jest dokładnością kompletnego wyboru trzech zdarzeń **wśród zaakceptowanych**, a nie standardową precision detektora. Wariant oracle używa znanych czasów zdarzeń, a więc nie jest wdrażalnym modelem. Porównania wariantów różnią się również mianownikiem (1000 vs 912), co należy uwzględnić przy interpretacji. Trójki lokalne pozostają podstawowym opisem zdarzenia; test izoluje ich identyfikację i relacje.
