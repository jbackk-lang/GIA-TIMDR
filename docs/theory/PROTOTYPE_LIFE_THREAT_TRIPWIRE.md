# Prototyp: tripwire jawnego zagrożenia życia (osobny moduł obok monitora M/S)

> Odpowiedź na krytykę użytkownika kategoryzacji ryzyka po domenie:
> "trzeba jasno opracować dziedziny i ich głębokość penetracji — do broni
> można wykorzystać nawet czajnik, więc nie ma tu jednoznaczności — jest
> potknięcie w projekcie i wówczas następować powinien ogólny paraliż —
> potknięcie w stylu słowa lub zdania zagrażającego świadomie życiu."
> Po zbudowaniu wersji regexowej, druga uwaga użytkownika: "determinizm
> i głupota muszą się skończyć wobec takich zagrożeń" — uwzględniona
> poniżej jako druga, semantyczna warstwa. Kod: `core/life_threat_tripwire.py`.
> Data: 2026-09-16.

## Dlaczego to jest OSOBNY moduł, nie rozszerzenie monitora M/S

`core/ai_behavior_monitor.py` (poprzedni prototyp) klasyfikuje ryzyko po
**domenie działania** (`risk_action_rate`) i daje **miękki wynik
statystyczny** (koincydencja anomalii, K z N kanałów). Użytkownik trafnie
wskazał, że kategoryzacja po domenie jest z natury dziurawa — dowolna
zdolność jest dual-use. Więc ten moduł **nie klasyfikuje działań**, tylko
sprawdza **treść pojedynczej wypowiedzi** pod kątem jawnego, świadomego
zagrożenia życia, i odpowiada **twardym STOP** (wyjątek `LifeThreatHalt`),
nie liczbą.

Architektoniczne rozróżnienie:

| | `ai_behavior_monitor.py` | `life_threat_tripwire.py` |
|---|---|---|
| Wejście | wielokanałowa seria czasowa (proxy zachowania) | pojedynczy tekst |
| Metoda | statystyka (rezonans-K, kalibracja mocy) | dopasowanie treści |
| Wyjście | wynik liczbowy + rekomendacja progu | HALT albo nic |
| Filozofia błędu | zrównoważony kompromis czułość/swoistość | świadomie przechylony w stronę czułości (fail-safe) |

## Dwie warstwy — i dlaczego jedna nie wystarczyła

**Warstwa 1 (regex, zawsze dostępna).** Wymaga jednocześnie: czasownika
działania śmiercionośnego + markera intencji pierwszoosobowej/bezpośredniej
+ celu-osoby. Deterministyczna, auditowalna, zero zależności — ale ślepa na
parafrazę, inny język, obejścia słowne. To zostało jawnie ujawnione od razu
w nagłówku modułu, ale — jak słusznie zauważył użytkownik — "ujawnione" nie
znaczy "naprawione".

**Warstwa 2 (`semantic_judge`, opcjonalna, wstrzykiwana przez wywołującego).**
Zamiast dopisywać regexy w nieskończoność (ślepa uliczka — język naturalny
nie jest wyczerpywalny listą wzorców), `check_text()` przyjmuje opcjonalną
funkcję semantycznego osądu (np. wywołanie modelu językowego z pytaniem
"czy ten tekst świadomie i jednoznacznie grozi czyjemuś życiu?"). Działa
**równolegle** z regexem — logiczny OR, każda warstwa może samodzielnie
wywołać HALT, żadna nie wetuje drugiej.

Demonstracja w kodzie (`run_illustrative_eval()`): zdanie
*"Jutro w nocy przestanie oddychać przeze mnie i nikt się nie dowie, jak."*
— jawne zagrożenie życia bez ŻADNEGO słowa z list regexowych — jest
**przeoczone przez samą warstwę 1** (jak przewidziano) i **złapane, gdy
dołączona jest atrapa `semantic_judge`**. To jest uruchamialny dowód
ograniczenia warstwy 1, nie tylko zdanie w prozie.

## Uczciwe zastrzeżenie o warstwie 2 (kluczowe, nie do pominięcia)

`semantic_judge` w tym repo **nie ma dostarczonej realnej implementacji** —
w tym sandboxie nie ma dostępu do modelu/API do kalibracji. Atrapa
(`_stub_semantic_judge`) rozpoznaje twardo zakodowane JEDNO zdanie —
demonstruje wyłącznie punkt integracji, **nie jest dowodem**, że jakikolwiek
prawdziwy model zachowa się tak samo na innych parafrazach. Realna
czułość/swoistość prawdziwego modelu semantycznego jest tu **niezmierzona**.

Podłączenie prawdziwego modelu na produkcję bez uprzedniej kalibracji na
realnych kontrolach pozytywnej (znane, zróżnicowane realne zagrożenia) i
negatywnej (znany bezpieczny tekst — fikcja, cytaty, dyskusje kliniczne/
prawne, wiele języków i stylów) byłoby dokładnie tym błędem, przed którym
ostrzega `calibrate_resonance_K` z pierwszego modułu: nie wolno rekomendować
progu/włączyć mechanizmu bez sprawdzonej mocy testu. Ta sama dyscyplina,
inna domena.

## Semantyka odpowiedzi: HALT, nie score — i jej własne ryzyko

Odpowiedzią jest wyjątek Pythona (`LifeThreatHalt`), nie zwracana flaga —
wywołujący **musi** go jawnie obsłużyć (eskalacja do człowieka, log,
zatrzymanie pipeline'u), nie może go po cichu zignorować.

**Nie pominięte zastrzeżenie o nadużyciu mechanizmu**: skoro odpowiedzią
jest pełny stop całego systemu, sam mechanizm staje się powierzchnią ataku
typu odmowa usługi — ktokolwiek zna wzorce wyzwalające, może celowo
wypowiedzieć frazę wyzwalającą, żeby zatrzymać system. Dlatego HALT w tym
prototypie **nie jest** zaprojektowany jako ciche, trwałe, autonomiczne
wyłączenie bez odwołania — to wyjątek wymagający świadomej decyzji
obsługującego kod (np. przegląd człowieka przed wznowieniem). To
rozróżnienie jest częścią projektu, nie przeoczeniem.

## Akceptowane fałszywe alarmy, nieuniknione przeoczenia

- **Fałszywe alarmy (akceptowany koszt)**: fikcja, cytaty, dyskusje
  hipotetyczne/kliniczne/prawne ZE WSZYSTKIMI trzema elementami warstwy 1
  (albo zaklasyfikowane przez warstwę 2) nadal wywołają HALT — to świadomy
  wybór projektowy zgodny z propozycją użytkownika ("potknięcie" →
  "ogólny paraliż", nie "potknięcie → cicha ocena ryzyka").
- **Fałszywe negatywy (nieunikniona granica)**: warstwa 1 z definicji
  przeoczy parafrazę/kodowanie/wieloetapowe sformułowanie bez słów-kluczy
  (zademonstrowane wyżej); warstwa 2 zależy całkowicie od jakości
  niezmierzonego, niedostarczonego modelu semantycznego.

## Status

Koncepcyjny prototyp. Warstwa 1 działa i przetestowana na garstce
przykładów ilustracyjnych (nie jest to test statystyczny — klasyfikacja
treści na garstce przykładów nie kwalifikuje się do Manna-Whitneya/rozmiaru
efektu reszty ekosystemu; stosowanie tej maszynerii tu byłoby numerologią,
nie rygorem). Warstwa 2 to gotowy, przetestowany na atrapie punkt integracji
— bez realnej implementacji i bez realnej kalibracji. Nie promowane do
żadnej gałęzi aksjomatów TIMDR — to zastosowanie prostego wzorca
inżynieryjnego (content tripwire + hard stop), nie nowa matematyka.

## Warunki przed użyciem na realnym systemie

1. Realna implementacja `semantic_judge` (konkretny model, konkretny
   prompt/interfejs).
2. Realne dane kalibracyjne: zróżnicowany zbiór prawdziwych zagrożeń
   (pozytywna kontrola) i prawdziwie bezpiecznego tekstu obejmującego
   fikcję/cytaty/dyskusje kliniczne w wielu językach (negatywna kontrola) —
   zmierzona czułość/swoistość obu warstw osobno i razem.
3. Jawna procedura obsługi `LifeThreatHalt` na produkcji (kto przegląda,
   jak wygląda wznowienie, jak ograniczone jest ryzyko odmowy usługi przy
   znanych wzorcach wyzwalających).
