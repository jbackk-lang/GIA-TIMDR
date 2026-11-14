# Wyniki pilota dynamiki — 2026-11-14

**Status:** eksperyment eksploracyjny na syntetycznym AR(1), nie walidacja pełnego TIMDR.

Uruchomiono lokalnie kod odpowiadający `dynamic_trajectory_pilot.py` (Python, biblioteka standardowa), a następnie skorygowano kontrolę SHUFFLED. Ziarna treningowe 1000–1099; testowe 9000–9049; 3 klasy STEP, RAMP, RECOVERY; 150 przypadków testowych, 16 okien po 64 próbki.

## Wyniki

| Reprezentacja | Trafność | Poprawne / 150 |
|---|---:|---:|
| STATIC: mean, std, min, max okiennych lag-1 | 0.7933 | 119 |
| SHUFFLED: osobna permutacja okien dla każdego ziarna, ta sama dla trzech klas tego ziarna | 0.6733 | 101 |
| DYNAMIC: zachowana kolejność 16 okiennych lag-1 | 1.0000 | 150 |

**Błąd wykryty w pierwszej wersji:** stała permutacja SHUFFLED (seed 123456) zachowywała identyfikowalny indeks czasu; dawała 1.0000, ale nie stanowiła kontroli usunięcia kolejności. Kod poprawiono tak, aby permutacja zależała od ziarna sesji (nie od etykiety). Po poprawce SHUFFLED = 0.6733.

## Co wolno wnioskować

W tym konkretnym, syntetycznym zadaniu zachowanie kolejności okien poprawia trafność względem dwóch uproszczonych kontroli. Nie dowodzi to wyższości dynamicznego TIMDR nad pełnym modelem statycznym, ponieważ DYNAMIC używa 16 cech, a STATIC tylko 4, i nie jest implementacją formalnych operatorów TIMDR.

## Co dalej

Wymagana kontrola równej liczby cech i pojemności modelu, bootstrap po niezależnych ziarnach, test parametrów poza treningiem, zmienny moment przełączenia, błędy zegara, dwa odbiorniki, przypadki nieidentyfikowalne i klasa UNKNOWN. Raportować opóźnienie wykrycia i powrót, nie tylko klasyfikację całego przebiegu.

**Reprodukcja:** `python docs/research/info_geometry/dynamic_trajectory_pilot.py`. Lokalnie odtworzono logikę programu; repozytoryjny plik poprawiono po audycie, ale nie został ponownie pobrany i uruchomiony bezpośrednio.
