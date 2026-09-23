# TIMDR — kalibracja, zamrożenie, test końcowy

Status: **zasada metodologiczna protokołu**, nie nowy aksjomat ani
zmiana wyniku wcześniejszych eksperymentów. Doprecyzowuje skrót
„zero tuningu po fakcie”: zakaz dotyczy dostrajania **do wyniku testu
końcowego**, nie uczciwej pracy na jawnie wydzielonej kalibracji.

## 1. Etap rozwoju i kalibracji — zmiany są dozwolone

Przed otwarciem zbioru testowego wolno sprawdzać schemat i jakość
danych, naprawiać błędy techniczne, ustalać progi z danych tła,
kalibrować model i porównywać z góry wskazane warianty. Wolno też
stwierdzić, że wybrana metoda nie ma mocy i przerwać eksperyment.

Warunki:

- używać wyłącznie zbiorów `train` i `calibration`, rozłącznych od
  `holdout` na właściwej jednostce niezależności (np. cały pomiar,
  osoba, sesja lub urządzenie, a nie sąsiednie okna);
- z góry określić, **co** wolno kalibrować i według jakiej reguły;
- zmianę nieprzewidzianą w planie oznaczyć nową wersją planu/kodu,
  z przyczyną, zakresem danych już obejrzanych i historią poprzedniej
  próby; nie zastępować po cichu starego planu;
- nie traktować wyniku na `train/calibration` jako niezależnego
  potwierdzenia hipotezy. Wielokrotne próby na calibration też mogą
  przeuczyć metodę, więc wymagają osobnego holdoutu.

Przykład: gdy pomiar treningowy ma 256575 zamiast 256000 próbek,
wolno zdiagnozować schemat i opisać nową, niezależną od etykiety regułę
wyrównania w kolejnej wersji planu — **zanim** otworzy się holdout.

## 2. Punkt zamrożenia

Przed testem końcowym zapisuje się identyfikatory źródeł i ich hashe,
podział danych, definicje cech/operatorów, wykluczenia, progi,
kontrole dodatnie i ujemne, test statystyczny, wielkość efektu,
korektę wielokrotnych porównań, warunki mocy oraz kryteria werdyktu.
Kod i plan powinny dostać osobny, identyfikowalny commit lub inny
niezmienny znacznik czasu. Brak takiego śladu należy jawnie zgłosić;
sam hash pliku liczony lokalnie nie dowodzi kolejności zdarzeń.

## 3. Jednorazowy test końcowy — zmian pod wynik już nie ma

Po otwarciu holdoutu wykonuje się zamrożony test i raportuje pełny
wynik, także negatywny albo `INCONCLUSIVE`. Nie zmienia się progów,
okien, cech, wykluczeń ani kierunku hipotezy w celu poprawy wyniku.
Diagnostyka błędu technicznego jest dopuszczalna, lecz poprawiony
przebieg na **tym samym, już obejrzanym holdoucie** ma status
eksploracyjny. Nowe twierdzenie potwierdzające wymaga nowego,
niezależnego holdoutu lub nowej domeny oraz nowej wersji planu.

Ta reguła nie osłabia kontroli: ich niepowodzenie nadal zatrzymuje
interpretację testu. Oddziela jedynie moment, w którym rozwój metody
jest legalny, od momentu, w którym zaczyna się ocena potwierdzająca.
