# Dynamiczna reprezentacja relacyjna wobec globalnego MIN–MAX–CZAS

Data: 2026-11-14. Eksperyment syntetyczny, uruchomiony lokalnie. Kod: `relational_sequence_test.py`.

## Projekt
2000 przykładów treningowych, 1000 testowych. Sygnał 128 próbek z szumem Gaussa σ=0.12, globalne ekstrema -5 w indeksie 16 i +5 w indeksie 112. Wewnętrzne pary impulsów Gaussa o przeciwnych znakach i szerokości 1.1 próbek w pozycjach (35,48) lub (68,81). Każda klasa ma identyczną globalną trójkę `(MIN, MAX, |t_max-t_min|/127)=(-5,5,96/127)`.

Przyszłość: niezależny szum innowacji w 128-próbkowym procesie AR(1), α=0.15 lub 0.85 zależnie od ukrytej klasy. Cel obliczony z autokorelacji przyszłego fragmentu (próg 0.5).

Porównanie: regresja logistyczna ze standaryzacją, uczona wyłącznie na treningu. Reprezentacje: globalne trzy cechy; **16 cech** z czterech z góry ustalonych okien `(10,23),(27,56),(60,90),(102,121)`, po cztery wartości `(min, max, t_min/127, t_max/127)`; oraz pełne 128 próbek.

## Wyniki wykonania
```
train/test 2000 1000 future_label_balance 0.5
global3 features 3 accuracy 0.5
relational16 features 16 accuracy 1.0
full128 features 128 accuracy 1.0
global_unique 1
```

## Interpretacja
W tej skonstruowanej rodzinie przebiegów lokalne zdarzenia odzyskują informację utraconą w globalnej trójce. Nie jest to dowód, że **dokładnie trzy współrzędne na zdarzenie** stanowią reprezentację wystarczającą: ekstraktor ma 16 wartości, a okna wybrano ze znajomością generatora. Wartości `(min,max,t_min,t_max)` są czterema cechami na okno, nie trzema; nie wolno przedstawiać tego jako potwierdzenia ścisłej hipotezy 3D. Kolejny test powinien użyć **trójek** `(min,max,Δt)` na okno oraz osobnych relacji pomiędzy oknami i porównać liczbę cech. Odrębny problem: bez ustalonych okien, przy zmianie pozycji impulsów, zdolność generalizacji może zaniknąć.

## Granice
Zadanie łatwe i skonstruowane pod lokalizację impulsów. Okna znane z góry. Nie ma testu na nieznanym generatorze, danych fizycznych ani przy silnym przesunięciu zdarzeń. Nie dowodzi ontologicznego charakteru czasu ani uniwersalnej kompresji sygnałów.
