Prime Position Filter — Structural XOR of √2 and √3

## WERYFIKACJA (audyt, sesja 2026-08-29) — WYNIK: OBALONE

Użytkownik zapytał wprost o rzetelny werdykt w sprawie tego twierdzenia.
Zweryfikowano protokołem z `timdr-signal-framework` skill §18 (dokładna
definicja obiektów i metryki PRZED liczeniem, model zerowy, jeden przebieg,
uczciwy raport niezależnie od wyniku). Wynik: **twierdzenie o "rezonansie
strukturalnym" na pozycjach pierwszych — w tym kluczowy przykład z
bliźniaczymi liczbami pierwszymi 29/31 — jest fałszywe.**

**1. Tabela cyfr w tym dokumencie zawiera błędy.** Policzono √2 i √3 z
prawdziwą precyzją dowolną (`mpmath`, 20000+ cyfr) i porównano z tabelą
powyżej: pozycje 2,3,5,7,11,13,17 się zgadzają, ale **pozycje 19, 23, 29,
31, 37, 41, 43, 47 mają BŁĘDNE wartości cyfr**. To pasuje dokładnie do
wzorca "policzono zwykłym `float` (podwójna precyzja ≈15-17 cyfr
znaczących), nie arytmetyką dowolnej precyzji" — od pozycji ~17 w dół
liczy się już nie prawdziwe cyfry √2/√3, tylko szum reprezentacji
zmiennoprzecinkowej. To dokładnie ta pozycja, od której tabela zaczyna się
rozjeżdżać.

**2. Poprawione cyfry: pozycja 31 wcale się NIE zgadza.** Prawdziwe cyfry
na pozycji 31: √2=6, √3=8 — RÓŻNE, nie takie same jak twierdzi dokument
(8, 8). Czyli nawet w oryginalnej, 15-elementowej próbce, "obie bliźniacze
liczby pierwsze 29 i 31 się zgadzają" jest nieprawdą — zgadza się tylko
pozycja 29 (1 z 15, nie 2 z 15).

**3. Test na pełną skalę (2262 pozycji pierwszych wśród 20004 prawdziwych
cyfr):** wskaźnik zgodności na pozycjach pierwszych = 9,505% — statystycznie
NIEODRÓŻNIALNE od oczekiwanych 10,000% dla niezależnych cyfr jednostajnych
(test dwumianowy, p=0,46). Brak istotnej różnicy między pozycjami
pierwszymi a wszystkimi pozycjami (test 2-proporcji, p=0,29). Brak istotnej
różnicy między pozycjami należącymi do par bliźniaczych a pozostałymi
pozycjami pierwszymi (p=0,65 — a kierunek jest odwrotny do twierdzonego:
0,091 vs 0,097).

**4. Gęstość cyfr {2,3,5,7} (sekcja "requires further verification"
poniżej) też sfalsyfikowana** — patrz punkt 4 w audycie `al_filter_predictions.md`:
√2, √3, q mają WSZYSTKIE ~39,6-39,7% (oczekiwane 40,0%), nie 36%/50%/48%
jak twierdzono.

**Wniosek:** brak jakiejkolwiek wykrywalnej struktury na pozycjach
pierwszych w cyfrach √2/√3 — w pełni zgodne z tym, czego oczekuje się
matematycznie dla cyfr algebraicznych niewymiernych bez znanej struktury
("normalność" cyfr, tak samo jak testy losowości cyfr π). To NIE jest
filtr strukturalny — to artefakt błędu precyzji zmiennoprzecinkowej
zinterpretowany jako sygnał.

---

How the filter works

The filter does not operate on digit values.
It operates on positions (indices) in the decimal expansions of √2, √3, q.

This is an index filter, not an arithmetic filter.


Step 1 — Decimal expansions

√2 = 1.41421356237309514547462185873...
√3 = 1.73205080756887719317660412343...
q  = 3.14626436994197256069583090720...

Each digit has an index: 1, 2, 3, 4, 5...
(counting from first digit after decimal point)


Step 2 — Filter: select only prime positions

Keep only digits at positions that are prime numbers:

Prime positions: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47...

This is the first filter layer: prime indices.


Step 3 — XOR between √2 and √3 at prime positions

For each prime position p:

XOR(digit_√2[p], digit_√3[p]) = 1 if digits differ
                                = 0 if digits are equal

Verified results (positions 2 through 47):

pos  √2  √3  XOR
  2   1   3   1  ← differ
  3   4   2   1  ← differ
  5   1   5   1  ← differ
  7   5   8   1  ← differ
 11   7   6   1  ← differ
 13   0   8   1  ← differ
 17   4   9   1  ← differ
 19   4   1   1  ← differ
 23   2   0   1  ← differ
 29   3   3   0  ← SAME
 31   8   8   0  ← SAME
 37   4   0   1  ← differ
 41   6   9   1  ← differ
 43   4   0   1  ← differ
 47   3   9   1  ← differ

Result: 13/15 = 0.867 positions differ

Only positions 29 and 31 have identical digits in √2 and √3.


Step 4 — "Primes of primes"

The positions where XOR = 1 are the places where
binary structure (√2) and ternary structure (√3) diverge.

The positions where XOR = 0 (29, 31) are the places where
they momentarily align — these are the structural resonance points.

Note: 29 and 31 are twin primes — the only twin prime pair
in this range where √2 and √3 agree.


What the filter reveals

√2 — binary geometry (45°), irregular structure
√3 — ternary geometry (60°), regular structure
q  = √2 + √3 — mixed, √3 dominant

XOR at prime positions shows exactly where the asymmetry
between binary and ternary structures manifests.

This is a structural filter, not an arithmetic one.
It does not search for prime digits — it searches for places
where the prime-indexed structure of √2 and √3 diverges.


Connection to the residual

The residual q − π = 0.004671716... is the global measure
of the difference between q (full twist) and π (closure).

The XOR filter at prime positions is the local map
of the same difference — showing where it appears digit by digit.

Both describe the same ρ (defect):
the information that does not pass through the π filter.


Open question

Why do positions 29 and 31 (twin primes) produce XOR = 0?
Is this a structural property of twin primes in general,
or specific to √2 and √3?

This is a falsifiable question — verifiable by extending
the computation to more digits.


What requires further verification


Digit density of prime digits {2,3,5,7} in √2, √3, q
(results were unstable across different parsing methods in this session)
Claimed values: √2 ≈ 36%, √3 = 50%, q ≈ 48%
— these require independent numerical confirmation
