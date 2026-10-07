# Zasady TIMDR w uczeniu lokalnego SI — 6–7 października 2026

Opis wyników rozwojowych prywatnego SI (AI-SI) w zadaniach słownych i polskim interfejsie. Nie zawiera kodu, wag, checkpointów ani pamięci. Wszystkie liczby dotyczą opisanych, ograniczonych testów, a nie ogólnego rozumienia języka. Szczegóły: [AI-SI, uczenie 6–7 października](https://github.com/jbackk-lang/AI-SI/blob/main/docs/SI_NAUKA_2026-10-06.md).

## Które zasady TIMDR zostały użyte i co dały

| Zasada TIMDR | Zastosowanie w SI | Wynik |
|---|---|---|
| **Zasada odniesienia** (znieś wspólne, czytaj resztę) | Liczby zastąpione znacznikami N1..Nk: parser czyta strukturę zadania, dokładne narzędzie wstawia liczby | Znane wzory zadań 249 → 296/300; 39 z 51 wcześniejszych błędów brało się z przepisywania cyfr |
| **Koincydencja kanałów** (rezonans M: kilka niezależnych sygnałów naraz) | Potwierdzenie odpowiedzi tylko przy zgodności: dwa parsery, ugruntowanie liczb, dokładny kalkulator, kanał znaczenia operacji, kanał nowości (odniesienie do znanego obszaru zdań) | 0 błędnych potwierdzeń na wszystkich zamrożonych testach i na 1730 prawdziwych zadaniach |
| **Mosty między gałęziami** | Most WordNet: nieznany czasownik → znany czasownik tej samej operacji, tylko gdy wszystkie znaczenia są zgodne. Most pytań: nieznane sformułowanie → znane pytanie tej samej klasy | Nowe czasowniki 208 → 286/300 (test zamrożony przed pracą); nowe pytania 247 → 272/300 |
| **Samokorekta wokół kotwicy** | Pętla nauki z niezależnym odniesieniem: Qwen proponuje przykłady, etykieta pochodzi z konstrukcji schematu lub z osobnego rozwiązania, sito przesiewa; wag Qwena nie trenujemy | Bez niezależnego odniesienia pętla utrwalała własne błędy (wynik negatywny) |
| **Protokół** (zamrożenie, jedno uruchomienie, wyniki negatywne) | Testy zamrażane przed pracą; test użyty do wyboru wersji oznaczany jako rozwojowy; połowa zestawu prawdziwych zadań nieużywana do strojenia | Opisane niżej wyniki negatywne |

## Najważniejszy wynik negatywny: sprawdzian na prawdziwych danych

Na 1730 jednodziałaniowych zadaniach z otwartych zbiorów SVAMP i ASDiv, pisanych przez ludzi, parser trafiał tylko **10%**. Na zadaniach z dwiema liczbami wynik był prawie taki sam jak przy losowym zgadywaniu. Mosty poprawiały wyniki tylko w świecie szablonów, w którym powstały. Bezpiecznik zadziałał: 7 potwierdzeń, wszystkie poprawne.

Wniosek dla ramy: **reguła wykonalności i odniesienie trzeba sprawdzić na danych spoza własnego generatora**, zanim doda się kolejne mosty. To ten sam błąd, co ocena metody tylko na syntetyce.

## Zmiana podejścia: role liczb

- **Nowy model:** ranking kandydatów (liczba A, liczba B, działanie) z prostymi wskazówkami ról. Liczba w zdaniu z „now/left/total” to wynik albo całość, „more than” oznacza porównanie, „each” grupy; do tego typ pytania (stan początkowy, różnica, suma, pozostało). Model sam uczy się, które połączenie ról daje które działanie.
- **Wynik czysty pierwszej wersji:** 49% na zamrożonym zestawie (wcześniej 10%).
- **Ze wskazówkami ról:** połowa nieużywana do strojenia 451 → 497/865, a w SI 925/1730.
- **Bez potwierdzania:** odpowiedzi tego modelu zawsze wymagają potwierdzenia. Kalibracja nie dała bezpiecznej reguły, bo kanały z tej samej rodziny modeli mają wspólną ślepą plamkę (ok. 10% błędów nawet przy najostrzejszej regule).

## Automat rośnięcia pojemności i koordynator nauki

- **Automat (zasada przepełnienia i przeuczenia):**
  - strata treningowa stoi → zwiększ liczbę neuronów;
  - strata spada, a wynik rozwojowy nie rośnie → stop i powrót do najlepszej epoki;
  - najlepszy rozmiar potwierdzany na 3 losowaniach startowych.
- **Wynik:** przy cechach typu „worek słów” więcej neuronów nie pomogło. 256 neuronów dało średnio tyle samo co model liniowy, a odpowiedź trwała 3,4 ms wobec 1,7 ms. Wąskim gardłem była reprezentacja, a nie pojemność.
- **Koordynator nauki:** jedna pętla dla modułów jako wtyczek. Każdy moduł przechodzi drogę źródło → sito → automat → podmiana wag tylko po poprawie na teście rozwojowym bez pogorszenia straży, z kopią zapasową. Podpięte są zadania słowne i polski maper pytań. W pierwszej próbie mapera kandydat nie przeszedł progu i czynne wagi zostały.

## Wieczór: mosty między modułami i tłumacz pod kontrolą

- **Most model ról ↔ czytnik kontekstu:** model, który czyta zadanie słowo po słowie, jest słaby sam (445 na połowie zestawu nieużywanej do strojenia). Połączony z modelem ról podnosi wynik 497 → 512; w SI prawdziwe zadania 925 → 944/1730. Gałąź użyta sama daje minus, a most daje plus, tak jak w obserwacji „klocków i trybików” TIMDR.
- **Polski maper:** katalog sprawdzonych zdań z etykietami ustalonymi przez autora (nauczyciel nie wymyśla etykiet) i czytnik kontekstu po formach SJP.PL. Zamrożony test 44 → 64/72.
- **Tłumacz neuronowy jako odniesienie zewnętrzne:** Opus-MT PL→EN (218 MB) proponuje tłumaczenie, a SI sprawdza, czy liczby i przeczenia przeszły bez zmian. Polskie zadania słowne 24 → 51/150. Tłumacz EN→PL halucynował, więc odpowiedzi po polsku zostają z ustalonych zdań.

## Ograniczenia

To eksperymenty rozwojowe w wąskiej domenie: proste zadania jednodziałaniowe po angielsku, z polskim tylko przez translator. Część liczb jest rozwojowa, bo wersje wybierano na tych samych testach; czyste pomiary są oznaczone. Nie jest to ogólny ranking SI ani dowód skuteczności całej ramy TIMDR.
