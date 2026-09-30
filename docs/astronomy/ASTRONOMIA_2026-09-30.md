# Astronomia i obserwacje — stan na 30.09.2026

Dwie aplikacje należą do **narzędzi inżynierskich / prototypów badawczych**, poddziedzina astronomia i obserwacje. Nie są dodatkowymi gałęziami formalnymi TIMDR. TIMDR jest ramą konstrukcyjną: wybór zegara, reprezentacji, odniesienia, kontroli jakości i porównań. Skuteczność każdej adaptacji oceniamy osobno.

## TIMDR-orbital-tracker

[Repo i pełna instrukcja](https://github.com/jbackk-lang/TIMDR-orbital-tracker) · [lokalna kopia kodu](../../applications/astronomy/TIMDR-orbital-tracker/).

Publiczne elementy orbitalne CelesTrak → klasyczny SGP4/Skyfield → pozycja, prędkość, kierunek obserwacji i przeloty. Dodano kojarzenie pomiarów z katalogiem oraz krótkoterminową korekcję kierunku. Dane ręczne, CSV/HTTP, pierwszy adapter Bluetooth SPP/COM/LX200. Zegar fotometryczny jest osobnym eksperymentem, nie pomiarem prędkości orbitalnej z jasności.

Według dokumentacji źródłowej: 23 testy i 30 syntetycznych prób śledzenia. Nie powtarzano ich przy tej synchronizacji dokumentacji. Są rzeczywiste elementy orbitalne, ale brak niezależnej walidacji na rzeczywistych pomiarach pozycji i na fizycznym teleskopie. Nie deklarujemy dokładności w metrach ani przewagi nad SGP4. Oryginalne wyniki: docs/VALIDATION_RESULTS.md w repo aplikacji.

## TIMDR-lightcurve-fewshot

[Repo i pełna instrukcja](https://github.com/jbackk-lang/TIMDR-lightcurve-fewshot) · [lokalna kopia kodu](../../applications/astronomy/TIMDR-lightcurve-fewshot/).

Gałąź sygnałowa M/S inspirowała reprezentację fazową i sito oparte na zgodności harmonicznych w czterech fragmentach obserwacji. Klasyfikator LDA i porównania z klasycznymi cechami, lasem losowym oraz siecią pozostają standardowymi narzędziami. To nowa adaptacja, nie przeniesiony wprost algorytm turbiny.

### Wyniki i granice

- **OGLE LMC:** 2000 gwiazd, klasy RRab/RRc/CEP-F/CEP-1O, 800 obiektów testowych, 30 losowań wsparcia, 4–160 etykiet na klasę, znane okresy katalogowe. Przy 160: macro-F1 TIMDR 96,70%, faza bez sita 96,43%, klasyczne + RF 97,78%. Główny wynik dla małych budżetów 4/8/16/32: różnica TIMDR–RF −1,59 pp (95% CI −2,17…−0,97); przewaga niepotwierdzona. Wyniki: RESULTS.md i PROTOCOL.md w repo źródłowym.
- **ASTROMER 1:** eksploracyjne porównanie zamrożonego enkodera MACHO + uśrednianie + metadane + LDA. Przy 160: 89,42%. To nie ASTROMER 2 ani pełne dostrajanie sieci; możliwe pokrycie obiektów pretreningu nie zostało wykluczone. Bez ogólnego twierdzenia o przewadze nad ASTROMER.
- **Tani pilot ATLAS:** 20 etykiet na klasę, 3 podziały, po 400 obiektów testowych, CB/DB/Mira/Pulse, okres szacowany z maks. 200 pomiarów. Macro-F1: TIMDR **84,82%**, faza bez sita **85,78%**, klasyczne + RF **91,35%**, kontrola losowych etykiet **24,82%**. Obecne sito nie poprawiło wyniku. Publiczne archiwum i przygotowanie danych różnią się od końcowego protokołu ASTROMER 2; wyników nie można traktować jako bezpośredniego pojedynku. [Raport i kod pilota](../../applications/astronomy/TIMDR-lightcurve-fewshot/experiments/atlas_budget/RAPORT.md).

### Ułatwienie pracy obserwatora

Lokalny interfejs CSV/DAT: jakość danych, faza, harmoniczne, wyjaśnienia, diagnostyka okresu i porównania OGLE. Tryb zdjęć czerpie pomysł osobnych wskazań i nakładek z **MAGE-IN-IMAGE-DECODER**; nie używa jego detektorów koloru jako astronomicznego dowodu.

Zdjęcie → kandydaci na gwiazdy i diagnostyka. Seria skalibrowanych, wyrównanych FITS → klasyczna fotometria względem wybranej gwiazdy odniesienia → CSV lub bezpośrednie przekazanie krzywej do głównego okna. Pomiar nie filtruje pikseli sitem TIMDR. Domyślny folder images/inbox; trzy syntetyczne przykłady po 96 klatek, trzy cykle i zadany okres 0,56 dnia: zmienna gwiazda, stała gwiazda, trzy prześwietlone klatki. Poprawny wynik dla stałej gwiazdy to diagnostyka słabego sygnału, nie wymuszona klasyfikacja.

**38 testów automatycznych przeszło lokalnie** po integracji zdjęcia → krzywa → analiza. Seria zmienna: 96 pomiarów, prześwietlona: 93 poprawne i 3 odrzucone. Wskazania klasy na symulacji służą demonstracji, nie walidacji astrofizycznej. Brak niezależnej walidacji fotometrii na rzeczywistym niebie, automatycznego wyrównywania, kalibracji dark/flat, identyfikacji katalogowej i potwierdzania stałości odniesienia.

## Kod, pochodzenie i dalsze badania

[Snapshoty źródeł i manifest SHA-256](../../applications/astronomy/README.md). Pełne aplikacje rozwijane są w osobnych repo. Włączono stan lokalny, także zmiany jeszcze nieopublikowane; odnośnik GitHub nie oznacza, że zawiera już każdą lokalną funkcję.

Następny etap: niezależne rzeczywiste obserwacje, porównanie fotometrii ze standardowym narzędziem oraz test reprezentacji z sitem i bez sita przy tych samych danych, okresach i klasyfikatorze. ZTF, Gaia, TESS, widma i obrazy są kierunkami przyszłych badań, nie wykonanymi walidacjami ani gwarancją przewagi.
