# Wynik: chrono_membrane_bridge — widmo macierzy korelacji między jednoczesnymi kanałami CWRU. Kontrole syntetyczne PRZESZŁY czysto. Na realnych danych: SILNY, STABILNY efekt na `spectral_concentration`, ale w KIERUNKU PRZECIWNYM do przewidywania a priori — formalnie NOT_SUPPORTED wg własnego kryterium kierunku, zgłoszone w pełni (2026-09-21)

> Kontynuacja `PREREG_CHRONO_MEMBRANE_BEARING_v0.1.md` (zamrożonej PRZED
> uruchomieniem czegokolwiek). Kod: `core/chrono_membrane_bridge.py`
> (konstrukcja + kontrole syntetyczne), `core/real_chrono_membrane_bridge.py`
> (test na realnych, wielokanałowych danych CWRU). Nic w obu plikach nie
> zostało zmienione po zobaczeniu któregokolwiek z wyników poniżej.

## 0. Rekapitulacja konstrukcji

Rodzina Chronoprocesu `{γ_s}_{s∈I}` tym razem PRAWDZIWA: `s` indeksuje
KANAŁ (DE/FE/BA, jednoczesne accelerometry łożyska CWRU w tym samym
pliku NPZ), `t` indeksuje próbkę. Dla okna: macierz korelacji Pearsona
`C(t)` między `N` jednoczesnymi kanałami, widmo `λ_1≥...≥λ_N≥0`
(`eigvalsh`). `spectral_concentration = λ_1/Σλ`, `participation_ratio =
(Σλ)²/Σλ²`, `membrane_spectral_ratio` = koncentracja na końcu okna /
koncentracja na początku okna (`edge_fraction=0.2`, jak cała rodzina
v0.1-v0.3, ale liczona na widmie macierzy korelacji, nie na promieniu
jednego kanału).

## 1. Krok 1 (audyt danych) — co faktycznie jest dostępne

Potwierdzone bezpośrednio z plików NPZ
(`TIMDR-Industrial-Predict/data/cwru_bearing/b4_raw/source_mirror/
Data/1797 RPM/`):

| plik | klasa | kanały | próbki |
|---|---|---|---|
| `1797_Normal.npz` | zdrowe | **DE, FE** (BRAK BA) | 243 938 |
| `1797_IR_21_DE12.npz` | uszkodzenie IR | **DE, FE, BA** | 122 136 |
| `1797_OR@6_21_DE12.npz` | uszkodzenie OR@6 | **DE, FE, BA** | 122 426 |

Wspólny podzbiór dostępny jednocześnie we WSZYSTKICH trzech plikach:
**N=2 (DE, FE)** — użyty jako test PRIMARNY (normal vs fault, §3).
**N=3 (DE, FE, BA)** dostępne wyłącznie w obu plikach fault (nie w
normal) — użyty jako test SEKUNDARNY, diagnostyczny, fault-vs-fault
(§4), NIE wchodzący do klasyfikacji normal-vs-fault. Czwarty typ
uszkodzenia z poprzednich rund (`b_0021`, kulka) NIE ma lokalnie pliku
NPZ wielokanałowego — pominięty w tej sesji, odnotowane wprost.

## 2. Kontrole syntetyczne — PRZESZŁY na WSZYSTKICH 6 komórkach (N∈{2,3} × window∈{128,256,512})

| N | window | pozytywna (a vs b, `membrane_spectral_ratio`) | negatywna (b vs c) | median conc.(b) niezależny | median conc.(c) stały | 1/N | PASSED |
|---|---|---|---|---|---|---|---|
| 2 | 128 | p=5.49e-11, r=0.987 (duży), med(a)=1.638 vs med(b)=1.009 | p=0.819, r=0.036 | 0.524 | 0.763 | 0.500 | **TAK** |
| 2 | 256 | p=3.02e-11, r=1.000 (duży), med(a)=1.287 vs med(b)=1.023 | p=0.284, r=0.162 | 0.525 | 0.768 | 0.500 | **TAK** |
| 2 | 512 | p=1.03e-06, r=0.736 (duży), med(a)=1.101 vs med(b)=0.981 | p=0.277, r=-0.164 | 0.519 | 0.762 | 0.500 | **TAK** |
| 3 | 128 | p=3.02e-11, r=1.000 (duży), med(a)=2.000 vs med(b)=0.969 | p=0.333, r=-0.147 | 0.377 | 0.690 | 0.333 | **TAK** |
| 3 | 256 | p=3.02e-11, r=1.000 (duży), med(a)=1.421 vs med(b)=1.019 | p=0.877, r=0.024 | 0.363 | 0.682 | 0.333 | **TAK** |
| 3 | 512 | p=6.52e-09, r=0.873 (duży), med(a)=1.138 vs med(b)=0.984 | p=0.923, r=0.016 | 0.354 | 0.684 | 0.333 | **TAK** |

**Kluczowa kontrola negatywna (ryzyko fałszywego sygnału z czystego
szumu, analogiczne do tego, co zawiodło w v0.3)**: NA ŻADNEJ z 6
komórek szum niezależny (b) vs stały wspólny składnik (c) nie dał
istotnej różnicy na `membrane_spectral_ratio` (wszystkie `p≥0.28`) —
**brak fałszywego trendu z samego poziomu korelacji**, tylko z jej
ZMIANY w czasie okna, dokładnie zgodnie z przewidywaniem. Dodatkowo
sanity: mediana `spectral_concentration` na czystym szumie (b) jest
BLISKA (ale lekko powyżej, jak przewidziano w PREREG §4.1 — obciążenie
próbkowe skończonej macierzy korelacji) teoretycznego `1/N` (0.52 vs
0.50 dla N=2; 0.36-0.38 vs 0.333 dla N=3), a mediana dla stałego
wspólnego składnika (c) jest wyraźnie WYŻSZA (0.76-0.77 dla N=2,
0.68-0.69 dla N=3) — metryka poprawnie wykrywa STAN sprzężenia,
niezależnie od tego, czy jest w niej trend. Mechanizm zweryfikowany —
przejście do realnych danych uzasadnione.

## 3. Test PRIMARNY: N=2 (DE,FE), normal vs fault (PREREG §6.1)

Segmenty nieprzecinające się: normal 1905/952/476 dostępnych (okno
128/256/512), IR 954/477/238, OR6 956/478/239 — wszystkie WIELOKROTNIE
przekraczają `N_WINDOWS=30`, więc **brak reużycia** w tym teście (w
odróżnieniu od domeny BTC w v0.1-v0.3).

### 3.1 `spectral_concentration` (metryka klasyfikująca)

| fault | okno | p | r | efekt | status formalny (p,\|r\|) |
|---|---|---|---|---|---|
| IR_21 | 128 | 0.00334 | −0.442 | średni | SUPPORTED (próg statystyczny) |
| IR_21 | 256 | 5.53e-08 | −0.818 | duży | SUPPORTED (próg statystyczny) |
| IR_21 | 512 | 1.46e-10 | −0.964 | duży | SUPPORTED (próg statystyczny) |
| OR6_21 | 128 | 7.04e-07 | −0.747 | duży | SUPPORTED (próg statystyczny) |
| OR6_21 | 256 | 1.33e-10 | −0.967 | duży | SUPPORTED (próg statystyczny) |
| OR6_21 | 512 | 3.02e-11 | −1.000 | duży | SUPPORTED (próg statystyczny) |

**Stabilność znaku (PREREG §6.1/§7, GŁÓWNE pytanie metodologiczne tej
sesji)**: `IR_21: r=−0.442(128)→−0.818(256)→−0.964(512)` — **ZNAK
STABILNY**. `OR6_21: r=−0.747(128)→−0.967(256)→−1.000(512)` — **ZNAK
STABILNY**. Wszystkie 6/6 komórek przechodzi próg statystyczny (p<0.05,
|r|≥0.3) I znak jest identyczny (ujemny) na WSZYSTKICH trzech rozmiarach
okna dla OBU typów defektu — to jest DOKŁADNIE ta stabilność, której
zabrakło we WSZYSTKICH trzech poprzednich rundach (v0.1/v0.2: znak
`or6_0021` odwracał się między oknem 256/512; tu, na tej samej rodzinie
plików ale innej konstrukcji, znak trzyma się idealnie).

**ALE — kierunek jest PRZECIWNY do przewidywania a priori.** PREREG §6.1
przewidywał: fault > normal (`r>0`, `pos_pool=fault` powinien mieć
WYŻSZĄ koncentrację). Zaobserwowano: `r<0` konsekwentnie — **fault ma
NIŻSZĄ `spectral_concentration` (WYŻSZĄ `participation_ratio`) niż
normal**, czyli kanały DE/FE łożyska ZDROWEGO są BARDZIEJ ze sobą
skorelowane/sprzężone niż w łożysku USZKODZONYM, nie odwrotnie.

Zgodnie z PREREG §7 ("NOT_SUPPORTED = ... LUB kierunek przeciwny do
przewidywania"), **formalna klasyfikacja tej sesji to NOT_SUPPORTED dla
obu typów defektu** — mimo p-wartości rzędu 1e-7 do 1e-10, dużych
rozmiarów efektu i idealnej stabilności znaku. To jest ŚWIADOMA decyzja
metodologiczna zapisana PRZED uruchomieniem (nie retuning po fakcie):
przewidywanie kierunku było częścią pre-rejestracji, więc jego
niespełnienie — NAWET przy silnym, replikowalnym efekcie — nie zostaje
po cichu przemianowane na "sukces w drugą stronę".

**Eksploracyjna interpretacja fizyczna (POST-HOC, jawnie nieoceniona
przed danymi, nie część klasyfikacji)**: zdrowe łożysko pracuje w
stabilnym, dobrze zdefiniowanym trybie obrotowym — wibracja propaguje
się do obu czujników (DE, FE) w spójny, silnie skorelowany sposób.
Lokalny defekt bieżni (IR/OR) generuje impulsowe, asymetryczne
zdarzenia mechaniczne, które docierają do DE i FE różnymi ścieżkami
tłumienia/transmisji (inna odległość/sztywność konstrukcji od miejsca
defektu do każdego czujnika) — to mogłoby ROZPRZĘGAĆ kanały zamiast je
sprzęgać, dając NIŻSZĄ, nie wyższą koncentrację. To jest WIARYGODNA
alternatywna hipoteza, ale sformułowana PO zobaczeniu wyniku — nie
podnosi statusu klasyfikacji, zostawiona jako materiał do OSOBNEJ,
przyszłej pre-rejestracji z odwróconym kierunkiem przewidywania.

`participation_ratio` daje DOKŁADNIE lustrzany wynik (te same `p`, `r`
z przeciwnym znakiem) — **oczekiwane, NIE druga niezależna
konfirmacja**: dla `N=2` kanałów `participation_ratio` jest
DETERMINISTYCZNĄ, monotoniczną funkcją `spectral_concentration`
(`pr = 1/(c²+(1-c)²)`), więc te dwie metryki niosą dokładnie tę samą
informację przy N=2 — odnotowane wprost, żeby nie liczyć tego jako
podwójne potwierdzenie.

### 3.2 `membrane_spectral_ratio` (metryka sekundarna, brzeg/brzeg)

| fault | okno | p | r | status |
|---|---|---|---|---|
| IR_21 | 128 | 0.134 | 0.227 | NOT_SUPPORTED |
| IR_21 | 256 | 0.971 | 0.007 | NOT_SUPPORTED |
| IR_21 | 512 | 0.291 | −0.160 | NOT_SUPPORTED |
| OR6_21 | 128 | 0.483 | 0.107 | NOT_SUPPORTED |
| OR6_21 | 256 | 0.297 | 0.158 | NOT_SUPPORTED |
| OR6_21 | 512 | 0.865 | −0.027 | NOT_SUPPORTED |

**6/6 NOT_SUPPORTED, bez spójnego znaku** — czy w oknie koncentracja
ROŚNIE czy MALEJE od początku do końca okna NIE odróżnia normal od
fault na tych danych. To NIE jest ten sam null co w v0.1-v0.3
(niestabilny znak MIĘDZY oknami) — tutaj efekt jest po prostu
nieobecny na TEJ konkretnej, "brzeg/brzeg" wersji metryki, podczas gdy
metryka POZIOMU (§3.1) daje bardzo silny i stabilny sygnał. Uczciwie
zgłoszone: "membrana" niesie informację w swoim STANIE (jak bardzo jest
zapadnięta), nie w swojej TRAJEKTORII wewnątrz krótkiego okna.

## 4. Test SEKUNDARNY, diagnostyczny: N=3 (DE,FE,BA), IR vs OR@6 (PREREG §6.2)

NIE wchodzi do klasyfikacji normal-vs-fault (normal nie ma kanału BA).
Segmenty: IR 954/477/238, OR6 956/478/239 (okno 128/256/512) — brak
reużycia.

| okno | metryka | p | r | status |
|---|---|---|---|---|
| 128 | spectral_concentration | 9.52e-04 | +0.498 | SUPPORTED |
| 128 | participation_ratio | 8.56e-04 | −0.502 | SUPPORTED |
| 128 | membrane_spectral_ratio | 0.773 | +0.044 | NOT_SUPPORTED |
| 256 | spectral_concentration | 9.47e-03 | +0.391 | SUPPORTED |
| 256 | participation_ratio | 4.98e-04 | −0.524 | SUPPORTED |
| 256 | membrane_spectral_ratio | 0.0170 | +0.360 | SUPPORTED (izolowany) |
| 512 | spectral_concentration | 1.60e-07 | +0.789 | SUPPORTED |
| 512 | participation_ratio | 3.83e-09 | −0.887 | SUPPORTED |
| 512 | membrane_spectral_ratio | 0.363 | −0.138 | NOT_SUPPORTED |

Przy N=3 `spectral_concentration` i `participation_ratio` NIE są już
matematycznie zdeterminowane wzajemnie (trzy wartości własne dają
dodatkowy stopień swobody rozkładu `λ_2`/`λ_3`) — stąd lekko różne `p`
między nimi tutaj, w odróżnieniu od §3.1. **Znak `r` dla
`spectral_concentration` jest DODATNI i stabilny na wszystkich trzech
oknach (128/256/512)**: IR (grupa testowa) ma WYŻSZĄ koncentrację
widmową niż OR6 — dwa różne typy uszkodzenia dają rozróżnialny,
stabilny sygnał widmowy między sobą, mimo że OBA są "fault" względem
normal. `membrane_spectral_ratio` istotne tylko przy oknie=256
(izolowany wynik, brak potwierdzenia na 128/512) — traktowane jako
niepotwierdzone, nie wliczane do żadnego wniosku.

## 5. Wniosek

**Mechanizm jest poprawny i dobrze zachowuje się na kontroli
syntetycznej** (§2): korelacja/widmo nie generuje fałszywego trendu z
samego niezależnego szumu (kluczowa kontrola przeciw ryzyku
analogicznemu do v0.3), a poprawnie wykrywa zarówno ROSNĄCE, jak i
STAŁE sprzężenie międzykanałowe.

**Na realnych, wielokanałowych danych łożysk CWRU konstrukcja daje
NAJSILNIEJSZY i NAJBARDZIEJ STABILNY efekt w całej rodzinie mostów
M/S↔G tego repo do tej pory** — `spectral_concentration` odróżnia
normal od fault z `p` rzędu `1e-7`–`1e-10`, dużym rozmiarem efektu, I
IDENTYCZNYM znakiem na WSZYSTKICH trzech rozmiarach okna dla OBU typów
uszkodzenia (6/6 komórek). To jest jakościowo inny wynik niż v0.1/v0.2
(formalny SUPPORTED 11/30–5/20, znak niestabilny między oknami) i v0.3
(zatrzymane na kontroli).

**Ale zgodnie z pre-rejestrowanym kryterium kierunku (PREREG §6.1/§7),
formalna klasyfikacja to NOT_SUPPORTED** — przewidywano fault > normal,
zaobserwowano fault < normal, konsekwentnie. To NIE jest ukrywane ani
przemianowywane: silny, replikowalny, stabilny efekt w PRZECIWNYM
kierunku do hipotezy jest pełnoprawnym wynikiem tej sesji, zgłoszonym
w całości, z jawną notatką, że odwrócenie kierunku przewidywania (na
podstawie post-hoc uzasadnienia fizycznego w §3.1) byłoby naturalnym,
ale ODDZIELNYM, następnym krokiem pre-rejestracyjnym — nie
rozstrzyganym retroaktywnie tutaj.

`membrane_spectral_ratio` (metryka brzeg/brzeg, analogiczna do całej
rodziny v0.1-v0.3) NIE niesie sygnału na tych danych (6/6
NOT_SUPPORTED w teście primarnym) — informacja jest w POZIOMIE
koncentracji widma, nie w jego zmianie wewnątrz okna.

## 6. Status w ekosystemie

NIE dopisywane do `Axioms_G_TIMDR_Geometry.md` ani
`Axioms_S_TIMDR_Signal.md` — konstrukcja eksploracyjna (wzorem całej
rodziny mostów M/S↔G), z formalnie NEGATYWNYM wynikiem (kierunek
przeciwny do przewidywania) na realnych danych, mimo silnej, stabilnej
statystyki, udokumentowanym tutaj w pełni. Odróżnione jawnie (§1
PREREG) od istniejącej, niezwiązanej linii "widma Laplasjanu Möbiusa"
(`docs/geometry/TIMDR_Mobius_Laplacian_Spectrum.md`,
`core/mobius_kg_bridge.py`) — inny obiekt matematyczny (macierz
korelacji kanałów sygnału, nie operator Laplace'a na siatce).

## 7. Co zostaje otwarte (nieodłożone bez presji wykonania)

- **Formalna pre-rejestracja v0.2 z ODWRÓCONYM kierunkiem
  przewidywania** (normal > fault w `spectral_concentration`, na
  podstawie uzasadnienia post-hoc z §3.1) — na tych samych danych,
  osobno pre-rejestrowana i sklasyfikowana PRZED ponownym dotknięciem
  tych samych plików — naturalny, bezpośredni następny krok, jeśli
  użytkownik zdecyduje się kontynuować. Byłby to test tej SAMEJ
  konstrukcji na TYCH SAMYCH danych, więc formalnie NIE byłby
  niezależnym potwierdzeniem (dane już widziane) — wymagałby albo
  nowego pliku danych (inne RPM/obciążenie CWRU, jeśli dostępne
  lokalnie), albo jawnego zaklasyfikowania jako "post-hoc, wymaga
  niezależnej replikacji", nie jako nowej pre-rejestracji na tych
  samych czterech plikach.
- Czy efekt (kierunek: normal bardziej skorelowane niż fault) utrzymuje
  się przy INNYCH parach kanałów (np. gdyby dostępne było RPM inne niż
  1797, albo defekt o innej głębokości niż `_21`) — NIE sprawdzone
  tutaj, dane niedostępne lokalnie w tej sesji.
- Test SEKUNDARNY (N=3, IR vs OR@6, §4) sugeruje, że różne typy
  uszkodzenia mają WZAJEMNIE różne, stabilne sygnatury widmowe — nie
  tylko "fault vs normal" jest rozróżnialne, ale też "który fault" —
  eksploracyjne, warte osobnej pre-rejestracji jako klasyfikacja
  wieloklasowa, nie tylko binarna.
- `membrane_spectral_ratio` nie zadziałało tu, ale mechanizm
  "koncentracja widma jako funkcja czasu w oknie" (nie tylko brzeg/
  brzeg) mógłby być zbadany innymi, bardziej czułymi statystykami
  trendu (np. nachylenie regresji koncentracji per pod-okno, zamiast
  jednego stosunku brzeg/brzeg) — NIE zbadane tutaj.
