# SI: nauka negacji, zachowanie umiejętności i niezależna kontrola

Data: 2 października 2026. Lokalny prototyp SI inspirowany konstrukcyjną ideą TIMDR. Publikujemy opis i wyniki, bez kodu SI, wag, checkpointów, pamięci użytkownika i danych jego plików.

## Podział ról

Sieć jest uczonym składnikiem systemu. Graf i dokładny kalkulator są jego narzędziami wykonania oraz kontroli. Graf rozwiązuje konkretną klasę problemów; jego wynik nie rozstrzyga potencjalnej wartości sieci w innych zadaniach. Należy oddzielać wartość całego układu, wkład uczonego składnika i wkład narzędzia. W tym eksperymencie nie sprawdzono jeszcze samodzielnego doboru narzędzia ani swobodnej interpretacji zadania.

## Negacja: poprawa z jawną regresją

1440 osobnych przykładów treningowych i 720 nowych przypadków oceny. Grupy nazw rozłączne: identyfikatory 0–23 w treningu i 24–39 w ocenie. Zamknięta domena obejmuje 40 syntetycznych podmiotów i 2–5 kroków relacji. Badano pełną ścieżkę, brak, rozgałęzienie, zaprzeczenie pozytywnej relacji, samą negację bez relacji pozytywnej oraz negację nieistotną dla pytania; także duplikaty i wpisy poza ścieżką.

Poprzedni wyuczony moduł: **600/720**. Pierwszy kandydat z informacją o negacji: **719/720** dla każdego z ziaren 42, 43 i 44. Poprawiono 120 przypadków, ale zepsuto jeden wcześniej poprawny: odpowiedź mimo brakującej relacji. Wszystkie 120 przypadków sprzecznej negacji rozpoznano poprawnie. Pierwszy kandydat nie spełnił zapisanej wcześniej bramki braku błędnych zaakceptowanych odpowiedzi i nie zastąpił samodzielnie poprzedniego modułu.

## Rozszerzenie zamiast utraty starej umiejętności

Po wykryciu regresji zachowano poprzedni wyuczony moduł wykrywania braków i rozgałęzień, a dołączono uczony składnik negacji. Nowy plan i dane zamrożono przed oceną zmienionej architektury.

| Ziarno | Kolejne nowe przypadki | Wcześniejszy test regresji | Błędne zaakceptowane | Niepotrzebne odmowy |
|---|---:|---:|---:|---:|
| 42 | 1440/1440 | 720/720 | 0 | 0 |
| 43 | 1440/1440 | 720/720 | 0 | 0 |
| 44 | 1440/1440 | 720/720 | 0 | 0 |

Trzy przebiegi używają tych samych przypadków; nie oznacza to 4320 niezależnych nowych zadań. Architektura została zmieniona po pierwszym wyniku — drugi test jest nową próbą rozwojową, nie niezależnym zewnętrznym benchmarkiem. Rozszerzenie przeszło własną wcześniej zapisaną bramkę i zostało podłączone lokalnie. Kontrola zgodności z grafem pozostaje włączona. Testy integracyjne potwierdziły działanie negacji oraz zachowanie uczenia, zapisu i odtwarzania pamięci.

## Dokładne obliczenia i osobny walidator

Kalkulator oblicza dokładnie na ułamkach wymiernych. Walidator ma odrębny parser i sprawdza wynik. Nie uczono Bielika arytmetyki w tym eksperymencie. Rachunki obejmują ograniczony zakres działań, nie interpretację zdań, jednostek, faktów ani dowodów. Wynik narzędzia jest oznaczany jako wynik narzędzia, nie odpowiedź uczonej sieci.

## Trzy warianty na tych samych nowych zadaniach

| Zadanie | Bielik | Ta sama odpowiedź Bielika + walidator | SI + walidator |
|---|---:|---:|---:|
| Jawne relacje | 0/24 | 0/24 | 24/24 |
| Dokładne rachunki | 3/24 | 3/24 | 24/24 |

W relacjach 23 odpowiedzi Bielika nie spełniły wymaganego formatu, jedna była błędna. Walidator odrzucił wszystkie 24. W rachunkach odrzucił 21 błędnych odpowiedzi i zachował trzy poprawne. Walidator nie naprawiał odpowiedzi.

Porównanie relacji dotyczy pierwszego kandydata, ocenionego przed zmianą architektury; nie podmieniono go w wynikach na późniejsze rozszerzenie. SI otrzymywało strukturalny zapis tych samych relacji, Bielik zapis tekstowy. Odpowiedzi oceniano w ustalonym formacie, z limitem 64 tokenów dla relacji i 24 dla rachunków. Nie wybierano dogodnych fragmentów po obejrzeniu wyników. W rachunkach wariant SI używa dokładnego narzędzia — **24/24 nie jest wynikiem neuronowej arytmetyki**.

Sam graf uzyskał 720/720; sam kalkulator również rozwiązuje badane rachunki. Wyniki pokazują praktyczną korzyść z narzędzi i kontroli oraz naukę negacji bez utraty wcześniejszych umiejętności po zmianie konstrukcji. Nie izolują jeszcze przewagi TIMDR nad innymi architekturami SI. Taką przewagę trzeba badać w uczeniu, interpretacji, doborze narzędzi i przenoszeniu umiejętności.

## Kontrola, rozmiar i pochodzenie

Stare testy zachowano jako zamrożoną regresję. Nie zmieniono reguł oceniania po obejrzeniu odpowiedzi tego porównania. Przeszło 30 testów; po ostatniej zmianie ponownie dziewięć testów integracji i uczenia w rozmowie. Sprawdzono działający interfejs oraz zgodność dwóch parserów na 200 losowych działaniach. Kontrola skrótów potwierdziła niezmienność zamrożonych checkpointów i zbiorów.

Nowy checkpoint negacji: **7557 bajtów (około 7,6 KB)**. Baza Bielika Q8_0: **1 699 568 288 bajtów (1,70 GB)**. Cały lokalny folder ze środowiskiem wykonawczym, modelami i eksperymentami: około **1,84 GB**; nie jest to rozmiar samego rdzenia.

Źródła lokalne: porównanie `20261002T124738707004Z`, rozszerzenie `20261002T130758804489Z`. [Zestawienie liczb i skróty raportów źródłowych](SI_NEGACJA_WALIDACJA_2026-10-02.json). Bez publikacji kodu nie zapewniamy niezależnego odtworzenia prywatnego SI; jest to archiwum wyników autora, nie zewnętrzna replikacja.
