# Wspólna detekcja lokalnych trójek i kalibracja zegara — 2026-11-14

## Pytanie
Czy niezależny zegar poprawia odczyt relacji pomiędzy trzema zdarzeniami MIN–MAX także wtedy, gdy chwile zdarzeń nie są znane i trzeba je wykryć w surowym, zaszumionym sygnale?

## Generator i metoda
256 próbek. Klasa 0: odstępy źródłowe między trzema zdarzeniami [30,60], klasa 1: [60,30]. Początek losowany w [30,105]. Każde zdarzenie jest parą impulsów Gaussa: ujemny o amplitudzie -2, a 8 próbek później dodatni o amplitudzie +2; szerokość 1.7. Biały szum Gaussa o σ=.1 lub .25; niezależnie brak 3% lub 18% próbek, z interpolacją liniową. Detektor: średnia ruchoma z 3 próbek; lokalne minima poniżej -.85, maksima powyżej +.85 w odległości 5..11 próbek, tłumienie sąsiadujących kandydatów. Gdy wykryto dokładnie 3 pary, wyznaczono odstępy pomiędzy ich początkami.

Czas obserwowany f(τ)=255(τ/255)^p, p=exp(U(-w,w)); w=1.5 albo 2.5. Niezależny zegar: 8 znaczników źródłowych równomiernie w [5,250], ich odczyty f(τ)+N(0,σ_z), σ_z=0 lub 2. Regresja izotoniczna wymusza monotoniczność odczytów znaczników; odwrotność zegara szacowana interpolacją. Decyzja: klasa 0, gdy pierwszy odstęp jest krótszy od drugiego; klasa 1 w przeciwnym razie. Bez uczenia na etykietach.

## Wyniki faktycznego uruchomienia
Każdy wariant ma 3000 przebiegów, ziarno 321. `coverage` oznacza wykrycie dokładnie 3 par zdarzeń. `pair_precision` oznacza odsetek **zaakceptowanych przebiegów**, w których początki wszystkich trzech wykrytych par różnią się od prawdziwych centrów o co najwyżej 3 próbki; nie jest to klasyczna precision detektora.

```
easy uncorrected coverage 1.0 pair_precision 1.0 conditional_accuracy 0.9197 all_samples_accuracy_if_unknown_wrong 0.9197
easy corrected coverage 1.0 pair_precision 1.0 conditional_accuracy 1.0 all_samples_accuracy_if_unknown_wrong 1.0
hard_ideal uncorrected coverage 0.9907 pair_precision 1.0 conditional_accuracy 0.9236 all_samples_accuracy_if_unknown_wrong 0.915
hard_ideal corrected coverage 0.9907 pair_precision 1.0 conditional_accuracy 1.0 all_samples_accuracy_if_unknown_wrong 0.9907
hard_noisy_clock uncorrected coverage 0.9907 pair_precision 1.0 conditional_accuracy 0.9236 all_samples_accuracy_if_unknown_wrong 0.915
hard_noisy_clock corrected coverage 0.9907 pair_precision 1.0 conditional_accuracy 0.9909 all_samples_accuracy_if_unknown_wrong 0.9817
hard_extreme_clock uncorrected coverage 0.9907 pair_precision 1.0 conditional_accuracy 0.8594 all_samples_accuracy_if_unknown_wrong 0.8513
hard_extreme_clock corrected coverage 0.9907 pair_precision 1.0 conditional_accuracy 0.9216 all_samples_accuracy_if_unknown_wrong 0.913
```

## Interpretacja
Korekcja zegara poprawia identyfikację kolejności krótszego i dłuższego odstępu także po automatycznej detekcji lokalnych zdarzeń. W najtrudniejszym wariancie trafność warunkowa rośnie z 85.94% do 92.16%. Gdy detektor nie znajduje dokładnie 3 zdarzeń, model zwraca UNKNOWN; w wariantach trudnych dotyczy to 0.93% przebiegów.

## Ograniczenia
Zdarzenia są silne i mają charakterystyczny, znany wzorzec (ujemny impuls, po 8 próbkach dodatni); nie dodano fałszywych impulsów o porównywalnej amplitudzie. Braki są niezależne, a nie blokowe. Znaczniki czasu są synchronizowane z czasem źródłowym i rozłożone na znanym zakresie. Prosta interpolacja po regresji izotonicznej może dawać obciążenia, szczególnie przy skrajnych warpach. Etykieta opisuje konstrukcję odstępów, nie przewidywanie niezależnej przyszłości. Nie należy wyciągać wniosku o uniwersalnej wystarczalności trójek.

## Reprodukcja
Skrypt wykonany lokalnie: `joint_detection_clock.py` (Python, numpy, scikit-learn), w pliku wynikowym rozmowy. Następny test: silne fałszywe zdarzenia, blokowe braki próbek, ocena kalibracji niepewności i rozdzielenie błędu detekcji od błędu zegara.
