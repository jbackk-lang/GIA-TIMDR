# 54A.8 — predyktor META na grafie zdarzeń

Źródło: docs/theory/TIMDR_EventGraph_Branch_Construction.md §5. Stan jest aktualizowany dopiero po zamknięciu okna.

Trzy deterministyczne syntetyczne strumienie po 16384 bajty; okna 64, predyktory opóźnień 1/3/64, reszty modulo 256, jeden gzip level 9 na strumień, wszystkie dekodowania zgodne.

| Dane | gzip sygnału | statyczna | adaptacyjna | META | geometria gzip | META + geometria |
|---|---:|---:|---:|---:|---:|---:|
| structured | 95 | 64 | 105 | 111 | 116 | 227 |
| switching | 554 | 2062 | 572 | 571 | 119 | 690 |
| random | 16407 | 16407 | 16407 | 16407 | 9852 | 26259 |

Wniosek: brak przewagi nad gzip. Różnica jednego bajta nad adaptacją w switching jest nieistotna. Geometryczne side information musi być identycznie uwzględniane w porównaniach całego grafu. Tu współrzędna y jest stała w oknie, a J praktycznie stałe, więc nie testujemy zmiennej geometrii. Heurystyka wyboru predyktora nie jest źródłowym prawem ewolucji TIMDR. Wyniki nie obejmują nagłówków kodeka. Kod testu: 54A8_EVENT.py (lokalny artefakt eksperymentu).