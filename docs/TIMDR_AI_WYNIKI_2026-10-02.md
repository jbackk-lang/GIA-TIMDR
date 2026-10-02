# Dluzsze relacje i uczenie z potwierdzonej korekty

Wykonano dwa kolejne eksperymenty lokalnego AI: rozszerzenie relacji do 2–5 krokow oraz rzeczywiste aktualizacje wag po nowych, potwierdzonych faktach. Nie trenowano polskiego ani wag Qwena. To dwa wspolpracujace klocki prototypu i osobne dema, nie gotowy ogolny asystent.

## Relacje, brak informacji i konflikty

Trening na 1200 przypadkach z lancuchami 2–3 krokow. Ocena obejmuje lancuchy 4–5 krokow i inne osoby niz trening. Sa trzy rowno liczne klasy: kompletne fakty, brakujace ogniwo, sprzeczne ogniwo. Niesprzeczne duplikaty i konflikty poza droga pytania nie powinny blokowac odpowiedzi. Liczba dodatkowych faktow jest losowana.

Rdzen czyta kolejne wpisy pamieci przez zamrozona projekcje poprzedniego modelu. Uczony lokalny odczyt 1059 parametrow rozpoznaje stan ogniwa; jawna regula konstrukcji zachowuje pierwszy problem i zatrzymuje publikowanie kandydata. Skladanie drogi i ta regula sa zaprogramowane, nie odkryte samodzielnie przez siec.

| Ziarno | Nowe lancuchy 4–5 | Krotsze 2–3 | Stary zestaw 2 krokow |
|---|---:|---:|---:|
| 42 | 960/960 | 480/480 | 240/240 |
| 43 | 960/960 | 480/480 | 240/240 |
| 44 | 960/960 | 480/480 | 240/240 |

Dodatkowy test bez treningu, przez zamrozony angielski modul wejscia: 960/960; 320/320 kompletnych, 320/320 brakow i 320/320 konfliktow. W konfliktach demo pyta o potwierdzenie poprawnej wersji. Qwen1.5B wybiera wypowiedz z jawnej, ograniczonej gramatyki; nie dopisuje swobodnie faktow.

Trzy ziarna korzystaja z tych samych zestawow. Nie oznacza to 2880 niezaleznych pytan. Slownik jest zamkniety (40 osob), pytania maja jawna liczbe krokow, a wejscie jezykowe uzywa waskiej rodziny angielskich zdan. Standardowy algorytm chodzenia po grafie z kontrola konfliktu ma tu rowniez 100%. Nie wykazano przewagi nad nim ani ogolnego rozumienia angielskiego.

Wczesniejszy GRU przenosil niepewnosc zle na dluzsze lancuchy i nadmiernie odmawial odpowiedzi. Pierwszy lokalny odczyt dzialal dobrze na gestszej pamieci, ale mial cztery bledy regresji na starym zestawie. Dopiero zmienna gestosc pamieci w treningu usunela te bledy. Wszystkie próby zachowano lokalnie, nie nadpisano nieudanych wyników.

## Rzeczywista aktualizacja wiedzy

Odrębny neuronalny modul wiedzy uczyl sie 24 poczatkowych relacji. Potem otrzymal trzy zmiany od jawnego syntetycznego nauczyciela. Wariant niepotwierdzonej propozycji nie wykonal ani jednej aktualizacji; hash wag pozostal bez zmian. Potwierdzenie uruchamialo 150 aktualizacji na nowym fakcie. Wariant z przypominaniem poprzednich, zweryfikowanych faktow laczyl korekte z ich powtorkami.

Nowych pytan posrednich nie uzyto w optymalizacji: ich odpowiedzi wymagaja zlozenia 2–5 relacji i skorzystania z nowego faktu, a ich podmiot nie jest podmiotem potwierdzonej korekty. Sam mechanizm wielokrotnego odczytu jest zaprogramowany; zmiana odpowiedzi wynika z rzeczywiscie zmienionych wag pamieci.

| Ziarno | Wariant | Nowe pytania posrednie / 30 | Zachowane fakty / 21 | Stare pytania posrednie / 54 |
|---|---|---:|---:|---:|
| 42 | Bez korekty | 0 | 21 | 54 |
| 42 | Korekta bez przypominania | 30 | 21 | 54 |
| 42 | Korekta z przypominaniem | 30 | 21 | 54 |
| 43 | Bez korekty | 0 | 21 | 54 |
| 43 | Korekta bez przypominania | 30 | 21 | 54 |
| 43 | Korekta z przypominaniem | 30 | 21 | 54 |
| 44 | Bez korekty | 0 | 21 | 54 |
| 44 | Korekta bez przypominania | 20 | 20 | 50 |
| 44 | Korekta z przypominaniem | 30 | 21 | 54 |

W kazdym wariancie z przypominaniem wszystkie trzy zmienione fakty byly poprawne. Bez przypominania ziarno 44 zapomnialo jeden poprzedni fakt, co zepsulo wiele zlozonych odpowiedzi. Dlatego mechanizm uczenia sesji domyslnie przypomina poprzednia wiedze. Jest to maly test pamieci, nie gwarancja braku zapominania przy duzej liczbie korekt.

## Zastosowanie i trwałość wiedzy

W lokalnym demonstratorze potwierdzona zmiana relacji zmieniła odpowiedź na inne, pośrednie pytanie z Adam na Tomasz. Zachowano 23 pozostałe fakty. Bez potwierdzenia odpowiedź i wagi pozostały bez zmian.

Zapis i ponowne odczytanie sesji odtworzyły identyczne wyniki oraz zaktualizowaną wiedzę. Sesja zachowuje wiedzę potwierdzoną i oddzielnie propozycję oczekującą na potwierdzenie. Uczenie przygotowywane jest na kopii modelu, a następnie przyjmowane. Wymagane jest jawne zewnętrzne źródło potwierdzenia; podanie nazwy źródła samo nie dowodzi jego prawdziwości.

Demonstrator zaczyna od kontrolowanej wiedzy początkowej. Nie połączono tego mechanizmu ze swobodną rozmową ani automatyczną weryfikacją faktów. Jest to uczenie z zewnętrznej korekty, nie samodzielne ustalanie prawdy.

## Weryfikacja i granice

22 różne testy implementacji przeszly: 14 poprzednich, 6 nowych razem z nimi i kolejne 2 dotyczace zapisu sesji i wymagania zrodla potwierdzenia. Checkpointy ponownie wczytano z identycznymi logitami. Testy niepotwierdzonej propozycji i samego wnioskowania wykazuja brak zmiany wag.

To eksperyment rozwojowy na danych syntetycznych. Wyniki wspieraja skladanie lokalnych sprawdzen oraz uczenie potwierdzonej korekty z zachowaniem poprzednich referencji w tej malej domenie. Nie dowodza ogolnej inteligencji, przewagi TIMDR nad znanymi konstrukcjami, autonomicznego samouczenia ani bezpieczenstwa dowolnej rozmowy. TIMDR pozostaje inspiracja do budowy; nie przypisano wektorom jezyka fizycznych faz czy rezonansu.

## Pochodzenie zapisu

Data: 2 października 2026. Źródło: lokalny raport eksperymentów projektu Al. Badania łańcuchów: sesja 20261002T081319387819Z; uczenie korekt: sesja 20261002T080554593904Z; trwała sesja: 20261002T082643000631Z. Ten dokument archiwizuje opis, dane liczbowe i ograniczenia. Nie zawiera kodu, poleceń uruchomienia, wag modeli ani danych osobowych rzeczywistych osób; imiona należą do syntetycznej domeny testowej.
