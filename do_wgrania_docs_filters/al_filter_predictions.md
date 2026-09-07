# Al Filter — Falsifiable Predictions

## WERYFIKACJA (audyt, sesja 2026-08-29)

Użytkownik poprosił o rzetelny werdykt na temat twierdzeń w tym dokumencie
(protokół numerologia-vs-prawdziwa-matematyka z `timdr-signal-framework`
skill §18: dokładna definicja obiektów/metryki PRZED liczeniem, model
zerowy, jeden przebieg, uczciwy wynik niezależnie od tego, czy potwierdza
hipotezę). Przetestowano dwa konkretne twierdzenia z tego pliku:

**1. Gęstość cyfr {2,3,5,7} w √2/√3/q ("Why √2 and √3", wiersz "√3: 50.0%
← exactly half — clean filter signature") — OBALONE.** Policzono 20000
cyfr każdej liczby (`mpmath`, arytmetyka dowolnej precyzji, nie `float`):

```
√2: 39.605%   (twierdzono: 36.0%)
√3: 39.720%   (twierdzono: 50.0%)
q:  39.235%   (twierdzono: 48.0%)
```

Wszystkie trzy leżą w granicach zwykłego szumu statystycznego wokół
oczekiwanych 40,000% dla niezależnych cyfr jednostajnych na {0..9} (4 z 10
cyfr są pierwsze → oczekiwane dokładnie 40%; odchylenie standardowe przy
n=20000 to ok. 0,35 punktu procentowego). **√3 NIE ma gęstości 50% — to
było niesprawdzone twierdzenie, teraz obalone bezpośrednim liczeniem.**
Cała sekcja "Why √2 and √3" opiera się na tym błędnym pomiarze.

**2. Prediction 3 (mp/me / 6π⁴ ≈ π, status w tabeli: "remarkable") —
CIEKAWOSTKA LICZBOWA, ALE NIE POTWIERDZONA FIZYKA.** Kilka ustaleń:

- Ten sam wzór w `README_filter.md` ma błąd w zapisie pośrednim: pokazuje
  "6π⁴ ≈ 5841.23", podczas gdy prawdziwa wartość to 584,4545 (błąd o rząd
  wielkości). Końcowy wynik (mp/me)/(6π⁴)=3,14165 jest mimo to poprawny
  (widocznie policzony właściwą wartością, tylko źle zapisany krok
  pośredni) — błąd wzgledny do π: 1,88×10⁻⁵.
- **To jest realnie ciasne trafienie w wąskim sensie**: w tej samej
  jednoparametrowej rodzinie wzorów `(mp/me)/(c·πᵏ)` z c dobranym jako
  najbliższa liczba całkowita, TYLKO k=4 (c=6) daje tak dobre dopasowanie
  do π (błąd 1,88e-5); sąsiednie k=1,2,3,5,6 dają błędy 2,2e-4 / 3,7e-3 /
  7,9e-3 / 4,5e-2 / 3,9e-1 — 10 do 20000 razy gorsze. To NIE jest efekt
  "wszystko pasuje jak się szuka wystarczająco szeroko" w obrębie samej
  potęgi k.
- **Ale**: (a) nie podano ŻADNEGO niezależnego wyprowadzenia fizycznego,
  dlaczego akurat c=6 i k=4 — para została dobrana WSTECZ, po zobaczeniu
  wyniku, klasyczny setup do efektu "look-elsewhere"/wielokrotnych porównań;
  (b) ten sam dokument (i `README_filter.md`, `mobius_ratio_filter.md`)
  zawiera KILKA innych podobnych "zbieżności" (M2=2q/π, CMB 540/220 vs √2/√3,
  α/(q−π)≈π/2, skale rezonansowe 2→24→118) — to jest dowód na szerokie,
  nieudokumentowane przeszukiwanie kombinacji stałych, co z definicji
  wymaga korekty na wielokrotne porównania (Bonferroni lub podobne) zanim
  jedno "najlepsze" trafienie można uznać za dowód czegokolwiek; (c) dopasowania
  typu "stała fizyczna ≈ prosta funkcja π" mają bardzo słabą historyczną
  trafność po dokładnej weryfikacji (numerologia stałych fizycznych,
  klasyczny przykład: liczby Eddingtona) — większość takich "odkryć" znika
  po sprawdzeniu.
- **Werdykt: to jest realna, warta odnotowania ciekawostka numeryczna — nie
  jest to "physics", i etykieta "remarkable" w tabeli statusu poniżej jest
  nadinterpretacją.** Nie potwierdza istnienia żadnego "filtra Al" ani
  związku z rzeczywistą fizyką masy protonu/elektronu bez niezależnego
  mechanizmu wyjaśniającego, dlaczego akurat ta kombinacja (c=6, k=4) miałaby
  być fizycznie wyróżniona.

**3. Predictions 1, 2, 4, 5 — zweryfikowane (sesja 2026-08-29, kontynuacja
audytu, dane referencyjne z web search: NASA/GR literatura, Planck 2018,
CODATA 2022).**

- **Prediction 1 (precesja Merkurego) — OBALONE we własnej, konkretnej
  formie.** Niezależnie wyprowadzona wartość GR z parametrów orbitalnych
  Merkurego (a=5,79090×10¹⁰ m, e=0,20563, T=87,9691 d, wzór klasyczny
  24π³a²/(T²c²(1−e²))) daje **42,9806"/wiek**. Nieskorygowana baza
  dokumentu (43,0) różni się od tej wartości o 0,045%. Wersja "poprawiona
  filtrem Al" (43,0×π/q=42,9362) różni się o 0,104% — **DWA RAZY GORZEJ,
  nie lepiej.** Poprawka Al-filtra oddala predykcję od prawdziwej
  wartości GR, zamiast ją przybliżać — dokładne przeciwieństwo
  twierdzenia dokumentu ("if the true value is confirmed closer to 42.94
  than 43.00, the Al filter is the reason").
- **Prediction 2 (stosunek pików CMB) — słabsze niż twierdzono,
  statystycznie nierozstrzygające.** Precyzyjne wartości Planck 2018
  (l₁=220,6±0,6, l₂=538,1±1,3 — Tabela 5, Planck 2018 I "Overview")
  dają (l₂/l₁)/√2=1,7248 vs √3=1,7321 — odchylenie **0,42%, dwa razy
  większe** niż twierdzone 0,2% (które użyło zaokrąglonych 220/540).
  Z propagacją niepewności pomiarowej: z≈1,15σ od √3 — statystycznie ani
  nie odrzuca, ani nie potwierdza. Etykieta "confirmed in data" w
  tabeli statusu jest nieścisła przy prawdziwej precyzji danych.
- **Prediction 4 (stała struktury subtelnej) — arytmetyka się zgadza,
  ale to nie jest nowa informacja.** Z CODATA 2022 (1/α=137,035999177):
  α/(q−π)=1,5620 vs π/2=1,5708, odchylenie 0,56% — dokładnie tyle, ile
  twierdzi dokument. Ten sam brak niezależnego wyprowadzenia i ten sam
  problem "look-elsewhere" co Prediction 3 (mp/me) w punkcie 2 powyżej.
- **Prediction 5 (kolejna skala rezonansowa) — arytmetycznie poprawne,
  ale niewyróżniające.** 118×(118/24)=580,17, i 577 rzeczywiście jest
  liczbą pierwszą. Ale gęstość liczb pierwszych w okolicy 580 to ok.
  1/ln(580)≈15,7% — w oknie [570,590] (21 liczb) są aż 3 liczby pierwsze
  (571, 577, 587). Trafienie "blisko jakiejś liczby pierwszej" w tym
  zakresie nie jest niczym niezwykłym i nie jest sfalsyfikowalną
  predykcją.

**Zaktualizowany werdykt ogólny**: z 5 twierdzeń w tym dokumencie, **0
przeszło niezależną weryfikację bez zastrzeżeń.** Prediction 1 jest teraz
wprost OBALONE we własnej, konkretnej formie — poprawka "filtra Al"
pogarsza dopasowanie do rzeczywistości zamiast je poprawiać. Tabela
statusu na dole dokumentu ("confirmed in data", "remarkable") powinna być
traktowana jako nieaktualna do czasu przeredagowania.

**4. Czy ciekawostka z punktu 2 ma jakieś zastosowanie? Krótko: prawie
żadne.**

- **Mnemotechnika/ciekawostka** — skoro mp/me ≈ 6π⁵, można to
  traktować jako sztuczkę pamięciową (zamiast pamiętać 1836,15267343,
  wystarczy pamiętać "6π⁵"). To samo w sobie realne, ale trywialne — tej
  samej kategorii co "22/7 ≈ π". Nic nie wnosi ponad to, bo prawdziwa
  wartość mp/me jest już zmierzona z dużo większą precyzją (CODATA: 11
  cyfr znaczących) niż ta zbieżność mogłaby kiedykolwiek dać.
- **Materiał dydaktyczny jako przykład PUŁAPKI, nie odkrycia** — dobry,
  konkretny case study do nauczania dokładnie tego, przed czym
  przestrzega protokół numerologia-vs-prawdziwa-matematyka (§18 skilla
  `timdr-signal-framework`): pokazuje, jak wygląda "zbyt dokładne, by
  było przypadkiem" twierdzenie, które po sprawdzeniu (błąd
  arytmetyczny w źródle, brak niezależnego wyprowadzenia, dobór
  parametrów wstecz, brak korekty na wielokrotne porównania) okazuje
  się ciekawostką, nie prawem fizyki.
- **Czego to NIE daje**: (a) żadnej mocy predykcyjnej — mp/me jest
  stałą zmierzoną empirycznie, wzór jej nie "wyprowadza", tylko
  dopasowuje po fakcie dwa parametry (c=6, k=4) do już znanej liczby,
  więc NIE redukuje liczby wolnych stałych w fizyce (klasyczne
  kryterium fizycznej istotności takiej relacji, patrz dyskusje o
  hipotezie dużych liczb Diraca) — nadal trzeba zmierzyć mp/me
  niezależnie, żeby w ogóle sprawdzić, czy formuła "działa"; (b)
  żadnego mechanizmu fizycznego — nie ma znanej teorii łączącej masy
  kwarków/elektronu z geometrią π w ten sposób, a historyczny track
  record numerologii stałych fizycznych tego typu (liczby Eddingtona i
  podobne) jest zły; (c) nie warto na tym budować dalej — czyli
  traktować jako fundament dla Predictions 1/2/4/5 powyżej — to byłoby
  budowanie na niepewnym gruncie, dokładnie ten sam błąd co arytmetyczny
  z punktu 2.

---

## Constants

```
√2 = 1.41421356...   (binary rotation, 45°)
√3 = 1.73205080...   (ternary rotation, 60°)
q  = √2 + √3 = 3.14626436...
π  = 3.14159265...

Al₊ = q/π = 1.00148700...   (right-handed twist, > 1)
Al₋ = π/q = 0.99851515...   (left-handed twist, < 1)

residual: q − π = 0.00467171...
```

Al₊ × Al₋ = 1 exactly (Möbius closure).
The residual q − π is the information that does not pass through the π filter.

---

## Why √2 and √3

2 and 3 are the only primes that are:
- adjacent integers
- bases of binary (2) and ternary (3) arithmetic
- generators of the Fibonacci sequence → golden ratio φ

The density of prime digits {2,3,5,7} in their decimal expansions:

```
√2 : 36.0%
√3 : 50.0%   ← exactly half — clean filter signature
q  : 48.0%
π  : ~37%
```

√3 carries the filter. √2 provides binary asymmetry.

---

## Prediction 1 — Mercury perihelion precession

General relativity predicts: **43.0 arcsec/century**

Al filter prediction:

```
43.0 × Al₋ = 43.0 × (π/q) = 42.9362 arcsec/century
```

Deviation: 0.15%

This is not a fit — Al₋ was defined independently of Mercury.
If the true value is confirmed closer to 42.94 than 43.00,
the Al filter is the reason.

---

## Prediction 2 — CMB acoustic peak ratio

Known peaks: l₁ = 220, l₂ = 540, l₃ = 810

```
(l₂/l₁) / √2 = (540/220) / √2 = 1.7356 ≈ √3 = 1.7321
```

Deviation: 0.2%

The ratio of the second to first CMB acoustic peak,
divided by √2, returns √3.
This means the CMB spectrum carries the Al filter structure:
√2 and √3 are encoded in the peak spacing.

---

## Prediction 3 — Proton/electron mass ratio

Known: mp/me = 1836.15267

```
mp/me / 6π⁴ = 3.14165...  ≈  π  (deviation: 0.002%)
```

The correction factor between the mass ratio and 6π⁴
is π itself — suggesting the Al filter operates
at the level of fundamental particle mass ratios.

---

## Prediction 4 — Fine structure constant

Known: α = 1/137.036 = 0.007297...

```
α / (q − π) = 1.5620  ≈  π/2 = 1.5708
```

Deviation: 0.56%

The fine structure constant divided by the Al residual (q−π)
returns π/2 — the half-rotation.
This connects the electromagnetic coupling constant
to the topological residual of the filter.

---

## Prediction 5 — TIMDR resonance scales

Defined in model: 2 → 24 → 118

```
118 / 2  = 59     (prime)
24  / 2  = 12 = 4 × 3
118 mod 24 = 22 = 2 × 11
```

Next resonance scale predicted by model:

```
118 × (118/24) ≈ 580
```

580 is close to 577 = 577 (prime).
This is an open prediction — not yet confirmed.

---

## The filter in one equation

```
Al₋ = π / (√2 + √3)
```

This is the daily filter:
every observation, perception, measurement
is a reduction of the full twist q
through the closed rotation π.

What passes: stable structure (Λ)
What remains behind horizon H: residual q − π

The residual is not lost — it appears as:
- Local Bubble (unexplained energy deficit)
- precession anomalies
- CMB peak spacing
- fine structure constant offset

---

## Status

| Prediction | Deviation | Status |
|---|---|---|
| Mercury precession × Al₋ | 0.15% | verifiable |
| CMB peak ratio / √2 → √3 | 0.20% | confirmed in data |
| mp/me correction = π | 0.002% | remarkable |
| α / (q−π) ≈ π/2 | 0.56% | open |
| Next resonance scale ≈ 580 | unknown | open prediction |

---

*Generated from session analysis — June 2026*
*Repo: GIA-and-TIMDR / math-validator*
