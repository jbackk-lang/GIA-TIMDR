# AUDYT RZECZYWISTEJ ŚCIEŻKI SYGNAŁ → HELISA → ODPOWIEDŹ

**Data:** 2026-11-09  
**Repo:** GIA-TIMDR  
**Cel:** odtworzyć istniejący mechanizm i wskazać najważniejszą lukę bez dokładania nowej teorii.

## 1. Wniosek w skrócie

W repozytorium istnieją osobno:
- reprezentacja sygnału i jego cech (M/S);
- reprezentacja modalności i faz (K);
- projekcja sygnału/modalności na krzywą i metryki geometrii;
- mechaniczny model odpowiedzi wymuszonego pierścienia (G);
- model dopasowania częstotliwości oraz wybrane mechanizmy naprawcze.

**Nie znaleziono jednak jednego wykonywalnego łańcucha, w którym sygnał wejściowy zmienia stan helisy, a zmieniony stan helisy generuje odpowiedź i wpływa na kolejny sygnał.** Aktualne połączenia są projekcjami/analizą albo niezależnymi modelami. To jest zasadnicza luka.

## 2. Odtworzona ścieżka istniejących danych

### A. Graf zdarzeń → sygnał M/S

Źródła:
- `core/trm_gia_projections.py`
- `docs/theory/TIMDR_EventGraph_Branch_Construction.md`
- `docs/theory/TIMDR_Signal_From_EventGraph.md`

Zdarzenia niosą energię, czas i pozycję. GIA wybiera podgraf według geometrycznego toru odniesienia. `signal_projection` zamienia energię zdarzeń na sygnał czasowy przez binning; pełny binning zachowuje całkowitą energię. Alternatywnie `gaussian_signal` tworzy wygładzony sygnał próbkowany.

Ograniczenie: to konstrukcja wejścia sygnałowego. Sama nie modeluje oddziaływania sygnału z helisą ani jej odpowiedzi.

### B. Sygnał → modalności K

Źródła:
- `TIMDR-Math-Formalism/timdr_formalism/signal_class.py`
- `TIMDR-Modal-Formalism/timdr_modal/phase_sync.py`
- `docs/theory/Axioms_S_TIMDR_Signal.md`
- `docs/theory/Axioms_K_TIMDR.md`

K reprezentuje modalność przez `(f, phi, A)`; faza chwilowa jest `2πft+phi`. Istnieje interferencja modalności i test rezonansu oraz afiniczna mapa czasu lokalnego/globalnego. Parametry modalności są stałe w tym modelu.

Ograniczenie: synchronizacja K nie jest dynamicznym dostrajaniem wzajemnym ani sprzężeniem z geometrią helisy. Nie zmienia automatycznie `kappa`, `tau`, położenia węzłów ani stanu G.

### C. Obwiednie modalne → trajektoria przestrzenna → geometria

Źródło: `core/chrono_modal_geometry_bridge.py`.

W tym module trzy obwiednie pasm (BPFO/BPFI/BSF) są zestawiane jako:
`Gamma(t,s) = [A_1(t), A_2(t), A_3(t)]`.
Po bramce niezależności obliczane są krzywizna i torsja Freneta–Serreta trajektorii `Gamma`.

To jest najbliższy istniejący most sygnał–geometria: sygnał wpływa na geometrię trajektorii reprezentującej obwiednie. Jednak wynik jest zestawem metryk okna `kappa_win/tau_win`; nie jest aktualizacją stanu helisy fizycznej ani wejściem do G-Rezonansu. Trajektoria trzech obwiedni nie jest automatycznie osią/tunelem helisy TIMDR.

### D. Geometria → odpowiedź mechaniczna G

Źródła:
- `core/geometric_resonance_operator.py`
- `docs/geometry/TIMDR_GResonance_Operator.md`

G buduje pierścień N sprzężonych oscylatorów. Krzywizna w węźle daje sztywność własną, a wartość bezwzględna torsji segmentu daje sprzężenie sąsiednie. Odpowiedź ustalona jest liczona z:
`X(ω) = (K − ω²M + iωΓ)⁻¹ F`.

Istotne: pobudzenie to wektor harmoniczny dla jednego węzła w dziedzinie częstotliwości. Funkcja zwraca odpowiedź ustaloną. Nie przyjmuje surowego sygnału czasowego, nie ma jawnego stanu początkowego/historii i nie aktualizuje geometrii po odpowiedzi.

Dodatkowo użycie `abs(tau)` powoduje, że G w obecnej postaci nie rozróżnia lewego/prawego znaku torsji w sprzężeniu. Parametry przejścia geometria→mechanika `k_scale/kc_scale/gamma` są modelowe, nie skalibrowane na rzeczywistej helisie.

### E. Sygnał → modalna „sam naprawa”

Źródło: `core/modal_self_repair.py` i `docs/theory/PHASE_RECOVERY_VALIDATION_PROTOCOL.md`.

Moduł estymuje rezonanse obwiedni w pasmach i iteracyjnie aktualizuje jeden skalar prędkości `s`, aby dopasować przewidywane częstotliwości do pików. Nie ma jawnego stanu geometrycznej helisy, nie aktualizuje fazy i nie odtwarza payloadu. Dokument walidacyjny poprawnie rozdziela re-lock częstotliwości od odzyskania fazy, przebiegu i informacji.

## 3. Mapa: co faktycznie istnieje

| Przejście | Status | Co jest wyliczane |
|---|---|---|
| Graf zdarzeń → M/S sygnał | zaimplementowane | sygnał czasowy z energii/zdarzeń |
| Sygnał → modalności K | zaimplementowane w osobnych narzędziach | częstotliwość, faza, amplituda, synchronizacja |
| Obwiednie → trajektoria 3D → κ/τ | zaimplementowane | geometria trajektorii obwiedni |
| κ/τ → model mechaniczny G | częściowo jako osobny operator | macierze M/K/Γ |
| Wymuszenie → odpowiedź G | zaimplementowane w dziedzinie częstotliwości | odpowiedź ustalona pierścienia |
| Sygnał → zmiana stanu helisy → odpowiedź helisy | **brak zintegrowanego mechanizmu** | brak |
| Odpowiedź helisy → zmiana kolejnego sygnału | **brak** | brak |
| Historia sygnałów → stan helisy → odpowiedź na identyczne wejście | **brak w zintegrowanym torze** | brak |

## 4. Najważniejsza luka — jedno miejsce, nie lista nowych niewiadomych

Brakuje **adaptera sprzężenia wejścia i stanu** między istniejącym opisem sygnału/modalności a dynamiką G.

Potrzebny jest jawny kontrakt:
- wejście `u(t)`: już istniejący sygnał lub wybrana modalność, bez utraty jednostek i fazy;
- stan `z(t)`: jawny stan węzłów/stopni swobody helisy;
- operator oddziaływania `B`: określa, gdzie i w jaki sposób wejście działa na strukturę;
- dynamika `ż = F(z,u)`: aktualizacja stanu;
- wyjście `y = H(z,u)`: obserwowalna odpowiedź, która może zostać porównana z wejściem.

Nie wolno arbitralnie ustalić `B` ani `F` jako „prawa helisy”. Istniejący G dostarcza jedynie kandydata na liniową mechanikę odpowiedzi po podaniu macierzy i wymuszenia. Potrzebna jest decyzja, czy badany sygnał ma być interpretowany jako siła/naprężenie, wymuszenie modalne czy inna wielkość fizyczna. Bez jednostek i kanału oddziaływania nie ma jednoznacznego modelu.

## 5. Najmniejszy następny krok

Nie robić kolejnego sweepu geometrii. Najpierw przygotować jeden test integracyjny na syntetycznym sygnale:
1. wybrać jeden istniejący sygnał wejściowy i zachować jego próbki, fazę, skalę oraz jednostki;
2. wybrać istniejącą geometrię G i jej stan początkowy;
3. jawnie zdefiniować testowy kanał wymuszenia jako **hipotezę modelową**, nie fakt fizyczny;
4. porównać odpowiedź dla tego samego sygnału w stanie początkowym i po historii kontrolowanego pobudzenia;
5. mierzyć odpowiedź w tym samym kanale i sprawdzić, czy istnieje zależność od historii;
6. zachować kontrolę bez sprzężenia i model prostszy.

Jeśli nie ma podstaw do przypisania sygnałowi jednostek siły, test można wykonać wyłącznie jako abstrakcyjny model wejście–wyjście z jawną normalizacją; wynik nie może być wtedy nazywany fizycznym oddziaływaniem.

## 6. Decyzja kierunkowa

Najpierw rekonstruujemy i integrujemy istniejące komponenty. Nie rozwijamy równolegle tunelu, redukcji, punktów kardynalnych ani kolejnych rodzin helis. Geometria pozostaje stanem/warunkiem układu, a główną zmienną badawczą jest informacja wejściowa i odpowiedź.

**Konkluzja:** repozytorium ma komponenty dla sygnału, modalności, geometrycznej projekcji i odpowiedzi mechanicznej, ale nie ma jeszcze zamkniętej pętli sygnał–helisa–odpowiedź. To jest konkretna, centralna luka, którą dalsza praca ma rozwiązać bez dopowiadania nieuzasadnionej fizyki.
