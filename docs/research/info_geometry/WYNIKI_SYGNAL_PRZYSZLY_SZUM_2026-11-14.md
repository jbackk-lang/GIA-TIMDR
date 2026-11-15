# MIN–MAX–CZAS z błędem lokalizacji ekstremów i przyszłym przebiegiem — 2026-11-14

**Status:** kod wykonany lokalnie, syntetyczny eksperyment. Kod: `noisy_future_signal.py`.

## Protokół
4000 prób na poziom szumu (σ=0,2,5,10,20 jednostek okna [0,100]). Ukryty reżim naprzemiennie 0/1; odległość ekstremów 12..32 (reżim 0) albo 58..78 (reżim 1), ich kolejność losowa. Czasy ekstremów są zakłócane niezależnym szumem Gaussa i obcinane do [0,100]. Zegar obserwatora: `f(t)=100s(t/100)^p`, `s=exp(U(-1,1))`, `p=exp(U(-.8,.8))`. Prognoza opiera się na stałych progach: `|Δt|>45` albo `|Δt|/T>.45`; bez treningu.

Przyszły fragment to 128 próbek procesu AR(1) z `α=.15` lub `α=.85` zależnie od ukrytego reżimu. Cel **wyliczany z przyszłego sygnału**: `1` gdy empiryczna autokorelacja opóźnienia 1 przekracza 0.5. W tych 20 000 próbach etykieta wyliczona z przyszłości była zgodna z ukrytym reżimem w 100%; zatem choć cel jest faktycznie mierzony z przyszłego sygnału, jest tu niemal równoważny zaprojektowanemu reżimowi.

## Wyniki rzeczywistego uruchomienia
```text
0 future_matches_regime 1.0 {'BASE': 0.5, 'SIGN': 0.5002, 'RAW': 0.7758, 'NORMALIZED': 0.9805}
2 future_matches_regime 1.0 {'BASE': 0.5, 'SIGN': 0.5002, 'RAW': 0.775, 'NORMALIZED': 0.976}
5 future_matches_regime 1.0 {'BASE': 0.5, 'SIGN': 0.5018, 'RAW': 0.7665, 'NORMALIZED': 0.9557}
10 future_matches_regime 1.0 {'BASE': 0.5, 'SIGN': 0.506, 'RAW': 0.747, 'NORMALIZED': 0.8888}
20 future_matches_regime 1.0 {'BASE': 0.5, 'SIGN': 0.5098, 'RAW': 0.6843, 'NORMALIZED': 0.7602}
```

## Wniosek i ograniczenia
W tym generatorze znormalizowany odstęp czasowy zachowuje większą część zaprojektowanej informacji o przyszłym reżimie niż surowy odstęp przy zmiennym zegarze. Przewaga maleje wraz z błędem pomiaru ekstremów. Nie jest to dowód uniwersalnej przewagi `Δt/T` ani redukowalności dowolnego sygnału do trzech liczb. Próg 0.45 dobrano z wiedzą o konstrukcji danych; nie ma odłożonego zbioru treningowego do doboru progu. Nie badano wykrywania ekstremów z zaszumionej amplitudy, jedynie perturbację ich czasów. Nie badano też rzeczywistych sygnałów.

## Następny krok
Zasymulować surowy zaszumiony przebieg obserwacji, wykrywać MIN/MAX z samych próbek i estymować ich czasy; trenować progi wyłącznie na niezależnych sesjach, testować na odłożonych. Wprowadzić niepewność pomiaru i `UNKNOWN`.
