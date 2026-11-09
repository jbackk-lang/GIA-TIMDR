# Minimalny test sprzężenia sygnał–G–odpowiedź (v0.1)

**Data:** 2026-11-09  
**Status:** wykonany syntetyczny test integracyjny; CI PASS.  
**Run:** https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42572283596  
**Kod:** `experiments/helix_signal_response/minimal_coupling_probe.py`

## 1. Co wykonano

Zintegrowano istniejący operator macierzy G z prostą integracją czasową układu:
[
M\ddot{x}+\Gamma\dot{x}+Kx=B u(t).
]

Wejściem jest jeden znormalizowany sygnał skalarny podawany do węzła 0. Macierze M/K/Γ pochodzą z istniejącego `build_ring_matrices`. Stan układu to `z=(x,v)`, a odpowiedzią jest przemieszczenie węzła pobudzanego.

Porównano dwa ramiona:
- stan zerowy / bez historii;
- stan po wcześniejszym kontrolowanym impulsie pobudzającym, po którym następuje cisza.

Oba ramiona otrzymują dokładnie ten sam sygnał testowy.

## 2. Wynik uruchomienia

GitHub Actions: **PASS**, 3/3 testy. Sweep nie był wykonywany; uruchomiono pojedynczy test integracyjny.

| Miara odpowiedzi węzła 0 | Wynik |
|---|---:|
| RMS odpowiedzi, stan zerowy | 0.0311099 |
| RMS odpowiedzi, stan po historii | 0.0838454 |
| RMS różnicy przebiegów | 0.0748333 |
| Maksymalna bezwzględna różnica | 0.1739572 |

Dla identycznego wejścia odpowiedź jest różna, gdy stan początkowy układu jest inny. W tym modelu wynika to z resztkowego stanu dynamicznego `(x,v)` pozostawionego przez wcześniejsze pobudzenie.

## 3. Co ten wynik ustala — i czego nie ustala

**Ustala:** istniejący model pierścienia G można rozszerzyć o czasową ewolucję stanu i podać mu próbki sygnału. W takiej konstrukcji odpowiedź zależy od stanu początkowego, więc mamy działający minimalny tor wejście→dynamika→wyjście oraz test zależności odpowiedzi od historii stanu.

**Nie ustala:** że rzeczywista helisa TIMDR fizycznie odbiera sygnał w ten sposób; że znormalizowana próbka jest siłą; że występuje pamięć informacyjna, adaptacja lub samonaprawa; że sygnał jest przetwarzany/odzyskiwany. Współczynnik wejście→siła jest arbitralnym wzmocnieniem modelowym bez kalibracji jednostek. Resztkowa odpowiedź mechaniczna nie jest dowodem trwałej pamięci.

To test integracji matematyczno-programistycznej, nie walidacja empiryczna.

## 4. Najważniejszy wniosek dla kierunku badań

Mamy teraz minimalny przykład, który pokazuje, jak można formalnie zamknąć fragment pętli:
`u(t) → z(t) → y(t)`.

Pozostaje jedna zasadnicza kwestia: **co w rzeczywistym mechanizmie helisy jest fizycznym kanałem, przez który informacja/sygnał oddziałuje na jej stan?** Dopóki nie ma uzasadnionego mapowania i jednostek, test pozostaje abstrakcyjny. Nie należy mnożyć parametrów ani rozwijać nowych modeli, zanim ten kanał nie zostanie ustalony na podstawie wcześniejszych badań/kodu.

## 5. Reprodukowalność i poprawki

Pierwszy run CI wykrył błąd ścieżki importu w teście. Ścieżkę poprawiono; ponowne uruchomienie przeszło: 3 testy, skrypt eksperymentalny i zapis artefaktu. Run końcowy: `42572283596`.

**Decyzja:** zachować jako proof-of-integration. Nie awansować wyniku do twierdzenia o fizycznym zachowaniu helisy.
