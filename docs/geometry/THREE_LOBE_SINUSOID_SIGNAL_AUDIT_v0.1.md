# Audyt sygnału trzech płatów sinusoidy: + − + (v0.1)

**Data:** 2026-11-09  
**Status:** eksperyment sygnałowy wykonany w CI; topologia przestrzenna pozostaje nierozstrzygnięta.

## 1. Konstrukcja testowa

Badamy trzy kolejne półokresy:

\[
s(t)=A\sin(\omega t),\qquad 0\le t\le\frac{3\pi}{\omega},\quad A,\omega>0.
\]

Płaty ograniczają cztery kolejne przejścia przez zero:

\[
t_k=\frac{k\pi}{\omega},\quad k=0,1,2,3.
\]

Ekstrema leżą w środkach płatów:

\[
t_k^*=\frac{(2k+1)\pi}{2\omega},\quad k=0,1,2.
\]

Otrzymujemy:
- znaki płatów: \((+1,-1,+1)\);
- znaki nachylenia w kolejnych zerach: \((+1,-1,+1,-1)\);
- wartości ekstremów: \((+A,-A,+A)\).

To są trzy płaty jednej sinusoidy, a nie trzy niezależne sygnały.

## 2. Wynik: znak jest informacją

Zastosowanie wartości bezwzględnej daje:

\[
(+1,-1,+1)\xrightarrow{|s|}(+1,+1,+1).
\]

Znika informacja o odwróceniu środkowego płata. Zatem wszelkie redukcje oparte na \(|s|\) tracą dokładnie tę cechę, którą chcemy zbadać. W implementacji przechowujemy znak każdego płata oraz pochodne na granicach osobno.

## 3. Ważny wynik: słowo +−+ nie rozróżnia kierunku przejścia

Sekwencja \((+,-,+)\) jest palindromiczna. Po odwróceniu kolejności próbek kolejność znaków płatów nadal wynosi \((+,-,+)\).

Kierunek przejścia zmienia się jednak:

\[
\frac{dt}{d\tilde t}=-1,
\]

więc znaki pochodnych i orientacja parametryzacji odwracają się. **Sam znak płatów nie koduje ręczności ani kierunku obiegu.** Potrzebujemy dodatkowego kanału orientacji: kierunku parametru, stycznej na granicy, orientacji ramy lub fazy obiegu.

To ważne dla hipotezy antycząstki / lewo- i prawoskrętności: nie wolno wnioskować o ręczności wyłącznie z sekwencji +−+.

## 4. Punkty kandydackie

Naturalne zdarzenia sygnałowe:
- cztery granice płatów: \(0,\pi/\omega,2\pi/\omega,3\pi/\omega\);
- trzy ekstrema: \(\pi/(2\omega),3\pi/(2\omega),5\pi/(2\omega)\).

Mogą być kandydatami na punkty kardynalne, ale nie są jeszcze punktami kardynalnymi helisy. Ich znaczenie przestrzenne wymaga mapy sygnał→oś/gałęzie.

## 5. Co nie zostało dowiedzione

Trzy płaty sygnału nie są automatycznie trzema przestrzennymi strunami ani topologicznym trójwęzłem. Sam skalar \(s(t)\) nie określa:
- współrzędnych 3D;
- połączeń między gałęziami;
- przeplotu i informacji nad/pod w projekcji;
- domknięcia krzywych;
- typu węzła/linku ani jego niezmienników.

Do dowodu trójwęzła potrzebna jest jawna mapa osadzenia przestrzennego oraz graf połączeń. W przeciwnym razie dowodzimy tylko trójpłatowej struktury sygnału.

## 6. Reprodukowalność

Kod: `experiments/helix_reduction/three_lobe_signal_audit.py`.  
Testy: `experiments/helix_reduction/tests/test_three_lobe_signal_audit.py`.

Testy kontrolują:
1. odzyskanie słowa +−+;
2. utratę znaku po wartości bezwzględnej;
3. palindromiczność sekwencji i odwrócenie orientacji parametru;
4. cztery granice płatów i znaki nachyleń;
5. odwrócenie polaryzacji po przesunięciu fazy o \(\pi\);
6. zakaz utożsamiania trzech płatów z trzema strunami przestrzennymi.

## 7. Następny test rozstrzygający

Należy zdefiniować operator osadzenia:

\[
\Gamma:\ (s(t),\operatorname{sign}\dot t,\Phi(t))\longrightarrow\mathbb R^3,
\]

w którym jawne są: faza przestrzenna \(\Phi\), oś, styczne na granicach płatów i reguła łączenia. Następnie porównać:
- mapę zachowującą znak;
- mapę z utraconym znakiem;
- mapę z odwróconą orientacją parametru.

Dopiero jeśli te warianty dają różne, stabilne własności przestrzenne/topologiczne, można mówić o sygnale jako źródle konstrukcji trójwęzła.

## 8. Wniosek roboczy

**Potwierdzone:** trzy półfale mają znaki +−+; wartość bezwzględna niszczy znak środkowego płata; sekwencja jest palindromiczna i sama nie rozróżnia kierunku obiegu.

**Niepotwierdzone:** że +−+ samo tworzy trójwęzeł. Do tego brakuje operatora osadzenia 3D i warunków sklejenia.

Wniosek ten jest falsyfikowalny i nie dopisuje geometrii, której sygnał skalarny nie zawiera.


## 10. Wynik CI i artefakt

Workflow [42565948968](https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42565948968) zakończył się sukcesem. Przeszły wszystkie testy jednostkowe oraz uruchomienia modeli kuli, jaja i audytu trzech płatów. Artefakt `helix-four-to-three-phase-locked-v02`, ID `13651795453`, SHA-256 `f98dd2b861c452974311799c280c0ef0b986e5df22cbb4b5cfb6b0aa38ff9672`.

Dla (A=1,\omega=1,\varphi=0):
- ekstrema: ((\pi/2,+1),(3\pi/2,-1),(5\pi/2,+1));
- granice: (0,\pi,2\pi,3\pi);
- znaki nachyleń na granicach: (+,-,+,-);
- słowo po odwróceniu przebiegu: nadal (+,-,+);
- orientacja parametru: (+1\to-1).

Wynik kluczowy jest negatywny, ale istotny: polaryzacja płatów nie wystarcza do odzyskania kierunku przebiegu. Kierunek musi być osobnym polem danych.


## 11. Dodatkowy wynik: domknięcie położenia nie oznacza domknięcia stycznej

Dla trzech półokresów (s(t)=A\sin(\omega t)), (t\in[0,3\pi/\omega]):

\[
s(0)=s(3\pi/\omega)=0,
\]
ale
\[
s'(0)=A\omega,\qquad s'(3\pi/\omega)=-A\omega.
\]

Zatem skalarna trajektoria domyka się w sensie (C^0), ale nie w sensie (C^1). Przy sklejeniu końców w tej samej orientacji parametru powstaje niezgodność stycznych (załamanie / odwrócenie kierunku). To nie jest detal numeryczny: jeśli płaty mają budować zamknięty obieg helisy, reguła szwu musi rozwiązać tę niezgodność.

Możliwe klasy rozwiązań do zbadania, bez wybierania jednej z góry:
1. dodać odcinek przejściowy, który obraca styczną;
2. zastosować identyfikację z odwróceniem orientacji (sprawdzić, czy geometria i rama pozwalają na takie sklejenie);
3. użyć innego zakresu fazy / dodatkowego płata, aby położenie i styczna zamknęły się jednocześnie;
4. traktować trzy płaty jako fragment większej trajektorii, a nie samodzielną pętlę.

Audyt koduje teraz (C^0) i (C^1) osobno, a test sprawdza, że pozycja się zamyka, natomiast styczna nie. Ten wynik daje konkretny warunek brzegowy dla przyszłego operatora sygnał→helisa.


## 12. Walidacja poprawki domknięcia

Po dodaniu jawnego testu zgodności stycznych workflow [42566568596](https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42566568596) zakończył się sukcesem. Krok `Unit tests` oraz uruchomienie audytu sygnałowego przeszły. Potwierdza to poprawność implementacji testu (C^0/C^1), nie fizyczny mechanizm trójwęzła.
