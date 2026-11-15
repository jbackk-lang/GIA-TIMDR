# MIN–MAX–Δt: czas relacyjny wobec nieznanego początku zegara

Data: 2026-11-14. **Status: uruchomiony test syntetyczny, nie dowód empiryczny TIMDR.**

## Hipoteza
Trójka `(MIN,MAX,Δt)`, gdzie `Δt=t_max−t_min`, zachowuje informację o porządku ekstremów i jest niezmiennicza względem wspólnego przesunięcia początku zegara `t→t+c`. To nie oznacza niezmienniczości względem dowolnej zmiany tempa czasu: przy nieliniowej reparametryzacji wartość `Δt` zmienia się.

## Protokół
1000 niezależnych prób na warunek; 64 próbki w oknie, `MIN=-1`, `MAX=+1`; kolejność ekstremów skorelowana z ukrytym reżimem przyszłości z prawdopodobieństwem 0.85. Przyszły fragment to 128 próbek AR(1) z `α=0.15` albo `α=0.85` zależnie od reżimu. Przyszłe próbki są generowane niezależnie warunkowo od reżimu. W kontroli negatywnej przyszły reżim jest losowany niezależnie od kolejności ekstremów. Początek zegara obserwatora losowy `U(-10000,10000)`.

Reguły predykcji ustalone przed eksperymentem (bez treningu): VALUES zawsze 0; RELATIVE_TIME przewiduje 1 dla `Δt>0`; ABSOLUTE_TIME przewiduje 1 dla `t_min+offset>0`. **Kontrola ABSOLUTE_TIME używa naiwnej reguły progu zero; nie jest to optymalnie wytrenowany model ani dowód, że absolutny czas nigdy nie pomaga.**

## Rzeczywisty wynik wykonania
```text
CORRELATED_FUTURE {'VALUES': 500, 'RELATIVE_TIME': 840, 'ABSOLUTE_TIME': 517} total 1000
NEGATIVE_CONTROL {'VALUES': 505, 'RELATIVE_TIME': 511, 'ABSOLUTE_TIME': 528} total 1000
```

Wynik 84% jest spodziewany, bo związek 85% **zaprojektowano w generatorze**. Test pokazuje odporność wybranej cechy na losowe przesunięcie początku czasu, a nie odkrycie prawidłowości przyrodniczej.

## Ważne ograniczenia
1. Trójka `MIN,MAX,Δt` traci informację o absolutnym czasie i wielu własnościach kształtu sygnału.
2. `Δt` nie jest niezmiennikiem przy zmianie tempa zegara; jego **znak** jest niezmiennikiem monotonicznej reparametryzacji.
3. W eksperymencie nie estymowano `α` z przyszłych danych; prognozowano jego ukryty reżim z wcześniejszego okna.
4. Losowy offset i arbitralny próg w kontroli ABSOLUTE_TIME nie rozstrzygają o wszystkich sposobach używania czasu absolutnego.
5. Nie badano szumu w wykrywaniu ekstremów ani prawdziwych danych.

## Następny krok
Testować nieznaną skalę zegara i nieliniową reparametryzację, porównując `Δt`, znak `Δt` i znormalizowane `Δt/T`, z estymacją niepewności ekstremów. Następnie przejść do rzeczywistych przebiegów z niezależnymi sesjami.
