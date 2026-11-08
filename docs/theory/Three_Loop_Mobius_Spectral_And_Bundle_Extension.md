# Trójpętlowy model Möbiusa — rozszerzenie spektralne i teoria wiązek (wersja robocza)

**Status:** propozycja formalizacji, nie aksjomat i nie walidacja eksperymentalna. **Przypisanie:** gałąź G (geometria/topologia); interfejs z META-DYNAMICS. **Zależność:** [model bazowy](Three_Loop_Mobius_Information_Dynamics.md). Rozszerzenie rozdziela trzy różne obiekty: graf sprzężeń, geometrię powierzchni oraz holonomię pola.

## A. Rozkład modalny i stabilność operatora

Niech P=[[0,1,0],[0,0,1],[1,0,0]], P³=I oraz J(λ)=P−λP², λ∈ℝ. Niech ω=exp(2πi/3), v_k=(1,ω^k,ω^{2k})ᵀ/√3, k=0,1,2. Wtedy Pv_k=ω^k v_k i

μ_k(λ)=ω^k−λω^{2k}, Jv_k=μ_k v_k.

Zachodzi |μ₀|=|1−λ| oraz |μ₁|²=|μ₂|²=1+λ+λ². Ponieważ J jest wielomianem macierzy unitarnej P, jest normalna i

||J^n||₂ = ρ(J)^n,  ρ(J)=max(|1−λ|,√(1+λ+λ²)).

**Twierdzenie A1 (kontrakcja):** dla λ∈ℝ operator J jest ścisłą kontrakcją w normie euklidesowej wtedy i tylko wtedy, gdy ρ(J)<1. Nierówności |1−λ|<1 i 1+λ+λ²<1 wymagają jednocześnie 0<λ<2 oraz −1<λ<0, co jest niemożliwe. Zatem **nie istnieje rzeczywiste λ, dla którego oryginalny J jest ścisłą kontrakcją**. Dla λ=0 operator jest unitarnym przesunięciem P i ρ(J)=1. Dla λ≠0 mamy ρ(J)>1 (dla λ<0: |1−λ|>1; dla λ>0: √(1+λ+λ²)>1).

**Wniosek A2:** dla dowolnego rzeczywistego λ≠0 istnieje początkowy stan modalny Ψ₀, którego norma rośnie jak ρ(J)^n. Nie jest poprawne utożsamianie λ z tłumieniem bez dodatkowej dynamiki.

Definiujemy operator z kontrolą skali A(λ,γ)=e^(−γ)J(λ)/ρ(J), γ≥0. Wtedy ||A||₂=e^(−γ), ||A^n||₂=e^(−nγ). Dla wymuszenia η_n i Ψ_{n+1}=AΨ_n+η_n:

||Ψ_n||₂ ≤ e^(−nγ)||Ψ₀||₂ + Σ_{j=0}^{n−1}e^(−(n−1−j)γ)||η_j||₂.

Jeżeli γ>0 i ||η_j||₂≤ε, to limsup ||Ψ_n||₂ ≤ ε/(1−e^(−γ)). Jest to oszacowanie typu wejście–stan, a nie zasada zachowania energii.

## B. Pole na wstędze Möbiusa i warunki brzegowe

Wstęgę opisuje iloraz M=([0,2π]×[−w,w]) / ((0,v)~(2π,−v)). Dla pola skalarnego f:M→ℂ zachodzi f(0,v)=f(2π,−v). Trzy amplitudy Ψ:M→ℂ³ spełniają ten warunek **składowo**, jeśli przyjmujemy trywialną wiązkę ℂ³ nad M.

Aby kodować dodatkowy obrót kanałów, można **zdefiniować osobną wiązkę** przez identyfikację (0,v,z)~(2π,−v,Hz), gdzie H∈U(3). Wówczas w lokalnych współrzędnych Ψ(2π,−v)=HΨ(0,v). Macierz H jest założeniem modelu; nie wynika z samej nieorientowalności wstęgi.

**Propozycja B1:** wybór H=P modeluje cykliczną permutację trzech kanałów przy przejściu przez szew. Wtedy H³=I, a fazy własne holonomii wynoszą 1,ω,ω². Alternatywa H=−I modeluje odwrócenie wszystkich trzech amplitud, ale jest **inną** hipotezą, nie automatycznym skutkiem topologii.

**Ostrożność:** dwukrotne przejście przez szew daje H² i przywraca orientację współrzędnej poprzecznej v, lecz nie musi przywracać wektora amplitud, jeśli H²≠I. W przypadku H=P do pełnego powrotu kanałów potrzeba trzech przejść; do jednoczesnego powrotu orientacji i kanałów — sześciu. To algebraiczna konsekwencja przyjętego sklejenia.

## C. Dynamika zgodna z holonomią

Dla stałej λ macierze J(λ) i P komutują: [J,P]=0. Stąd również [A(λ,γ),P]=0. Przy H=P ewolucja zachowuje warunek sklejenia:

Ψ_{n+1}(2π,−v)=AΨ_n(2π,−v)=AHΨ_n(0,v)=HAΨ_n(0,v)=HΨ_{n+1}(0,v),

pod warunkiem, że wymuszenie spełnia η_n(2π,−v)=Hη_n(0,v).

**Twierdzenie C1 (zgodność):** liniowy operator ewolucji A na włóknie zachowuje warunek sklejenia z H, jeśli AH=HA, a wymuszenie respektuje ten sam warunek. Dla H=P i A będącego wielomianem P zgodność zachodzi automatycznie.

Dla H zależnego od położenia albo λ=λ(u,v) należy osobno sprawdzić zgodność po obu stronach szwu. Nie wolno wtedy automatycznie stosować dowodu dla stałej macierzy.

## D. Odwzorowanie toroidalne a nieorientowalność

Funkcja T(θ,φ)=((R+r cosθ)cosφ,(R+r cosθ)sinφ,r sinθ) przy R>r>0 opisuje torus orientowalny. Zastąpienie θ przez 3θ/2 nie zmienia obrazu przy pełnym pokryciu kątów: daje reparametryzację / wielokrotne pokrycie. Nie tworzy nieorientowalności. Konstrukcja Möbiusa wymaga sklejenia (u,v)~(u+2π,−v), a jej standardowe zanurzenie ma brzeg, w odróżnieniu od torusa.

## E. Predykcje rozdzielające konkurencyjne modele

- **M0 (kontrola orientowalna):** Ψ(2π,v)=Ψ(0,v), H=I.
- **M1 (wstęga, bez mieszania kanałów):** Ψ(2π,−v)=Ψ(0,v), H=I.
- **M2 (wstęga + cykliczne mieszanie):** Ψ(2π,−v)=PΨ(0,v), H=P.
- **M3 (wstęga + inwersja amplitud):** Ψ(2π,−v)=−Ψ(0,v), H=−I.

Samo porównanie lokalnego widma J nie rozróżni M0–M3, gdyż J nie zależy od H. Do rozróżnienia potrzebny jest eksperyment transportu po pętli / warunek brzegowy w modelu przestrzennym. Mierzalną predykcją w modelu symulacyjnym jest transformacja kanałów po kolejnych obiegach: H^mΨ. Dla M2 cykl kanałów ma okres 3, dla M3 znak ma okres 2, a dla M0/M1 amplitudy bezpośrednio wracają po jednym obiegu (różnica M0/M1 dotyczy współrzędnej poprzecznej).

## F. Plan walidacji i kryteria falsyfikacji

1. Obliczyć analitycznie i numerycznie widmo J dla λ∈[−2,2]; potwierdzić A1.
2. Dla γ>0 przetestować nierówność oszacowania wejście–stan przy deterministycznym i losowym η.
3. Sprawdzić komutator [A,P]=0 i zgodność warunków brzegowych C1.
4. W symulatorze transportu wykonać 1,2,3,6 obiegów i porównać M0–M3.
5. Dla obserwacji rzeczywistych zdefiniować procedurę pomiaru trzech kanałów, jednostki, niepewność, model szumu i prerejestrowany test porównawczy. **Bez tego nie ma podstaw do deklaracji walidacji empirycznej.**

## G. Mapa pojęć

- **G (geometria):** orientowalność, sklejenie, wiązka, holonomia H.
- **META-DYNAMICS:** stan Ψ_n, operator A, wymuszenie η, oszacowania stabilności.
- **Nie wynika z modelu:** zachowanie energii fizycznej, redukcja entropii termodynamicznej, rzeczywisty toroidalny przepływ informacji lub empiryczne istnienie trzech pętli.

Dokument jest propozycją testowalnego modelu pomocniczego, bez zmiany istniejących aksjomatów GIA-TIMDR.
