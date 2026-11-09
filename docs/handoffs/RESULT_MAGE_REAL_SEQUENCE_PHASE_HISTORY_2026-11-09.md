# WYNIK: historia fazowa w rzeczywistych sekwencjach MAGE (UCSD Ped2)

**Data:** 2026-11-09  
**CI:** https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42585600447  
**Status:** wykonanie PASS na 3 sekwencjach; analiza reprezentacji, nie walidacja fizyczna helisy.

## 1. Dane i metoda

Wykorzystano obrazy zapisane w repozytorium `jbackk-lang/MAGE-IN-IMAGE-DECODER`:
- Test001: 180 klatek; adnotacja anomalii 61–180;
- Test002: 180 klatek; adnotacja anomalii 95–180;
- Test003: 150 klatek; adnotacja anomalii 1–146.

Każdą klatkę zmniejszono do 180×120, odjęto średnią jasność i obliczono zespolone 2D FFT. Zachowano 10 789 koszyków częstotliwości o istotnej średniej amplitudzie, z wyłączeniem okolicy DC. Historię zapisano jako fazę początkową oraz uporządkowane przyrosty:
[
\Delta\phi_t(k)=\arg(F_{t+1}(k)\overline{F_t(k)}).
]
Porównano rekonstrukcję w prawidłowej kolejności, rekonstrukcję po deterministycznym przetasowaniu przyrostów i relację przy odwróceniu kolejności klatek.

## 2. Wyniki rekonstrukcji

| Sekwencja | Klatki | MAE rekonstrukcji uporządkowanej | MAE po tasowaniu | Iloraz błędów |
|---|---:|---:|---:|---:|
| Test001 | 180 | 3.26×10⁻⁶ rad | 1.380 rad | 422 858× |
| Test002 | 180 | 2.70×10⁻⁶ rad | 1.383 rad | 511 926× |
| Test003 | 150 | 2.50×10⁻⁶ rad | 1.393 rad | 557 975× |

To pokazuje, że uporządkowane przyrosty fazy wraz z fazą początkową kodują przebieg fazowy sekwencji, a losowe przetasowanie niszczy możliwość odtworzenia oryginalnej historii. Odwrócenie czasu spełniło tożsamość `Δφ_reverse = -reverse(Δφ_forward)` z maksymalnym błędem numerycznym 4.77×10⁻⁷ rad.

**Ważne ograniczenie:** dokładna rekonstrukcja jest matematycznie oczekiwaną konsekwencją definicji przyrostów fazy. Nie dowodzi autonomicznej pamięci pola ani helisy. Test potwierdza poprawność reprezentacji i zachowanie kolejności danych.

## 3. Czy aktywność fazowa rozróżniała odcinki normalne i anomalne?

Średnia z modułu przyrostów fazy na ważnych koszykach FFT, porównana opisowo z adnotacjami datasetu:

| Sekwencja | Przejścia normalne | Średnia normalna (rad) | Przejścia anomalne | Średnia anomalna (rad) |
|---|---:|---:|---:|---:|
| Test001 | 59 | 0.4543 | 119 | 0.4754 |
| Test002 | 93 | 0.4352 | 85 | 0.5794 |
| Test003 | 3 | 0.4787 | 145 | 0.5184 |

Test002 wykazuje większą średnią aktywność fazową w zakresie adnotacji anomalii; Test001 różnica jest niewielka. Test003 ma tylko 3 przejścia normalne w dostępnej sekwencji, więc porównanie jest niewystarczające. Nie wykonano testu statystycznego, korekty ruchu kamery ani walidacji na niezależnych klipach — nie wolno z tego wnioskować o detekcji anomalii ani specyficzności sygnału.

## 4. Wniosek dla TIMDR

1. MAGE ma rzeczywiste sekwencje, na których można badać ewolucję zespolonego widma, a nie tylko statyczne pole.
2. Reprezentacja `F_0 + ordered Δφ_t` zachowuje kolejność zmian i pozwala odtworzyć fazę kolejnych klatek.
3. Sam rozkład przyrostów fazowych nie wystarcza: ich porządek w czasie jest istotny.
4. Prosty wskaźnik średniego modułu przyrostu nie rozdziela konsekwentnie odcinków normalnych i anomalnych.
5. To nadal analiza obrazów, a nie dowód, że pole jest nośnikiem pamięci helisy. Do TIMDR można przekazać reprezentację historii, ale mapowanie na S/GS-Matrix wymaga osobnej hipotezy i testu.

## 5. Następny test

Przed GS-Matrix należy:
- zarejestrować klatki przestrzennie lub skorygować globalny ruch;
- odróżnić zmianę fazy wynikającą z translacji/sceny od zmian strukturalnych;
- przetestować fazę lokalną i koherencję między sąsiednimi koszykami, nie tylko globalną średnią;
- porównać historię fazową z prostymi baseline'ami: różnica obrazu, przepływ optyczny, amplituda widma;
- wykonać walidację na większej liczbie klipów i kontrolach bez anomalii.

**Decyzja:** zachować ten tor jako kandydat na temporalny adapter pola. Nie integrować go jeszcze z mechanicznym G-Rezonansem.
