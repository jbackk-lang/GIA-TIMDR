# 51B.13+ — minimalna pamięć procesu: twierdzenie, kontrprzykład, zegar

Data: 2026-11-17. Status: **formalizacja matematyczna i plan testów**, nie wynik eksperymentalny ani nowe odkrycie twierdzenia o stanach przyczynowych.

## Motto i zakres

**Czy istnieje najmniejsza reprezentacja przeszłości zachowująca całą informację o przyszłości?**

Następnie: **Czy predykcyjnie istotne obserwable M/S, G, K i META są projekcjami tej reprezentacji?**

„Przyszłość” oznacza wyraźnie określoną zmienną losową lub trajektorię F; minimalność jest relatywna do rozkładu procesu i obserwowanych informacji. Nie oznacza minimalnego wymiaru, liczby bitów ani kosztu obliczeniowego.

## 1. Twierdzenie (standardowe, nie nowe TIMDR)

Niech H i F będą zmiennymi losowymi o wartościach w przestrzeniach standardowych borelowskich. Niech K(h,·) będzie wersją regularnego rozkładu warunkowego F|H=h. Przestrzeń miar probabilistycznych na przestrzeni F wyposażamy w sigma-ciało ewaluacyjne. Definiujemy stan S=ε(H)=K(H,·).

**Wystarczalność:** dla każdego mierzalnego B zbioru możliwych przyszłości P(F∈B|H)=S(B) prawie na pewno. Ponieważ S jest funkcją H, z własności wieży P(F∈B|S)=S(B) prawie na pewno. Zatem F i H są warunkowo niezależne przy zadanym S.

**Minimalność:** niech T=g(H) będzie dowolnym innym deterministycznym stanem wystarczającym predykcyjnie: P(F∈B|H)=P(F∈B|T) p.n. dla wszystkich mierzalnych B. Wybierzmy regularny rozkład Q(t,·)=P(F∈·|T=t). Wtedy K(H,·)=Q(T,·) p.n. jako miary probabilistyczne (równość na przeliczalnej klasie generującej, a następnie rozszerzenie). Stąd S=q(T) p.n. dla mierzalnego q(t)=Q(t,·). Zatem każdy wystarczający stan T musi zachować co najmniej rozróżnienia obecne w S.

**Jednoznaczność:** tylko do równoważności mierzalnej / przelabelowania na nośniku rozkładu, p.n. Dwie wersje regularnych rozkładów mogą różnić się na historiach o zerowym prawdopodobieństwie.

**Granice:** nie twierdzimy, że S jest skończenie wymiarowy, obliczalny z danych skończonych, ma najkrótsze kodowanie ani że rekonstruuje H. To klasyczny rodzaj konstrukcji causal states / predictive sufficient statistics; TIMDR może wnieść nowe własności dopiero przez zegary, projekcje i kompresję.

## 2. Kontrprzykład: brak pełnej rekonstrukcji M/S i K

Niech X_0,X_1,… będą niezależnymi Bernoulli(1/2). H_t=(X_0,…,X_t), F_t=(X_{t+1},X_{t+2},…). Dla każdej historii h o dodatnim prawdopodobieństwie P(F_t∈·|H_t=h) jest ten sam rozkład produktu. S_t jest więc stały.

Jednak obserwabla M/S: X_t nie jest funkcją S_t, bo przy tym samym stanie S_t przyjmuje wartości 0 i 1 z dodatnim prawdopodobieństwem. Dla t≥1 obserwabla K: amplituda współczynnika FFT okna (X_{t-1},X_t) również bywa różna przy tym samym S_t (np. 00 kontra 01). Nie istnieją deterministyczne projekcje z S_t odzyskujące te obserwable.

**Rozstrzygnięcie:** hipoteza „wszystkie historyczne reprezentacje M/S,G,K,META są funkcjami S” jest ogólnie fałszywa. Sensowna hipoteza wymaga zdefiniowania **predykcyjnie istotnych** obserwabli; dla nich należy osobno dowieść faktoryzacji przez S. Gdy funkcja r(H) nie jest stała na klasach ε(H), nie faktoryzuje się przez S.

## 3. Testy zegara Chronoprocesu — trzy eksperymenty

### T1. Odwracalne przelabelowanie (kontrola zerowa)
- Proces: dwustanowy łańcuch Markowa z P(X_{t+1}=X_t)=0.9.
- Zegar A: indeks n; zegar B: deterministyczne, ściśle rosnące przekształcenie u=f(n), znane wraz z odwrotnością; zachowujemy te same obserwacje i te same zdarzenia przyszłe.
- Hipoteza: klasy równoważności historii są izomorficzne, mimo różnych znaczników czasu.
- Kontrola: ten sam warunkowy rozkład przyszłości po dopasowaniu indeksów; brak „odkrycia” wyłącznie z reskalowania osi.

### T2. Zegar zdarzeń usuwający czas oczekiwania
- Proces: zdarzenia odnowy o czasie oczekiwania zależnym od ukrytego reżimu Z∈{A,B}; np. warunkowo wykładniczy z intensywnością λ_A≠λ_B, reżim stały podczas trajektorii; każdemu zdarzeniu towarzyszy ten sam znacznik 1.
- Zegar A: fizyczne znaczniki zdarzeń i czasy oczekiwania; zegar B: wyłącznie numer kolejnego zdarzenia, bez interwałów.
- Cel: przewidywanie czasu do kolejnego zdarzenia. Historia A aktualizuje posterior Z; B traci tę informację. Różne filtracje, inne stany predykcyjne.
- Kontrola: porównanie także celu „kolejny znacznik”, dla którego zegar B może wystarczać. Zmiana przyszłości/targetu musi być jawna.

### T3. Zegar obrotowy z prędkością zmienną
- Proces: sygnał o impulsach fazowych związanych z kątem θ(t)=∫ω(s)ds i z modulacją uszkodzenia; ω(t) zmienne, rejestrowane.
- Wariant A: próbki w sekundach bez informacji o ω; B: próbki w kącie z jawną transformacją i tą samą dostępną informacją o ω; C: próbki w kącie z usuniętym przebiegiem ω.
- Cel 1: następny impuls względem kąta; cel 2: czas fizyczny do następnego impulsu.
- Oczekiwanie: B może poprawić stabilność reprezentacji numerycznej, ale przy pełnej odwracalności nie dowodzi przyrostu informacji; C może stracić informację potrzebną do celu 2.
- Mierniki: warunkowy log-loss / błąd predykcji, kalibracja, rozmiar stanu, odtwarzalność; osobno dokładność i koszt estymacji ω.

## 4. Bramka formalna przed eksperymentami
1. Ustalić filtracje, przestrzenie H i F oraz dostępność informacji w chwili predykcji.
2. Dla T1 dowieść izomorfizmu stanów; dla T2/T3 skonstruować pary historii sklejanych przez jeden zegar, ale rozróżnianych przez drugi.
3. Rozdzielić zmianę zegara od zmiany obserwacji i od zmiany celu przewidywania.
4. Nie dopasowywać preprocessingu ani parametrów na test; wyniki syntetyczne nie są niezależnym potwierdzeniem empirycznym.
5. Sprawdzić wcześniejsze wyniki linii 51B i literaturę computational mechanics / predictive state representations przed roszczeniem nowości.

## 5. Kryterium rozwoju GIA
Dla operatora C_GIA(H) mierzyć stratę predykcyjną względem pełnej historii oraz referencyjnego stanu ε(H), wraz z kosztem opisu. Uznawać kompresję za predykcyjnie bezstratną tylko przy jawnej równości rozkładów warunkowych (lub z góry ustalonej tolerancji dla wersji przybliżonej). Nie mylić selekcji PCA z dowodem kompresji przyczynowej.
