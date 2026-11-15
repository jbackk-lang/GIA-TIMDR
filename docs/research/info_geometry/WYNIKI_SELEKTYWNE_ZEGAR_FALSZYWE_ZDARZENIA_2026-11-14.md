# TIMDR — selektywna klasyfikacja relacji przy fałszywych zdarzeniach i nieliniowym zegarze

Data: 2026-11-14. **Faktycznie uruchomiony** skrypt lokalny: `selective_clock_distractors.py`. W repozytorium kod będzie wymagał osobnego zsynchronizowania; niniejszy raport jest kompletnym zapisem pomiarów.

## Cel i konstrukcja
Trzy zdarzenia MIN–MAX z odstępami źródłowymi (30,60) albo (60,30), start U(35,100). Silny nieliniowy zegar f(t)=255(t/255)^p, p=exp(U(-1.6,1.6)). Przebieg 256 próbek: trzy właściwe pary impulsów Gaussa o amplitudach -2,+2, trzy fałszywe pary o amplitudach 1.6..2.3, szum σ=.22, jeden brakujący blok 10..24 próbek, interpolowany liniowo. Automatyczny detektor ekstremów: wygładzanie 3-punktowe, minima poniżej -.85, maksimum powyżej .85 w odległości 5..11 próbek, tłumienie kandydatów bliższych niż 12 próbek. Spośród wszystkich trójek kandydatów wybierana jest minimalizująca funkcję błędu dopasowania do oczekiwanych odstępów. Zegar: 10 niezależnych znaczników czasu źródłowego w [10,245], odczyty z szumem σ=0,1.5,4; korekta przez monotoniczne wymuszenie odczytów i odwrotną interpolację. Bez korekty i po korekcie porównywane są te same reguły.

Zbiory: 1200 przykładów walidacyjnych, ziarno 710; 1800 testowych, ziarno 711, dla każdego wariantu. Dla docelowej trafności walidacyjnej 85% albo 90% wybierany jest **największy** próg akceptacji z siatki [0,100] co .5 przy minimalnym pokryciu 5%. Próg zamrożony przed testem. Klasy zrównoważone.

## Wyniki faktycznego uruchomienia
```
MARKER_NOISE 0
raw target 0.85 validation_threshold None
raw target 0.9 validation_threshold None
raw always (coverage 1.0, accuracy 0.4856, all_correct 0.4856)
calibrated target 0.85 threshold 5.0 validation (0.3908, 0.8593, 0.3358) test (0.4133, 0.8495, 0.3511)
calibrated target 0.9 threshold 2.5 validation (0.3117, 0.9091, 0.2833) test (0.3367, 0.8927, 0.3006)
calibrated always (1.0, 0.5878, 0.5878)
MARKER_NOISE 1.5
raw target 0.85 validation_threshold None
raw target 0.9 validation_threshold None
raw always (1.0, 0.4856, 0.4856)
calibrated target 0.85 threshold 2.5 validation (0.1717, 0.8592, 0.1475) test (0.1767, 0.8019, 0.1417)
calibrated target 0.9 validation_threshold None
calibrated always (1.0, 0.5733, 0.5733)
MARKER_NOISE 4
raw target 0.85 validation_threshold None
raw target 0.9 validation_threshold None
raw always (1.0, 0.4856, 0.4856)
calibrated target 0.85 validation_threshold None
calibrated target 0.9 validation_threshold None
calibrated always (1.0, 0.5428, 0.5428)
```
Krotki (coverage, accepted_accuracy, correct_fraction_all). `None` oznacza brak progu spełniającego zadany warunek na walidacji, a nie 0% trafności.

## Interpretacja
Przy silnych fałszywych zdarzeniach i nieliniowym zegarze korekcja zwiększa trafność wymuszonej odpowiedzi jedynie z ~48.6% do 54–59%. Ostrożna selekcja podnosi trafność zaakceptowanych przykładów, lecz ogranicza pokrycie. Próg dopasowany do 85% na walidacji przy szumie znaczników σ=1.5 nie osiąga tego celu w teście (80.2%). Sam wybór progu na walidacji **nie zapewnia formalnej gwarancji ryzyka selektywnego**.

## Ograniczenia
Syntetyczny generator, dopasowanie do znanych odległości 30/60, bez niezależnej przyszłości. Funkcja dopasowania i wybór najlepszego zestawu mogą mylić zdarzenia. Znaczniki są zsynchronizowane i rozmieszczone równomiernie. Progi dobierane na ograniczonym zbiorze; brak przedziałów ufności i formalnej kontroli ryzyka. Następny eksperyment: testy przy błędach dopasowania trójek, kalibracja probabilistyczna i osobna ocena pokrycia i błędu.
