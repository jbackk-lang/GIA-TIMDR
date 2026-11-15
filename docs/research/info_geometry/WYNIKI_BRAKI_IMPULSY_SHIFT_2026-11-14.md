# Brakujące próbki, impulsy zakłócające i zmiana kształtu — 2026-11-14

**Status:** wykonany lokalnie test syntetyczny. Kod wykonywalny w artefakcie rozmowy `robust_raw_signal.py`; wynik nie jest walidacją na danych rzeczywistych.

## Protokół

Obserwacja: 101 próbek, dwa przeciwne impulsy Gaussa, ukryty odstęp 12–32 lub 58–78. Przyszłość: 128 próbek AR(1) o α=0.2 lub α=0.8; etykieta wyznaczona z autokorelacji przyszłego fragmentu >0.5. Wykrywanie ekstremów: 7-punktowa średnia ruchoma na obserwacji po interpolacji brakujących próbek. Cechy: MIN i MAX interpolowanego przebiegu oraz |t_max−t_min|/100. Regresja logistyczna ze standaryzacją, uczona wyłącznie na 2000 sygnałów treningowych. Testy po 1000 nowych przykładów.

Trening i test zwykły: szerokość impulsów U(1.5,3.0), szum amplitudy σ=0.12, losowe braki ~5% próbek. Test przesunięcia rozkładu: szerokość U(3.0,6.0), losowe braki ~25%, liczba zakłóceń impulsowych Poisson(2), amplituda każdego zakłócenia 1..2.5. Przyszłość jest syntetyczna i nadal skorelowana z odstępem przez z góry ustalony generator.

## Wyniki uruchomienia

```text
MODE IN_DISTRIBUTION median_extrema_gap_error 0.0
FEATURES 2 accuracy 0.5 confident_accuracy None unknown 1.0
FEATURES 3 accuracy 1.0 confident_accuracy 1.0 unknown 0.0
MODE SHIFTED median_extrema_gap_error 1.0
FEATURES 2 accuracy 0.512 confident_accuracy None unknown 1.0
FEATURES 3 accuracy 0.987 confident_accuracy 0.987 unknown 0.002
```

`UNKNOWN`: heurystyka |p−0.5|<0.2. Model dwuwymiarowy nie uzyskał żadnej pewnej decyzji, stąd `None` dla trafności warunkowej, a nie 0%. W przesuniętym teście model trzycechowy odrzucił 2/1000 prognoz; trafność w pozostałych 998 wyniosła 98.7% po zaokrągleniu.

## Ograniczenia

Sygnały mają **dwa dominujące impulsy**, a reżim przyszłości jest z założenia zakodowany w odstępie. Wynik nie dowodzi, że dowolny sygnał można zredukować do MIN/MAX/CZAS bez straty informacji. Test nie obejmuje zmiennego zegara, nieregularnych znaczników czasu ani rzeczywistych pomiarów. Model nie ma formalnie skalibrowanej niepewności.

## Następny test

Wielokrotne ekstrema i zakłócenia, w których globalne MIN/MAX mogą wskazać niewłaściwe zdarzenia; osobno porównać z cechami pełnego przebiegu i sprawdzić, kiedy redukcja 3D zawodzi.
