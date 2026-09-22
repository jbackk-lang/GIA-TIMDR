# Pre-rejestracja: chrono_modal_geometry_bridge — most K→G, obwiednie trzech rezonansów łożyska jako trajektoria 3D (krzywizna/skręt)

> Status: PRE-REJESTRACJA, zamrożona PRZED dotknięciem jakichkolwiek
> danych (kod jeszcze nie napisany w chwili zapisania tego dokumentu).
> Data: 2026-09-22. Pierwsza formalizacja mostu K→G w tej sesji —
> wcześniej ten kierunek istniał w katalogu mostów tylko jako opis
> intuicyjny ("rezonans→krzywizna"), bez jawnego wzoru. NIE reużywa
> `chrono_sphere_bridge` (odrzucony v0.1/v0.2, patrz `RESULT_
> CHRONO_SPHERE_BRIDGE_v0.2.md`) — inny obiekt geometryczny (krzywizna/
> skręt Freneta-Serreta na trajektorii w ℝ³, nie kierunek+promień na
> S² z ważoną prędkością kątową), ale dzieli z nim TEN SAM
> zdiagnozowany rodzaj ryzyka (saturacja przy dominacji jednego
> wymiaru), sprawdzany tu jawnie jako osobna kontrola (§5.2), nie
> zakładany za bezpieczny z powodu innego wzoru.

## 0. Skąd to się bierze

Domknięcie mostu K→G z katalogu mostów Chronoprocesu
(ustalonego w tej sesji): wejście — widmo `Φ(f)` jednego kanału M/S;
wyjście — obiekt geometryczny gałęzi G (krzywizna `κ`, skręt `τ`,
kierunek `u(t)`). Łańcuch przekształceń:

```
Φ(f)  --filtr pasmowy-->  Φ_res,s(f)   (s = 1..3, trzy pasma)
Φ_res,s(f)  --odwrotna FFT + obwiednia Hilberta-->  A_s(t)
A_s(t)  --zanurzenie-->  Γ(t,s) = A_s(t)·e_s  ⊂ ℝ³
Γ(t,s)  --geometria Freneta-Serreta-->  κ(t), τ(t)
```

**Dlaczego dokładnie 3 pasma, nie 4**: łożysko CWRU ma cztery
udokumentowane częstotliwości charakterystyczne (BPFO, BPFI, BSF,
FTF — §2). Wybrane tu **BPFO, BPFI, BSF** — bezpośrednio odpowiadają
trzem fizycznym miejscom uszkodzenia testowanym w tej serii (bieżnia
zewnętrzna, bieżnia wewnętrzna, kulka — dokładnie te same trzy pliki
CWRU co w `chrono_sphere_bridge` §6). FTF (częstotliwość koszyka) jest
pominięta — to częstotliwość modulacji/sidebandów, nie bezpośredni
wskaźnik konkretnego uszkodzenia, i dawałaby czwarty wymiar, w którym
klasyczne wzory Freneta-Serreta (zdefiniowane dla ℝ³) przestają być
jednoznaczne bez dodatkowych uogólnień — pominięta celowo, żeby
uniknąć tej komplikacji w v0.1, nie przez przeoczenie.

**Realizacja obietnicy z krytyki mostu G→K/sfera**: `s` indeksuje
PASMA CZĘSTOTLIWOŚCI wydobyte z JEDNEGO kanału (DE), nie fizyczne
kanały DE/FE/BA — więc `Normal` (który ma DE) wchodzi do porównania,
w odróżnieniu od sfery.

## 1. Audyt nazw PRZED użyciem

Grep na całym `GIA-TIMDR`: `chrono_modal_geometry`, `modal_geometry_bridge`,
`frenet`, `curvature_from_envelope` — **zero kolizji**. `κ`/`τ` jako
nazwy zmiennych nie kolidują z istniejącym `Axioms_G_TIMDR_Geometry.md`
(tamtejsza krzywizna to operator Weingartena na siatce 2D, inny obiekt
matematyczny — skręt powierzchniowy z G8/G9, nie krzywizna/skręt
krzywej 1D w ℝ³ — rozróżnienie odnotowane wprost, jak przy każdym
poprzednim moście).

## 2. Częstotliwości charakterystyczne łożyska CWRU (zweryfikowane, nie z pamięci)

Geometria łożyska drive-end SKF 6205-2RS JEM (źródło: dokumentacja
CWRU Bearing Data Center, zweryfikowana wyszukiwaniem 2026-09-22, nie
przyjęta z pamięci): **N=9 kulek, d=7.94 mm (średnica kulki), D=39.04
mm (średnica podziałowa), kąt kontaktu θ=0°**.

Standardowe wzory kinematyki łożyska tocznego (`fr` = częstotliwość
obrotowa wału):

```
BPFO = (N/2)·fr·(1 - (d/D)·cosθ)      # bieżnia zewnętrzna
BPFI = (N/2)·fr·(1 + (d/D)·cosθ)      # bieżnia wewnętrzna
BSF  = (D/d)·fr·(1 - ((d/D)·cosθ)²)   # kulka, konwencja "2x" (dwa kontakty na obrot kulki wzgledem koszyka)
FTF  = (fr/2)·(1 - (d/D)·cosθ)        # koszyk (NIE uzywane w v0.1, patrz SS0)
```

**Uwaga o konwencji BSF, zapisana wprost**: istnieją w literaturze dwie
konwencje (pojedyncza częstotliwość obrotu kulki względem koszyka, i
podwojona — dwa kontakty z bieżniami na jeden obrót kulki). Tu przyjęta
konwencja "2x" (powszechniejsza w cytowanej literaturze diagnostyki
łożysk), policzona i zweryfikowana zgodnością mnożnika z niezależnie
znalezionym źródłem (§ poniżej).

Dla `RPM=1797` (fr=1797/60=29.9500 Hz), policzone bezpośrednio z
powyższych wzorów (zweryfikowane zgodnością mnożnika z niezależnym
źródłem internetowym, które podało mnożniki 3.585/5.415/4.714 bez
podania jednostek Hz — zgodność do 4 cyfr znaczących):

| częstotliwość | mnożnik ×fr | wartość przy 1797 RPM |
|---|---|---|
| BPFO | 3.5848 | **107.364 Hz** |
| BPFI | 5.4152 | **162.186 Hz** |
| BSF (2x) | 4.7135 | **141.169 Hz** |
| FTF (nieużywane) | 0.3983 | 11.929 Hz |

## 3. Konstrukcja (zamrożona)

### 3.1 Pasma (zamrożone z góry, z geometrii, nie "na oko")

Szerokość względna pasma: **±15% częstotliwości środkowej** (konwencja
standardowa w analizie obwiedniowej/demodulacji rezonansów — pasmo na
tyle szerokie, żeby objąć sidebandy modulacji defektu, na tyle wąskie,
żeby nie mieszać sąsiednich częstotliwości charakterystycznych, które
przy tej geometrii są oddalone o >30% od siebie nawzajem — sprawdzone:
BPFO=107.4, BPFI=162.2, BSF=141.2 Hz, minimalny odstęp
|BSF-BPFI|=21.0 Hz > 15%·141.2=21.2 Hz — **na granicy, odnotowane
wprost jako ryzyko częściowego nakładania się pasm BSF/BPFI**, nie
ukryte):

```
pasmo_BPFO = [107.364·0.85, 107.364·1.15] = [91.26, 123.47] Hz
pasmo_BPFI = [162.186·0.85, 162.186·1.15] = [137.86, 186.51] Hz
pasmo_BSF  = [141.169·0.85, 141.169·1.15] = [120.00, 162.34] Hz
```

**Nakładanie pasm BPFI i BSF przy górnej/dolnej granicy jest realne
(162.34 vs 137.86-186.51) — odnotowane jako znane ograniczenie
konstrukcji v0.1, nie naprawiane retroaktywnie zmianą szerokości po
zobaczeniu tego nakładania (szerokość ±15% była ustalona PRZED
policzeniem konkretnych granic pasm).** Jeśli bramka niezależności
(§3.3) odrzuci nadmierną liczbę okien z tego powodu, będzie to
zgłoszone jako diagnoza, nie obejście.

### 3.2 Filtr pasmowy + obwiednia Hilberta

Dla kanału `x_DE(t)` na oknie: FFT `Φ(f) = FFT(x_DE)`, maskowanie w
dziedzinie częstotliwości (zera poza pasmem — unika wyboru rzędu
filtru IIR/FIR, czysto FFT-domenowe), odwrotna FFT daje przefiltrowany
sygnał czasowy `x_res,s(t)`, transformata Hilberta daje obwiednię
`A_s(t) = |hilbert(x_res,s(t))|`.

**Decymacja obwiedni (zamrożona z góry)**: `A_s(t)` liczona przy pełnym
`fs=12000 Hz` jest silnie nadpróbkowana względem pasma szerokości rzędu
dziesiątek Hz — decymacja do `fs_env=500 Hz` (współczynnik 24), przed
liczeniem różnic skończonych w §3.4, żeby uniknąć sytuacji, w której
kolejne próbki trajektorii są niemal identyczne (szum numeryczny
dominowałby nad prawdziwą krzywizną).

### 3.3 Bramka niezależności (reużyta z chrono_sphere_bridge, ten sam kod)

Na trzech obwiedniach `(A_BPFO, A_BPFI, A_BSF)` (po decymacji): macierz
korelacji, `λ_1/Σλ<0.9` — reużywa `channel_correlation_matrix`/
`spectrum_from_correlation`/`spectral_concentration` z
`timdr_geometry.spectral_family`, identyczny mechanizm jak przy sferze.
Okno odrzucone, jeśli nie przejdzie.

### 3.4 Trajektoria i geometria Freneta-Serreta

```
Γ(t,s) = A_s(t)·e_s,   e_1=(1,0,0), e_2=(0,1,0), e_3=(0,0,1)   (s=BPFO,BPFI,BSF)
```

Różnice skończone centralne na zdecymowanej trajektorii (krok `Δ`,
jedna próbka po decymacji):

```
γ'(t)   ≈ (Γ(t+Δ) - Γ(t-Δ)) / (2Δ)
γ''(t)  ≈ (Γ(t+Δ) - 2Γ(t) + Γ(t-Δ)) / Δ²
γ'''(t) ≈ (Γ(t+2Δ) - 2Γ(t+Δ) + 2Γ(t-Δ) - Γ(t-2Δ)) / (2Δ³)     (standardowa piata-punktowa)

κ(t) = ‖γ'(t) × γ''(t)‖ / ‖γ'(t)‖³
τ(t) = [(γ'(t) × γ''(t)) · γ'''(t)] / ‖γ'(t) × γ''(t)‖²
```

**Obsługa degeneracji (zamrożona, nie dobrana po zobaczeniu danych)**:
gdy `‖γ'(t)‖ < ε_1` (trajektoria lokalnie nieruchoma — floor
`ε_1=1e-6` w jednostkach obwiedni) LUB `‖γ'×γ''‖ < ε_2` (trajektoria
lokalnie prosta — `ε_2=1e-9`): `κ(t)=0` z konwencji (odcinek prosty ma
krzywiznę zero — to jest matematycznie poprawna granica, NIE
maskowanie wyniku), `τ(t)` odnotowane jako brak wartości (skręt
odcinka prostego jest formalnie nieokreślony, nie zero) — te punkty
WYKLUCZONE z agregacji `τ`, ale WŁĄCZONE (jako 0) do agregacji `κ`.

## 4. Metryki okna (zamrożone)

Dla każdego okna: `κ_win = mediana(κ(t))`, `τ_win = mediana(τ(t)
ważnych)` po WYKLUCZENIU okien odrzuconych przez bramkę §3.3. Mediana
(nie średnia) — odporność na ewentualne pojedyncze duże wartości przy
`‖γ'‖` bliskim, ale nie poniżej, progu `ε_1`.

## 5. Kontrole syntetyczne (zamrożone PRZED implementacją)

### 5.1 Bramka sanity (jak w sferze) — trzy skorelowane obwiednie

Trzy "obwiednie" będące niemal kopiami tego samego sygnału + znikomy
szum — bramka §3.3 powinna odrzucić ≥90% takich okien. Zatrzymanie,
jeśli nie przejdzie, PRZED testem głównym.

### 5.2 Test główny — dominujący rezonans (kontrola RYZYKA saturacji, DWUSTRONNA)

**Kontrola (b) NEGATYWNA/tło**: trzy niezależne obwiednie o podobnej,
stałej średniej amplitudzie i niezależnym szumem wokół niej (symulacja
"żadne pasmo nie dominuje").

**Kontrola (a) — dominujący rezonans**: jedna obwiednia (np. `A_1`,
odpowiadająca BPFO) dostaje istotnie podwyższoną, zmienną w czasie
amplitudę względem pozostałych dwóch (symulacja "jedno pasmo
dominuje", fizycznie odpowiadające aktywnemu uszkodzeniu w tej
lokalizacji) — POZOSTAŁE dwie obwiednie niezmienione względem (b).

**Test DWUSTRONNY, kierunek NIE przewidziany a priori** — w
odróżnieniu od poprzednich preregów tej serii, tu jawnie NIE zakładamy
z góry, że `κ_win(a) > κ_win(b)`. Powód zapisany wprost: krytyka mostu
G→K (§0) wykazała konkretny mechanizm, w którym dominacja jednego
wymiaru SPŁASZCZA geometrię (trajektoria prostuje się wzdłuż jednej
osi, krzywizna → 0) — to jest REALNA, znana hipoteza konkurencyjna
wobec "dominujący rezonans = wyższa krzywizna", nie hipoteza zerowa do
odrzucenia z góry. Obie możliwości są zapisane jako sensowne wyniki:

- **`κ_win(a) > κ_win(b)`, istotne**: dominujący rezonans WZBOGACA
  geometrię trajektorii (bo wprowadza silną, ale NIE zdegenerowaną
  strukturę czasową w jednym wymiarze, podczas gdy pozostałe dwa dają
  krzywiznę z ich interakcji) — most K→G przez Freneta-Serreta
  DZIAŁA w kierunku przeciwnym do tego, co zawiodło przy sferze.
- **`κ_win(a) < κ_win(b)`, istotne**: TEN SAM mechanizm saturacji co
  przy `chrono_sphere_bridge` — dominacja spłaszcza geometrię
  niezależnie od konkretnego wzoru (kierunek na S² czy krzywizna w
  ℝ³) — most K→G ODRZUCONY, DRUGI niezależny dowód na tę samą
  strukturalną słabość, tym razem w innej konstrukcji matematycznej.
- **brak istotnej różnicy**: metryka nieczuła na to rozróżnienie w
  ogóle.

Mann-Whitney U (`alternative="two-sided"`) + rank-biserial `r` na
`κ_win`, ten sam test na `τ_win` (osobno, bez łączenia — `τ` ma inną
interpretację niż `κ`, nie sumowana z nią). `SUPPORTED` (w
którymkolwiek kierunku) = `p<0.05`, `|r|≥0.3`; wynik zgłoszony z
jawnym kierunkiem, nie tylko "istotne/nieistotne".

**Siatka**: `WINDOW_SIZES` syntetyczne (obwiednie po decymacji, jednostki
próbek zdecymowanych) `{250, 500, 1000}` (odpowiadające ~0.5s/1.0s/2.0s
przy `fs_env=500Hz`), `N_WINDOWS=30`, `SEED=0`, `ALPHA=0.05`.

## 6. Realne dane (URUCHAMIANE WYŁĄCZNIE, jeśli §5 przejdzie z jednoznacznym kierunkiem)

Kanał `DE` z czterech plików 1797 RPM/0.021" (`Normal`, `IR_21`,
`OR@6_21`, `B_21` — wszystkie mają DE). Okno `T_win=1.0s` (12000
próbek przed decymacją, §3.2). Trzy porównania: **Normal vs IR_21**,
**Normal vs OR@6_21**, **Normal vs B_21** — w odróżnieniu od sfery,
Normal WCHODZI do testu (§0), bo `s` nie wymaga kanału BA.

**Przewidywanie kierunku dla realnych danych ustalane DOPIERO po
wyniku kontroli §5.2** (nie da się ustalić teraz, uczciwie — sama
kontrola ma rozstrzygnąć, w którą stronę idzie efekt; to jest
jawnie odnotowane odstępstwo od wcześniejszych preregów tej serii,
uzasadnione tym, że tu mamy dwie konkurencyjne, fizycznie sensowne
hipotezy, nie jedną). Korekta Bonferroniego dla 3 porównań × 2 metryki
(κ,τ) = 6 testów: `α_corr=0.05/6≈0.0083`.

## 7. Status

Zamrożone. Kolejność: (1) `core/chrono_modal_geometry_bridge.py` —
konstrukcja + bramka sanity + kontrola dominującego rezonansu (§5),
NAJPIERW; (2) jeśli §5.2 da jednoznaczny, stabilny kierunek (dowolny):
`core/real_chrono_modal_geometry_bridge.py` na DE z czterech plików
CWRU (§6); (3) `docs/geometry/RESULT_CHRONO_MODAL_GEOMETRY_BRIDGE_v0.1.md`
z pełnym wynikiem, łącznie z odrzuceniem, jeśli §5.2 potwierdzi
mechanizm saturacji zamiast wzbogacenia.
