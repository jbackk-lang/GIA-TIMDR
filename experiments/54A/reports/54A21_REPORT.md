# 54A.21 — Dopasowanie długości pętli do błędu modelu

## Wykonanie
Uruchomiono lokalnie 28 wariantów: cztery deterministyczne syntetyczne strumienie po 32768 rekordów, cztery stałe długości okna (64/256/1024/4096) oraz trzy adaptacyjne (model, geometry, cost; start 256). Format rekordów: <IhhhB, 11 B. Kodek: byte shuffle + zlib1, każdy blok ma 6 B metadanych. Każdy wariant przeszedł bezstratny roundtrip.

Regulator modelowy mierzy średnią bezwzględną resztę predykcji stałej prędkości w trzech współrzędnych. Regulator geometryczny dodaje test zgodności kierunków kolejnych wektorów ruchu. Regulator cost porównuje rozmiar zlib(shuffle(bloku)) z rozmiarem bloku. Każdy regulator podejmuje decyzję wyłącznie po zakończeniu bloku, dla następnego bloku. Długość podwajana przy stabilności lub dzielona przez 2 w przeciwnym razie, zakres 64–4096.

## Wyniki (bajty)
| Dane | fixed4096 | model | geometry | cost |
|---|---:|---:|---:|---:|
| linear | 10506 | **10465** | **10465** | **10465** |
| turn | **8855** | 10159 | 10159 | 10159 |
| mixed | **122672** | 163777 | 163777 | 124041 |
| random | **232222** | 287196 | 287196 | 287196 |

Dla linear poprawa to zaledwie 41 B (0.39%) względem fixed4096. Na pozostałych trzech zbiorach fixed4096 jest najlepszy. Geometry i model podejmują identyczne decyzje i dają identyczne rozmiary; geometria dodatkowo obciąża CPU. W mieszanych danych regulator cost jest lepszy od model/geometry, ale wciąż gorszy od fixed4096.

## Interpretacja
Negatywny wynik dla badanych polityk. **To nie jest test pełnego formalnego stanu TIMDR (Lambda, tau, rho, J)**; geometry to jedynie heurystyczny test wyrównania kierunków. Czas mierzony pojedynczym przebiegiem w Pythonie, więc nie należy go uogólniać. Nie testowano danych rzeczywistych.

## Lepszy następny eksperyment
Zamiast zmieniać wyłącznie długość bloku, wybierać **model predykcji i kodek** na podstawie oszacowanego kosztu reszt predykcji na poprzednich oknach; użyć histerezy i progów opartych na liczbie bajtów. Uczciwa ablacja: bez geometrii vs geometria vs sam koszt, ze stałą wielkością bloku i osobnym testem adaptacyjnej wielkości. Testować na niezależnych danych rzeczywistych.

Kod i pełne wyniki lokalne: `54A21.py` i `54A21_RESULTS.json` (do pobrania z rozmowy). Repo zawiera zweryfikowane podsumowanie i raport.
