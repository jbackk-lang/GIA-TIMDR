# Audyt spójności dokumentacji poza archiwum — 23.11.2026

## Zakres i metoda

Audyt wykonano na drzewie gałęzi `main` z 23 listopada 2026 r. Drzewo zawiera 1 121 plików binarnych i tekstowych oraz 523 pliki z rozszerzeniami Markdown/RST/TXT. Liczby opisują inwentaryzację drzewa, nie liczbę dokumentów przeczytanych w całości.

W pierwszym przebiegu sprawdzono 16 dokumentów wejściowych: główne README, mapę repozytorium, stan projektu, indeks dokumentacji, architekturę, roadmapę i handoffy badawcze, README czterech formalizmów oraz indeksy astronomii, skryptów i eksperymentów. Sprawdzono 228 odnośników Markdown w tych dokumentach względem ścieżek i katalogów w aktualnym drzewie Git.

Nie wykonano jeszcze pełnego audytu treści wszystkich 523 dokumentów, zewnętrznych adresów HTTP(S), kotwic wewnątrz dokumentów, ani zgodności wszystkich instrukcji z uruchomieniem kodu i testów. Nie oceniano prawdziwości twierdzeń naukowych.

## Wyniki potwierdzone

1. W 14 z 16 dokumentów wejściowych wszystkie sprawdzane odnośniki względne prowadziły do istniejących plików lub katalogów.
2. W `TIMDR-Geometry-Formalism/README.md` znaleziono dwa błędne odwołania:
   - ścieżka do aksjomatów prowadziła do nieistniejącego podkatalogu `GIA-TIMDR/docs/...`, mimo że dokument znajduje się w `../docs/theory/`;
   - odnośnik licencji wskazywał `LICENSE`, podczas gdy w tym module plik ma nazwę `LICENSE.txt`.
3. README formalizmów zawierały również nieaktualne prefiksy ścieżek `GIA-TIMDR/docs/...` i `GIA-TIMDR/SKILL...`, odziedziczone po wcześniejszym układzie katalogów. Zastąpiono je ścieżkami względnymi właściwymi dla obecnego położenia modułów.
4. Mapa repozytorium ma datę 22.11.2026, a główny `README.md` zawiera aktualizacje badawcze z 15.11.2026. Ich kluczowe odnośniki do plików istnieją w drzewie.

## Dodatkowa kontrola generatora statusu

Skrypt `scripts/stan_projektu.py` szuka w głównym README wierszy tabeli zawierających link w formacie `[wynik](...)`. W aktualnym README nie ma ani jednego takiego wiersza. Bez zabezpieczenia uruchomienie generatora zastąpiłoby istniejącą tabelę 31 wyników pustą tabelą i oznaczyło ją bieżącą datą. Dodano więc kontrolę: przy braku wierszy źródłowych skrypt kończy działanie z komunikatem i nie zapisuje zmian.

## Rozbieżność wymagająca osobnej decyzji

`STAN_PROJEKTU.md` zawiera ręczną migawkę z 30.09.2026 i automatyczny bilans z 28.09.2026. Główny README opisuje późniejsze wyniki listopadowe, a mapa repozytorium była aktualizowana 22.11.2026. Nie zmieniono daty ani treści tego dokumentu automatycznie: samo przesunięcie daty bez ponownego uzgodnienia wyników, ograniczeń i tabel byłoby nierzetelne. Wymaga to pełnego porównania ręcznej części `STAN_PROJEKTU.md` z aktualnym README, roadmapą i najnowszymi checkpointami.

## Ograniczenia i następne kontrole

- Audyt linków dotyczył 16 dokumentów wejściowych, a nie całego korpusu 523 plików.
- Nie sprawdzono jeszcze wszystkich odwołań zapisanych jako zwykły tekst lub ścieżki w blokach kodu.
- Nie sprawdzono zewnętrznych URL-i, kotwic, wersji zależności ani tego, czy komendy z instrukcji działają w czystym środowisku.
- Nie zmieniano wyników eksperymentów, prerejestracji ani danych. Zmieniono jedynie skrypt pomocniczy, aby brak danych wejściowych nie powodował utraty istniejącej tabeli.
- Żaden plik nie został usunięty.

Następny bezpieczny etap: porównanie statusu projektu i roadmapy z najnowszymi checkpointami, a następnie osobny audyt README każdego obszaru i instrukcji uruchomienia. Każda zmiana treści merytorycznej powinna zachować historyczne wyniki i ich werdykty.
