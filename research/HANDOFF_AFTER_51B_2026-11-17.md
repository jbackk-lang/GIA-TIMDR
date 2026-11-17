# GIA–TIMDR — przekazanie prac po serii 51B

**Data:** 2026-11-17  
**Status:** seria syntetyczna 51B zamknięta roboczo; brak potwierdzonej przewagi operacyjnego GIAFilter na rzeczywistych danych.  
**Cel:** umożliwić kontynuację badań bez powtarzania eksperymentów i bez przenoszenia nieuzasadnionych twierdzeń.

## 1. Co jest ustalone

1. Dla reprezentacji `Z=C(H)` deterministycznie wyznaczonej z historii `H`, nierówność przetwarzania danych daje `I(F;Z) <= I(F;H)`. Geometria nie tworzy informacji o przyszłości spoza historii. **Nie wyklucza to** przewagi jednej niedoskonałej reprezentacji nad drugą; wyklucza przewagę nad globalnym optimum w tej samej klasie i przy tym samym budżecie.
2. 51B.18: istnieje konstruktywny proces, w którym geometryczne odrzucenie rzadkiego sygnału daje dodatnią stratę predykcyjną. Weryfikacja użytkownika dotyczyła referencyjnego `gia_select`, nie operacyjnego `GIAFilter`.
3. 51B.19: dokładna optymalizacja predykcyjna osiąga `Delta=0` w prostym syntetycznym zadaniu, podczas gdy selekcja geometryczna może mieć `Delta>0`. Hybryda zależy od siły kary geometrycznej.
4. 51B.20–22: w syntetycznych modelach trafny prior może poprawić efektywność próbkową, a błędny ją pogorszyć. `n_epsilon` jest pierwszym punktem **badanej siatki**, nie teoretycznym minimum; granice Wilsona były punktowe i bez korekty na wybór progu/wielokrotne porównania.
5. 51B.23: test referencyjnego wyboru geometrycznego przy ręcznie sterowanej zgodności pozycji; w raportowanym przebiegu nie wykazano przewagi H nad P. Lokalny test był rekonstrukcją używanych funkcji, nie bezpośrednim wykonaniem checkoutu.
6. 51B.24: syntetyczna kalibracja PCA; wyniki wskazują zależność od zgodności geometrii z sygnałem. Lokalna implementacja odpowiadała algorytmowi referencyjnemu, nie operacyjnemu.
7. 51B.25: audyt skali operacyjnej logiki `GIAFilter`; `max_residual` wymaga kalibracji. Test lokalny dotyczył rekonstrukcji logiki, nie bezpośredniego importu klasy.

**Najbardziej obronny wniosek:** geometria może być użytecznym uprzedzeniem indukcyjnym / regularizatorem, ale jej korzyść zależy od zgodności z procesem, kosztu błędów i budżetu reprezentacji. Nie ma obecnie dowodu ogólnej ani rzeczywistej przewagi predykcyjnej operacyjnego GIAFilter.

## 2. Czego nie ustalono

- Przewagi `filters/_vendor_senscore_gia_filter.py::GIAFilter` na niezależnych danych rzeczywistych.
- Przewagi asymptotycznej nad dokładnym predykcyjnym optimum przy tym samym budżecie.
- Uniwersalnej poprawy `n_epsilon` dzięki geometrii.
- Odporności na zmianę domeny i rozkładu; wartości `Gamma(Z)=I(F;E|Z)` dla rzeczywistych środowisk.
- Równości kosztu bitowego reprezentacji (liczba zdarzeń jest tylko uproszczonym przybliżeniem).
- Braku przecieku informacji w starszych benchmarkach, jeżeli standaryzacja była dopasowana do całego zbioru lub występowały skorelowane okna z tej samej jednostki fizycznej.

**Uwaga o weryfikacji:** odróżniać (a) wykonanie kodu przez użytkownika, (b) wykonanie lokalne, (c) lokalną rekonstrukcję modułu i (d) samo zapisanie kodu na GitHubie. Nie zamieniać żadnej z tych kategorii w inną w raportach. Wyniki 51B.23–25 nie zastępują bezpośredniego testu oryginalnego operacyjnego modułu.

## 3. Główny kierunek, gdy dane będą dostępne: jeden uczciwy benchmark

**Pytanie:** czy operacyjny `GIAFilter` poprawia predykcję lub efektywność próbkową względem P i prostych baseline'ów, przy identycznym rzeczywistym koszcie reprezentacji?

Protokół minimalny:
1. Wybrać jeden zbiór danych zawierający surowe hity / pozycje / czas i przyszłą etykietę lub przyszłe obserwacje. Jeśli brak współrzędnych hitów, **nie** udawać testu GIAFilter.
2. Podział według niezależnych jednostek fizycznych / przebiegów / urządzeń, nie losowo według sąsiadujących okien. Osobno train, validation, test.
3. Wszystkie parametry geometrii, normalizacji, progów i modeli dopasowywać wyłącznie na train/validation. Test pozostaje nietknięty.
4. Porównać: bez filtra, geometryczny G, czysto predykcyjny P, hybrydowy H, oraz kontrolę losową; identyczny budżet bitowy lub raport krzywej jakość–koszt. Liczyć metadane, identyfikatory, czas i graf.
5. Raportować `Delta` lub odpowiednio skalibrowany proper scoring rule, częstość rzadkich błędów, `Delta(n)`, `n_epsilon`, przedziały ufności z resamplowaniem na poziomie jednostki fizycznej oraz koszty obliczeniowe.
6. Raportować wyniki negatywne, także gdy GIA nie daje korzyści. Zamrozić protokół przed analizą testu.

**Blokada na dziś:** brak niezawodnego pobrania danych zewnętrznych w środowisku wykonawczym (błędy DNS). Nie twierdzić, że rzeczywisty benchmark został wykonany.

## 4. Alternatywne kierunki badań

### A. Teoria minimalnego stanu predykcyjnego (bez GIA)
Badać `S_H=P(F|H)`, klasy równoważności historii i mierzalne aproksymacje `S_H`. Cel: zidentyfikować, co dokładnie musi przetrwać kompresję, zanim narzuci się geometrię. Kryterium: `Delta=I(F;H|Z)`.

### B. Predykcyjna kompresja przy prawdziwym budżecie
Porównać `min Delta(Z)` przy ograniczeniu `L(Z)<=B` (liczba bitów, wliczając pozycje, czasy, identyfikatory, krawędzie i parametry filtra). Wykreślić front Pareto: jakość–rozmiar–czas. To usuwa pozorną równość wynikającą z samej liczby zdarzeń.

### C. Odporność środowiskowa / transfer
Badać `Gamma(Z)=I(F;E|Z)` oraz zmianę ryzyka przy przejściu train→test do innej domeny. Warunek: środowiska rzeczywiście rozdzielone, bez dopasowania parametrów do domeny testowej.

### D. Kalibracja i selekcja prioru
Zamiast zakładać trafność geometrii `q`, estymować jej wartość na walidacji i włączać regularizację tylko wtedy, gdy przewidywany zysk przewyższa koszt błędów. Porównać stałe `lambda` z adaptacyjnym `lambda`; uwzględnić koszt samego strojenia.

### E. Analiza rzadkich zdarzeń i bezpieczeństwa utraty informacji
Dla zdarzeń rzadkich raportować nie tylko średnią `Delta`, lecz warunkowy KL, recall sygnału i maksymalną stratę w podgrupach. Cel: zapobiec ukryciu dużych strat przez małą częstość.

### F. Inżynieria i audyt operacyjnego filtra
Bez nowych twierdzeń teoretycznych: testy regresyjne oryginalnej klasy, skala `max_residual`, deterministyczność `_robust_axis`, przypadki degeneracji PCA, testy jednostek i powtarzalność wersji vendora. Osobno sprawdzić, czy filtr zawsze zachowuje zamierzony budżet.

## 5. Kryterium zakończenia kolejnej fazy

Nie mnożyć kolejnych syntetycznych przykładów „PASS”. Nowa faza kończy się jednym z dwóch uczciwych wyników:
- **Wynik pozytywny:** niezależny test oryginalnego `GIAFilter` pokazuje istotny i powtarzalny zysk przy porównywalnym koszcie reprezentacji, bez przecieku danych.
- **Wynik negatywny:** brak przewagi, udokumentowane warunki zawodności i decyzja, czy geometria ma pozostać tylko opcjonalnym priorem.

## 6. Pliki źródłowe

- `research/51B18_GIA_RARE_EVENT_TEST.py`
- `research/51B19_EXACT_BUDGET.py`
- `research/51B20_FINITE_SAMPLE.py`
- `research/51B22_PRIOR_ROBUSTNESS.py`
- `research/51B22_PRIOR_ROBUSTNESS_REPORT.md`
- `research/51B23_REFERENCE_GIA_PRIOR.py`
- `research/51B23_REFERENCE_GIA_PRIOR_REPORT.md`
- `research/51B25_OPERATIONAL_GIA_SCALE_AUDIT.md`
- `core/trm_gia_projections.py`
- `filters/_vendor_senscore_gia_filter.py`

51B.21 i 51B.24 mają lokalne artefakty z wcześniejszej sesji; nie zakładać ich obecności w repozytorium bez osobnej weryfikacji.

---

**Decyzja przekazania:** zakończyć bieżącą serię 51B bez deklaracji przewagi GIA. Preferowany dalszy krok: rzeczywisty benchmark operacyjny, gdy dostępne będą dane. Jeżeli nie, wybrać jeden z kierunków A–F i sformułować niezależne kryterium falsyfikacji przed rozpoczęciem pracy.
