# Informacja, czas i geometria — rozdzielenie pojęć

**Status:** notatka teoretyczna, 2026-11-14. Bez twierdzenia o odkryciu nowej cząstki.

## Trzy różne znaczenia informacji

1. **Shannon:** informacja obserwacji `i(x)=-log2 p(x)` zależy od modelu prawdopodobieństwa. Entropia `H(X)` jest średnim zaskoczeniem.
2. **Predykcyjna:** `I(X_past; X_future)` to informacja wzajemna między przeszłością i przyszłością; zależy od zdefiniowanych zmiennych i rozkładu.
3. **Fizyczna:** zapis, przesłanie i usunięcie informacji wymagają fizycznego nośnika i procesu; bit nie jest sam przez się cząstką elementarną.

## Definicja robocza „zdarzenia informacyjnego”

Niech `O_t` oznacza obserwację w chwili `t`, a `M` model obserwatora. Zdarzenie `e=(t_0,t_1,O_{t_0},O_{t_1},M)` nazywamy *rozróżnialnym*, jeśli ustalony wcześniej test odróżnia odpowiednie hipotezy stanów przy określonej częstości fałszywych alarmów. Minimalność jest **względna do aparatury, szumu, czasu obserwacji i reguły decyzji**. Nie wnioskujemy o uniwersalnej minimalnej porcji informacji.

## Geometryczna hipoteza operacyjna

Rekonstruujemy trajektorię `X(t)` i jej geometryczne cechy `G(t)`. Hipoteza: `I(Y_future; G_past | B_past) > 0`, gdzie `B` zawiera ustalone klasyczne cechy. To właściwsza formalizacja „dodatkowej informacji” niż sama duża krzywizna. W praktyce szacowanie warunkowej informacji wzajemnej jest trudne; w pierwszym etapie używamy zysku predykcyjnego na niezależnym teście, nie twierdząc, że jest to bezpośredni estymator CMI.

## Rola czasu

- Sam odstęp `Δt` nie tworzy automatycznie informacji o stanie.
- Szybkość informacji (np. bity/s) zależy od procesu i kodowania; nie jest samym czasem.
- Transformacja skali czasu zmienia numeryczne pochodne i może zmieniać cechy geometryczne. Weryfikujemy, co pozostaje niezmiennicze przy zmianie parametryzacji.
- Analogia z fotonem wymagałaby konkretnego przewidywania fizycznego (np. prawa dyspersji, zachowania energii, oddziaływania), którego na razie nie ma.

## Warunki obalenia hipotezy

Jeżeli po kontroli autokorelacji, widma, złożoności modelu i przecieku danych geometria nie poprawia predykcji na niezależnych sesjach, hipoteza o jej **dodatkowej wartości w danym zadaniu** nie jest potwierdzona. Nie obala to automatycznie innych zastosowań geometrii ani nie potwierdza „cząstki informacji”.

## Kolejne pytania

Czy cechy geometrii są stabilne względem zmiany jednostek amplitudy? Czy można wyznaczyć niezmienniki parametryzacji czasowej? Czy topologia trajektorii wnosi wartość po kontroli widma? Czy przejścia między reżimami mają powtarzalne sygnatury w wielu domenach?
