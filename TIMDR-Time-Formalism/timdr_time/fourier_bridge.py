"""
timdr_time/fourier_bridge.py

Most Fouriera M/S<->K: standardowa transformata między reprezentacją
sygnału w dziedzinie czasu a jego reprezentacją częstotliwościową.
Dla równomiernie próbkowanego sygnału rzeczywistego `fft_modalities()`
wykorzystuje jednostronne FFT i tworzy modalności z jej współczynników.
To jest dokładna transformata dyskretna dla skończonego wektora próbek;
nie oznacza identyczności obiektów M/S i K ani nie stanowi modelu
fizycznej dualności korpuskularno-falowej fotonu.

Związek z zasadą nieoznaczoności jest węższy i matematyczny: nierówność
czas–częstotliwość Gabora dla pary zmiennych sprzężonych Fouriera ma
analogiczną postać do nierówności położenie–pęd Heisenberga, po
uwzględnieniu konwencji jednostek. Dla przyjętych tu odchyleń
standardowych w czasie i częstotliwości (Hz) impuls gaussowski osiąga
granicę `Delta_t*Delta_f = 1/(4*pi)`. Nie jest to wyjaśnienie ani
dowód fizycznej dualności fotonu.

W TIMDR: `x(t)` z gałęzi M/S (`timdr_formalism.chronosignal`) jest
reprezentacją w dziedzinie czasu, a modalności `(f,phi,A)` z gałęzi K
(`timdr_modal`) są reprezentacją przez składowe sinusoidalne. FFT
daje konkretną mapę między tymi reprezentacjami, bez utożsamiania ich.

## Dlaczego to NIE lamie nieredukowalnosci galezi

`GIA-TIMDR/docs/theory/TIMDR_Branch_Specification.md` wymaga, zeby M/S
i K byly formalnie odrebne. Ten modul tego nie neguje: nie twierdzi,
ze "x(t) TO JEST (f,phi,A)". Twierdzi, ze istnieje KONKRETNA, znana
TRANSFORMATA (FFT) miedzy jednym a drugim -- dokladnie tak, jak istnieje
transformata miedzy funkcja i jej pochodna, bez utozsamiania funkcji z
pochodna. `timdr_time/chronoprocess.py` (Xi=(T,x,Gamma,phi)) CELOWO
nie ma zadnej takiej funkcji -- ten modul jest jedynym, jawnie
wyodrebnionym wyjatkiem, uzasadnionym tym, ze FFT jest ustalona,
rygorystyczna matematyka, nie nowa hipoteza.

## Zasada nieoznaczonosci Gabora -- co dokladnie jest tu policzone

Dla energetycznie wazonych odchylen standardowych (Delta_t = odchylenie
std rozkladu |x(t)|^2 wzgledem srodka ciezkosci w czasie; Delta_f =
odchylenie std rozkladu A_k^2 WOKOL ZERA w czestotliwosci -- zero jest
poprawnym srodkiem dla KAZDEGO sygnalu rzeczywistego, bo jego pelne,
dwustronne widmo jest zawsze symetryczne wzgledem f=0 z symetrii
Hermite'a; rfft zwraca tylko polowe nieujemna, wiec liczenie wariancji
"wokol zera" zamiast "wokol sredniej jednostronnej" jest tym, co
odtwarza poprawna, fizyczna wariancje pelnego widma) -- dla impulsu
gaussowskiego `x(t)=exp(-(t-t0)^2/(2*sigma^2))` wyprowadzono TU, w tej
sesji, recznie (nie przepisane z pamieci):

    Delta_t = sigma/sqrt(2)
    Delta_f = 1/(2*sqrt(2)*pi*sigma)
    Delta_t * Delta_f = 1/(4*pi)  -- NIEZALEZNE od sigma

Wyprowadzenie: energia w czasie |x(t)|^2=exp(-(t-t0)^2/sigma^2) ma
wariancje sigma^2/2 (Gaussian o "efektywnym tau^2=sigma^2/2"). Ciagla
transformata Fouriera x(t) to (co do stalej) exp(-2*pi^2*sigma^2*f^2),
wiec jej energia |X(f)|^2 jest Gaussianem o wariancji 1/(8*pi^2*sigma^2)
wokol f=0. sqrt tych wariancji daje wzory powyzej; iloczyn upraszcza
sie do 1/(4*pi), niezaleznie od sigma -- dokladnie granica
Gabora/Heisenberga OSIAGANA (rownosc, nie tylko nierownosc) przez
impuls gaussowski, znany fakt z analizy Fouriera.

UWAGA O DYSKRETYZACJI: powyzsze jest wyprowadzone w granicy ciaglej.
Testy w tests/test_fourier_bridge.py licza to na DYSKRETNEJ,
SKONCZONEJ siatce (FFT o skonczonej rozdzielczosci) -- oczekiwane sa
odchylenia rzedu kilkunastu-kilkudziesieciu procent od 1/(4*pi), stad
szerokie tolerancje w tych testach (ten sam wzorzec co
tests/test_geometry_weingarten.py).

UWAGA O WYKONANIU: po dodaniu regresji wag Parsevala aktualny
`tests/test_fourier_bridge.py` zawiera 12 testow. Wszystkie przeszly
w GitHub Actions w przebiegu workflow `Repository regression checks`
dla commitu `ec28c9bb` (krok `Test Time formalism and Fourier bridge`).
To potwierdza wykonanie testow regresyjnych w CI, nie dowodzi samo w
sobie ogolnej poprawnosci matematycznej mostu poza zakresem testow.
"""
from __future__ import annotations

from typing import List, Sequence, Tuple

import numpy as np

from . import _bootstrap  # noqa: F401

try:
    from timdr_modal import Modality as _Modality
except ImportError as e:
    raise ImportError(
        "Nie mozna zaimportowac timdr_modal. Sprawdz, czy "
        "TIMDR-Modal-Formalism istnieje jako repo-siostra (oczekiwana "
        "sciezka wzgledna ../TIMDR-Modal-Formalism)."
    ) from e


__all__ = [
    "fft_modalities",
    "temporal_spread",
    "spectral_spread",
    "time_bandwidth_product",
]


def _finite_signal(values: Sequence[float], name: str = "x") -> np.ndarray:
    arr = np.asarray(values, dtype=float)
    if arr.ndim != 1 or arr.size == 0:
        raise ValueError(f"{name} musi byc niepustym wektorem 1D")
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"{name} musi zawierac wylacznie skonczone wartosci")
    return arr


def _positive_dt(dt: float) -> float:
    dt = float(dt)
    if not np.isfinite(dt) or dt <= 0.0:
        raise ValueError("dt musi byc skonczone i > 0")
    return dt


def fft_modalities(
    x: Sequence[float], dt: float, include_dc: bool = False
) -> Tuple[List[_Modality], float]:
    """x(t) [rownomiernie probkowany, odstep dt] -> lista Modality(f,phi,A).

    Standardowy rozklad Fouriera sygnalu rzeczywistego (rfft), przepisany
    na obiekty K-branchowe. Konwencja fazy: K uzywa sin(2*pi*f*t+phi)
    (timdr_modal.instantaneous_phase); rekonstrukcja FFT naturalnie daje
    cosinusy (X_k=|X_k|*e^{i*theta_k} -> skladowa |X_k|*cos(2*pi*f*t+theta_k)).
    Zeby dwie konwencje sie zgadzaly, faza modalnosci jest przesunieta:
    phi_k := angle(X_k) + pi/2 (bo sin(a+pi/2)=cos(a)) -- to jest
    sprawdzone w tests/test_fourier_bridge.py przez porownanie
    `timdr_modal.interference()` na zwroconych modalnosciach z
    oryginalnym sygnalem (dokladny test odtworzenia).

    Zwraca (modalnosci, dc_offset) -- dc_offset to srednia sygnalu
    (skladowa f=0), zwrocona OSOBNO domyslnie (include_dc=False),
    zeby uniknac degenerowanej modalnosci o f=0 w typowym uzyciu
    (np. karmienie wyniku do is_resonant()). Ustaw include_dc=True,
    zeby DC bylo wlaczone jako zwykla Modality(f=0,...) w liscie --
    WYMAGANE przy liczeniu spectral_spread() dla sygnalow niebazowanych
    na zerze (np. impuls gaussowski dodatni), bo dla takich sygnalow
    DC jest SZCZYTEM widma, nie czyms do odrzucenia (patrz uzycie w
    time_bandwidth_product poniżej i w testach).

    Rzuca ValueError dla sygnalow < 2 probek.
    """
    x = _finite_signal(x)
    dt = _positive_dt(dt)
    n = x.size
    if n < 2:
        raise ValueError("fft_modalities() wymaga >= 2 probek")

    with np.errstate(over="ignore", invalid="ignore"):
        X = np.fft.rfft(x)
    if not np.all(np.isfinite(X)):
        raise ValueError("widmo FFT przekracza zakres reprezentacji float")
    freqs = np.fft.rfftfreq(n, d=dt)
    dc_offset = float(X[0].real) / n

    is_even = (n % 2 == 0)
    nyquist_index = n // 2 if is_even else None

    modalities: List[_Modality] = []
    start_k = 0 if include_dc else 1
    for k in range(start_k, len(X)):
        special = (k == 0) or (is_even and k == nyquist_index)
        factor = (1.0 / n) if special else (2.0 / n)
        amplitude = factor * float(np.abs(X[k]))
        phi = float(np.angle(X[k])) + np.pi / 2.0
        modalities.append(_Modality(f=float(freqs[k]), phi=phi, A=amplitude))

    return modalities, dc_offset


def temporal_spread(x: Sequence[float], dt: float) -> Tuple[float, float]:
    """(t_srednie, Delta_t) -- srodek ciezkosci i odchylenie standardowe
    rozkladu ENERGII |x(t)|^2 w dziedzinie czasu (wazona wariancja
    wokol wlasnej sredniej -- poprawne dla dowolnego sygnalu, niezaleznie
    od tego, gdzie lezy jego "srodek")."""
    x = _finite_signal(x)
    dt = _positive_dt(dt)
    n = x.size
    t = np.arange(n, dtype=float) * dt
    if not np.all(np.isfinite(t)):
        raise ValueError("os czasu przekracza zakres reprezentacji float")
    scale = float(np.max(np.abs(x)))
    if scale == 0.0:
        raise ValueError("sygnal zerowy -- rozklad energii w czasie niezdefiniowany")
    # Skalowanie nie zmienia rozkladu wag x^2, a chroni przed overflow
    # dla sygnalow o bardzo duzej, ale skonczonej amplitudzie.
    weights = (x / scale) ** 2
    total = float(weights.sum())
    t_mean = float(np.sum(t * weights) / total)
    t_var = float(np.sum((t - t_mean) ** 2 * weights) / total)
    if not np.isfinite(t_mean) or not np.isfinite(t_var):
        raise ValueError("momenty czasowe przekraczaja zakres reprezentacji float")
    return t_mean, float(np.sqrt(t_var))


def spectral_spread(
    modalities: Sequence[_Modality], nyquist_frequency: float | None = None
) -> Tuple[float, float]:
    """(0.0, Delta_f) -- energetyczne odchylenie widma wokol zera.

    Dla amplitud z jednostronnego rFFT wagi energii nie sa po prostu A**2:
    skladowe wewnetrzne reprezentuja pary +/-f, wiec ich waga jest A**2/2.
    DC i bin Nyquista (jesli istnieje) nie maja partnera i zachowuja wage
    A**2. ``nyquist_frequency`` nalezy podac dla widma rFFT z parzysta
    liczba probek; bez niego wszystkie dodatnie czestotliwosci sa
    traktowane jako biny wewnetrzne. Dla dowolnej listy modalnosci K
    przekazanej bez informacji o pochodzeniu z rFFT stosowana jest ta
    sama jawna konwencja: dodatnie czestotliwosci maja wage A**2/2.

    Wariancja jest liczona wokol zera, zgodnie z symetria pelnego widma
    rzeczywistego sygnalu. Pierwszy element krotki pozostaje 0.0 dla
    symetrii API z temporal_spread().
    """
    if len(modalities) == 0:
        raise ValueError("pusta lista modalnosci")
    if any(not isinstance(m, _Modality) for m in modalities):
        raise ValueError("modalities musi zawierac obiekty Modality")
    f = np.array([m.f for m in modalities], dtype=float)
    amplitudes = np.array([m.A for m in modalities], dtype=float)
    # DC to dokładnie f=0; małe dodatnie częstotliwości nadal są
    # binami wewnętrznymi i muszą zachować wagę A²/2.
    dc = f == 0.0
    if nyquist_frequency is not None:
        if not np.isfinite(nyquist_frequency) or nyquist_frequency <= 0.0:
            raise ValueError("nyquist_frequency musi byc dodatnie i skonczone")
        nyquist = np.isclose(np.abs(f), nyquist_frequency, rtol=1e-12, atol=1e-15)
    else:
        nyquist = np.zeros(f.shape, dtype=bool)
    amplitude_scale = float(np.max(np.abs(amplitudes)))
    if amplitude_scale == 0.0:
        raise ValueError("wszystkie amplitudy zerowe -- rozklad energii w częstotliwości niezdefiniowany")
    scaled_amplitudes = amplitudes / amplitude_scale
    weights = 0.5 * scaled_amplitudes ** 2
    weights[dc | nyquist] = scaled_amplitudes[dc | nyquist] ** 2
    total = float(weights.sum())
    f_scale = float(np.max(np.abs(f)))
    if f_scale == 0.0:
        return 0.0, 0.0
    f_var_scaled = float(np.sum(((f / f_scale) ** 2) * weights) / total)
    delta_f = f_scale * np.sqrt(f_var_scaled)
    if not np.isfinite(delta_f):
        raise ValueError("szerokosc widma przekracza zakres reprezentacji float")
    return 0.0, float(delta_f)

def time_bandwidth_product(x: Sequence[float], dt: float, include_dc: bool = False) -> float:
    """Delta_t * Delta_f -- iloczyn czas-pasmo, ilosciowa tresc zasady
    nieoznaczonosci Gabora dla sygnalu x. Nie zaklada zadnej konkretnej
    dolnej granicy w kodzie (patrz naglowek modulu za wyprowadzenie
    1/(4*pi) dla impulsu gaussowskiego, testowane osobno w
    tests/test_fourier_bridge.py) -- ta funkcja tylko liczy sam iloczyn."""
    x = _finite_signal(x)
    dt = _positive_dt(dt)
    modalities, _ = fft_modalities(x, dt, include_dc=include_dc)
    _, delta_t = temporal_spread(x, dt)
    n = np.asarray(x).size
    nyquist = 1.0 / (2.0 * dt) if n % 2 == 0 else None
    _, delta_f = spectral_spread(modalities, nyquist_frequency=nyquist)
    product = delta_t * delta_f
    if not np.isfinite(product):
        raise ValueError("iloczyn czas-pasmo przekracza zakres reprezentacji float")
    return float(product)
