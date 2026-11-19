# RESULTS 022 — Audyt IAAFT i jakości dopasowania kontroli

2026-11-19. Rzeczywiste 16 nagrań CWRU, 50 okien po 2048 próbek, 80 zdarzeń i 80 kontroli, predykcja RMS w następnym oknie; leave-one-recording-out. 12 niezależnych zestawów sygnałów IAAFT, po 12 iteracji (seed 20261120). Dokładny rozkład amplitud, przybliżone widmo.

| Metryka | Wynik |
|---|---:|
| AUROC oryginału | 0.6375 |
| Średnie AUROC 12 surogatów | 0.531875 |
| Zakres 2.5–97.5% surogatów | 0.4453–0.5750 |
| Jednostronne Monte Carlo p | 1/13 = 0.0769 |
| Mediana różnicy log RMS par oryginalnych | 0.004784 |
| Średnia median różnicy log RMS par surogatów | 0.019057 |
| Mediana względnego błędu L2 modułu FFT surogatów | 0.006677 |
| Maks. względny błąd L2 modułu FFT | 0.084138 |

Surogaty: AUROC 0.5025, 0.5750, 0.5750, 0.5650, 0.5500, 0.5375, 0.5475, 0.4725, 0.5200, 0.5700, 0.4350, 0.5325.

**Wniosek:** oryginał przewyższa wszystkie 12 surogatów, ale p=0.0769 nie jest rozstrzygające. Co ważniejsze, dopasowanie par po RMS jest ok. cztery razy gorsze w surogatach. To możliwy konfunder: porównanie nie izoluje nieznanej pamięci. Widmo zachowane dobrze w medianie, lecz maksymalny błąd 8.4% wskazuje na potrzebę dalszej diagnostyki zbieżności. Globalny IAAFT usuwa również znane impulsy i niestacjonarność.

**Nie potwierdzono nowego mechanizmu ani przewagi CHF.** Następny test: identyczna jakość dopasowania par w oryginałach i surogatach, lokalnie stacjonarne kontrole, więcej replikacji i niezależny zbiór.

Kod wykonywalny i JSON z faktycznego uruchomienia udostępniono w rozmowie jako `chf_stage_022.py` i `CHF_AFTER_EVENT_022.json`.
