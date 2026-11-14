# Ścisłe lokalne trójki MIN–MAX–Δt i kolejność relacyjna — 2026-11-14

## Protokół
2000 sygnałów treningowych i 1000 testowych dla przesunięć zdarzeń 0, 4, 10, 18 próbek. Sygnały po 128 próbek, szum Gaussa σ=0.12, globalne MIN=-5 przy indeksie 16 i MAX=5 przy 112. Wewnętrzne impulsy Gaussa w pozycjach 35,48 lub 68,81, przesuwane w teście. Przyszły przebieg: 128 próbek AR(1), α=0.15 albo 0.85; etykieta mierzona z przyszłej autokorelacji >0.5. Losowania numpy seed 61 (trening) i 62 (test). Regresja logistyczna ze standaryzacją trenowana wyłącznie na oryginalnym położeniu zdarzeń.

Cztery ustalone okna: [10,23), [27,56), [60,90), [102,121). Z każdego okna dokładnie trzy wartości: (MIN,MAX,(indeks_MAX−indeks_MIN)/(długość_okna−1)). Porównano: globalne 3 cechy, uporządkowane 4×3=12, te same 4 trójki posortowane według wartości (bez identyfikacji okien), 12 cech plus cztery stałe współrzędne okien, pełny przebieg 128.

**Uwaga:** stałe cztery pozycje okien są takie same dla każdej próbki i nie dodają informacji klasyfikacyjnej, lecz porządek trójek jawnie koduje tożsamość okna. Nie jest to niezależny od układu współrzędnych graf zdarzeń.

## Wyniki rzeczywistego uruchomienia
```
SHIFT 0 future-label-match 1.0
global 3 0.5
triples 12 1.0
unordered 12 0.994
triples_plus_position 16 1.0
full 128 1.0
SHIFT 4 future-label-match 1.0
global 3 0.5
triples 12 1.0
unordered 12 0.995
triples_plus_position 16 1.0
full 128 0.907
SHIFT 10 future-label-match 1.0
global 3 0.5
triples 12 1.0
unordered 12 0.496
triples_plus_position 16 1.0
full 128 0.01
SHIFT 18 future-label-match 1.0
global 3 0.5
triples 12 0.689
unordered 12 0.473
triples_plus_position 16 0.689
full 128 0.695
```

## Interpretacja
W skonstruowanej rodzinie przebiegów cztery uporządkowane lokalne trójki (12 wartości) zachowują informację niedostępną dla jednej globalnej trójki. Przy przesunięciu o 10 próbek utrata tożsamości okien powoduje spadek skuteczności do losowej. Model pełnego przebiegu wykazuje silny błąd generalizacji (1% trafności) wskutek zmian położenia impulsów; nie oznacza to, że pełny przebieg zawiera mniej informacji, lecz że użyty liniowy klasyfikator słabo uogólnia na przesunięcie.

Nie dowiedziono uniwersalnej wystarczalności lokalnych trójek. Generator świadomie łączy położenie impulsów z przyszłym reżimem; proste ustalone okna są dopasowane do jego konstrukcji. Znak Δt jest zachowany w lokalnych trójkach, ale pozycja absolutna każdego okna jest ukryta w indeksie okna, nie w samej trójce. Nie badano automatycznej segmentacji ani zegara obiektu.

## Następny test
Automatycznie wykrywać zdarzenia bez ustalonych okien; reprezentować każde przez dokładnie (MIN,MAX,Δt), a relacje między zdarzeniami przez osobne krawędzie. Sprawdzić generalizację przy translacji, nieregularnym próbkowaniu i wielu zakłóceniach.
