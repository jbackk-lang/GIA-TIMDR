"""
Testy timdr_formalism.meta_validator -- uniwersalny walidator Lambda-tau-rho-J.

Zasada projektowa (spojna z test_pipeline.py): unikac asercji opartych na
"typowym" zachowaniu pojedynczego losowego ciagniecia -- kazdy test albo
uzywa danych z duza, celowo wstrzykniana separacja/korelacja (kontrolka
pozytywna), albo czystych danych bez zadnej patologii (kontrolka
negatywna), zeby wynik nie zalezal od szczegolow implementacji scipy/numpy
fallbacku. Kazdy z 5 obszarow specyfikacji ma co najmniej jedna kontrolke
pozytywna (wykrywa problem, gdy jest) i jedna negatywna (nie faluje
alarmem, gdy danych nic nie jest nie tak).
"""
import numpy as np
import pytest

from timdr_formalism.meta_validator import (
    MetaSeriesData,
    MetaValidationReport,
    validate_shape_and_ranges,
    validate_channel_isolation,
    diagnose_phase_thresholds,
    compare_regimes,
    phase_stability_diagnostic,
    cross_run_consistency,
    validate_meta_series,
    _spearman_numpy,
    _ks_2samp_numpy,
)


def _clean_series(n=50, seed=0) -> MetaSeriesData:
    """Czysta, w pelni poprawna seria -- kotwica dla kontrolek negatywnych."""
    rng = np.random.default_rng(seed)
    Lambda = rng.uniform(0.0, 1.0, n)
    tau = rng.uniform(0.0, 2.0, n)
    rho = rng.uniform(0.0, 1.0, n)
    J = rng.uniform(0.0, 1.0, n)
    magnitude = rng.uniform(0.0, 0.05, n - 1)
    phases = ["stabilna"] * (n - 1)
    return MetaSeriesData(Lambda, tau, rho, J, magnitude, phases)


# ---------------------------------------------------------------------
# Obszar 1/2: ksztalt i zakresy
# ---------------------------------------------------------------------

def test_shape_ranges_clean_series_passes():
    report = validate_shape_and_ranges(_clean_series())
    assert report.passed
    assert report.errors() == []


def test_shape_mismatch_flags_error():
    data = _clean_series(n=50)
    data.tau = list(data.tau)[:-5]  # skroc jeden kanal
    report = validate_shape_and_ranges(data)
    assert not report.passed
    assert any(i.code == "length_mismatch" for i in report.errors())


def test_nan_in_channel_flags_error():
    data = _clean_series()
    Lambda = np.array(data.Lambda, dtype=float)
    Lambda[3] = np.nan
    data.Lambda = Lambda
    report = validate_shape_and_ranges(data)
    assert not report.passed
    assert any(i.code == "non_finite" for i in report.errors())


def test_out_of_unit_interval_flags_warning():
    data = _clean_series()
    rho = np.array(data.rho, dtype=float)
    rho[0] = 5.0  # poza [0,1]
    data.rho = rho
    report = validate_shape_and_ranges(data)
    assert report.passed  # to warning, nie error
    assert any(i.code == "out_of_unit_interval" for i in report.warnings())


def test_tau_out_of_unit_interval_not_flagged_by_default():
    """tau MOZE legalnie przekroczyc 1 (iloraz wzgledem progu) -- domyslnie
    nie jest w expect_unit_interval, wiec nie powinien generowac warninga."""
    data = _clean_series()
    tau = np.array(data.tau, dtype=float)
    tau[0] = 50.0
    data.tau = tau
    report = validate_shape_and_ranges(data)
    assert not any(i.code == "out_of_unit_interval" and "tau" in i.message for i in report.issues)


def test_invalid_phase_label_flags_error():
    data = _clean_series()
    phases = list(data.phases)
    phases[0] = "nieznana_faza"
    data.phases = phases
    report = validate_shape_and_ranges(data)
    assert not report.passed
    assert any(i.code == "invalid_phase_labels" for i in report.errors())


def test_magnitude_length_mismatch_flags_error():
    data = _clean_series(n=50)
    data.magnitude = list(data.magnitude) + [0.01]  # o jeden za dlugo
    report = validate_shape_and_ranges(data)
    assert not report.passed
    assert any(i.code == "magnitude_length_mismatch" for i in report.errors())


# ---------------------------------------------------------------------
# Obszar 3: izolacja kanalow
# ---------------------------------------------------------------------

def test_channel_isolation_clean_series_no_warning():
    report = validate_channel_isolation(_clean_series(seed=1))
    assert report.warnings() == []


def test_channel_isolation_detects_duplicated_channel():
    """Kontrolka pozytywna: wstrzyknij J = rho (identyczny sygnal pod
    dwoma nazwami) -- dokladnie wzorzec Omega=D+|R| / Synoptyk-v3 V1."""
    rng = np.random.default_rng(2)
    n = 60
    Lambda = rng.uniform(0, 1, n)
    tau = rng.uniform(0, 2, n)
    rho = rng.uniform(0, 1, n)
    J = rho.copy()  # zdublowany kanal
    magnitude = rng.uniform(0, 0.05, n - 1)
    phases = ["stabilna"] * (n - 1)
    data = MetaSeriesData(Lambda, tau, rho, J, magnitude, phases)
    report = validate_channel_isolation(data)
    warned = [i for i in report.warnings() if i.code == "high_channel_correlation"]
    assert warned
    assert any("rho" in i.message and "J" in i.message for i in warned)
    assert report.channel_correlations["rho-J"] > 0.99


def test_channel_isolation_constant_channel_no_crash():
    """Kanal stale rowny (std=0) nie powinien wywalic sie na dzieleniu
    przez zero -- korelacja powinna byc raportowana jako None."""
    data = _clean_series(seed=3)
    data.J = [0.5] * len(data.J)
    report = validate_channel_isolation(data)
    assert any(v is None for k, v in report.channel_correlations.items() if "J" in k)


def test_spearman_numpy_matches_known_monotonic_relationship():
    x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    y = np.array([2.0, 4.0, 6.0, 8.0, 10.0])
    assert _spearman_numpy(x, y) == pytest.approx(1.0)
    y_inv = y[::-1]
    assert _spearman_numpy(x, y_inv) == pytest.approx(-1.0)


# ---------------------------------------------------------------------
# Obszar 4: diagnostyka progow fazowych
# ---------------------------------------------------------------------

def test_thresholds_never_reached_flags_warning():
    data = _clean_series()  # magnitude w [0, 0.05], daleko ponizej 0.1
    report = diagnose_phase_thresholds(data, thresholds=(0.1, 1.0))
    assert any(i.code == "thresholds_never_reached" for i in report.warnings())
    assert report.magnitude_stats["fraction_ge_transitional_threshold"] == 0.0


def test_thresholds_reached_no_never_reached_warning():
    rng = np.random.default_rng(4)
    data = _clean_series()
    data.magnitude = rng.uniform(0.05, 0.5, len(data.magnitude))  # przekracza 0.1 czesciowo
    report = diagnose_phase_thresholds(data, thresholds=(0.1, 1.0))
    assert not any(i.code == "thresholds_never_reached" for i in report.issues)


def test_thresholds_suggestion_always_present_and_labeled_diagnostic():
    report = diagnose_phase_thresholds(_clean_series())
    info = [i for i in report.issues if i.code == "suggested_percentile_thresholds"]
    assert len(info) == 1
    assert info[0].severity == "info"
    assert "DIAGNOSTYCZNA" in info[0].message


# ---------------------------------------------------------------------
# Obszar 5: walidacja statystyczna
# ---------------------------------------------------------------------

def test_compare_regimes_detects_shift():
    """Kontrolka pozytywna: dwie grupy z ogromna separacja -> male p w obu testach."""
    rng = np.random.default_rng(5)
    group_a = rng.uniform(0.0, 0.1, 40)
    group_b = rng.uniform(10.0, 10.1, 40)
    result = compare_regimes(group_a, group_b)
    assert result["mann_whitney"].pvalue < 0.001
    assert result["ks_pvalue"] < 0.001
    assert result["ks_statistic"] == pytest.approx(1.0)


def test_compare_regimes_no_shift():
    """Kontrolka negatywna: te same rozklady -> duze p."""
    rng = np.random.default_rng(6)
    group_a = rng.normal(0, 1, 200)
    group_b = rng.normal(0, 1, 200)
    result = compare_regimes(group_a, group_b)
    assert result["mann_whitney"].pvalue > 0.05


def test_ks_2samp_numpy_matches_scipy_when_available():
    pytest.importorskip("scipy")
    from scipy.stats import ks_2samp as scipy_ks
    rng = np.random.default_rng(7)
    a = rng.normal(0, 1, 60)
    b = rng.normal(0.8, 1, 60)
    d_np, p_np = _ks_2samp_numpy(a, b)
    ref = scipy_ks(a, b)
    assert d_np == pytest.approx(ref.statistic, abs=1e-9)
    assert p_np == pytest.approx(ref.pvalue, abs=0.02)


def test_phase_stability_high_flip_rate_flags_warning():
    phases = ["stabilna", "krytyczna"] * 30  # flip co krok = 100% flip rate
    report = phase_stability_diagnostic(phases)
    assert any(i.code == "high_phase_flip_rate" for i in report.warnings())
    assert report.magnitude_stats["phase_flip_rate"] == pytest.approx(1.0)


def test_phase_stability_low_flip_rate_no_warning():
    phases = ["stabilna"] * 50 + ["krytyczna"] * 5  # jedna zmiana na 55 krokow
    report = phase_stability_diagnostic(phases)
    assert report.warnings() == []


def test_cross_run_consistency_stable_runs_no_warning():
    runs = [np.random.default_rng(i).uniform(0.09, 0.11, 30) for i in range(5)]
    report = cross_run_consistency(runs)
    assert report.warnings() == []
    assert report.magnitude_stats["cross_run_cv"] < 1.0


def test_cross_run_consistency_unstable_runs_flags_warning():
    """Kontrolka pozytywna: jeden przebieg-outlier dominujacy srednia."""
    runs = [
        np.full(30, 0.001),
        np.full(30, 0.001),
        np.full(30, 0.001),
        np.full(30, 5.0),  # outlier
    ]
    report = cross_run_consistency(runs)
    assert any(i.code == "high_cross_run_variability" for i in report.warnings())


def test_cross_run_consistency_insufficient_runs():
    report = cross_run_consistency([np.array([0.1, 0.2])])
    assert any(i.code == "insufficient_runs" for i in report.issues)


# ---------------------------------------------------------------------
# Integracja: validate_meta_series
# ---------------------------------------------------------------------

def test_validate_meta_series_clean_passes():
    report = validate_meta_series(_clean_series(seed=8))
    assert report.passed


def test_validate_meta_series_combines_all_areas():
    """Zbuduj serie z wieloma jednoczesnymi problemami i sprawdz, ze
    walidator wykrywa je WSZYSTKIE naraz (obszary 2/3/4/5-flapping)."""
    rng = np.random.default_rng(9)
    n = 60
    Lambda = rng.uniform(0, 1, n)
    tau = rng.uniform(0, 2, n)
    rho = rng.uniform(0, 1, n)
    J = rho.copy()  # duplikat -> obszar 3
    magnitude = rng.uniform(0.0, 0.01, n - 1)  # nigdy nie osiaga progu -> obszar 4
    phases = ["stabilna", "krytyczna"] * ((n - 1) // 2)  # flapping -> obszar 5
    data = MetaSeriesData(Lambda, tau, rho, J, magnitude, phases)
    report = validate_meta_series(data)
    codes = {i.code for i in report.issues}
    assert "high_channel_correlation" in codes
    assert "thresholds_never_reached" in codes
    assert "high_phase_flip_rate" in codes


def test_validate_meta_series_domain_check_fn_hook_is_applied():
    def fake_domain_check(data: MetaSeriesData) -> MetaValidationReport:
        r = MetaValidationReport()
        r.add("error", "domain", "custom_rule_violated", "test hook zadzialal")
        return r

    report = validate_meta_series(_clean_series(seed=10), domain_check_fn=fake_domain_check)
    assert not report.passed
    assert any(i.code == "custom_rule_violated" for i in report.errors())


def test_format_report_contains_all_issues():
    report = MetaValidationReport()
    report.add("warning", "isolation", "test_code", "testowa wiadomosc")
    text = report.format_report()
    assert "test_code" in text
    assert "testowa wiadomosc" in text
    assert "WARNING" in text
