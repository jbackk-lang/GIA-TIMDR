# DNA → rozwój → helikalna morfologia: przegląd biologiczny dla TIMDR

**Data:** 2026-11-09  
**Status:** synteza literatury i audyt repozytoriów; nie jest to nowy dowód fizyczny ani wynik eksperymentu TIMDR.

## 1. Hipoteza użytkownika — sformułowanie robocze

Informacja dziedziczna może sterować powstawaniem struktur o geometrii helikalnej. DNA przenosi informację, a rozwój biologiczny przekształca ją przez mechanizmy molekularne, komórkowe i mechaniczne w geometrię organizmu lub muszli. W tym sensie DNA i helikalna morfologia są powiązane przez łańcuch przyczynowy, a nie przez konieczność przechowywania gotowego geometrycznego rysunku w DNA.

## 2. Co potwierdza literatura

### 2.1 Kierunek skrętu może być genetycznie sterowany

W ślimaku słodkowodnym *Lymnaea stagnalis* gen matczyny **Lsdia1** (formin związany z aktyną) został wykazany jako determinant kierunku skrętu muszli dextral/sinistral. W eksperymencie CRISPR bialleliczne mutacje frameshift prowadziły do sinistralnie skręconego potomstwa przez kolejne generacje na tle genetycznym normalnie dextralnym. Autorzy wskazali, że gen ustawia chiralność już na etapie jednokomórkowym, przed późniejszymi asymetriami rozwoju.

Źródło: Abe & Kuroda, *Development* (2019), PMID 31088796, https://pubmed.ncbi.nlm.nih.gov/31088796/

To jest mocny przykład, że informacja genetyczna może wpływać na znak chiralności organizmu i muszli. Nie oznacza jednak, że Lsdia1 koduje całą krzywą muszli.

### 2.2 Informacja genetyczna przechodzi przez komórkowy mechanizm rozwoju

Badania nad *Lymnaea* opisują sekwencję: gen/matczyny produkt → organizacja cytoszkieletu i orientacja pierwszych podziałów → asymetria lewo/prawo → asymetria ciała. Praca o fizycznych podstawach chiralnego skrętu muszli podkreśla, że cytoszkielet i mechanika rozwoju komórek są pośrednikami, a relacja między spiralnym bruzdkowaniem zarodka a późniejszym skrętem muszli nie jest prostym odwzorowaniem 1:1.

Źródło: *The physical basis of mollusk shell chiral coiling*, PNAS (2021), https://pmc.ncbi.nlm.nih.gov/articles/PMC8651239/

### 2.3 Geometria muszli powstaje przez przyrostowy wzrost i mechanikę

Badanie wzrostu i morfogenezy muszli gastropodów wykazało asymetrie proliferacji i orientacji podziałów w nabłonku płaszcza, które korelują z kluczowymi cechami wzrostu muszli. Autorzy opisują logarytmiczny skręt jako wspólną geometrię wielu muszli, ale wskazują, że mechanizmy rozwojowe są złożone i zależą od regionalnych stref wzrostu.

Źródło: *Growth and morphogenesis of the gastropod shell*, PNAS (2019), https://pmc.ncbi.nlm.nih.gov/articles/PMC6452709/

Model mechaniczny z 2021 r. proponuje ponadto, że interakcja między miękkim ciałem ślimaka a rosnącą muszlą może generować skręt; geometria nie wynika wyłącznie z lokalnego programu wydzielania na brzegu muszli.

Źródło: *The physical basis of mollusk shell chiral coiling*, PNAS (2021), https://pmc.ncbi.nlm.nih.gov/articles/PMC8651239/

Przegląd biologii muszli wskazuje na współdziałanie mechanizmów genetycznych/komórkowych i fizycznych, w tym białek macierzy, regulacji rozwoju, mineralizacji, ograniczeń wzrostu i samoorganizacji.

Źródło: *Deciphering mollusc shell production*, Biological Reviews (2020), https://onlinelibrary.wiley.com/doi/full/10.1111/brv.12640

### 2.4 DNA samo jest nośnikiem informacji i strukturą helikalną, ale są to dwie różne własności

DNA łączy sekwencyjny zapis zasad z fizykochemicznymi właściwościami polimeru. Sekwencja wpływa zarówno na kodowanie RNA/białek, jak i na lokalne właściwości strukturalne DNA. Nie należy jednak utożsamiać helisy molekularnej DNA z makroskopową spiralą muszli: to różne obiekty, skale i mechanizmy.

Źródło: *DNA structure and function*, FEBS Journal (2015), https://onlinelibrary.wiley.com/doi/10.1111/febs.13307

## 3. Łańcuch przyczynowy — użyteczny dla TIMDR

Proponowany biologiczny łańcuch (nie nowy aksjomat):

`DNA / informacja dziedziczna`
→ `ekspresja genów i produkty matczyne`
→ `stan cytoszkieletu / organizacja komórki`
→ `orientacja podziałów i chiralność zarodka`
→ `asymetria ciała i organizacja płaszcza`
→ `lokalne pole wzrostu + wydzielanie + mechanika`
→ `przyrostowa geometria muszli`.

Ważne: DNA nie musi kodować współrzędnych każdej części muszli. Wystarczy, że steruje regułami i parametrami procesu rozwojowego, który iteracyjnie wytwarza strukturę.

## 4. Mapowanie na język TIMDR — tylko analogia funkcjonalna

| Biologia | Rola w modelu TIMDR | Status |
|---|---|---|
| Sekwencja DNA / dziedziczna regulacja | informacja wejściowa / warunki początkowe | rzeczywisty nośnik biologiczny |
| Ekspresja genów / białka | transformacja informacji do działania komórkowego | znany mechanizm biologiczny |
| Cytoszkielet i organizacja komórek | stan pośredni (z) | znany mechanizm biologiczny |
| Asymetria wzrostu płaszcza | lokalne pole/warunki brzegowe wzrostu | obserwowane w badaniach |
| Mechanika ciała i muszli | sprzężenie zwrotne / ograniczenia fizyczne | modelowane i częściowo badane |
| Przyrost geometrii muszli | obserwowalne wyjście (y) | mierzalna morfologia |

Schemat dynamiczny:
`z(t+1) = F(z(t), D, e(t), m(t))`
`y(t+1) = y(t) + G(z(t), m(t))`

gdzie D oznacza informację dziedziczną, e — stan/aktywność komórkową, m — mechaniczne i środowiskowe warunki wzrostu, z — stan rozwojowy, y — geometrię rosnącej muszli. Jest to abstrakcja organizująca znane etapy, nie zwalidowane równanie biologiczne.

## 5. Co wykazał audyt repozytoriów TIMDR

- **TIMDR-DNA** nie modeluje morfogenezy ani geometrii DNA. Jest narzędziem demonstracyjnym do analizy głębokości pokrycia sekwencjonowania i kandydatów CNV; README jawnie zaznacza, że nie jest narzędziem klinicznym i testy używają danych syntetycznych.
- **Helix-Lock** jest projektem kryptograficznym/plikowym. „Helix” w nazwie nie oznacza modelu biologicznej helisy ani dynamiki DNA.
- **GIA-TIMDR** ma rozdzielone moduły sygnału, geometrii i odpowiedzi mechanicznej, ale nie ma biologicznego łańcucha DNA→rozwój→morfologia ani skalibrowanego prawa sprzężenia.
- Wcześniejszy eksperyment MAGE potwierdził możliwość przechowania uporządkowanej historii przyrostów fazy w reprezentacji FFT. Nie stanowi dowodu biologicznego ani dowodu, że DNA/muszla realizują ten sam operator.

## 6. Wniosek

Hipoteza w jej ostrożnej postaci jest zgodna z biologią: **informacja DNA może sterować regułami rozwoju, które przez komórkowe i mechaniczne procesy wytwarzają chiralną/helikalną morfologię**. Dla *Lymnaea stagnalis* istnieje szczególnie mocny dowód genetyczny dla kierunku skrętu.

Nie wynika z tego, że:
- każda helisa biologiczna ma ten sam mechanizm;
- DNA przechowuje gotowy kształt muszli jako bezpośredni geometryczny wzorzec;
- makroskopowa muszla jest powiększoną kopią helisy DNA;
- obecny model G-Rezonans lub GS-Matrix opisuje ten biologiczny proces.

Najbardziej obiecujący most do TIMDR to nie podobieństwo wizualne spiral, lecz **informacja → pośredni stan dynamiczny → lokalne reguły wzrostu → przyrost geometrii → sprzężenie zwrotne mechaniki**.

## 7. Minimalny następny test

Nie zaczynać od twierdzenia, że DNA i muszla mają tę samą fizykę. Zbudować test rozdzielający trzy poziomy:
1. **kod/warunki początkowe:** parametr chiralności dziedzicznej (dextral/sinistral);
2. **reguła procesu:** przyrostowy model wzrostu brzegu muszli z różnicą lokalnych prędkości/ekspansji;
3. **geometria wyjściowa:** znak skrętu, tempo wzrostu, promień kolejnych zwojów i odchylenie od modelu logarytmicznego.

Test powinien sprawdzić, czy zmiana parametru chiralności i reguł wzrostu odtwarza jakościowo znane klasy geometrii, bez dopasowywania parametrów do wyniku testowego. W drugiej kolejności dodać sprzężenie mechaniczne miękkiego ciała z krawędzią muszli.

**Decyzja:** traktować biologię muszli jako wzorzec architektury informacji sterującej rozwojem. Nie utożsamiać tego jeszcze z fizycznym mechanizmem helisy TIMDR.
