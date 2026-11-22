# Indeks eksperymentów GIA-TIMDR

Eksperymenty są grupowane według tematu badawczego. Zachowujemy cienkie punkty zgodności w dawnych ścieżkach, żeby nie zerwać starszych poleceń, importów i odnośników.

## Serie uporządkowane katalogowo

| Obszar | Lokalizacja | Zakres |
|---|---|---|
| 54A | [54A/](54A/README.md) | kod, raporty i wyniki serii 54A |
| Chronoproces | [chronoprocess/](chronoprocess/README.md) | odzyskiwanie fazy, historia czasowa i pętle sprzężone |
| Geometria graniastosłupa rombowego | [rhombic_prism/](rhombic_prism/README.md) | osie śrubowe, widma, symetrie i certyfikaty |
| Odbicia i wielościany | [reflections/](reflections/README.md) | odbicia BC, pentachoron, graniastosłupy i czworościan |
| Charakterystyka helis | [helix_characterization/](helix_characterization/) | geometria helis, rurki i testy |
| Redukcja helis | [helix_reduction/](helix_reduction/) | redukcje powierzchni, audyty płatów i testy |
| Odpowiedź sygnałowa helisy | [helix_signal_response/](helix_signal_response/) | minimalne sprzężenie i testy |
| Historia fazy MAGE | [mage_temporal_phase_history/](mage_temporal_phase_history/) | testy historii fazowej |
| Redukcja jądrowa | [nuclear_reduction/NRG-01/](nuclear_reduction/NRG-01/README.md) | NRG-01: źródła, audyty i testy |
| Zachowanie pola fazowego | [phase_field_preservation/](phase_field_preservation/) | model zachowania pola fazowego i test |

## Zgodność ze starszymi ścieżkami

Kod źródłowy 52 skryptów z dawnego poziomu głównego został przeniesiony do trzech katalogów tematycznych. W starych lokalizacjach pozostawiono małe adaptery zgodności, które przekazują uruchomienie do nowej lokalizacji i udostępniają symbole przy imporcie. Dzięki temu wcześniejsze polecenia i importy nadal mają punkt wejścia.

- Nowy kod rozwijaj w katalogach tematycznych, nie w adapterach.
- Workflow GitHub Actions obserwują nowe katalogi tematyczne.
- Testy istniejące w `tests/` zachowują dotychczasowe importy przez adaptery.
- Skrypty uruchamiaj z katalogu głównego repozytorium.

## Zasady dalszego porządkowania

Nie przenosimy kodu rdzenia (`core/`), aplikacji (`applications/`) ani testów integracyjnych (`tests/`) do katalogu eksperymentów. Każde kolejne przeniesienie wymaga równoległej aktualizacji workflow, importów, dokumentacji i kontroli testów.
