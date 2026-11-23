# Audyt implementacji formalizmów — 23.11.2026

**Stan kodu objęty audytem:** commit [93445b81](https://github.com/jbackk-lang/GIA-TIMDR/commit/93445b81).  
**Potwierdzenie wykonania:** [GitHub Actions run #45100749836](https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/45099524340).

Ten dokument zapisuje konkretne kontrole i poprawki wykonane po audycie spójności dokumentacji. Zielone testy potwierdzają zachowanie implementacji w sprawdzonym zakresie; nie są dowodem prawdziwości wszystkich aksjomatów ani walidacją empiryczną.

## Zakres

Przejrzano implementacje i testy czterech obszarów:

- Math / M–S — szeregi sygnałowe, demodulacja obwiedni, GS-Matrix i protokół statystyczny;
- Geometry / G — siatki, normalne i dyskretny operator kształtu Weingartena;
- Modal / K — fazy, interferencja i rezonans;
- Time — nośnik Chronoprocesu oraz most Fouriera M/S↔K.

## Zmiany merytoryczne

### Math / M–S

- Funkcje sygnałowe odrzucają puste, wielowymiarowe i niefinitywne wejścia oraz niepoprawne parametry próbkowania/pasm.
- Detektor anomalii obsługuje jawne, niezależne okno referencyjne. Ujawniono i udokumentowano ograniczenie historycznego trybu in-sample: przy n≤5 i progu 2σ żaden punkt nie może zostać oznaczony. Dla krótkich okien zalecana jest referencja niezależna od ocenianych próbek.
- Kalibracja rezonansu używa domyślnie rozkładu Poissona-dwumianowego z empirycznych marginalnych częstości flag. Normalny baseline P(|Z|>2) jest dostępny jawnie tylko dla niezależnego baseline populacyjnego/referencyjnego.
- defekt_flags() nie wyłącza już detekcji, gdy percentylowy rozstęp P90–P10 jest zerowy. Seria stała nadal daje brak flag, ale rzadki niezerowy skok jest wykrywany.
- Widmo amplitudowe obwiedni stosuje poprawne skalowanie jednostronne: biny wewnętrzne są podwajane, DC i Nyquist nie.
- GS-Matrix waliduje wymiary i skończoność macierzy, stanu początkowego oraz parametrów integracji.
- Protokół prerejestracji tworzy migawkę parametrów i weryfikuje fingerprint przy odczycie pliku; modyfikacja zapisanych parametrów bez aktualizacji fingerprintu jest odrzucana.
- Generator AR(1) wymaga stacjonarnego zakresu |phi| < 1; test Manna–Whitneya waliduje próby i używa zgodnej aproksymacji asymptotycznej w backendach SciPy/NumPy.
- Werdykt testu rangowego nie przedstawia Manna–Whitneya jako ogólnego testu median. Sparowany test Wilcoxona raportuje ograniczoną do [-1,1] korelację rangowo-dwuseryjną.
- Korekta Bonferroniego i poziom alfa odrzucają niepoprawne wartości wejściowe.
- Interpretacja testów rangowych rozróżnia mediany opisowe od kierunku efektu rangowego; sparowany Wilcoxon używa ograniczonej do [-1,1] korelacji rangowo-dwuseryjnej.
- Operator Theta_bif i klasyfikator sygnału walidują dziedzinę parametrów, progi, maski cutoff i spójność kanałów.
- Aksjomat S5 został poprawiony: miara zero dotyczy algebraicznych granic w przestrzeni całych wektorów próbek i wymaga absolutnej ciągłości łącznego rozkładu wejścia.

### Geometry / G

- Mesh odrzuca niefinitywne współrzędne, indeksy poza zakresem, indeksy niecałkowite, powtórzone wierzchołki i trójkąty o zerowym polu.
- Dyskretny operator kształtu sprawdza indeks punktu, rozmiar tablicy normalnych i listy sąsiedztwa; normalne sąsiadów są normalizowane przed dopasowaniem.
- Zachowano jawny test konwencji znaku krzywizny dla sfery z normalnymi skierowanymi na zewnątrz.
- Definicje G3–G9 doprecyzowują zależność od przesunięcia i stycznej projekcji oraz nie przypisują różniczkowalności normy w zerze.

### Modal / K

- Rezonans porównuje fazy jako kąty modulo 2π, przez najkrótszą odległość kołową.
- Parametry modalności i czasy wejściowe muszą być skończone; tolerancje rezonansu muszą być nieujemne.
- Predykat is_resonant() zwraca natywną wartość logiczną.
- Aksjomat K5 i opis implementacji są zgodne co do faz początkowych oraz ścisłych progów.

### Time / Chronoprocess i Fourier

- Nośnik Chronoprocesu musi być skończony i ściśle rosnący; odrzucane są również odstępy, których nie da się reprezentować w typie float.
- Most Fouriera waliduje jednowymiarowość sygnału, skończoność próbek i dodatni, skończony krok próbkowania.
- Momenty energii są liczone ze skalowaniem wag, aby ograniczyć przepełnienia dla dużych, ale skończonych amplitud.
- DC jest rozpoznawane jako dokładnie zerowa częstotliwość; małe dodatnie częstotliwości pozostają binami wewnętrznymi.
- Zachowano wagi energii Parsevala dla DC, binów wewnętrznych i Nyquista.

## Wynik CI

| Zestaw | Wynik |
|---|---:|
| Math / M–S | 343 passed |
| Geometry / G | 123 passed |
| Modal / K | 42 passed, 5 skipped |
| Time | 38 passed |
| **Razem** | **573 passed, 5 skipped** |

Wszystkie trzy zadania workflow Repository regression checks zakończyły się sukcesem: formalism-regressions, compatibility-and-syntax i uncovered-regressions.

**Pięć pominiętych przypadków Modal** wymaga zewnętrznych plików fal sejsmicznych Ridgecrest 2019 z repozytorium siostrzanego TIMDR-Earthquake-Core/data/ridgecrest_2019/real_waveform_CLC_RIO/*.csv. Nie są to zaliczone testy ani wynik walidacji na realnych danych. Pozostałe wyniki CI są testami implementacji i przypadków syntetycznych.

## Ograniczenia pozostające jawnie otwarte

1. Nie wykonano pełnej walidacji Geometry na niezależnym zbiorze rzeczywistych pomiarów powierzchni.
2. Testy Modal na realnych danych Ridgecrest pozostają pominięte, dopóki wymagane pliki nie będą dostępne w checkoutcie.
3. skret_flags() liczy nachylenia po indeksie próbki, a nie względem nieregularnych znaczników czasu. Dokumentacja jawnie ogranicza jego zakres; wariant timestamp-aware pozostaje osobnym zadaniem.
4. Testy syntetyczne nie dowodzą prawdziwości aksjomatów ani skuteczności detektorów w dowolnej domenie.
5. Most Fouriera opisuje dyskretną transformację sygnału czasu do reprezentacji częstotliwościowej; nie jest modelem ani dowodem fizycznej dualności korpuskularno-falowej fotonu.

## Wniosek

Wykryte niezgodności implementacyjne i błędy dziedziny wejściowej zostały poprawione i objęte regresjami. Dokumentacja kluczowych formalizmów została zsynchronizowana z zakresem testów. Audyt naukowy i empiryczny nie jest zakończony; powyższe ograniczenia pozostają częścią statusu projektu.
