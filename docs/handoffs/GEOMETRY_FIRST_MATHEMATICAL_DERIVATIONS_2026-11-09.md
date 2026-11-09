# Geometria jako podstawa formalizacji — pierwsze wyprowadzenia i ograniczenia

**Data:** 2026-11-09  
**Cel:** odróżnić relacje wynikające z geometrii od hipotez o mechanizmie TIMDR.

## 1. Zasada metodologiczna

Nie dobieramy geometrii do wygodnego równania. Najpierw definiujemy obiekt, osie, parametry i warunki brzegowe; następnie wyprowadzamy relacje matematyczne i dopiero potem budujemy operator oddziaływania.

## 2. Logarytmiczne prawo rozszerzania promienia

Jeśli empirycznie przyjmujemy stały względny przyrost promienia na jednostkę kąta:
`dr/dθ = b r`,
to przez rozdzielenie zmiennych:
`dr/r = b dθ`,
a po całkowaniu:
`r(θ)=r₀ exp(bθ)`.

Po jednym obrocie:
`q = r(θ+2π)/r(θ) = exp(2πb)`,
więc:
`b = ln(q)/(2π)`.

To wyprowadzenie jest matematycznie ścisłe **pod warunkiem stałego b**. Nie dowodzi, że rzeczywista helisa/muszla ma stałe b. To trzeba mierzyć.

## 3. Wymiar osiowy

Dla stałego przesunięcia osiowego na jednostkę kąta:
`dz/dθ = c`,
otrzymujemy:
`z(θ)=z₀+cθ`,
a skok osiowy na obrót:
`P=2πc`.

Parametry b i c opisują różne rzeczy: b — względne rozszerzanie promienia, c — translację wzdłuż osi. Nie wolno ich utożsamiać ani łączyć bez dodatkowego warunku modelu.

## 4. Chiralność

Chiralność nie wynika z samego dodatniego promienia. Wprowadźmy orientację parametryzacji ε∈{−1,+1}:
`x(θ)=r(θ)cos(εθ)`,
`y(θ)=r(θ)sin(εθ)`,
`z(θ)=z₀+cθ`.

Znak ε określa kierunek obiegu w płaszczyźnie xy względem ustalonej orientacji osi. Znak musi być raportowany wraz z konwencją osi i kierunkiem obserwacji; samo słowo „lewy/prawy” bez konwencji może być niejednoznaczne.

Warto rozdzielić:
- znak obiegu (chiralność);
- tempo rozszerzania promienia b;
- skok osiowy P;
- geometrię przekroju/krzywej generującej.

To są niezależne parametry, dopóki nie zostanie dowiedzione ich sprzężenie.

## 5. Ważne ograniczenie: muszla nie jest zwykłą helisą

Model muszli ślimaka zwykle opisuje ruch i skalowanie krzywej generującej (otworu muszli) wokół osi, a nie tylko jedną krzywą helikalną. Parametry obejmują m.in. tempo ekspansji zwoju, translację wzdłuż osi, położenie krzywej generującej względem osi oraz proporcje jej przekroju.

Literatura:
- A developmentally descriptive method for quantifying shape in gastropod shells (2020): https://pmc.ncbi.nlm.nih.gov/articles/PMC7061706/
- Going round the twist—an empirical analysis of shell coiling in helicospiral gastropods (Paleobiology 2021/2022): https://doi.org/10.1017/pab.2021.8
- A Mathematical Model for Mollusc Shells Based on Parametric Surfaces... (2023): https://www.mdpi.com/1424-2818/15/3/431

Szczególnie ważny wynik empiryczny: badanie 25 gatunków i 176 muszli wykazało, że tradycyjne założenia izometrii i wykładniczego wzrostu nie opisują wszystkich gatunków. Zatem logarytmiczna helisa jest użytecznym modelem bazowym, nie uniwersalnym prawem dla każdej muszli.

## 6. Konsekwencja dla TIMDR

Nie przenosić bezpośrednio parametrów muszli na helisę TIMDR. Najpierw trzeba zdefiniować jej własną geometrię:
1. oś i tunel osiowy;
2. krzywą/krzywe generujące;
3. lokalny skręt i jego znak;
4. parametry rozszerzania i przesunięcia;
5. warunki brzegowe i miejsca przejść;
6. ewentualną deformację przekroju.

Następnie sprawdzić, które parametry są stałe, a które zależą od stanu/sygnału. Dopiero wtedy można wyprowadzić operator odpowiedzi.

## 7. Czego to jeszcze nie dowodzi

Powyższe równania dowodzą konsekwencji przyjętych założeń geometrycznych. Nie dowodzą:
- że sygnał zmienia b, c lub ε;
- że pole jest pamięcią helisy;
- że GS-Matrix jest prawem mechanicznym;
- że G-Rezonans jest odpowiedzią biologiczną lub fizyczną;
- że geometria muszli i geometria TIMDR są tym samym obiektem.

Następny rygorystyczny krok to zdefiniowanie geometrii TIMDR bez narzucania modelu muszli i sprawdzenie jej parametrów na istniejących danych/repozytorium.
