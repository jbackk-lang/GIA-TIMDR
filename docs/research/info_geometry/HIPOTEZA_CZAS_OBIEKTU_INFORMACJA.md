# Hipoteza czasu obiektu i czasu obserwatora jako składnika informacji

**Data:** 2026-11-14. **Status:** hipoteza formalna i program falsyfikacji; nie aksjomat, nie wynik empiryczny.

## Motywacja autora

Badamy sygnał *w czasie*. Trzecia cecha reprezentacji MIN–MAX–CZAS może odzwierciedlać deltę wynikającą z czasu badanego obiektu i niosącą informację o jego przebiegu. To może oznaczać, że relacja czasowa jest niezbędnym składnikiem opisu informacji dynamicznej. Nie utożsamiać tego z dowodem, że czas jest konieczny dla **każdej** informacji, w tym statycznej.

## Dwa zegary i obserwacja

- `τ`: parametr czasu badanego obiektu / procesu, jeśli jest fizycznie lub operacyjnie definiowalny.
- `t`: czas odbiornika / obserwatora.
- `τ=ψ(t)`: mapa synchronizacji, monotoniczna i różniczkowalna tam, gdzie używamy pochodnej.
- `y(t)=R(H(x(ψ(t))))+η(t)`: obserwacja przez kanał `H`, odbiornik `R` i szum `η`.

Możliwe różnice:
- `δ(t)=ψ(t)−t` **tylko gdy oba zegary są sprowadzone do porównywalnej skali i punktu zerowego**;
- `Δτ_k=ψ(t_{k+1})−ψ(t_k)` oraz `Δt_k=t_{k+1}−t_k`;
- `r_k=Δτ_k/Δt_k` (względne tempo, bez wymogu wspólnego zera);
- `dτ/dt` dla ciągłej mapy.

Dla `x(τ)=A cos(2π f₀τ+φ)` oraz regularnej `ψ`, chwilowa częstotliwość względem odbiornika wynosi `f_obs(t)=f₀ ψ'(t)`. To **tożsamość matematyczna dla założonego modelu fazy**, nie dowód odrębnego ontologicznego „czasu informacji”. Dla sygnału wieloskładnikowego i nieznanej fazy potrzebne są dodatkowe warunki.

## Identyfikowalność

Z pojedynczego `y(t)` nie da się ogólnie oddzielić zmiany dynamiki obiektu od zmiany mapy `ψ`: `x∘ψ` może mieć wiele rozkładów na `x` i `ψ`. Potrzebny niezależny zegar, marker referencyjny, synchronizacja dwóch odbiorników lub jawne założenia. Dwa odbiorniki nie usuwają automatycznie wspólnego dryftu zegara/kanału.

## Konsekwencja dla MIN–MAX–CZAS

Nie wolno zakładać, że jedna liczba `t` koduje równocześnie `t_obs`, `τ_obj`, `t_min`, `t_max` i relację między nimi. Publiczna trójka może mieć `(MIN,MAX,Δτ/Δt)` **tylko gdy** taka semantyka została ustalona, a obie skale czasowe są mierzalne. Pełny Chronoproces może zachowywać metadane zegarów bez nazywania ich „trzema cechami”.

## Program testowy

1. Sygnał o stałej częstotliwości w czasie obiektu, rejestrowany przy stałym i zmiennym `ψ'(t)`; kontrola niezależnego znacznika czasu obiektu.
2. Ten sam obserwowany przebieg generowany (a) przez zmianę częstotliwości źródła oraz (b) przez zmianę tempa zegara; wykazać nierozróżnialność bez referencji.
3. Dodać niezależną referencję zegara; sprawdzić odzyskiwanie `ψ'` i rozdzielenie hipotez.
4. Porównać `(MIN,MAX,t_obs)`, `(MIN,MAX,t_max−t_min)`, `(MIN,MAX,Δτ/Δt)` w prognozie przyszłego stanu przy rozdzielonych sesjach.
5. Sprawdzić przypadki, w których relacja czasowa **nie wnosi** informacji, i klasę `UNKNOWN`.

## Zakres wniosku

Czas jest konieczny do opisu **porządku, tempa i ewolucji** procesu. Czy relacja czasu obiektu i obserwatora wnosi dodatkową informację predykcyjną w danym układzie, jest pytaniem empirycznym. Uniwersalna teza „czas jest niezbędnym elementem każdej informacji” wymaga osobnego aksjomatu/definicji i nie wynika z dotychczasowych syntetycznych pilotów.

**Zgodność:** `docs/theory/TIMDR_Chronoprocess.md` (nie utożsamiać automatycznie czasów gałęzi), `docs/theory/TIMDR_Branch_Specification.md`.
