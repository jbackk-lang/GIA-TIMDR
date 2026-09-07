# Chronoproces Ξ=(T,x,Γ,φ) — most między trzema gałęziami TIMDR

> **Status: konstrukcja formalna z działającym, testowalnym kodem w
> czterech repo-siostrach — wszystkie cztery mają teraz potwierdzone
> przez użytkownika przejście testów (patrz §6 niżej). Nie jest to
> rozszerzenie żadnej gałęzi ani nowy zestaw aksjomatów — żadna z
> istniejących aksjomatyzacji (Axioms_S/G/K) nie została zmieniona.**

## Geneza

Sekcja 7.3 głównego README (`t_lokalne=f(τ_globalne)`) od dawna
postulowała, że czas lokalny jest projekcją stanu globalnego pola —
ale bez formalnej definicji `f`. Pierwsza próba uogólnienia tego na
trzy gałęzie TIMDR (M/S, G, K) na raz — "czas jako powierzchnia
zakrzywiona w G, czas jako moduł w K" — miała realny błąd: pojedyncza
trajektoria czasu jest krzywą 1D, nie ma operatora kształtu (błąd
kategorii, nie literówka), a `f` w K było postulowane bez żadnej
definicji dziedziny/przeciwdziedziny. Konstrukcja poniżej to poprawka
tamtej próby — zbudowana tak, żeby nie łamać zasady nieredukowalności
gałęzi z `TIMDR_Branch_Specification.md`.

## 1. Nośnik T i trzy niezależne rzuty

`T` — uporządkowany zbiór chwil (np. znaczniki czasu). To NIE jest
"czas" żadnej gałęzi — czysty indeks, czytany inaczej przez każdą z
nich. Chronoproces:

```
Ξ = (T, x, Γ, φ)
  x: T → ℝᵈ           -- gałąź M/S
  Γ: T×I → ℝ³          -- gałąź G (I: domena "sąsiednich" trajektorii)
  φ: T → (f,φ,A)       -- gałąź K
```

**Żadnej identyfikacji między rzutami.** Chronoproces nie twierdzi, że
"czas" jest tym samym obiektem matematycznym w M/S, G i K — to byłby
dokładnie błąd, przed którym chronią `TIMDR_Branch_Specification.md` i
`TIMDR_Twists.md`. Kod: `TIMDR-Time-Formalism/timdr_time/chronoprocess.py`
— trzy oddzielne metody dostępowe, zero logiki spinającej wyniki jednej
gałęzi z drugą (jedyny, jawnie wyodrębniony wyjątek: §5 niżej).

## 2. Rzut M/S — tempo i drift

`tempo(t)=t[i+1]-t[i]`, `drift(t)=tempo_zmierzone(t)-tempo_nominalne`
(wymaga jawnego zegara referencyjnego). Czysta reinstancja istniejącego
obiektu `x:T→ℝᵈ` z `Axioms_S_TIMDR_Signal.md` — **zero nowych
aksjomatów**. Detektory anomalia/defekt/skręt z §1 skilla
`timdr-signal-framework`, zastosowane wprost do tempa/driftu.

**Kod:** `TIMDR-Math-Formalism/timdr_formalism/chronosignal.py`.

## 3. Rzut G — kongruencja Γ(t,s)

Naprawa błędu z genezy: pojedyncza trajektoria (krzywa 1D) nie ma
operatora kształtu. Potrzeba RODZINY trajektorii `{γ_s}_{s∈I}`,
`Γ(t,s)=γ_s(t)`, żeby obraz `S=Γ(T×I)⊂ℝ³` był prawdziwą powierzchnią
2D — wtedy `n(p)`, `S_p`, `T_S(p)` z Aksjomatów G3/G8/G9 działają
dosłownie, bez metafory. Trzy kanoniczne przykłady o znanej
analitycznie krzywiźnie (płaska/walcowa/sferyczna kongruencja) — domena
`I` (co dokładnie parametryzuje "sąsiednie" trajektorie) zostaje
decyzją modelową, nie matematycznym rozstrzygnięciem.

**Analogia, nie równoważność:** konstrukcja odpowiada matematyce
kongruencji geodezyjnych w OTW (ekspansja/ścinanie/skręt, równanie
Raychaudhuriego) — krzywizna kongruencji mówi o zbieżności/rozbieżności
sąsiednich procesów w czasie. Rozkład θ/σ/ω **NIE jest zaimplementowany
ani wyprowadzony** — to była wskazana analogia uzasadniająca sensowność
`T_S` tutaj, nie twierdzenie o równoważności.

**Kod:** `TIMDR-Geometry-Formalism/timdr_geometry/chronocongruence.py`.

**Powiązanie z Aksjomatem G10 (dodany później, ta sama sesja).** Jeden
generator `γ_s` rodziny `{γ_s}` — pojedyncza trajektoria 1D — może być
czytany jako obwiednia w sensie G10 (`Axioms_G_TIMDR_Geometry.md`):
`(P,Q)` z G10b charakteryzowałoby TĘ JEDNĄ krzywą (jej udział
prostoliniowy/łukowy), podczas gdy `T_S`/`W_S` z G3/G8/G9
charakteryzuje POWIERZCHNIĘ `S=Γ(T×I)` powstałą z CAŁEJ rodziny — dwa
różne, uzupełniające się poziomy (krzywa vs. rodzina krzywych/
powierzchnia), nie to samo pojęcie pod dwiema nazwami. To jest
obserwacja strukturalna, NIE zaimplementowana i nie wymagana przez
istniejący kod `chronocongruence.py` — zero zmian w Ξ, zgodnie z
zasadą "zero nowych aksjomatów" tego dokumentu (G10 sam jest
aksjomatem gałęzi G, nie częścią Chronoprocesu).

## 4. Rzut K — mapa synchronizacji faz f

Formalizuje dosłownie `t_lokalne=f(τ_globalne)` z §7.3 głównego README:
dwie modalności `(f,φ,A)` (Aksjomat 3), lokalna i globalna; `f` znajduje
taki `t_lokalne`, przy którym faza chwilowa `θ(t)=2πft+φ` (argument
sinusa z Aksjomatu 4) oscylatora lokalnego zrównuje się z fazą chwilową
globalnego w chwili `τ_globalne`:

```
t_lokalne = (f_globalne/f_lokalne)·τ_globalne + (φ_globalne-φ_lokalne)/(2π·f_lokalne)
```

**Granica zakresu:** ta mapa jest AFINICZNA, bo Aksjomaty K3/K4
modelują modalność jako oscylator o stałych parametrach, nie sprzężony
(Kuramoto-style). Pełniejsza, nieliniowa wersja wymagałaby rozszerzenia
`Axioms_K_TIMDR.md` o dynamikę sprzężenia — jawnie NIE zrobione tutaj.
Zero nowych aksjomatów; K miało dotąd zero implementacji kodu w ogóle,
to jest pierwsza.

**Kod:** `TIMDR-Modal-Formalism/timdr_modal/phase_sync.py`.

## 5. Most Fouriera M/S↔K — jedyny wyjątek od nieredukowalności

Dualizm falowo-cząsteczkowy fotonu ma dokładne źródło matematyczne:
zasada nieoznaczoności Heisenberga ma tę samą strukturę co klasyczna
zasada nieoznaczoności Gabora dla sygnałów. `x(t)` z M/S ("cząstka" —
dokładna lokalizacja w czasie) i modalność `(f,φ,A)` z K ("fala" —
dokładna lokalizacja w częstotliwości) są połączone KONKRETNĄ, znaną
transformatą (FFT), nie utożsamione — to jedyny, jawnie oznaczony
wyjątek od zasady "zero mostów" z §1.

Wyprowadzono ręcznie w tej sesji (nie przepisane z pamięci): dla
impulsu gaussowskiego `Δt·Δf=1/(4π)` dokładnie, niezależnie od
szerokości impulsu — granica Gabora/Heisenberga OSIĄGANA (nie tylko
spełniona). Pełne wyprowadzenie w nagłówku pliku źródłowego.

**Kod:** `TIMDR-Time-Formalism/timdr_time/fourier_bridge.py`.

## 6. Status uczciwie

| Element | Repo | Wykonanie |
|---|---|---|
| M/S: tempo/drift | `TIMDR-Math-Formalism` | ✅ **62/63 pytest, potwierdzone przez użytkownika** (1 błąd niezwiązany: lokalny `PermissionError` katalogu tymczasowego Windows, nie kod tego projektu) |
| G: kongruencja Γ(t,s) | `TIMDR-Geometry-Formalism` | ✅ **17/17 pytest, potwierdzone przez użytkownika** (w tym istniejące wcześniej testy Weingartena) |
| K: mapa synchronizacji f | `TIMDR-Modal-Formalism` | ✅ **17/17 pytest, potwierdzone przez użytkownika** (1 test najpierw padł z powodu błędu float w samym teście, nie w kodzie — naprawiony, patrz `tests/test_phase_sync.py`) |
| Ξ: orkiestracja | `TIMDR-Time-Formalism/chronoprocess.py` | ✅ **8/8 pytest, potwierdzone przez użytkownika** (import między trzema repo-siostrami + wszystkie trzy delegacje) |
| Most Fouriera | `TIMDR-Time-Formalism/fourier_bridge.py` | ✅ **10/10 pytest, potwierdzone przez użytkownika** (część jednotonowa dokładna algebrą + część gaussowska w szerokich tolerancjach ±30%) |

Wszystkie cztery repo-siostry mają teraz potwierdzone przez użytkownika
przejście testów — łącznie 62/63 + 17/17 + 17/17 + 18/18.

## Powiązane

- [`TIMDR_Branch_Specification.md`](TIMDR_Branch_Specification.md) —
  zasada nieredukowalności, którą ta konstrukcja respektuje.
- [`TIMDR_Twists.md`](TIMDR_Twists.md) — dyscyplina "to samo słowo,
  inny obiekt", ten sam duch co §1 powyżej.
- [`Axioms_S_TIMDR_Signal.md`](Axioms_S_TIMDR_Signal.md),
  [`Axioms_G_TIMDR_Geometry.md`](Axioms_G_TIMDR_Geometry.md),
  [`Axioms_K_TIMDR.md`](Axioms_K_TIMDR.md) — żadna nie zmieniona przez
  ten dokument.
- Główne README, §7.3 "Czas lokalny jako projekcja τ globalnego" —
  oryginalny postulat, który §4 powyżej formalizuje.
- `GIA-TIMDR/SKILL_timdr-signal-framework.md` §4 — skrót tej
  konstrukcji w formie wzorca wielokrotnego użytku.
