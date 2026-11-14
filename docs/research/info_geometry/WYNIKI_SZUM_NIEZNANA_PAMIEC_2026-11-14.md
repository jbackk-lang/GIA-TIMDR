# TIMDR — szum, lokalne trójki i nieznany współczynnik pamięci (2026-11-14)

Eksperyment rzeczywiście wykonany lokalnie. 3500 przykładów treningowych, 2000 testowych, 1000 resetów; seed 2026111407.

## Model
Homometryczne historie A=[0,1,4,10,12,17] i B=[0,1,8,11,13,17]. Sześć par impulsów (MIN=-0.4a, MAX=a, Δt=2), a~U(.8,1.2), długość przebiegu 128, losowe przesunięcie. Stan pamięci z[t+1]=alpha*z[t]+x[t], alpha~U(.82,.94); przyszły sygnał alpha*z[128]+N(0,.045). Szum obserwacji N(0,.1). Automatyczny detektor find_peaks(prominence=.40,distance=4) wybiera sześć maksimów i ich poprzedzające minima. Regresja StandardScaler+Ridge(alpha=10), ocena na niezależnym teście.

## Rzeczywiste wyniki
| Cechy | R² | RMSE |
|---|---:|---:|
| Globalna trójka | 0.00596 | 0.10226 |
| Moc FFT | -0.00916 | 0.10304 |
| Wykryte lokalne trójki | 0.00892 | 0.10211 |
| Odstępy zdarzeń | 0.00337 | 0.10240 |
| Lokalne trójki + odstępy | 0.01159 | 0.10197 |
| Globalna trójka + odstępy | 0.00889 | 0.10211 |
| Lokalne trójki + odstępy + znane alpha | 0.52858 | 0.07042 |
| Globalna trójka + odstępy + znane alpha | 0.52674 | 0.07056 |
| Surowy zaszumiony przebieg | 0.15000 | 0.09456 |
| Surowy przebieg + znane alpha | 0.66887 | 0.05902 |
| Rzeczywisty stan pamięci (oracle) | 0.79765 | 0.04614 |

Detektor odzyskał sześć właściwych maksimów we wszystkich przykładach testowych. Kontrola resetu: średnia przyszłego sygnału 0.00004, odchylenie 0.04602. Dla sparowanych idealnych historii o alpha=.88 i a=1: globalne trójki identyczne [-.4,1,2], maksymalna różnica mocy FFT 1.42e-14, różnica stanów 0.002664, różnica przyszłej odpowiedzi 0.002344, po resecie 0.

## Wniosek
Sama znajomość relacji czasowych nie wystarcza przy nieznanej szybkości zanikania pamięci. Dodanie znanego alpha poprawia R² z 0.012 do 0.529. Nie należy jednak interpretować wyniku Ridge jako granicy dostępnej informacji: interakcje nieliniowe alpha×odstępy nie były modelowane. Detekcja była łatwa (brak fałszywych zdarzeń); symulacja nie dowodzi nowego prawa fizyki. Kod źródłowy eksperymentu: `noisy_dynamic_triplets.py` (lokalny plik towarzyszący raportowi).

## Następny test
Porównać modele z nieliniowymi interakcjami i oszacowanym, a nie oracle, współczynnikiem alpha. Dodać fałszywe zdarzenia i brakujące próbki.