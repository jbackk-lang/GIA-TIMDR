# Widmo FFT, faza i STFT przy wyrównanym budżecie cech — 2026-11-14

## Cel i protokół
Porównanie MIN–MAX–CZAS, widma mocy FFT, zespolonego FFT (z informacją fazową), lokalnego widma STFT, autokorelacji i MIN–MAX–CZAS+STFT. Generator i funkcje bazowe pochodzą z `spectral_relational_comparison.py`. Trening 2400 sygnałów (łagodne zakłócenia), walidacja 800 (silne), niezależny test 1200 (silne), test łatwy 1200 i kontrola negatywna 1200 (niezależne etykiety). Reprezentacje redukowane do budżetu 3, 8 lub 16 wymiarów poprzez standaryzację i PCA **dopasowane wyłącznie na treningu**. Modele: regresja logistyczna z C w {0.01,0.1,1,10}, dobieranym na walidacji. Wyniki testowe nie służyły do wyboru C. Kod: `spectral_phase_stft_test.py`.

## Wyniki: trudny zbiór testowy
| Cechy | 3 | 8 | 16 |
|---|---:|---:|---:|
| MIN–MAX–CZAS | .7125 | .7125 | .7125 |
| FFT moc | .7283 | .7250 | .7367 |
| FFT zespolone (faza) | .5808 | .5833 | .5800 |
| STFT moc | .5750 | .5567 | .5817 |
| Autokorelacja | .7342 | .7783 | .7792 |
| MIN–MAX–CZAS+STFT | .5717 | .5658 | .5892 |

## Modele wybrane wyłącznie na walidacji
- 3 cechy: MIN–MAX–CZAS, walidacja .7525, trudny test .7125, łatwy .9992, negatywna .5117.
- 8 cech: autokorelacja, walidacja .7588, trudny test .7783, łatwy .9933, negatywna .4900.
- 16 cech: autokorelacja, walidacja .7625, trudny test .7792, łatwy .9950, negatywna .4908.

## Interpretacja
Autokorelacja wygrywa w zadaniu, w którym klasa jest zakodowana w odległości między impulsami. Widmo mocy jest również użyteczne, ale słabsze w tym budżecie i z PCA. Zespolone FFT zawiera fazę, jednak jego liniowe współrzędne zależą od absolutnego przesunięcia impulsów; przy losowych przesunięciach i PCA może wypaść gorzej. STFT-moc w oknach 32 próbek, skok 16, nie uogólnia się dobrze w tym prostym liniowym modelu.

## Ograniczenia i uwagi
To nadal **syntetyczne dane z zaprojektowanym związkiem odstępu i przyszłego AR(1)**. Faza nie została zbadana za pomocą niezmienniczej na przesunięcia reprezentacji fazowej ani nieliniowego modelu. STFT i zespolone FFT są redukowane PCA bez nadzoru, co może usuwać informację predykcyjną. Cechy czasowe mają 3 współrzędne, ale używają wartości ekstremów i odstępu z zegara nieliniowego; widmo/autokorelacja liczone są według indeksów próbek. Nie należy interpretować różnic jako uniwersalnego rankingu reprezentacji.

## Następny test
Wariant par o **identycznym widmie mocy**, ale odwróconej kolejności czasowej, aby odizolować informację fazową i relacyjną. Porównać czas, widmo mocy, fazę i STFT z rzeczywistym rozróżnianiem kolejności.
