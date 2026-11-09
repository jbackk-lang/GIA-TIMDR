# Geometryczny lift 2D → 3D: obrót jako operator przejścia, sygnał jako część geometrii (v0.1)

**Data:** 2026-11-09  
**Status:** synteza matematyczna istniejących komponentów i hipotezy autora; nie jest jeszcze prawem fizycznym TIMDR.  
**Punkt wyjścia autora:** obrót jest redukcją/przejściem ze stanu dwuwymiarowego do trójwymiarowego; analogicznie sygnał może być częścią geometrii, a nie zewnętrznym wejściem.

## 1. Rozróżnienie matematyczne: obrót nie zmienia wymiaru sam z siebie

Obrót w płaszczyźnie należy do SO(2), a obrót przestrzenny do SO(3). Żaden z nich samodzielnie nie zamienia obiektu 2D w 3D. Do przejścia 2D→3D potrzebny jest **lift/embedding**: określenie, jak dwuwymiarowy stan zostaje osadzony w przestrzeni oraz jak zmienia się jego rama i położenie osiowe.

Dlatego roboczo rozdzielamy:
1. stan źródłowy 2D (figura/pole i faza);
2. operator orientacji (F(s)\in SO(3));
3. postęp osiowy (z(s));
4. mapę osadzenia do \(\mathbb R^3\).

W TIMDR słowo „redukcja” może opisywać regułę przejścia reprezentacji, ale jej matematyczną treścią musi być jawna mapa, nie sam obrót.

## 2. Minimalny geometryczny lift fazorowy

Niech sygnał źródłowy będzie reprezentowany jako zespolony/fazorowy stan:
\[
u(s)=A(s)e^{i\phi(s)}=q_1(s)+i q_2(s),
\qquad q_1=A\cos\phi,\quad q_2=A\sin\phi.
\]
Nie interpolujemy ani nie redukujemy go do samego zawiniętego kąta \(\phi\). Para \((q_1,q_2)\) zachowuje cykliczność i znak nawinięcia.

Dla ortonormalnej ramy \(F(s)=[e_1(s),e_2(s),e_3(s)]\in SO(3)\), mapę do przestrzeni można zapisać:
\[
\boxed{X(s)=C(s)+q_1(s)e_1(s)+q_2(s)e_2(s)+z(s)e_3(s).}
\]
To jest minimalna mapa sygnał→geometria: składowe kwadraturowe stają się współrzędnymi w płaszczyźnie poprzecznej, a trzecia współrzędna/postęp osiowy daje wymiar przestrzenny. Przy stałych \(A,\phi'(s),z'(s)\) i stałej ramie otrzymujemy helikalną trajektorię; zmienne faza, amplituda, rama lub oś dają uogólnioną helisę/powierzchnię.

Szczególny przypadek:
\[
X(\phi)=C+R[\cos\phi\,e_1+\sin\phi\,e_2]+c\phi\,e_3
\]
jest standardową helisą kołową. To pokazuje, jak faza może być współrzędną geometrii, a nie tylko etykietą sygnału.

## 3. Obrót jako dyskretny operator przejścia

Dla kolejnych modułów:
\[
F_{n+1}=F_n R_n,\qquad R_n\in SO(3).
\]
Pozycja kolejnego punktu może mieć postać:
\[
X_{n+1}=X_n+\Delta z_n e_{3,n+1}
+A_n(\cos\phi_n e_{1,n+1}+\sin\phi_n e_{2,n+1}).
\]
Macierz \(R_n\) musi wynikać z jawnej reguły przejścia modułu (np. odbicie/sklejenie czworościanów), a nie z dopasowania do oczekiwanej helisy. Iloczyn \(R_0R_1\cdots R_{m-1}\) opisuje holonomię ramy; jego oś i kąt są mierzalnym wynikiem.

**Uwaga:** obrót ramy i przyrost fazy sygnału to dwa różne obroty. Mogą być sprzężone, ale nie wolno utożsamiać ich bez równania sprzężenia.

## 4. Co już potwierdzają istniejące testy w GIA-TIMDR

### 4.1. Zachowanie fazy w transformacji do pola
`experiments/phase_field_preservation/phase_field_preservation.py` oraz `docs/handoffs/RESULT_PHASE_FIELD_CHIRALITY_PRESERVATION_2026-11-09.md` pokazują syntetycznie, że interpolacja \((\cos\phi,\sin\phi)\) zachowuje winding +1/−1, podczas gdy interpolacja zawiniętego kąta jako skalaru gubi nawinięcie. Test nie dowodzi fizycznego sprzężenia, ale ustala bezpieczną reprezentację fazy.

### 4.2. Synoptyk-v3 jako wzorzec adaptera pola
`docs/handoffs/SYNOPTYK_V3_FIELD_TRANSFORM_CLUE_FOR_HELIX_2026-11-09.md` dokumentuje pipeline: sygnał → pole → cechy pola → adapter stanu. Kierunek/wektor jest rozkładany na składowe przed interpolacją; cechy orientowane (np. wirowość) trzeba zachować osobno od niezmienników lustrzanych (np. modułu gradientu i radialnego widma).

### 4.3. Ograniczenie istniejącego G-Rezonansu
`core/geometric_resonance_operator.py` używa \(|\tau|\) w sprzężeniu mechanicznym, zatem obecna macierz G nie zachowuje znaku torsji. Nie może być jeszcze traktowana jako kompletny operator przejścia faza/orientacja→odpowiedź helisy.

### 4.4. Minimalny test historii
`experiments/helix_signal_response/minimal_coupling_probe.py` pokazuje różną odpowiedź modelu oscylatorowego dla identycznego sygnału i różnych stanów początkowych. Jest to proof-of-integration, nie prawo fizyczne ani dowód, że sygnał stanowi geometrię.

## 5. Rozdzielenie czterech obiektów w badaniu

- **Faza sygnału** \(\phi\): zmienna cykliczna; znak winding niesie orientację.
- **Rama geometryczna** \(F\): orientacja lokalnego układu współrzędnych; jej transport daje holonomię.
- **Krzywa osiowa** \(C(s)+z(s)e_3(s)\): przebieg przestrzenny/tunel.
- **Ograniczenie brzegowe**: kula/jajo i przesunięcie środków wpływają na dopuszczalne położenia/orientacje.

Możliwy most TIMDR musi jawnie określić sprzężenie między nimi, np.:
\[
R_n=\mathcal{T}(G_n,u_n),\qquad
\phi_{n+1}=\phi_n+\Delta\phi_n,
\]
ale postać \(\mathcal{T}\) i \(\Delta\phi_n\) pozostają do wyprowadzenia z reguły modułu i sygnału.

## 6. Następny test rozstrzygający — bez tworzenia kolejnego modelu fizycznego

1. Użyć istniejących danych fazorowych i reguły modułowej BC jako oddzielnych wejść kontrolnych.
2. Zbudować referencyjny lift 2D→3D z powyższej mapy i zweryfikować, że odtworzony sygnał zachowuje amplitudę, fazę i winding.
3. Zastosować kolejno: ramę stałą, ramę obracaną oraz ramę transportowaną regułą odbicia czworościanu.
4. Zmierzyć osobno przyrost fazy \(\Delta\phi\), obrót ramy \(R_n\), holonomię, promień i postęp osiowy.
5. Odwrócić znak fazy oraz lustrzanie odbić moduł. Znak winding i orientowane miary powinny odwrócić się zgodnie z konwencją; nieorientowane miary mogą pozostać takie same.
6. Dopiero po przejściu testów reprezentacji zdefiniować sprzężenie sygnału z przesunięciem środków kuli/czworościanu i sprawdzić, czy ograniczenie brzegowe generuje mierzalny obrót ramy.

## 7. Falsyfikowalne rozróżnienie

- Jeśli sam lift \((q_1,q_2,z)\) daje helisę przy stałej ramie, to faza jest geometrycznie kodowana, ale nie ma jeszcze sprzężenia sygnał–rama.
- Jeśli transport ramy przez \(R_n\) zmienia holonomię, ale faza sygnału pozostaje stała, mamy obrót geometryczny niezależny od sygnału.
- Jeśli kontrolowana zmiana sygnału zmienia \(R_n\) lub odpowiedź graniczną przy stałej geometrii wejściowej, jest kandydat na sprzężenie sygnał–geometria.
- Jeśli po rekonstrukcji ginie winding lub znak chiralności, lift nie zachowuje pełnej informacji i nie może być użyty jako operator TIMDR.

## 8. Wniosek

Robocza interpretacja autora jest matematycznie testowalna jako **geometryczny lift 2D→3D, w którym faza sygnału jest współrzędną, a obrót jest operatorem transportu/orientacji**. Istniejące testy GIA dostarczają już komponentu zachowania fazy i wzorca transformacji do pola. Brakuje jednego jawnego prawa: jak sygnał i reguła modułu wspólnie wyznaczają obrót ramy oraz jak warunki brzegowe (kula/jajo i przesunięcie środków) ograniczają ten proces.

Nie twierdzimy jeszcze, że to fizyczne prawo helisy. To formalny most, który można teraz testować bez mieszania sygnału, fazy, ramy, osi i granicy w jeden parametr.
