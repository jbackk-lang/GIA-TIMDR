# NRG-01 / równoległy test orientacji helisy — raport wykonania

**Data wykonania:** 2026-11-09  
**Status:** pierwszy przebieg zakończony powodzeniem (GitHub Actions)  
**Workflow run:** https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42562770837  
**Commit wejściowy:** `e46692966544761f8925e33d118a9c0de29a7862`  
**Źródło grafu:** IAEA LiveChart API, `fields=ground_states`  
**Artefakt:** `nrg01-parallel-tracks`, ID `13650540554`, SHA-256 `fde856f7a7e744a413da954d0d4f2550e531ee42b19fff841992e3beebc1b146`  
**Zakres:** graf stanów podstawowych; kanały α, β⁻, β⁺ i EC automatycznie mapowane tylko wtedy, gdy reguła bilansu jest jednoznaczna. Pozostałe kanały pozostają nierozstrzygnięte.

## 1. Kontrola wykonania

Wszystkie kroki workflow zakończyły się sukcesem:
- testy jednostkowe;
- pobranie danych IAEA;
- budowa grafu;
- analiza struktury grafu;
- kontrola analityczna znaku skrętu;
- zapis artefaktów.

Artefakt zawiera `graph.json`, `graph_analysis.json`, `helix_handedness.json` oraz surowe odpowiedzi CSV dla każdego pobranego nuklidu.

## 2. Wyniki grafu nuklidów

| Miara | Wynik |
|---|---:|
| Węzły / nuklidy | 48 |
| Rozpoznane krawędzie | 54 |
| Kanały nierozstrzygnięte | 12 |
| Węzły o stopniu wyjściowym 2 | 9 |
| Maksymalny stopień wyjściowy | 2 |
| Węzły bez rozpoznanej krawędzi wyjściowej | 3 |

Histogram stopnia wyjściowego: 3 węzły stopnia 0, 36 stopnia 1, 9 stopnia 2. Brak węzłów stopnia 3 w tym pobranym, częściowym grafie.

Dziewięć rozpoznanych punktów rozgałęzienia:
- `221Fr`: α → `217At`; β⁻ → `221Ra`;
- `218Po`: α → `214Pb`; β⁻ → `218At`;
- `217At`: α → `213Bi`; β⁻ → `217Rn`;
- `218At`: α → `214Bi`; β⁻ → `218Rn`;
- `212Bi`: β⁻ → `212Po`; α → `208Tl`;
- `213Bi`: β⁻ → `213Po`; α → `209Tl`;
- `214Bi`: β⁻ → `214Po`; α → `210Tl`;
- `210Pb`: β⁻ → `210Bi`; α → `206Hg`;
- `210Bi`: β⁻ → `210Po`; α → `206Tl`.

Sumy rozgałęzień mogą minimalnie odbiegać od 100% z powodu zaokrągleń danych źródłowych.

### 2.1. Trzy komponenty

Graf ma trzy słabo spójne komponenty, osiągalne odpowiednio z wybranych jąder startowych:
- U-238: 20 węzłów;
- Th-232: 12 węzłów;
- Np-237: 16 węzłów.

**Ostrożność interpretacyjna:** trzy komponenty wynikają z wyboru trzech niezależnych jąder startowych i nie są dowodem na uniwersalną trójdzielność natury ani na trójhelikalny węzeł TIMDR. Są trzema porównywalnymi ścieżkami eksperymentalnymi.

### 2.2. Punkty przejścia jako kandydaci na punkty kardynalne

Dziewięć rozgałęzień to konkretne zdarzenia w grafie, które można porównywać z punktami kardynalnymi wyłącznie na poziomie roli abstrakcyjnej: zmiana kanału / rozgałęzienie / przejście. Nie są one automatycznie punktami na osi helisy. W kolejnym kroku należy badać kolejność zdarzeń, ich etykiety kanałów i zachowane obserwable.

### 2.3. Redukcja 4→3

Analizator znalazł nakładające się czterowęzłowe podgrafy z rozgałęzieniami, ale nie wykazał naturalnej, fizycznie uzasadnionej redukcji czterech stanów do trzech. Eksploracyjne klasy równoważności grupują zachowanie kanałów i status, celowo pomijając Z,N; każda taka agregacja traci tożsamość nuklidu i nie może być uznana za fizyczną redukcję bez wskazania obserwabli, które mają być zachowane.

**Wniosek NRG-01 / przebieg 1:** występują rzeczywiste rozgałęzienia binarne; nie zaobserwowano rozgałęzień trójkanałowych ani dowodu na naturalną redukcję 4→3. Wynik jest ograniczony do pobranych danych stanów podstawowych i rozpoznanych kanałów.

## 3. Równoległy test znaku skrętu helisy

Dla idealnej helisy kołowej:
[
r(t)=(R\cos t, R\sin t, ht)
]
podpisana torsja wynosi:
[
\tau_g=\frac{h}{R^2+h^2}.
]

Dla (R=1), (|h|=0.5):
- wariant prawoskrętny: (+0.4);
- wariant lewoskrętny: (-0.4);
- wartości bezwzględne są równe, znaki przeciwne.

Test przeszedł. Potwierdza to, że projekcja do (|\tau_g|) usuwa informację o ręczności. W rejestrze po redukcji należy zachować co najmniej: podpisaną torsję, podpisany skok, orientację osi, fazę i kolejność zdarzeń kardynalnych.

To test analityczny idealnej helisy, a nie pomiar istniejącej helisy TIMDR. Nie stanowi dowodu, że przeciwna ręczność oznacza antycząstkę.

## 4. Integralność i odtwarzalność

SHA-256 plików wynikowych:
- `graph.json`: `9850a6cdc976e01f75e55eda8b199b595a29541dc115dca3d21e97a7311d2da9`;
- `graph_analysis.json`: `fd9ef4a7c9f4dc07b5b267e415ff80f17941df13b97889ef56fd0b1e440d6710`;
- `helix_handedness.json`: `8ccdb2ade462106b2b38dae8801c8cddb507e0367d658b020924c9bd13f5d259`;
- ZIP artefaktu: `fde856f7a7e744a413da954d0d4f2550e531ee42b19fff841992e3beebc1b146`.

Artefakt workflow jest przechowywany przez GitHub Actions przez 90 dni. Zawiera surowe CSV, więc umożliwia odtworzenie grafu bez ponownego pobierania tych samych odpowiedzi źródłowych.

## 5. Następne kroki

1. Rozszerzyć import o kanały SF, emisję neutronów/protonów i przejścia poziomów, zamiast traktować je jako brakujące krawędzie.
2. Zweryfikować rozgałęzienia z ocenionymi danymi ENSDF/NNDC, w tym niepewności.
3. Zbudować porównanie ścieżek z zachowaniem etykiet kanałów, nie tylko stopni węzłów.
4. Zdefiniować operator mapujący zdarzenia grafu na kandydatów punktów kardynalnych helisy; sprawdzić, czy odwzorowanie zachowuje kolejność i strukturę rozgałęzień.
5. Dla helisy TIMDR wyznaczyć podpisaną torsję i skok na danych geometrycznych źródłowych; sprawdzić warunki brzegowe, węzeł trójhelikalny i punkty, w których klasyczna torsja jest nieokreślona.
6. Przetestować redukcję na parach lewo-/prawoskrętnych i wykazać, że znak nie zanika.

**Zasada nadrzędna:** nie redukować geometrii przez wartość bezwzględną skrętu; nie utożsamiać grafu nuklidów z węzłem topologicznym; nie przypisywać etykiety antycząstki na podstawie samej ręczności geometrycznej.


## 6. Powtórzenie z limitem rozmiaru grafu

Po dodaniu bezpiecznego limitu `--max-nodes=250` uruchomiono ponownie cały workflow: [run 42562827240](https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42562827240). Wszystkie kroki ponownie zakończyły się sukcesem. Wyniki były zgodne z pierwszym przebiegiem: 48 nuklidów, 54 rozpoznane przejścia, 12 kanałów nierozstrzygniętych, 9 rozgałęzień; 48 surowych odpowiedzi CSV. Podpisane torsje kontrolne ponownie wyniosły +0.4 i −0.4.

Drugi artefakt: `nrg01-parallel-tracks`, ID `13650530264`, SHA-256 `cbe4f5771cdc3c668c73c99d19a9dff6524874740622e8548b069bfb77a4ec3b`. Powtórzenie potwierdza stabilność tego przebiegu pipeline'u, ale nie usuwa ograniczeń zakresu danych ani nie stanowi niezależnej walidacji fizycznej.
