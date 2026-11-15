# TIMDR — lokalne trójki, relacje i kwadratury fazowe: niezależna prognoza fal (2026-11-14)

Skrypt `phase_triplets_comparison.py` uruchomiony lokalnie; seed 202611140813. 2400 przykładów (1500 trening, 400 niewykorzystanych, 500 test), fs=80 Hz, 160 próbek historii. Generator: suma dwóch tłumionych sinusoid, f1~U(4,8), f2=f1+U(.4,1.5), amplitudy .65–1.2, fazy losowe, tłumienia .03–.25, szum historii i celu .12. Horyzonty 2,10,30 próbek. Detekcja sześciu najwyższych lokalnych maksimów, każdemu odpowiada MIN z poprzednich dziewięciu próbek, Δt w sekundach; odstępy między maksimami. Faza: osiem zespolonych projekcji na siatkę częstotliwości 4..10 Hz, real/imag, ostatnie 100 próbek. Model wspólny StandardScaler+Ridge(alpha=100), bez dostrajania.

| Cechy | R² h2 | R² h10 | R² h30 |
|---|---:|---:|---:|
| Trójki | -.00440 | -.01644 | -.02561 |
| Trójki+odstępy | -.01473 | -.01874 | -.02829 |
| Kwadratury fazowe | .59336 | .12672 | .00029 |
| Trójki+odstępy+faza | .59266 | .12263 | -.02477 |
| Surowy sygnał | .89700 | .59739 | .00974 |
| Surowy+faza | **.90352** | **.60634** | **.01098** |

Algorytm zwrócił sześć maksimów dla wszystkich przykładów, lecz nie weryfikowano, czy odpowiadają prawdziwym zdarzeniom fizycznym. **Wynik negatywny**: trójki i relacje nie dodają wartości ponad fazę, a surowy przebieg jest lepszy. Uwaga: osiem częstotliwości siatki nie stanowi estymacji prawdziwych dwóch częstotliwości; brak modelu nieliniowego i CI. Wyniki nie są bezpośrednio porównywalne z wcześniejszym eksperymentem 150 przebiegów, bo generator i podział są inne. Przed twierdzeniem o kompresji TIMDR konieczne są adekwatne relacje fazowo-czasowe oraz silne klasyczne baseline, w tym model dwóch tłumionych fal.