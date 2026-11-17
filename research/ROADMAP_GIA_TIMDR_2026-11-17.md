# GIA-TIMDR — decyzja badawcza i plan pracy (2026-11-17)

Status: **plan rozwojowy i audyt statyczny**, nie nowy wynik empiryczny. Nie zmienia historycznych prerejestracji ani wyników.

## Decyzja
TIMDR rozwijamy przede wszystkim jako **framework konstrukcji reprezentacji i operatorów procesowych**, nie jako twierdzenie o uniwersalnej przewadze klasyfikatora. Priorytet: (1) Chronoproces i dobór zegara, (2) fizycznie zakotwiczone reprezentacje M/S↔K, (3) formalne własności GIA, (4) META-DYNAMICS jako odrębna hipoteza o zmianie reżimów.

## Co już jest
- Cztery gałęzie M/S, G, K, META i wspólny Chronoproces: `README.md`, `ARCHITEKTURA_TIMDR.md`, `docs/theory/TIMDR_Chronoprocess.md`.
- Referencyjny graf zdarzeń, zamrożona selekcja PCA, projekcje i kontrole syntetyczne: `docs/theory/TIMDR_EventGraph_Branch_Construction.md`, `core/trm_gia_projections.py`.
- Historyczne testy z sukcesami i porażkami: `STAN_PROJEKTU.md`. Wynik aplikacyjny nie stanowi dowodu na całą teorię.
- Wcześniejsze audyty porównania modeli i krzywych uczenia: `research/benchmark/TIMDR_HMM_LSTM_TRANSFORMER_AUDIT_2026-11-17.md` oraz `TIMDR_PADERBORN_CODE_AUDIT_2026-11-17.md`.

## Ustalenia wymagające korekty metodologicznej
1. **Preprocessing transdukcyjny / leakage statystyk**: `core/real_paderborn_resonance_sieve.py::score` definiuje `stdz(X)` i wylicza średnią/odchylenie dla wszystkich próbek danego warunku `cond`, a dopiero potem korzysta z indeksów `tr` i `te`. Tak samo `core/real_paderborn_real_damage.py::evaluate`. Statystyki cech testowych uczestniczą w transformacji. To nie jest dopasowanie wyłącznie na treningu. Wymaga osobnego, jawnie eksploracyjnego przeliczenia; **nie wolno po cichu nadpisać historycznych RESULT**.
2. **Nierówna informacja wejściowa**: w Paderborn TIMDR wykorzystuje `rpm(cond)`; porównywane reprezentacje raw/spec nie otrzymują jawnie tej samej zmiennej. Kontrola: raw/spec ±RPM, TIMDR ±kotwica RPM, te same łożyska/foldy.
3. **Zużyty holdout**: pomiary Paderborn były już wielokrotnie oceniane. Powtórka na nich służy audytowi i developmentowi, nie nowemu niezależnemu potwierdzeniu.
4. **Wynik syntetyczny != empiryczny**: testy TRM/GIA dowodzą własności konkretnej konstrukcji pod podanymi założeniami, nie przewagi nad modelami sekwencyjnymi.
5. **Ograniczenia infrastruktury**: dostępność archiwum, możliwość rozpakowania, poprawny schemat MATLAB i realne obliczenie to oddzielne bramki. Nie uznawać zielonego pobrania za eksperyment.

## Cztery strumienie pracy

### A — Chronoproces / zegar (najwyższy priorytet)
Pytanie: kiedy reprezentacja względem zdarzenia, fazy lub obrotu poprawia uogólnianie wobec czasu fizycznego?
- Wspólne wejście i identyczne informacje pomocnicze dla wszystkich wariantów.
- Testy niezmienniczości na syntetycznych sygnałach z kontrolowaną zmianą tempa, szumem i dryftem; osobno testy na nowym realnym źródle.
- Ablacje: czas zwykły / czas znormalizowany / oś kątowa; zewnętrzny RPM kontra RPM estymowane z sygnału.
- Mierniki: błąd, stabilność na zmianę tempa, opóźnienie, koszt; z góry określony próg sukcesu.

### B — Reprezentacje M/S↔K
Pytanie: czy fizycznie interpretowalne kotwice i normalizacja tła zwiększają przenoszalność między urządzeniami?
- Zestawić proste baselines: envelope, order spectrum, PSD, STFT, klasyczne cechy + LDA/logistic/RF.
- Oddzielić korzyść z cech, metadanych i klasyfikatora; wyrównać budżet strojenia.
- Grupować train/test po fizycznym urządzeniu; skalery i selekcję cech dopasowywać **tylko na train**.

### C — Matematyka GIA
Pytanie: które własności selekcji grafu zachodzą przy zamrożonej referencji, a które przy ponownym dopasowaniu?
- Formalnie odróżnić monotoniczność względem inkluzji, idempotencję, stabilność z marginesem i odporność na kontaminację.
- Wykazać kontrprzykłady dla braku marginesu, zdegenerowanego PCA, refitowania i zmiany jednostek.
- Testy własności + krótkie dowody z jawnymi założeniami. Nie nazywać samego PCA rezonansowym pomiarem fazowym.

### D — META-DYNAMICS
Pytanie: czy (Λ,τ,ρ,J) przewiduje zmianę reżimu wcześniej niż klasyczne metody change-point?
- Definiować reżim, czas dostępności informacji i jednostkę obserwacji przed testem.
- Porównać CUSUM, EWMA i prosty detektor zmian z wariantami META.
- Kontrolować leakage przyszłości, fałszywe alarmy i opóźnienie detekcji.

## Kolejność i kryteria stopu
1. **Teraz**: zamrozić eksperymentalne automatyczne pobieranie Paderborn; zachować kod i historię. Nie dodawać nowych uruchomień bez diagnostyki.
2. **Audyt**: przygotować wersję train-only preprocessingu jako nową implementację/analizę; zachować stary kod i wynik dla reprodukcji.
3. **Dowody formalne**: GIA property tests i kontrprzykłady; możliwe bez danych zewnętrznych.
4. **Pierwszy nowy eksperyment**: wybrać jedno pytanie o zegar lub kotwicę, prerejestrować protokół i nowe dane niezależne od historycznego Paderborn.
5. **Dopiero potem**: benchmark modeli; raportować wszystkie wyniki, również zerowe i negatywne.

Bramka jakości każdego eksperymentu: jawne źródło + manifest i checksumy, jawny split, train-only preprocessing, parytet informacji wejściowej, kontrola negatywna, wersja kodu, koszt obliczeń, wynik i ograniczenia.

## Czego nie twierdzimy
Nie ma na dziś niezależnego dowodu, że TIMDR jako całość przewyższa HMM/LSTM/Transformer. Pojedyncze sukcesy aplikacyjne nie dowodzą ogólnej przewagi ani nowych praw fizyki. Prerejestracje i stare wyniki zachowują historyczny status.

## Zakres przeglądu
Sprawdzono główne dokumenty architektury, stanu projektu, Chronoprocesu, konstrukcji EventGraph, dwa skrypty Paderborn oraz wcześniejsze audyty. Nie wykonano pełnego audytu wszystkich plików i repozytoriów ekosystemu; dalsze twierdzenia wymagają takiej weryfikacji.
