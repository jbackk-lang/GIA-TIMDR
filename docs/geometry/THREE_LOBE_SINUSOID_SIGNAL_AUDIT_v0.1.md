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
