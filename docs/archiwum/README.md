# Archiwum GIA-TIMDR

To katalog **historycznych, datowanych dokumentów oraz raportów porządkowych**. Zachowuje dawne opisy, wyniki, oceny i ślady kolejnych etapów organizacji repozytorium. Dokument archiwalny opisuje stan z podanej daty — nie jest automatycznie bieżącym werdyktem projektu.

## Jak czytać archiwum

- **Źródło historyczne** — dawny opis lub podsumowanie; zachowuje ówczesny język i ocenę.
- **Migawka wyników** — zestawienie eksperymentów przeniesione z README w określonym dniu; liczby i werdykty należy czytać razem z datą oraz linkowanym raportem.
- **Raport audytowy / inwentaryzacja** — zapis kontroli wykonanej w konkretnym zakresie i czasie; późniejszy raport może rozszerzać wcześniejszy, ale nie unieważnia jego historycznego wyniku.

Nie poprawiamy po cichu starych wyników ani nie usuwamy materiałów tylko dlatego, że są długie, podobne lub nieaktualne. Korekty bieżącej nawigacji wprowadzamy w indeksie, a korekty merytoryczne opisujemy osobno.

## Pełny indeks plików

Stan indeksu: **23 listopada 2026 r.** W katalogu znajduje się 7 plików: ten indeks oraz 6 dokumentów archiwalnych i kontrolnych.

### A. Historia projektu i dawne opisy

| Data / okres | Dokument | Co zawiera i jak go traktować |
|---|---|---|
| przed 2026-09-23 | [Historia dawnego README](HISTORIA_README.md) | Obszerny, dawny opis GIA-TIMDR/TRM sprzed porządkowania z 23.09.2026. Zachowuje pierwotną narrację i dopiski o różnym statusie; nie traktować jako specyfikacji ani aktualnego opisu osiągnięć. |
| 2026-09-23 | [Podsumowanie projektu TIMDR](PODSUMOWANIE_PROJEKTU_2026-09-23.md) | Datowany przegląd czterech gałęzi, eksperymentów, zastosowań oraz wyników pozytywnych i negatywnych. To historyczna migawka całego ekosystemu. |

### B. Zachowane zestawienia badań

| Data | Dokument | Co zawiera i jak go traktować |
|---|---|---|
| 2026-11-14 (zawiera także starsze wyniki) | [Szczegółowe zestawienie eksperymentów — migawka README](WYNIKI_EKSPERYMENTOW_MIGAWKA_README_2026-11-14.md) | Tabela porównań i interpretacji przeniesiona z głównego README. Zachowuje werdykty i liczby z chwili migracji; do oceny konkretnego wyniku przejść do źródłowego pliku RESULT. |

### C. Audyty i inwentaryzacje archiwum

| Data | Dokument | Zakres i ograniczenia |
|---|---|---|
| 2026-11-14 | [Audyt archiwum — etap 3](AUDYT_2026-11-14.md) | Wczesna, ograniczona kontrola 18 odnośników w jednym podsumowaniu. Dokumentuje ówczesny zakres; nie jest pełnym audytem katalogu. |
| 2026-11-23 | [Inwentaryzacja archiwum](INWENTARYZACJA_2026-11-23.md) | Migawka CSV pięciu plików wejściowych i ich SHA-256. Nie obejmowała dwóch później dodanych raportów kontrolnych, więc liczba pięciu nie jest bieżącą liczbą plików w katalogu. |
| 2026-11-23 | [Audyt odnośników i identycznych plików](AUDYT_LINKOW_I_DUPLIKATOW_2026-11-23.md) | Sprawdzenie względnych odnośników w sześciu dokumentach istniejących przed utworzeniem tego raportu oraz identycznych blobów w repozytorium. To audyt linków i duplikatów bajtowych, nie audyt podobieństwa treści ani kompletności badań. |

## Co jest aktualne poza archiwum

- [Główny README](../../README.md) — bieżący punkt wejścia i najnowsze podsumowanie projektu.
- [Mapa repozytorium](../../REPOZYTORIUM.md) — nawigacja po kodzie, dokumentacji, prerejestracjach i wynikach.
- [Roadmapa Chronoprocesu](../../research/ROADMAP_GIA_TIMDR_2026-11-17.md) oraz [indeks checkpointów Chronoprocesu](../../research/chronoproces/README.md) — datowane postępy tej linii badań.
- [Migawka stanu projektu z 30.09.2026](../../STAN_PROJEKTU.md) — dokument historyczny, nie bieżący status całego repozytorium.
- [Wyniki i prerejestracje geometrii](../geometry/) — dokumentacja źródłowa eksperymentów domenowych.

## Zasady utrzymania

1. Zachowuj oryginalne dokumenty, daty, wyniki, werdykty i historię Git.
2. Nowy dokument archiwalny dodawaj do indeksu z datą, kategorią, krótkim opisem i statusem.
3. Przed przeniesieniem pliku sprawdzaj linki przychodzące i wychodzące; po przeniesieniu testuj je ponownie.
4. Nie scalaj automatycznie dokumentów podobnych tematycznie — mogą opisywać różne daty, zbiory danych lub etapy.
5. Rozróżniaj wynik historyczny, późniejszą korektę i aktualny stan projektu.
6. Raport inwentaryzacji zawsze opisuje stan na dzień pomiaru; po dodaniu lub przeniesieniu plików nie przedstawiaj jego liczebności jako aktualnej bez ponownego skanu.

## Dlaczego pliki pozostają w jednym katalogu

Na tym etapie nie przenoszę dokumentów do podkatalogów. Wiele odnośników względnych prowadzi bezpośrednio do istniejących nazw plików, a rozdzielenie katalogu na historię, wyniki i audyty wymagałoby szerokiej aktualizacji linków w całym repozytorium. Czytelny podział tematyczny jest obecnie zapewniony przez ten indeks. Fizyczne przenosiny można wykonać później, jeśli pełny audyt linków przychodzących wykaże, że są bezpieczne.
