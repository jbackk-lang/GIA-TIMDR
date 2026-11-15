# TIMDR — homometryczne historie i liniowa pamięć dynamiczna (2026-11-14)

## Hipoteza
Różne relacje czasowe zdarzeń o jednakowym globalnym widmie i globalnej trójce mogą prowadzić do różnych przyszłych odpowiedzi układu dynamicznego, jeżeli układ zachowuje pamięć historii.

## Model i protokół
Dwa homometryczne układy impulsów A=[0,1,4,10,12,17], B=[0,1,8,11,13,17]. Długość sygnału 96, zdarzenia od indeksu 78, amplituda wspólna dla impulsów w danej próbie U(.8,1.2). Stan pamięci z[t+1]=.88*z[t]+x[t], z[0]=0. Przyszłość przez 16 próbek: y[k]=(.88**k)*z[96]+epsilon, epsilon~N(0,.05), k=1..16. Osobne 4000 trening, 2000 test i 2000 reset. Przewidujemy pierwszą przyszłą próbkę metodą Ridge(alpha=1), bez doboru hiperparametrów.

## Wyniki faktycznego uruchomienia
R² na 2000 testach:
- globalna trójka MIN MAX podpisana Δt: 0.811716
- FFT moc: 0.809874
- odstępy zdarzeń: 0.179710
- globalna trójka + odstępy: 0.968789
- FFT moc + odstępy: 0.967001
- surowy przebieg: 0.970703
- prawdziwy stan z: 0.970693

Dokładna homometria przy jednakowych amplitudach: maksymalna różnica widm mocy 1.776e-14. Obie globalne trójki przykładowe [0,1,78]. Odstępy A=[1,3,6,2,5], B=[1,7,3,2,4].

Średni stan na teście: A=2.359055, B=2.631701. Średnia pierwsza próbka przyszłości: A=2.074439, B=2.314791. Dla sparowanych sygnałów o jednostkowej amplitudzie: z_A=2.369351674, z_B=2.623731373, różnica przyszłej próbki 0.223854135. Po interwencyjnym ustawieniu z=0 w obu przypadkach różnica wynosi dokładnie 0. W oddzielnym zbiorze resetu średnie pierwsze próbki: A=-0.000931, B=0.002775 (szum).

## Interpretacja
Przyszłość nie jest zaprogramowana z etykiety: wynika z równania pamięci liniowej. Informacja o kolejności lokalnych zdarzeń pozwala odzyskać różnicę w stanie z, której nie identyfikują globalne trójki i globalne widmo. Sam wektor odstępów nie zawiera informacji o amplitudzie, dlatego jego R² jest niski. Połączenie trójki z relacjami odzyskuje niemal całą informację istotną dla tej odpowiedzi.

## Ograniczenia i falsyfikacja
To symulacja liniowego filtru z pamięcią, nie pomiar fizyczny i nie dowód, że informacja jest niezależną siłą. Znana stała zaniku .88; czyste impulsy bez szumu wejściowego, detektor zdarzeń ma dane idealne. Zmiana kolejności impulsów przy stałym z[96] nie może zmienić przyszłości tego Markowowskiego układu. Interwencja resetująca z zeruje wpływ historii; dowodzi mediacji przez stan, nie niezależnej sprawczości abstrakcyjnej informacji. R² dla cech globalnych jest wysokie dzięki amplitudzie; wyniki nie oznaczają, że globalne cechy są bezwartościowe. Wektor odstępów to relacja między lokalnymi trójkami, nie zamiennik trójek.

## Następny krok
Sprawdzić ten sam układ z automatycznie wykrywanymi lokalnymi trójkami MIN–MAX–Δt, szumem obserwacji, nieznanym współczynnikiem zaniku i kontrolowanym resetem stanu; porównać z modelem autoregresyjnym i estymatorem stanu.
