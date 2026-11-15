# TIMDR — uczony filtr geometryczny, test odporności (2026-11-14)

Uruchomiono `learned_geometry_filter.py`, seed 202611140826. 1400 treningowych procesów, 3 niezależne zbiory po 500 testowych. Każdy proces ma 4 przyczynowe i 8 zakłócających identycznych trójek. Cztery impulsy pobudzają oscylator z r=.975, ω=.31; cel to stan 12 próbek później, szum σ=.035.

**Uczenie nadzorowane:** wzorzec nie jest podany jako liczby, ale prawdziwe indeksy czterech zdarzeń przyczynowych są dostępne w treningu. Mediana posortowanych odstępów to [9,16,25]. Filtr przegląda 495 czwórek i minimalizuje odległość odstępów od wzorca; predyktor HistGradientBoostingRegressor.

| Test | Filtr R² | Oracle R² | Odzysk zdarzeń | Cała czwórka |
|---|---:|---:|---:|---:|
| Ta sama geometria | .81296 | .99886 | 96.15% | 85.4% |
| Jitter ±2 próbki | -.25102 | .37870 | 50.85% | 9% |
| Skala czasu ×1.5 | -.73716 | -.07134 | 35.75% | 0% |

Baselines R² dla tej samej geometrii: losowy -.07194, pierwsze cztery .08040, wszystkie odstępy .03320. Dla jitter: -.10340, -.08614, -.03052. Dla skali ×1.5: -.06101, -.15209, -.09371.

**Wniosek:** wzorzec geometryczny nauczony z etykiet działa w znanym rozkładzie, lecz nie jest odporny na zmianę skali ani jitter. Także oracle z prawdziwymi zdarzeniami traci jakość poza rozkładem, zatem degradacja wynika również z modelu prognozy. Syntetyczny generator, jeden seed, brak CI, trójki zadane zamiast wykrytych. Następny test: bezwymiarowe relacje odstępów i trening wieloskalowy.