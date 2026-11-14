# Falsyfikacja uniwersalności globalnego MIN–MAX–CZAS — 2026-11-14

## Hipoteza i protokół
Czy trzy globalne cechy `(min(x), max(x), |t_max−t_min|/127)` wystarczą do predykcji dynamiki przyszłego sygnału, gdy informacja znajduje się w zdarzeniach wewnętrznych?

Wygenerowano 2000 obserwacji treningowych i 1000 testowych, każda po 128 próbek. Wspólne globalne ekstrema: `x[16]=-5`, `x[112]=5`. Dwa impulsy wewnętrzne: dla klasy 0 `x[35]=1.5`, `x[48]=-1.5`; dla klasy 1 `x[68]=1.5`, `x[81]=-1.5`. Dodano niezależny szum równomierny ±0.05 i ponownie ustawiono ekstrema globalne. W obu klasach globalna trójka jest dokładnie `(-5,5,96/127)`.

Przyszłość: niezależnie losowany 128-próbkowy AR(1) z `α=.15` albo `α=.85` warunkowo od klasy. Etykieta mierzona z autokorelacji przyszłego przebiegu >0.5. Regresja logistyczna ze standaryzacją, porównanie trzech cech, pełnych 128 próbek oraz dwóch wskazanych próbek wewnętrznych (te ostatnie są kontrolą informacyjną, a nie niezależnie wyuczonym ekstraktorem).

## Wyniki rzeczywistego uruchomienia
```text
MIN_MAX_TIME 0.5 features 3
FULL_WAVEFORM 1.0 features 128
INTERIOR_EVENT_TIME 1.0 features 2
unique_3D_features_train 1
future_label_agreement_with_generator 1.0
example_3D [[-5.0, 5.0, 0.7559055118110236], [-5.0, 5.0, 0.7559055118110236]]
```

## Wniosek
Dwie klasy mają **identyczną** globalną reprezentację MIN–MAX–CZAS, a mimo to ich przyszłe procesy są rozróżnialne z pełnej obserwacji. Żaden klasyfikator oparty wyłącznie na tej trójce nie odzyska informacji o klasie, gdy rozkłady klas są zrównoważone. To konstrukcyjny kontrprzykład dla **uniwersalnej bezstratnej reprezentacji** wszystkich sygnałów przez globalne MIN/MAX/odstęp ekstremów.

Nie obala Chronoprocesu ani ogólnej TIMDR; sugeruje konieczność zachowania struktury zdarzeń lub innego dynamicznego kodowania. Przykład jest sztucznie łatwy dla modelu pełnego przebiegu; nie należy interpretować 100% jako osiągnięcia na rzeczywistych sygnałach.

## Następne badanie
Sprawdzić kompresję relacyjną: sekwencję ekstremów, ich względne czasy i amplitudy; porównać z globalnym 3D i pełnym przebiegiem na zróżnicowanych generatorach i przy ograniczonym budżecie cech.
