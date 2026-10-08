# Lokalne SI według zasad TIMDR — stan 8 października 2026

Prywatne SI autora jest małym, lokalnym systemem. Ma 14 własnych sieci (razem 2,81 mln parametrów, 11,20 MB wag) oraz dokładne narzędzia: kalkulator, kalendarz, słownik SJP.PL (4,69 mln form) i dostęp do źródeł. Zasady TIMDR są w nim zasadami działania. Ten dokument opisuje wyniki, nie publikuje kodu, wag ani pamięci SI.

## Odniesienie
Liczby, daty i fakty podaje dokładne narzędzie albo niezależne źródło, a nie pamięć sieci. Tabele i arkusze (CSV, XLSX) liczy dokładnie i sprawdza drugim obliczeniem. Daty liczy kalendarzem i sprawdza numerem dnia juliańskiego oraz kongruencją Zellera. Wielkanoc liczy dwiema niezależnymi metodami (zgodne dla lat 1583–4099). Zamrożone testy: tabele 15/15, dokumenty 15/16, daty 9/11; pozostałe poprawnie niepotwierdzone.

## Koincydencja kanałów
Odpowiedź ma jeden z trzech stanów: potwierdzone, odrzucone albo do potwierdzenia. Fakt o świecie jest potwierdzony tylko wtedy, gdy zgadzają się co najmniej dwa niezależne źródła i żadne nie przeczy. Źródła to polska i angielska Wikipedia (czytana tym, czego SI sama się nauczyła), Wikidane i Biblioteka Narodowa. Każde źródło jest pokazane z ✓ albo ✗, cytatem i adresem. Zamrożony test faktów: 66 ze 126 pytań potwierdzonych, po polsku i po angielsku. Zamrożone testy SI: 0 fałszywych potwierdzeń.

## Mosty
SI sama wybiera, czego się uczy, i uczy się czytać Wikipedię: mosty słów („birth” = „born”) oraz wzorce zapisu dat i liczb („( [DATA] –”, „ur. [DATA]”, „premiered on [DATA]”, „the population was [LICZBA]”). Sędzią jest Wikidata. Na zamrożonych hasłach SI czyta poprawnie po angielsku 83 z 215 pytań (start od 0), a po polsku 87 z 287 (start od 0). Błędów czytania: 0.

## Sito i zamrożony test
Nowa wersja wchodzi tylko wtedy, gdy poprawia wynik na zamrożonych danych, niczego nie pogarsza i nie dodaje błędnych potwierdzeń. Każda podmiana ma kopię zapasową i zapis wyniku przed zmianą i po niej.

## Samokorekta
Gdy źródła podają różne wartości, SI szuka wyjaśnienia w artykułach:
- kalendarz juliański i gregoriański (np. „31 lipca [O.S.]”);
- znana data chrztu, nie urodzenia;
- dwie możliwe daty („22 lub 23 kwietnia”);
- data niepewna („prawdopodobnie 1832, inne źródła podają 1834 lub 1835”).

Gdy większość źródeł się zgadza, a inna jest tylko wartość odczytana przez SI z artykułu, SI uznaje to za własny błąd czytania (albo za różnicę w samym artykule) i odsyła ten artykuł do nauki czytania.

## Ciekawość i nagroda za postęp
SI prowadzi mapę wiedzy: co sprawdziła, skąd to wie i czego jeszcze nie wie. Sama zadaje sobie pytania:
- z dziur na mapie („znam urodzenie, nie znam śmierci”);
- z powiązań haseł (rodzina, nauczyciele, uczniowie, miejsca, uczelnie, dzieła);
- ze sporów źródeł.

Wybiera rodzaje pytań, w których najszybciej robi postęp, a odkłada te, w których kolejne próby nic nie dają. Uczy się także wtedy, gdy komputer jest bezczynny. Pierwszy dzień: 973 własne pytania, 543 odpowiedzi potwierdzone co najmniej dwoma źródłami, mapa wiedzy z 997 faktami o 879 hasłach. Mapa jest zapisana w bazie SQLite, ok. 340 B na fakt razem z hasłem.

## Przepełnienie i wzrost
Automat rośnięcia powiększa sieć albo okno wzorców przy zastoju; podmiana następuje tylko po poprawie. Zadania słowne: 944 z 1730 prawdziwych zadań (SVAMP/ASDiv), zawsze z prośbą o potwierdzenie.

## Rozmowa
SI rozumie polskie i angielskie polecenia. Poprawia literówki i brakujące polskie znaki, pokazując, co zrozumiała. Mówi, co potrafi, i podaje przykłady użycia swoich modułów. Na polecenie „sprawdź się” uruchamia własne testy. Odpowiada też, czego się dowiedziała i co ciekawi ją teraz.

Publiczne repozytorium z opisem wyników: [AI-SI](https://github.com/jbackk-lang/AI-SI).
