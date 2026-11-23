# Audyt metody ekstrakcji fazy w walidacji modalnej

Data: 2026-11-23  
Zakres: `TIMDR-Modal-Formalism/timdr_modal/real_data_validation.py` na gałęzi `maintenance/repo-hygiene-audit-2026-11-23`.  
Cel: oddzielić poprawność walidacji wejścia i kodu od zasadności interpretacji fizycznej estymowanych parametrów `(f, phi, A)`.

## Co robi obecna implementacja

- Wczytuje ślady CLC/RIO, odrzuca wartości niefinitywne, nieciągłe/niemalejące znaczniki czasu i odstęp próbkowania niezgodny z 100 Hz.
- Dzieli sygnał na niepokrywające się okna; domyślnie 10 s, czyli 1000 próbek.
- Odejmuję średnią, wykonuje `rfft`, wybiera bin o największej amplitudzie poza DC.
- Przyjmuje kąt tego współczynnika FFT po korekcie o `+pi/2` jako fazę sinusową w pierwszej próbce okna.
- Przelicza fazę na wspólny początek śladu przez `phi_global = wrap(phi_local - 2*pi*f_peak*t_start)`.

## Ustalenia matematyczne i ograniczenia

### 1. Rozdzielczość częstotliwości

Dla `fs=100 Hz` i `N=1000` próbek rozdzielczość siatki FFT wynosi:

`df = fs/N = 0.1 Hz`.

Wybrany `f_peak` jest częstotliwością binu, a nie estymatorem z interpolacją maksimum ani wynikiem dopasowania sinusoidy. Błąd kwantyzacji może dochodzić do połowy odstępu binów, tj. około 0,05 Hz (przy założeniu, że rzeczywisty składnik leży między sąsiednimi binami).

### 2. Kąt pojedynczego binu nie jest ogólnie fazą sygnału szerokopasmowego

Dla sinusoidy o częstotliwości dokładnie trafiającej w bin, bez zakłóceń i przy odpowiednio długim oknie, korekta konwencji DFT/cosinus–sinus `+pi/2` jest uzasadniona. Nie wynika z tego jednak, że kąt współczynnika FFT dominującego binu sygnału szerokopasmowego jest fazą fizycznej modalności.

Gdy częstotliwość nie trafia w bin, energia rozlewa się na sąsiednie biny. Bez okna taperującego wyciek widma może zmienić kąt wybranego współczynnika. W sygnale wieloskładnikowym kąt pojedynczego binu jest fazą zespolonej projekcji sygnału na daną częstotliwość, a nie automatycznie fazą jednego oscylatora.

W konsekwencji `(f_peak, phi_local, A_peak)` należy obecnie traktować jako cechy dominującej projekcji widmowej w oknie, nie jako bezwarunkowo poprawny pomiar modalności.

### 3. Przeliczenie fazy na początek śladu wzmacnia błąd częstotliwości

Przeliczenie `phi_global = phi_local - 2*pi*f_peak*t_start` jest algebraicznie poprawne, jeśli `phi_local` i `f_peak` opisują ten sam rzeczywisty składnik sinusoidalny. Jeśli częstotliwość jest obciążona błędem `delta_f`, błąd fazy po przeniesieniu do początku śladu rośnie jak `2*pi*delta_f*t_start`. Dla późniejszych okien może więc być duży nawet przy niewielkim błędzie częstotliwości.

### 4. Wspólny czas próbkowania nie gwarantuje wspólnej fazy fizycznej

Identyczny czas startu zapisów i zgodne próbkowanie są warunkami koniecznymi do porównania faz, ale nie wystarczają same w sobie do wykazania wspólnego odniesienia fazowego pomiędzy stacjami. Należy udokumentować korekty czasu/metadata akwizycji oraz odpowiedź instrumentalną kanałów (w tym orientację, polaryzację i ewentualną korektę odpowiedzi instrumentu). Surowe liczby z dwóch różnych torów pomiarowych nie muszą mieć bezpośrednio porównywalnej fazy fizycznej.

### 5. Permutacja nie naprawia błędów estymacji

Null permutacyjny ocenia, czy sparowanie indeksów okien daje inny wynik niż losowe parowanie już wyekstrahowanych cech. Nie sprawdza, czy te cechy są poprawnymi estymatorami fizycznych częstotliwości i faz. Nie rozwiązuje też problemu wspólnej odpowiedzi instrumentalnej ani błędu estymacji fazy.

## Wniosek

Walidacje wejścia (finite values, monotoniczne znaczniki czasu, zgodność fs, długość okna) są wartościowe i powinny pozostać. Obecny ekstraktor może służyć jako jawnie opisany, eksploracyjny wskaźnik dominującego binu FFT. Sam wynik tego pipeline'u nie wystarcza jednak do stwierdzenia fizycznego rezonansu modalnego między stacjami.

Nie zmieniamy istniejących wyników, prerejestracji ani kodu badawczego w ramach tego audytu porządkowego. Nie należy dopisywać pozytywnego ani negatywnego werdyktu fizycznego na podstawie samego audytu kodu.

## Zalecana ścieżka walidacji przed twierdzeniem o rezonansie

1. Zachować bieżący ekstraktor jako wariant bazowy i nie nadpisywać jego wyników.
2. Dodać niezależny wariant estymacji: dopasowanie sinusoidalne / regresja harmoniczna w oknie, z oceną reszt i niepewności częstotliwości oraz fazy; porównać go z interpolacją maksimum FFT i wariantem z oknem taperującym.
3. Przeprowadzić testy syntetyczne z częstotliwościami dokładnie na binie i pomiędzy binami, wieloma składowymi, szumem, dryftem częstotliwości i znanym przesunięciem fazy. Zmierzyć błąd `f`, `phi` i wpływ przeniesienia fazy na odległy czas odniesienia.
4. Zweryfikować metadane obu stacji: synchronizację zegarów, opóźnienia, odpowiedzi instrumentów, orientację kanałów i korektę odpowiedzi.
5. Dopiero potem wykonać prerejestrowane porównanie na danych rzeczywistych, z niepewnością i kontrolami negatywnymi.

Status: audyt metodologiczny; nie jest nowym wynikiem empirycznym ani formalnym dowodem.
