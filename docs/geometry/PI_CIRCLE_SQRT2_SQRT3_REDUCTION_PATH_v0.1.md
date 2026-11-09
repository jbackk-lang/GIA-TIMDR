# Druga ścieżka redukcji TIMDR: konstrukcja koła, π oraz długości √2 i √3 (v0.1)

**Data:** 2026-11-09  
**Status:** ścieżka przypomniana przez autora; historyczna konstrukcja źródłowa nieodnaleziona jeszcze w bieżącym drzewie GIA-TIMDR.  
**Zasada:** nie utożsamiać sumy √2+√3 z π. Najpierw odtworzyć konkretną konstrukcję i jej rolę w redukcji.

## 1. Pozycja w programie

Autor wskazuje drugą, niezależną drogę analizy redukcji: analogię do π i idealnej konstrukcji koła, z użyciem sumy pierwiastków √2 i √3. Ta ścieżka ma być badana równolegle do redukcji trójkąt → czworościan → konfiguracja czterowęzłowa / trójwęzłowa.

Nie zakładamy, że jest to ta sama operacja co redukcja grafu ani że daje bezpośrednio kąt skrętu helisy. Potencjalny wspólny wynik trzeba wykazać przez wspólne niezmienniki lub mapę między konstrukcjami.

## 2. Kontrola arytmetyczna

\[
\sqrt2+\sqrt3\approx3.1462643699419726
\]
\[
\pi\approx3.1415926535897932
\]
\[
(\sqrt2+\sqrt3)-\pi\approx0.0046717163521794.
\]

Zatem suma √2+√3 jest bliskim przybliżeniem π (błąd względny ok. 0.1487%), ale nie jest równa π. Ponadto √2 i √3 są liczbami algebraicznymi, a ich suma również jest algebraiczna; π jest przestępne. W konsekwencji żadna skończona konstrukcja oparta wyłącznie na operacjach algebraicznych na tych długościach nie daje dokładnie π.

To nie unieważnia analogii. Możliwe, że chodzi o:
- konstrukcję przybliżającą obwód koła;
- granicę ciągu konstrukcji wielokątnych;
- sumę odcinków/cięciw przypisanych różnym sektorom;
- proporcję długości, a nie równość √2+√3=π;
- regułę redukcji, w której √2 i √3 są dwoma składnikami lub stanami, a π pełni rolę granicy/normalizacji.

## 3. Geometria okręgu — punkty kontrolne

Dla okręgu jednostkowego:
- cięciwa kąta środkowego 90° ma długość √2;
- cięciwa kąta środkowego 120° ma długość √3;
- obwód wynosi 2π, a półobwód π.

Wartości √2 i √3 pojawiają się więc naturalnie w geometrii kwadrantu i sześciokąta foremnego. To daje możliwy most geometryczny do modułów trójkątnych, czworościanu i sześcianu, ale nie identyfikuje jeszcze konkretnej konstrukcji autora.

Dla okręgu o promieniu r powyższe cięciwy mają długości r√2 i r√3. Należy jawnie zapisać promień i normalizację przed porównywaniem ich z π.

## 4. Pytania dowodowe

1. Czy √2 i √3 oznaczają długości cięciw, przekątnych, promieni, boków, czy współczynniki redukcji?
2. Czy suma jest dosłowną sumą długości, czy sumą znormalizowanych proporcji?
3. Czy π jest wartością docelową, granicą procesu, obwodem/średnicą, czy symbolem idealnej konstrukcji koła?
4. Czy konstrukcja jest skończona, czy graniczna (ciąg wielokątów)?
5. Jaki obiekt redukuje się: obwód, pole, graf, trajektoria, faza czy liczba stopni swobody?
6. Czy reguła zachowuje orientację i znak skrętu?
7. Czy ta sama mapa redukcji działa dla obu dróg: bryłowo-węzłowej i kołowo-pierwiastkowej?

## 5. Minimalne testy

### C1 — odtworzenie rysunku/konstrukcji
Zebrać pierwotny diagram, wzory i kolejność operacji. Bez tego nie wybierać interpretacji.

### C2 — wymiarowanie
Wszystkie długości wyrazić względem jednego promienia/boku jednostkowego. Oddzielić długości od bezwymiarowych stosunków.

### C3 — dokładność
Sprawdzić, czy π jest:
- dokładne (wtedy konstrukcja nie może być skończoną konstrukcją algebraiczną z √2 i √3);
- przybliżane (wtedy wyznaczyć błąd i zbieżność);
- granicą (wtedy podać ciąg i udowodnić granicę).

### C4 — redukcja
Zdefiniować operator R_pi i jego niezmienniki. Sprawdzić, czy zachowuje obwód, pole, orientację, fazę lub inną wielkość, którą konstrukcja deklaruje jako zachowaną.

### C5 — porównanie ścieżek
Porównać wynik z redukcją grafową/bryłową przez wspólne wielkości: relacje incydencji, liczbę stopni swobody, kąt orientacji, holonomię lub jawnie zdefiniowany niezmiennik. Nie wystarczy podobieństwo wizualne.

## 6. Status źródeł w GIA-TIMDR

W przeszukanym drzewie bieżącej gałęzi main nie znaleziono jeszcze źródłowego pliku z frazami/tematem π, √2, √3 i konstrukcji koła. Nie oznacza to, że konstrukcja nie istnieje w innych repozytoriach, archiwum, lokalnym katalogu autora lub wcześniejszych notatkach. Należy odzyskać źródło zamiast rekonstruować je z pamięci modelu.

## 7. Zasada robocza

Traktować ścieżkę π–√2–√3 jako niezależną gałąź badania redukcji. Nie wpisywać równości π=√2+√3 ani nie używać tej sumy jako dowiedzionego kąta/długości TIMDR. Priorytetem jest odzyskanie idealnej konstrukcji koła, normalizacji, operatora redukcji i dowodu dokładności lub zbieżności.
