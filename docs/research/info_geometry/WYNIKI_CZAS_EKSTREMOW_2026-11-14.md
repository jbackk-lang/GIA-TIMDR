# Eksperyment: czy czas ekstremów niesie dodatkową informację?

**2026-11-14. Status: uruchomiony lokalnie test syntetyczny, standard library Python.**

## Konstrukcja

64 próbki na przebieg; tło losowe w [-0.6,0.6], dwa skrajne zdarzenia o amplitudach -1 i +1, ich pozycje wybrane losowo z wnętrza okna. Klasy: MAX_FIRST i MIN_FIRST. Dla każdego ziarna oba przebiegi mają dokładnie te same wartości minimum (-1), maksimum (+1) i czas końca okna (63), lecz odwróconą kolejność zdarzeń. Podział po ziarnach: trening 1000–1099, test 9000–9049; 100 przypadków testowych. Klasyfikator: najbliższy centroid euklidesowy na wybranych cechach.

## Wyniki uruchomienia

```text
representation,correct,total,accuracy
VALUES,50,100,0.500
EVENT_TIME,100,100,1.000
RELATIVE_TIME,100,100,1.000
```

- `VALUES=(min,max,t_end)`
- `EVENT_TIME=(min,max,t_min,t_max,t_end)`
- `RELATIVE_TIME=(min,max,t_max-t_min,t_end)`

Asercje potwierdzają identyczność reprezentacji VALUES dla sparowanych przebiegów oraz różnicę RELATIVE_TIME.

## Interpretacja i ograniczenia

To **konstrukcyjny kontrprzykład** dla tezy, że MIN/MAX/czas końca zachowują wszelką informację o kolejności zdarzeń. Wynik 100% jest oczekiwany, ponieważ etykietę zdefiniowano przez znak `t_max-t_min`; nie jest niezależnym dowodem na wartość czasu dla zewnętrznego zadania predykcyjnego ani potwierdzeniem TIMDR. Ponadto `EVENT_TIME` ma pięć liczb, a `RELATIVE_TIME` cztery, nie trzy. Jeśli wynik ma mieć dokładnie trzy cechy, należy zdefiniować, co dokładnie koduje współrzędna `czas`; pojedynczy czas końca okna nie zachowuje kolejności ekstremów.

**Kolejny uczciwy test:** etykieta niezdefiniowana przez czas ekstremów, lecz np. niezależny przyszły stan; sprawdzić, czy historia ekstremów zwiększa skuteczność prognozy. Testować zmienny zegar, zakłócenia, równoległych odbiorników i nieznaną kategorię sygnału.

Kod: `extrema_time_test.py`. Uruchomiono w lokalnym środowisku Python; wyniki powyżej są rzeczywistym wyjściem programu.
