# TIMDR — rodzina transformacji z odbić ścian czworościanu

**Data:** 2026-11-09  
**Status:** klasyfikacja dokładna słów odbić stałych ścian, długości 1–6; CI uruchomione.

## 1. Pytanie

Czy helisa BC i orbity kołowe są szczególnymi przypadkami większej rodziny transformacji generowanych przez odbicia?

Badamy cztery odbicia względem czterech płaszczyzn ścian początkowego foremnego czworościanu o wierzchołkach (±1,±1,±1) z odpowiednim parzystym układem znaków. Wszystkie współrzędne i macierze afiniczne są liczone dokładnie w Q=Fraction.

Konwencja: słowo (i,j,...) oznacza najpierw odbicie i, potem j itd. Sąsiednie identyczne generatory redukują się, ponieważ s_i²=id.

## 2. Wynik enumeracji

| Długość słowa | Zredukowane słowa | Różne mapy afiniczne | Typy map |
|---:|---:|---:|---|
| 1 | 4 | 4 | 4 odwracające orientację |
| 2 | 12 | 12 | 12 obroty |
| 3 | 36 | 36 | 36 odwracające orientację |
| 4 | 108 | 108 | 84 obroty, 24 śruby |
| 5 | 324 | 324 | 324 odwracające orientację |
| 6 | 972 | 972 | 516 obrotów, 456 śrub |

W zakresie długości do 6 każde zredukowane słowo daje inną mapę afiniczną. To wynik skończonego przeszukania, nie dowód, że grupa nie ma relacji o większej długości.

## 3. Dokładny wynik dla słów długości 2

Wszystkie 12 słów długości 2 są czystymi obrotami. Dla każdego:

cos(phi) = -7/9.

Jest to ten sam kąt obrotu, który pojawił się w poprzednim eksperymencie naprzemiennych odbić dwóch ścian. Niewymierność phi/(2 pi) wynika z twierdzenia Nivena: wymierny cosinus kąta będącego wymierną wielokrotnością pi może przyjąć tylko 0, ±1/2, ±1.

## 4. Nowy wynik: słowa długości 4 tworzą rodzinę śrub

Wśród 108 słów długości 4 dokładnie 24 są ruchami śrubowymi. Są to wszystkie 24 permutacje czterech różnych generatorów (każda ściana występuje dokładnie raz). Dla wszystkich 24 map otrzymujemy te same niezmienniki:

cos(theta) = -79/81,

h² = 64/5, czyli |h| = 8/sqrt(5).

Pozostałe 84 słowa długości 4 są czystymi obrotami. W szczególności rodzina śrubowa nie jest pojedynczym przypadkiem numerycznym: wynika dokładnie z całej klasy 24 słów.

## 5. Długość 6

Z 972 zredukowanych słów długości 6:
- 516 daje czyste obroty;
- 456 daje ruchy śrubowe.

To wskazuje, że ruchy śrubowe są częstym elementem tej grupy słów, a nie wyjątkiem. Klasyfikacja dokładnych osi, kątów i przesunięć wszystkich 456 śrub pozostaje kolejnym krokiem.

## 6. Porównanie z BC

Dokładna referencja `core/boerdijk_coxeter_tetrahelix.py` opisuje uporządkowaną helisę BC z:
- cos(theta_BC) = -2/3;
- osiowym przesunięciem na krok w przyjętej konwencji = -2/sqrt(5).

Rodzina 24 słów stałościennych ma cos(theta)=-79/81 i |h|=8/sqrt(5), więc nie jest tą samą izometrią BC. Wspólna jest klasa geometryczna ruchu śrubowego oraz pochodzenie z odbić, nie identyczne parametry.

Kluczowe zastrzeżenie: BC odbija jeden wierzchołek względem płaszczyzny wyznaczonej przez trzy aktualne wierzchołki. Jest to rekurencja z ruchomą płaszczyzną i aktualizacją części stanu. Cztery stałe odbicia ścian generują natomiast grupę afinicznych izometrii działających na całą przestrzeń. Nie wolno utożsamiać tych dwóch dynamik bez osobnego twierdzenia łączącego.

## 7. Wniosek

Tak — istnieje wyraźna rodzina transformacji generowanych przez odbicia: zawiera czyste obroty i ruchy śrubowe. Pierwsza dokładnie wyodrębniona klasa śrubowa pojawia się już przy długości 4, jako wszystkie permutacje czterech ścian. Przy długości 6 śruby stanowią 456 z 972 zredukowanych słów.

To daje matematyczny kierunek: klasyfikować słowa grupy odbić według niezmienników izometrii (część obrotowa, oś, przesunięcie osiowe), a następnie badać, czy rekurencja BC może zostać opisana jako szczególna reguła wyboru ruchomych generatorów z tej szerszej rodziny.

Nie wykazano jeszcze węzłów ani fraktalności. Stałe odbicia są izometriami i nie wprowadzają same z siebie zmiany skali.

## 8. Reprodukcja

Kod: `experiments/reflection_word_family.py`

Uruchomienie: `python experiments/reflection_word_family.py`

CI: https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42601192457

## 9. Status CI

GitHub Actions zakończył workflow powodzeniem: 15/15 testów jednostkowych, eksperyment BC, drzewo gałęzi oraz klasyfikacja słów odbić długości 1–6 przeszły. Logi klasyfikacji potwierdzają dokładnie podane wyżej liczności i niezmienniki: https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42601192457.


## 10. Rozszerzenie do długości 8 i test zamknięcia orbit

Klasyfikację rozszerzono do długości 8. Dokładne wyniki:
| Długość | Zredukowane słowa | Różne mapy | Obroty | Śruby |
|---:|---:|---:|---:|---:|
| 2 | 12 | 12 | 12 | 0 |
| 4 | 108 | 108 | 84 | 24 |
| 6 | 972 | 972 | 516 | 456 |
| 8 | 8748 | 8748 | 2964 | 5784 |

Długości nieparzyste 1, 3, 5, 7 zawierają odpowiednio 4, 36, 324, 2916 map odwracających orientację. W badanym zakresie każde zredukowane słowo daje inną mapę afiniczną.

Dla każdego czystego obrotu z długości 2, 4, 6 i 8 zebrano dokładny wymierny cosinus kąta. Żaden nie należy do zbioru {0, ±1/2, ±1}. Z twierdzenia Nivena wynika, że żaden z tych kątów nie jest wymierną wielokrotnością pi, a zatem żaden czysty obrót nie ma skończonego rzędu. Dla punktu poza osią powtarzanie takiego obrotu daje orbitę gęstą na okręgu.

Każda transformacja sklasyfikowana jako śruba ma niezerowy przesuw wzdłuż osi, więc jej iteracje nie mogą zamknąć orbity punktu. W konsekwencji **żadne pojedyncze zredukowane słowo długości 2, 4, 6 lub 8, powtarzane w kółko jako ta sama izometria, nie daje niebanalnej zamkniętej orbity punktowej**.

To nie wyklucza zamkniętych krzywych budowanych przez zmienne sekwencje różnych transformacji, ani zamkniętych trajektorii w modelu z ruchomymi płaszczyznami. Nie stanowi też pełnej klasyfikacji węzłów.

## 11. Porównanie z BC i węzłami

Dla referencyjnej helisy BC cos(theta)=-2/3 oraz osiowy postęp na krok wynosi -2/sqrt(5). Kąt jest niewymierną wielokrotnością 2*pi (Niven), a postęp osiowy jest niezerowy. Zatem powtarzana mapa śrubowa BC również nie zamyka się do okresowej orbity. Daje helisę, nie zamknięty węzeł.

Wniosek: zamknięty węzeł nie powstanie przez samo wielokrotne zastosowanie jednego z tych obrotów lub ruchów śrubowych. Aby uzyskać węzeł, trzeba badać bardziej złożoną zamkniętą ścieżkę z przełączaniem generatorów, warunkiem powrotu całej konfiguracji do stanu początkowego oraz geometrią łączącą kolejne punkty bez samoprzecięć.

## 12. Status walidacji i zakres wniosku

GitHub Actions zakończył się powodzeniem: 15/15 testów jednostkowych, most BC, drzewo odbić i klasyfikacja słów do długości 8 — PASS:
https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42601951429

W trakcie rozszerzenia pierwsze uruchomienie CI ujawniło błąd zakresu pętli (skrypt wciąż generował warstwy tylko do długości 6, mimo że nowy test pytał o długość 8). Poprawiono granicę enumeracji, dodano oczekiwane liczności dla długości 7 i 8, a następne pełne CI przeszło.

**Wniosek matematyczny:** dla stałych odbić ścian czworościanu rozpoznaliśmy rodzinę izometrii, której powtarzane elementy dają albo nieokresowe orbity kołowe, albo niezamknięte helisy. Nie znaleźliśmy zamkniętych orbit w tym trybie. Hipoteza, że węzły pojawiają się przy przełączaniu różnych odbić lub w rekurencji ruchomych ścian BC, pozostaje otwarta i wymaga odrębnego testu.


## 13. Test zamknięcia konfiguracji jako nieuporządkowanego czworościanu

Samo sprawdzenie, czy złożenie odbić jest identycznością afiniczną, mogłoby przeoczyć sytuację, w której czworościan wraca do tego samego zbioru czterech punktów, ale wierzchołki są permutowane. Dlatego dodano osobny test stabilizatora początkowego czworościanu: dla każdej zredukowanej sekwencji sprawdzamy dokładnie, czy obraz zbioru czterech wierzchołków jest równy zbiorowi początkowemu po posortowaniu punktów.

Wynik do długości słowa 10:
- 0 nietrywialnych powtórzeń map afinicznych pomiędzy różnymi długościami;
- 0 powrotów do początkowego nieuporządkowanego czworościanu;
- na długości 10: 78 732 różne mapy, w tym 15 324 obroty i 63 408 ruchów śrubowych.

Liczności dla długości 9 i 10 zostały dodane jako jawne asercje w skrypcie. Pełny CI zakończył się powodzeniem:
https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42602486417

### Interpretacja i granice

Dla modelu, w którym stanem jest obraz początkowego foremnego czworościanu pod działaniem czterech stałych odbić ścian, nie znaleziono zamkniętego nietrywialnego cyklu do długości 10, nawet po utożsamieniu permutacji wierzchołków. To mocniejszy wynik niż sam brak powrotu macierzy do identyczności.

Nie dowodzi to braku cykli o większej długości. Nie wyklucza też zamkniętych krzywych w modelu z dodatkowymi stopniami swobody (np. zmienną orientacją wewnętrzną, innym stanem etykiet, sprzężeniem kilku czworościanów albo inną regułą przejścia). W szczególności nie jest to jeszcze dowód, że TIMDR nie może tworzyć węzłów. Jest to ograniczenie konkretnego modelu stałych odbić.
