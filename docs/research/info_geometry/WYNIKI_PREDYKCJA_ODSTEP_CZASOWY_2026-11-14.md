# Predykcyjna wartość odstępu czasowego — 2026-11-14

**Status:** kod rzeczywiście uruchomiony lokalnie, eksperyment syntetyczny. Nie jest to walidacja TIMDR ani test na rzeczywistych sygnałach.

## Pytanie
Czy odporna na monotoniczne reparametryzacje cecha `sgn(Δt)` jest równie użyteczna predykcyjnie jak odstęp `Δt` i odstęp względny `Δt/T`?

## Protokół
Dla każdego wariantu zegara 2000 prób, ziarno ustalone. Przyszły **reżim docelowy** 0/1 jest przypisany do krótkiego (12..32 jednostek) albo długiego (58..78) odstępu między ekstremami; kolejność ekstremów losowa. Nie symulowano tu przyszłego przebiegu AR — oceniano przewidywanie etykiety przyszłego reżimu. Kontrola negatywna losuje przyszły reżim niezależnie od odstępu. `MIN=-1` i `MAX=1` są stałe i nie wpływają na regułę.

Zegary: identity `f(t)=t`; affine `f(t)=c+s t`; nonlinear `f(t)=c+100s(t/100)^p`, `s=exp(U(-1,1))`, `p=exp(U(-0.8,0.8))`, `c~U(-1000,1000)`. Czas pierwotny `t∈[0,100]`. Reguły bez treningu: SIGN przewiduje 1 dla dodatniej delty, RAW_DELTA dla `|Δt|>45`, NORMALIZED_DELTA dla `|Δt|/T>0.45`. Progi ustalono zgodnie z generatorem, dlatego test jest ilustracją niezmienniczości, nie oceną uczenia.

## Wynik rzeczywistego wykonania
```text
identity signal {'SIGN': 0.4995, 'RAW_DELTA': 1.0, 'NORMALIZED_DELTA': 1.0} negative {'SIGN': 0.5215, 'RAW_DELTA': 0.5115, 'NORMALIZED_DELTA': 0.5115}
affine signal {'SIGN': 0.5195, 'RAW_DELTA': 0.7775, 'NORMALIZED_DELTA': 1.0} negative {'SIGN': 0.5115, 'RAW_DELTA': 0.488, 'NORMALIZED_DELTA': 0.483}
nonlinear signal {'SIGN': 0.498, 'RAW_DELTA': 0.7645, 'NORMALIZED_DELTA': 0.985} negative {'SIGN': 0.5045, 'RAW_DELTA': 0.4965, 'NORMALIZED_DELTA': 0.4895}
```

## Interpretacja
Znak odstępu jest niezmienniczy na monotoniczne zmiany czasu, lecz traci informację o długości odstępu. Odstęp surowy jest podatny na skalowanie. Odstęp względny zachowuje informację o długości i jest niezmienniczy na dodatnie transformacje afiniczne. Przy badanych umiarkowanych nieliniowych transformacjach działał bardzo dobrze, ale **nie jest ogólnie niezmienniczy**; 98.5% zależy od zakresu losowanych deformacji i separacji klas.

W kontroli negatywnej wszystkie trzy cechy osiągały wyniki bliskie losowym.

## Granice
Nie badano szumu lokalizacji ekstremów, nieznanej długości okna, różnych zegarów dla zdarzeń, danych rzeczywistych ani prognozy pełnego przebiegu. Nie należy wyciągać wniosku, że `Δt/T` zawsze przewyższa inne kodowania czasu.

## Następny krok
Zasymulować przyszły przebieg niezależnie warunkowo od ukrytej dynamiki, dodać szum detekcji ekstremów i nieliniowe warp o dużej amplitudzie; porównać metryki na odłożonych sesjach. Rozważyć jawny pomiar `Δτ/Δt` dla dwóch zegarów.
