# TIMDR — identyfikowalność pamięci: długość sondy, szum i braki (2026-11-14)

Wykonany eksperyment: skrypt `probe_identifiability_sweep.py`, 2400 trening, 1000 walidacja (zarezerwowana, niewykorzystana do strojenia), 2000 test. Ziarno 2026111410. Dwie homometryczne historie impulsowe A=[0,1,4,10,12,17], B=[0,1,8,11,13,17], układ z[t+1]=α z[t]+x[t], α~U(.82,.94), amplituda U(.8,1.2). Przyszłość y=z[128]α^8+ε, ε~N(0,.045). Sondy k=0..7 obserwują z[128]α^k+szum. Szum sondy σ∈{0,.018,.05,.10}, niezależne braki 0%,25%,50%, liczba dostępnych pozycji 0,1,2,4,8. Zawsze prognoza tej samej próbki k=8. Regresja StandardScaler+Ridge(alpha=10) na obserwacjach i maskach braków, oddzielnie dla każdej konfiguracji. Odtwarzanie α z logarytmicznej regresji dostępnych dodatnich pomiarów, bez używania prawdziwego α.

## Test R² (wybrane konfiguracje)
| Liczba sond | σ=.018, braki 0% | σ=.018, braki 25% | σ=.10, braki 50% |
|---|---:|---:|---:|
| 0 | 0.0000 | 0.0000 | 0.0000 |
| 1 | 0.5536 | 0.4169 | 0.1244 |
| 2 | 0.5680 | 0.4749 | 0.2110 |
| 4 | 0.5789 | 0.5184 | 0.3101 |
| 8 | 0.5896 | 0.5521 | 0.3772 |

Dla σ=.018 bez braków estymacja α metodą log-liniową: MAE 0.0756 (2 sondy), 0.0531 (4), 0.0459 (8). Dla σ=0 i bez braków MAE 0.0043, gdyż słabe amplitudy poniżej progu powodują użycie wartości domyślnej .88. Braki 50% dają co najmniej dwie dostępne próbki w 24.8% przypadków przy dwóch pozycjach, 68.5% przy czterech i 96.7% przy ośmiu.

## Matematyczny kontrprzykład identyfikowalności
Przy jednej bezszumowej obserwacji z=0.15 nie da się określić α. Dla α=.82 przyszła wartość po 8 krokach wynosi 0.030662, a dla α=.94 wynosi 0.091435. To dwie różne przyszłości zgodne z tym samym pojedynczym pomiarem. Dwie niezerowe bezszumowe obserwacje z0,z1 w modelu bez wymuszenia wystarczają do identyfikacji α=z1/z0, lecz w szumie estymacja może być niestabilna.

## Wnioski i ograniczenia
Jedna sonda wystarcza do częściowego przewidywania, ale nie do identyfikacji dwóch parametrów (stan, tempo zaniku). Więcej obserwacji zwiększa R² w tym generatorze. Wysoki R² nie oznacza dokładnego odzyskania α. Użyto idealnie znanej struktury modelu, bez zakłóceń wejścia w fazie wygaszania; szum przyszłości ogranicza maksymalną jakość. Walidacja nie służyła do wyboru modelu. Lokalne trójki i relacje definiują historię wejścia, ale nie są dodatkowymi cechami regresji w tym eksperymencie — badamy obserwowalność stanu pamięci, nie przewagę reprezentacji TIMDR. Wyniki są syntetyczne, nie dowodzą fizycznej sprawczości informacji.

Następny test: obserwowalność przy ukrytym wymuszeniu, zmianie α w czasie i rzeczywistych lokalnych trójkach z automatycznej detekcji.