# Pre-rejestracja: modal_band_energy_bridge v0.2 — pełna demodulacja obwiedniowa (rezonans przez kurtozę → obwiednia → widmo obwiedni)

> Status: PRE-REJESTRACJA, zamrożona PRZED zmianą kodu. Data:
> 2026-09-22. v0.1 ZAMKNIĘTY jako błędny wariant (`RESULT_
> MODAL_BAND_ENERGY_BRIDGE_v0.1.md`) — filtrował bezpośrednio wokół
> niskiej częstotliwości charakterystycznej, pomijając krok demodulacji
> rezonansu, który jest sednem standardowej "envelope spectrum
> analysis". v0.2 dodaje ten brakujący krok — to jest POPRAWKA
> METODOLOGICZNA (przywrócenie standardowej, ugruntowanej metody), NIE
> nowy wymysł ani tuning progu pod wynik.

## 0. Co się zmienia względem v0.1

v0.1: `x_DE → filtr nisko (BPFO/BPFI/BSF) → obwiednia → średnia`.
v0.2: `x_DE → filtr WYSOKO (pasmo rezonansu, wybrane przez kurtozę) →
obwiednia → WIDMO obwiedni → wysokość piku przy BPFO/BPFI/BSF w TYM
widmie`. Dane, pliki, hashe — bez zmian (§2 v0.1). Częstotliwości
charakterystyczne — bez zmian (zweryfikowane w
`PREREG_CHRONO_MODAL_GEOMETRY_BRIDGE_v0.1.md` §2).

## 1. Wybór pasma rezonansu (zamrożony, a priori, BEZ podglądania różnic normal/fault)

**Kluczowa zasada uczciwości**: pasmo rezonansu wybierane WYŁĄCZNIE z
pliku `Normal` (zdrowego), PRZED jakimkolwiek porównaniem z plikami
uszkodzeń — bo rezonans strukturalny jest właściwością czujnika/
obudowy, nie samego uszkodzenia, więc wybór z sygnału zdrowego jest
metodologicznie uzasadniony i nie jest podglądaniem różnicy między
grupami (kryterium — kurtoza, maksimum impulsywności — nie zależy od
tego, jaki sygnał testowy będzie później porównywany).

```
CANDIDATE_BANDS = [(500,1000),(1000,1500),(1500,2000),(2000,2500),
                    (2500,3000),(3000,3500),(3500,4000),(4000,4500),
                    (4500,5000)]   # Hz, 9 pasm po 500Hz, 500-5000Hz

dla kazdego pasma (f_lo,f_hi):
    x_filt = bandpass_fft(x_DE_Normal, fs=12000, f_lo, f_hi)
    kurt = kurtoza_nadmiarowa(x_filt)     # scipy.stats.kurtosis, fisher=True (0=Gauss)

resonance_band = pasmo z MAKSYMALNA kurtoza
```

Zakres `500–5000 Hz` wybrany a priori: poniżej 500 Hz wchodzimy w
zasięg samych częstotliwości charakterystycznych (107–186 Hz z
pasmami) i ich niskich harmonicznych — filtr rezonansu musi być
WYRAŹNIE oddzielony od pasma poszukiwanego w widmie obwiedni, inaczej
demodulacja miesza się z sygnałem docelowym. Górna granica 5000 Hz —
poniżej Nyquista (6000 Hz przy fs=12000), z zapasem na filtr.

## 2. Metryka: wysokość piku w widmie obwiedni (zamrożona)

```
x_res(t) = bandpass_fft(x_DE, fs=12000, *resonance_band)     # to samo pasmo dla WSZYSTKICH 4 plikow
A(t) = |hilbert(x_res(t))|
A_c(t) = A(t) - mean(A(t))                                    # usuniecie skladowej DC przed FFT
Phi_env(f) = |rfft(A_c)| / len(A_c)                            # widmo amplitudowe obwiedni, znormalizowane

metric_s = max( Phi_env(f) dla f w [freq_s - 2, freq_s + 2] )  # okno +-2Hz wokol BPFO/BPFI/BSF
```

Okno `±2 Hz` (zamrożone a priori): przy `T_win=1.0s` rozdzielczość FFT
to dokładnie `1 Hz`, a częstotliwości charakterystyczne są
niecałkowite (107.364, 162.186, 141.169 Hz) — maksimum w oknie ±2Hz
zabezpiecza przed utratą piku między prążkami FFT, bez rozmycia na
sąsiednie, niezwiązane struktury (odstęp między BPFI i BSF to 21 Hz —
patrz ryzyko nakładania odnotowane w PREREG v0.1 modal_geometry §3.1,
tu NIE dotyczy bezpośrednio, bo szukamy tylko wysokości pojedynczego
prążka, nie całego pasma filtracyjnego).

## 3. Kontrole syntetyczne (zamrożone PRZED implementacją) — klasyczny sygnał testowy demodulacji

Standardowy sygnał testowy dla analizy obwiedniowej: powtarzające się,
wykładniczo tłumione impulsy (symulacja uderzenia defektu wzbudzającego
rezonans) w stałym okresie `T=1/f_target`, na tle szerokopasmowego
szumu.

```
f_target = 100 Hz (czestotliwosc "defektu" testowego, w skali fs_syn)
fs_syn = 5000 Hz
impuls(t) = exp(-t/tau) * sin(2*pi*f_res_syn*t),  tau=0.001s, f_res_syn=1200 Hz  # "rezonans" syntetyczny
sygnal(t) = suma impulsow w okresie T=1/f_target + bialy szum tla
```

- **(a) POZYTYWNA**: powyższy sygnał z impulsami przy `f_target=100Hz`.
  Przewidywanie: `Phi_env(100Hz)` (po pełnej demodulacji: filtr wokół
  `f_res_syn=1200Hz` wybrany przez kurtozę na TYM SAMYM sygnale — w
  syntetyce nie ma osobnego "pliku Normal", więc pasmo rezonansu
  wybierane z samego sygnału testowego, odnotowane jako różnica
  względem realnego pipeline'u, gdzie wybór jest z Normal) istotnie
  WYŻSZE niż w kontroli (b).
- **(b) NEGATYWNA**: czysty biały szum szerokopasmowy, bez żadnej
  periodyczności ani rezonansu. Przewidywanie: `Phi_env(100Hz)` niskie,
  bez systematycznej struktury.

`WINDOW_SIZES` syntetyczne (próbki) `{2500, 5000, 10000}` (0.5/1.0/2.0s
przy `fs_syn=5000Hz`), `N_WINDOWS=30`, `SEED=0`, `ALPHA=0.05`.
Mann-Whitney, oczekiwane `p<0.05`, `|r|≥0.3`, `median(a)>median(b)`.

## 4. Realne dane (URUCHAMIANE WYŁĄCZNIE, jeśli §3 przejdzie)

Bez zmian względem v0.1 §5-§6: te same 4 pliki, te same 3 pary
dopasowane (IR→BPFI, OR→BPFO, B→BSF), jednostronny test `"greater"`,
korekta Bonferroniego na 3, sprawdzenie stabilności połówkowej. Pasmo
rezonansu (§1) policzone RAZ z `Normal`, użyte identycznie dla
wszystkich czterech plików.

## 5. Status

Zamrożone. Kolejność: (1) rozszerzenie `core/modal_band_energy_bridge.py`
o wybór pasma rezonansu (kurtoza) i metrykę widma obwiedni (§1-§2); (2)
kontrole syntetyczne (§3), NAJPIERW; (3) jeśli PASSED: realne dane
CWRU (§4); (4) `docs/geometry/RESULT_MODAL_BAND_ENERGY_BRIDGE_v0.2.md`
z pełnym wynikiem, łącznie z ewentualnym kolejnym odrzuceniem, bez
retuningu po fakcie.
