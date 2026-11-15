# Relacje czasowe niezależne od początku obserwacji — 2026-11-14

## Pytanie
Czy informacja o przyszłej dynamice może być zachowana w lokalnym odstępie między zdarzeniami, gdy ich absolutne położenie jest losowe i zmienia się pomiędzy treningiem a testem?

## Protokół
Sygnał obserwowany ma 128 próbek, dwa impulsy Gaussa o przeciwnych znakach, odstęp 12–20 (reżim 0) lub 35–43 (reżim 1), szum Gaussa σ=0.12. Początek pary impulsów losowany niezależnie od klasy. Dodatkowo ustawiono stałe globalne ekstrema -6 w próbce 0 i +6 w próbce 127; globalna trójka jest identyczna dla wszystkich klas. Trening 2400 przykładów z początkiem w [16,64]; test 1200 z początkiem w [5,75]; dodatkowy test 1200 z początkiem w [50,75].

Detektor otrzymuje wyłącznie surowe próbki: wygładza je średnią ruchomą pięciopunktową, pomijając dwie skrajne kotwice, i wybiera maksimum oraz minimum wygładzonego sygnału. Cechy: globalne (MIN,MAX,Δt), lokalne (MIN,MAX,podpisane Δt), lokalny odstęp bezwzględny, odstęp plus położenie środka, położenia obu ekstremów, pełny przebieg 128. Wszystkie klasyfikatory: standaryzacja + regresja logistyczna uczona tylko na treningu.

Przyszłość: osobno generowany 128-próbkowy AR(1), α=.15 albo .85, zależnie od reżimu; etykieta z empirycznej autokorelacji opóźnienia 1 >.5. W obu zbiorach etykieta z przyszłości zgadzała się z reżimem generatora w 100%. Kontrola negatywna: niezależne przemieszanie etykiet przyszłości.

## Rzeczywiste wyniki wykonania
```
test future_label_agreement 1.0 median_gap_error 0.0 gap_error_gt_5 0.0
global3 0.5
local_triplet 1.0
relational_gap 1.0
relational_plus_center 1.0
absolute_position 1.0
full128 0.8233
shifted future_label_agreement 1.0 median_gap_error 0.0 gap_error_gt_5 0.0
global3 0.5
local_triplet 1.0
relational_gap 1.0
relational_plus_center 1.0
absolute_position 1.0
full128 0.7867
negative_control_relational_gap 0.49
```

## Interpretacja
Informacja o klasie została **celowo zakodowana w odstępie** dwóch impulsów. Wynik 100% nie jest odkryciem niezależnej zależności fizycznej. Pokazuje, że przy takim generatorze lokalny odstęp jest odporny na translację zdarzeń. Lokalna trójka z podpisaną różnicą czasu już zawiera wystarczającą informację; dodatkowy graf relacyjny nie daje w tym teście zysku. Wynik pełnego przebiegu dotyczy tylko liniowej regresji logistycznej, nie teoretycznej informacji w 128 próbkach.

## Ograniczenia
Detektor wykorzystuje wiedzę o dwóch przeciwnych impulsach i pomija skrajne kotwice; liczba i znaki zdarzeń są znane. Nie ma fałszywych impulsów, silnych braków próbek ani zmiennego zegara. Nie porównano nieliniowych klasyfikatorów pełnego przebiegu. Nie wykazano uniwersalnej wystarczalności 3D.

## Następny test
Wprowadzić dodatkowe fałszywe zdarzenia, nieznaną liczbę impulsów, brakujące próbki i zegar nieliniowy. Wymagać wykrycia właściwej pary oraz raportować precyzję detektora, trafność prognozy i UNKNOWN.
