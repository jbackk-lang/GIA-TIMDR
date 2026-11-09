# Audyt: płaty sinusoidy +−+ a podpisana torsja klasycznego trefoila (v0.1)

**Data:** 2026-11-09  
**Status:** porównanie analityczne wykonane; bezpośrednie mapowanie niepotwierdzone.

## 1. Pytanie

Czy środkowy ujemny płat sinusoidy może odpowiadać wyjątkowemu odwróceniu orientacji w środkowej części trójwęzła TIMDR?

Porównano słowo znaków trzech półfal ((+,-,+)) z podpisaną torsją Freneta klasycznej krzywej trefoil już używanej w repozytorium:

\[
\begin{aligned}
x(t)&=\sin t+2\sin 2t,\\
y(t)&=\cos t-2\cos 2t,\\
z(t)&=-\sin 3t.
\end{aligned}
\]

Torsję obliczono z pochodnych analitycznych:
\[
\tau(t)=\frac{(r'\times r'')\cdot r'''}{\|r'\times r''\|^2}.
\]
To unika artefaktów różnic skończonych w tym teście.

## 2. Wynik liczbowy

Parametr podzielono na trzy równe sektory ([0,2\pi/3)), ([2\pi/3,4\pi/3)), ([4\pi/3,2\pi)).

Dla 12 000 próbek:
- średnia podpisana torsja w każdym sektorze: około (+0.05343);
- udział próbek z dodatnią torsją: około (57.71\%);
- udział próbek z ujemną torsją: około (42.29\%);
- zakres torsji w każdym sektorze: około ([-0.22222,+0.35294]).

Trzy sektory mają ten sam rozkład torsji z dokładnością numeryczną. Co więcej, **w każdym sektorze torsja przyjmuje zarówno znaki dodatnie, jak i ujemne**.

## 3. Interpretacja

To nie daje wzorca sektorów (+,-,+). Kanoniczny trefoil ma trzykrotną symetrię: jego trzy sektory są równoważne pod względem rozkładu podpisanej torsji. Środkowy sektor nie jest wyróżniony jako jedyny o przeciwnym znaku.

Wynik jest więc negatywny dla najprostszego utożsamienia:
[
\text{znak płata sinusoidy}\equiv\text{znak torsji odpowiedniego sektora trefoila}.
]

Nie obala to hipotezy, że znak sygnału steruje inną wielkością orientacyjną — np. fazą gałęzi, orientacją lokalnej ramy lub skrętem pasma. Pokazuje jednak, że nie jest nią bezpośrednio znak torsji Freneta klasycznego trefoila.

## 4. Co rzeczywiście wnosi do TIMDR

1. Odrzuca prostą mapę „ujemny drugi płat = ujemna torsja środkowego loba”.
2. Wymusza rozdzielenie polaryzacji sygnału, orientacji parametru, torsji osi i skrętu ramy.
3. Daje kontrolę zerową: jeśli przyszła mapa przypisze środkowemu sektorowi wyjątkowy znak torsji, musi wyjaśnić, skąd bierze się złamanie trzykrotnej symetrii.
4. Kieruje następny eksperyment ku ramie/framingowi trzech gałęzi, a nie ku samej krzywej trefoil.

## 5. Ograniczenia

To porównanie używa klasycznego trefoila jako obiektu odniesienia. Nie jest on automatycznie tym samym, co postulowany trójwęzeł trzech helis TIMDR. Nie zdefiniowano jeszcze operatora mapującego płaty sygnału na trzy krzywe przestrzenne ani reguły szwu. Nie wyprowadzono zatem ani topologii, ani fizycznej interpretacji antycząstki.

## 6. Reprodukowalność

- Kod: `experiments/helix_reduction/trefoil_lobe_correspondence_audit.py`
- Testy: `experiments/helix_reduction/tests/test_trefoil_lobe_correspondence.py`
- CI: workflow Helix four-to-three surface reduction uruchamia audyt i dołącza JSON do artefaktów.

**Wniosek:** dotychczasowy test +−+ nie wyjaśnia orientacji trójwęzła. Jego wartość polega teraz na wskazaniu, czego nie wolno utożsamiać. Następny sensowny obiekt to podpisana orientacja ramy trzech gałęzi i jej zachowanie na szwie.
