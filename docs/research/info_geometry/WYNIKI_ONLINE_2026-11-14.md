# Pilot detekcji online — wyniki eksploracyjne

Data: 2026-11-14. Status: uruchomiono lokalnie skrypt `timdr_online.py` (nie jest pełną implementacją TIMDR). Nie stosowano uczenia ani kalibracji na niezależnym zbiorze.

## Model
2048 próbek AR(1), 32 okna po 64. Kalibracja bazowa: pierwsze 8 okien. Zmiana aktywna w próbkach [768,1536), tj. okna 12–23. Pięć klas: NONE, SOURCE (a=.35→.75), CHANNEL (filtr średniej dwóch próbek), RECEIVER_A i RECEIVER_B (clipping ±.6). Niezależny szum pomiarowy σ=.07 na obu torach. Ziarna 9000–9049. Wykrywanie online: dla każdego odbiornika maksimum z bezwzględnych z-score autokorelacji lag-1 i odchylenia standardowego, próg 2.5, wymagane dwa kolejne okna. Baza wyliczona z pierwszych ośmiu okien; podłoga odchylenia .06. Nie korzysta z przyszłych okien.

## Wyniki (liczba sesji z co najmniej jednym alarmem w fazie)

| Scenariusz | Aktywna zmiana / 50 | Przed zmianą / 50 | Po zmianie / 50 | Mediana opóźnienia w próbkach |
|---|---:|---:|---:|---:|
| NONE | 7 | 2 | 7 | 256 (fałszywy alarm) |
| SOURCE | 49 | 2 | 12 | 128 |
| CHANNEL | 50 | 2 | 10 | 128 |
| RECEIVER_A | 50 | 2 | 8 | 128 |
| RECEIVER_B | 50 | 2 | 8 | 128 |

Opóźnienie liczone od początku zaburzenia do końca okna, w którym wykryto pierwsze zdarzenie. Po zmianie alarm może wynikać zarówno z fluktuacji, jak i z niedoskonałego powrotu / historii filtra. To nie jest jeszcze walidacja detekcji powrotu.

## Co wynika
- Detekcja w tej symulacji jest czuła na sztucznie wprowadzone zmiany, ale ma alarmy fałszywe.
- Wspólna detekcja A/B nie rozróżnia SOURCE od CHANNEL: wynik `SHARED_UNRESOLVED` jest celowo nierozstrzygnięty.
- Algorytm nie implementuje formalnych mostów TIMDR; korzysta tylko z dynamicznie aktualizowanych wskaźników M/S.
- Dwa kolejne okna oznaczają opóźnienie wykrycia i nie mogą zostać pominięte przy raportowaniu.
- Nie wolno traktować tego jako walidacji online na danych rzeczywistych.

## Kolejne kontrole
1. Osobny zbiór kalibracyjny dla progu i wymaganego czasu podtrzymania alarmu.
2. Współczynnik fałszywych alarmów na godzinę lub na liczbę okien, a nie tylko liczba sesji.
3. Wykrywanie powrotu do normy z histerezą i okresami przejściowymi.
4. Oddzielne etykiety `A_ONLY`, `B_ONLY`, `SHARED_UNRESOLVED`, `UNKNOWN` z macierzą pomyłek.
5. Dynamiczne ścieżki M/S, K, G, META i jawne mosty, przy zachowaniu poprawnych domen operatorów.
6. Test z niewidzianymi filtrami, parametrami generatora, zegarem i poziomem szumu.

**Reprodukcja:** wykonany skrypt jest udostępniony jako osobny artefakt rozmowy `timdr_online.py`; nie został jeszcze skopiowany do repozytorium. Dane liczbowe są eksploracyjne.
