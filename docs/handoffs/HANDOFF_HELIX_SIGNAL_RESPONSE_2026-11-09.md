# HANDOFF — HELIX/TIMDR: sygnał → helisa → odpowiedź

**Data:** 2026-11-09  
**Repozytorium nadrzędne:** GIA-TIMDR  
**Status:** punkt wznowienia pracy po resecie. Ten dokument ma zachować kierunek i zapobiec ponownemu rozproszeniu badań.

## 1. Cel nadrzędny — nie zmieniać

Badamy **wpływ informacji/sygnału na helisę TIMDR i odpowiedź helisy**.

Pytanie główne:
**Co sygnał robi z helisą, jak helisa na niego odpowiada i czy odpowiedź zależy od wcześniejszej historii sygnałów?**

Schemat:
`sygnał wejściowy → mechanizm oddziaływania w helisie → odpowiedź → wpływ odpowiedzi na kolejny sygnał`.

Nie wracać do katalogowania samych właściwości helisy jako głównego celu. Użytkownik wskazuje, że pamięć, samonaprawa i inne właściwości helisy były już przedmiotem wcześniejszych badań. Traktować je jako istniejący kontekst badawczy, ale przy używaniu ich jako przesłanek w konkretnym modelu odszukać odpowiednie źródła i nie dopisywać niezweryfikowanych szczegółów.

## 2. Najważniejsza korekta metodologiczna

Analiza mechanizmu miała pomóc zrozumieć sprzężenie sygnału z helisą. Nie wolno mnożyć niewiadomych ani rozwijać pobocznych eksperymentów bez wskazania, jak rozwiązują główne pytanie.

**Następny krok to nie nowa teoria i nie kolejny sweep parametrów. Najpierw prześledzić istniejący kod GIA-TIMDR i odtworzyć drogę sygnału od wejścia do odpowiedzi helisy.**

Dla każdego istniejącego elementu ustalić:
1. co jest wejściem i w jakiej reprezentacji;
2. gdzie i jak sygnał oddziałuje ze strukturą;
3. jaki stan helisy może się zmienić;
4. jakie wyjście/odpowiedź jest obliczane lub mierzone;
5. czy wynik zależy od historii;
6. co jest zaimplementowane, co jest hipotezą, a czego w kodzie brak.

Najpierw audyt istniejących modułów i przepływu danych. Dopiero potem wskazać **jedną** najważniejszą lukę i zaprojektować minimalny test.

## 3. Istniejące punkty zaczepienia — nie utożsamiać ich

- **G / G-Rezonans:** `core/geometric_resonance_operator.py`, model mechanicznej odpowiedzi układu w rodzaju `M x'' + Γ x' + Kx = F(t)`. To pobudzenie i odpowiedź mechaniczna; nie jest samo w sobie pełnym modelem informacji. W dotychczasowym audycie odnotowano użycie `|τ|`, które może usuwać znak chiralności ze sprzężenia.
- **K:** modalności `(f, φ, A)` i synchronizacja. Nie zakładać, że samo K zmienia geometrię helisy.
- **M/S:** analiza/klasyfikacja sygnału czasowego. Jej „rezonans” nie jest automatycznie tym samym co rezonans mechaniczny G ani fazowy K.
- **T:** szkic pola informacyjnego/modalnego/rezonansowego; nie uznawać za zwalidowane prawo sprzężenia bez jawnego równania i testu.
- **Helix-Lock:** eksperyment chiralności wskazywał, że znak orientacji/torsji może być tracony przez użycie wartości bezwzględnej. Zachować znak i fazę w analizie.

Nie scalać G/K/M/T w jeden operator bez matematycznego mostu.

## 4. Minimalny model pojęciowy

`u(t)` — wejściowy sygnał/informacja.  
`z(t)` — stan helisy przed i po pobudzeniu.  
`y(t)` — obserwowalna odpowiedź.

`z(t+1) = F(z(t), u(t))`  
`y(t) = G(z(t), u(t))`

To na razie schemat identyfikacji, nie gotowe prawo fizyczne. Nie wymyślać postaci F i G bez podstawy w istniejącym kodzie lub danych.

Rozróżniać:
- reakcję: wyjście zmienia się po pobudzeniu;
- pamięć: identyczny sygnał testowy daje różną odpowiedź zależnie od historii/stanu;
- adaptację: zmieniają się parametry odpowiedzi po serii pobudzeń;
- samonaprawę: układ wraca do niezależnie określonego stanu odniesienia po zakłóceniu;
- odzyskanie informacji: odtwarzany jest payload/stan informacyjny, nie tylko energia lub częstotliwość.

## 5. Minimalny test rozstrzygający — dopiero po audycie ścieżki

Porównać odpowiedź na **identyczny sygnał testowy** dla:
- stanu odniesienia/świeżego;
- stanu po wcześniejszym, kontrolowanym pobudzeniu.

Utrzymać identyczne warunki i mierzyć z góry wybrany kanał odpowiedzi. Dodać kontrolę bez sprzężenia. Jeśli odpowiedź zależy od historii, wykazać efekt wejście–wyjście zależny od stanu. Jeśli nie — nie zakładać pamięci w tym kanale.

Nie rozszerzać od razu na wszystkie amplitudy, częstotliwości, topologie i geometrie. Najpierw jeden poprawnie zdefiniowany tor sygnału.

## 6. Co zostaje na drugim planie

- HC-01: matematyczna helisa kołowa i jej analityczne parametry — punkt odniesienia, nie główny cel.
- HC-01-TUBE: geometria tunelu — cecha struktury, którą można wykorzystać jako zmienną objaśniającą odpowiedź.
- Redukcja 4→3, próg 90°, √2/√3, punkty kardynalne i interpretacje TRM — hipotezy wtórne. Nie prowadzić teraz osobnego programu ich rozstrzygania.
- Nie mnożyć rodzin helis i sweepów, dopóki audyt ścieżki sygnału nie pokaże, że są konieczne.

## 7. Zasada prowadzenia pracy po wznowieniu

Każdy krok ma odpowiedzieć: **jak to przybliża nas do zrozumienia wpływu sygnału na helisę i jej odpowiedzi?**

Raportować krótko:
- co znaleziono w istniejącym kodzie;
- co jest rzeczywiście wykonywane;
- czego nie ma;
- jedna luka o największym znaczeniu;
- następny minimalny test.

Nie twierdzić, że uruchomiono eksperyment, jeśli jedynie zapisano protokół lub kod. Oddzielać zapis w repo, testy CI, wykonanie eksperymentu i interpretację wyniku.

## 8. Dokumenty źródłowe w GIA-TIMDR

- `docs/geometry/HELIX_SIGNAL_RESPONSE_COUPLING_v0.1.md` — synteza sprzężenia sygnał–helisa–odpowiedź.
- `docs/theory/HELIX_TIMDR_RESEARCH_PROGRAM.md` — nadrzędny program badań, szczególnie sekcje 36–37.
- `docs/geometry/HELIX_CHARACTERIZATION_PROTOCOL_HC01_v0.1.md` — charakterystyka geometryczna HC-01, materiał pomocniczy.
- `docs/geometry/RESULT_HC01_CIRCULAR_HELIX_PILOT_2026-11-09.md` — wyniki pilotażowe HC-01/TUBE, materiał pomocniczy.

**Jednozdaniowe wznowienie:** Otwórz ten handoff, przejrzyj istniejące moduły G/K/M/T oraz kod Helix-Lock i zrekonstruuj rzeczywisty przepływ sygnału przez helisę aż do jej odpowiedzi; nie rozpoczynaj nowych pobocznych badań przed tym audytem.


## 9. Wynik audytu istniejącego przepływu (2026-11-09)

Audyt zapisany w `docs/handoffs/AUDIT_SIGNAL_TO_HELIX_RESPONSE_PATH_2026-11-09.md`. Ustalono: graf zdarzeń może generować sygnał M/S; K wyznacza modalności (f,φ,A) i afiniczną synchronizację; `chrono_modal_geometry_bridge.py` mapuje trzy obwiednie na trajektorię Γ i mierzy jej κ/τ; G buduje mechaniczny pierścień i oblicza odpowiedź harmoniczną ustaloną; `modal_self_repair.py` dopasowuje skalar częstotliwości s. Są to osobne komponenty/projekcje, nie zamknięty sprzężony tor.

**Kluczowy wynik:** brakuje wykonywalnego przejścia: sygnał wejściowy → jawne oddziaływanie z fizycznym/abstrakcyjnym stanem helisy → aktualizacja stanu → obserwowalna odpowiedź → wpływ odpowiedzi na kolejne wejście. G nie przyjmuje obecnie przebiegu sygnału w czasie ani historii; jego odpowiedź jest ustalona w dziedzinie częstotliwości. Most chrono-modal mierzy geometrię trajektorii obwiedni, ale nie aktualizuje stanu G. K nie dostraja dynamicznie geometrii. `abs(tau)` w G usuwa znak chiralności.

**Następny krok:** nie robić kolejnego sweepu. Wybrać jeden istniejący sygnał i jeden kanał wymuszenia, określić jednostki/normalizację i jawnie oznaczyć mapowanie sygnału na wymuszenie jako hipotezę modelową. Następnie zbudować minimalny test integracyjny z identycznym sygnałem testowym dla stanu odniesienia i stanu po historii pobudzenia. Bez uzasadnienia jednostek wynik pozostaje abstrakcyjnym testem wejście–wyjście, nie fizycznym dowodem.
