# Audyt podobieństwa implementacji: core, filters i applications — 23.11.2026

## Zakres i metoda

Przegląd wykonano na gałęzi `maintenance/repo-hygiene-audit-2026-11-23`, commit bazowy audytu: `9933fc968166a0e19fb79915fc3dca635a57122d`.

Zakres obejmuje pliki Python w katalogach `core/`, `filters/` i `applications/`. W drzewie znaleziono łącznie 139 plików Python: 103 w `core/`, 2 w `filters/` oraz 34 w `applications/`. Sprawdzono strukturę modułów, nazwy funkcji/klas oraz reprezentatywne pary wersjonowanych implementacji. Nie jest to pełny test semantycznej równoważności wszystkich 139 plików ani wykonanie testów.

## Ustalenia

### 1. Wersje mostów chronologicznych nie są zamiennymi kopiami

- `core/chrono_cone_bridge.py`, `chrono_cone_bridge_v2.py` i `chrono_cone_bridge_v3.py` realizują różne definicje metryk i kontroli. Zmieniają się m.in. odniesienie fazy, konstrukcja krzywej oraz kontrola ryzyka szumu.
- `core/real_chrono_cone_bridge.py` i `real_chrono_cone_bridge_v2.py` mają podobny szkielet testu na danych CWRU/sejsmicznych/BTC, ale v2 używa innej metryki i dodatkowej wielkości pomocniczej. Opis v2 deklaruje zachowanie danych i parametrów dla porównywalności.
- Decyzja: zachować oba warianty. Nie scalać ich przez prostą podmianę importu ani nie usuwać starszej prerejestrowanej ścieżki.

### 2. Mosty membranowe zachowują odrębne protokoły walidacyjne

- `real_chrono_membrane_bridge.py` opisuje test pierwotny i wtórny na kanałach z jednego źródła danych.
- `real_chrono_membrane_bridge_v0_2.py` wprowadza podział nagrań na część kalibracyjną i czasowo odosobnioną część testową.
- `real_chrono_membrane_bridge_independent.py` korzysta ze świeżego archiwum, innych RPM, typów i rozmiarów uszkodzeń; jego deklarowanym celem jest niezależna walidacja.
- Wspólne funkcje segmentacji i próbkowania są podobne, ale ich kontekst danych, protokół i znaczenie wyników są różne.
- Decyzja: zachować osobne pliki eksperymentalne. Ewentualne wydzielenie helperów wymagałoby osobnego testu regresji i potwierdzenia, że nie zmienia zamrożonej metodologii.

### 3. Warianty modalnej energii pasmowej są kolejnymi metodami, nie kopiami

- `real_modal_band_energy_bridge.py` liczy energię w zdefiniowanych pasmach i testuje dopasowane/niedopasowane pary.
- `real_modal_band_energy_bridge_v2.py` importuje wspólne ładowanie danych, segmentację i stałe z v1, ale zastępuje estymator energii pełną demodulacją obwiedni z wyborem pasma rezonansu.
- Decyzja: pozostawić v1 jako odtwarzalny punkt odniesienia; v2 słusznie reużywa część interfejsu i nie jest samodzielną kopią całego pipeline'u.

### 4. Katalog applications zawiera odrębne aplikacje dziedzinowe

W przejrzanym drzewie znajdują się co najmniej dwa wyraźnie wydzielone podprojekty:
- `applications/astronomy/TIMDR-lightcurve-fewshot/` — przygotowanie danych, cechy, predykcja, benchmark, UI, raportowanie i testy pipeline'u.
- `applications/astronomy/TIMDR-orbital-tracker/` — katalog obserwacji, orbita, rotacja, Bluetooth, CLI, serwer i testy trackera.

Podobieństwo nazw takich jak `run_demo.py` i `run_app.py` nie jest dowodem duplikacji. Zakresy funkcjonalne obu aplikacji są różne. Na tym etapie nie ma podstaw do przenoszenia ich kodu do wspólnego modułu.

### 5. Filtry mają odrębne odpowiedzialności

- `filters/prime_spectrum_filter.py` implementuje analizę widma odstępów między liczbami pierwszymi i klasyfikację wyrażenia.
- `filters/_vendor_senscore_gia_filter.py` zawiera dostosowany filtr zdarzeń geometrycznych (m.in. PCA i odporną oś).
- `filters/__init__.py` pozostaje pustym znacznikiem pakietu Python.
- Decyzja: brak podstaw do łączenia tych modułów.

## Co warto zrobić później

1. Dla rodzin `real_chrono_*` dodać testy kontraktowe, które potwierdzają zgodność segmentacji i próbkowania z prerejestracjami, bez zmiany protokołów.
2. Dla `real_modal_band_energy_bridge_v2.py` utrzymać jawny import wspólnych loaderów i stałych z v1; to obecnie ogranicza powielanie.
3. W przyszłym przeglądzie sprawdzić odwołania i testy aplikacji astronomicznych jako osobnych podprojektów, zamiast scalać je na podstawie podobnych nazw plików.
4. Pełne porównanie AST/tokenów i testy wykonawcze wszystkich 139 plików pozostają poza zakresem tego przeglądu.

## Decyzja porządkowa

W tym etapie nie usunięto ani nie przeniesiono kodu z `core/`, `filters/` ani `applications/`. Zidentyfikowane podobieństwa są związane z kolejnymi wersjami metod, wspólnymi protokołami lub odrębnymi aplikacjami. Usunięcie ich jako „duplikatów” byłoby ryzykowne i mogłoby usunąć historię eksperymentalną.

Nie uruchamiano testów ani CI w ramach tego przeglądu; raport nie stwierdza ich zaliczenia.
