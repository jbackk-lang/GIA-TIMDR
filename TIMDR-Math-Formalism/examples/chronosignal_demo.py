"""
examples/chronosignal_demo.py

Demonstracja "czasu jako sygnalu" (tempo/drift, timdr_formalism.chronosignal)
przepuszczonego przez pelny protokol tego repo (Hypothesis ->
Preregistration -> run_controls -> mann_whitney_test -> format_report),
dokladnie tak samo jak examples/prime_resonance_demo.py robi to dla
liczb pierwszych.

Hipoteza: licznik detektora "defekt" na serii tempa (odstepow miedzy
kolejnymi zdarzeniami) jest wyzszy w oknach, w ktorych do regularnego
tempa z autoskorelowanym jitterem (AR(1)) wstrzykniety zostal jeden
nienaturalny skok, niz w oknach czystego regularnego tempa bez
wstrzykniecia.

Dane sa CALKOWICIE SYNTETYCZNE (nie realny zegar/log zdarzen) -- to jest
demo mechaniki, analogiczne do prime_resonance_demo.py, NIE walidacja na
realnych danych (tamta jest w real_weather_resonance_validation.py, dla
rezonansu, nie dla tempa/driftu -- odpowiednika dla tempa/driftu na
realnych danych na razie nie ma).

UWAGA O WYKONANIU: ten skrypt zostal napisany w sesji bez dostepu do
sandboxa bash -- parametry (phi=0.95, sigma=0.3, jump_size=8.0) zostaly
dobrane recznie tak, zeby stosunek progu defektu do odchylenia
standardowego roznic dawal wyrazna separacje (patrz komentarz w
`_regular_tempo_with_jitter` ponizej za algebre), ale NIE zostal
faktycznie uruchomiony. Uruchom go sam, zanim zaufasz drukowanym
liczbom:

    python examples/chronosignal_demo.py
"""
from __future__ import annotations

import numpy as np

from timdr_formalism import (
    Hypothesis,
    Preregistration,
    run_controls,
    mann_whitney_test,
    format_report,
    ar1_noise,
)
from timdr_formalism.chronosignal import tempo, drift, defekt_flags

NOMINAL = 60.0       # "nominalny" odstep miedzy zdarzeniami (dowolna jednostka)
PHI = 0.95            # autokorelacja AR(1) jittera tempa
SIGMA = 0.3           # odchylenie innowacji AR(1)
JUMP_SIZE = 8.0       # wstrzyknieta wielkosc skoku (>>  typowy diff, patrz nizej)
FACTOR = 0.3          # prog detektora "defekt" (ten sam domyslny co w chronosignal.py)
WINDOW_SIZE = 50

# Dlaczego te parametry dają "czysty" background zamiast zalewu
# fałszywych trafień: dla AR(1) ze stacjonarnym std sigma_x =
# SIGMA/sqrt(1-PHI^2), próg defektu (0.3 * rozstęp p90-p10 serii) i
# odchylenie std różnic diff(series) = sigma_x*sqrt(2*(1-PHI)) mają
# stosunek próg/std_diff ~ 2.43 przy PHI=0.95 (rozkład różnic jest w
# przybliżeniu normalny) -> P(|diff|>próg) ~ 1.5% na krok, czyli
# tło ma średnio < 1 flagę na 49-elementowe okno. Wstrzyknięty skok
# JUMP_SIZE=8.0 jest ~25x większy niż sigma_x (~0.96) -> gwarantowane
# 2 flagi (wejście i wyjście ze skoku), niezależnie od jittera.


def _regular_tempo_with_jitter(window_size: int, seed) -> np.ndarray:
    return NOMINAL + ar1_noise(window_size, phi=PHI, sigma=SIGMA, seed=seed)


def _tempo_with_injected_jump(window_size: int, seed) -> np.ndarray:
    s = _regular_tempo_with_jitter(window_size, seed).copy()
    mid = window_size // 2
    s[mid] += JUMP_SIZE
    return s


def _defekt_count_metric(series: np.ndarray) -> float:
    return float(np.sum(defekt_flags(series, factor=FACTOR)))


def main() -> None:
    # --- Ilustracja tempo()/drift() na jawnych znacznikach czasu ---
    example_intervals = _regular_tempo_with_jitter(20, seed=42)
    example_timestamps = np.concatenate(([0.0], np.cumsum(example_intervals)))
    print("=== tempo()/drift() na przykladowych znacznikach czasu ===")
    print("timestamps (pierwsze 5):", np.round(example_timestamps[:5], 3))
    print("tempo(t)   (pierwsze 5):", np.round(tempo(example_timestamps)[:5], 3))
    print(
        "drift(t) wzgledem nominal=%.1f (pierwsze 5):" % NOMINAL,
        np.round(drift(example_timestamps, nominal_interval=NOMINAL)[:5], 3),
    )
    print()

    # --- Pelny protokol: Hypothesis -> Preregistration -> controls -> test ---
    hypothesis = Hypothesis(
        name="tempo_defekt_wykrywa_wstrzykniety_skok",
        description=(
            "Licznik flag detektora 'defekt' (|diff(tempo)| > "
            f"{FACTOR}*(p90-p10)) na serii tempa jest wyzszy w oknach z "
            "jednym wstrzknietym, nienaturalnym skokiem niz w oknach "
            "czystego regularnego tempa z jitterem AR(1)."
        ),
        effect_description=(
            "roznica median liczby flag 'defekt' na okno miedzy grupa "
            "testowa (skok wstrzykniety) a grupa tla (brak skoku)"
        ),
    )
    params = {
        "nominal": NOMINAL, "phi": PHI, "sigma": SIGMA,
        "jump_size": JUMP_SIZE, "factor": FACTOR, "window_size": WINDOW_SIZE,
    }
    prereg = Preregistration.create(hypothesis, params)
    print("=== Preregistration ===")
    print(f"fingerprint: {prereg.fingerprint[:16]}...")
    print()

    controls = run_controls(
        metric_fn=_defekt_count_metric,
        positive_injector=lambda w, s: _tempo_with_injected_jump(w, s),
        negative_generator_a=lambda w, s: _regular_tempo_with_jitter(w, s),
        negative_generator_b=lambda w, s: _regular_tempo_with_jitter(w, s),
        n_windows=30,
        window_size=WINDOW_SIZE,
        seed=0,
    )

    if not controls.passed:
        print(format_report(hypothesis, controls, main_result=None))
        return

    rng = np.random.default_rng(1)
    seeds_test = rng.integers(0, 2**31 - 1, size=40)
    seeds_bg = rng.integers(0, 2**31 - 1, size=40)
    test_values = [
        _defekt_count_metric(_tempo_with_injected_jump(WINDOW_SIZE, int(s)))
        for s in seeds_test
    ]
    bg_values = [
        _defekt_count_metric(_regular_tempo_with_jitter(WINDOW_SIZE, int(s)))
        for s in seeds_bg
    ]
    wynik = mann_whitney_test(test_values, bg_values)
    print(format_report(hypothesis, controls, wynik))


if __name__ == "__main__":
    main()
