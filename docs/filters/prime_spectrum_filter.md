# Prime Spectrum Filter  
### Jak działa filtr na liczby pierwsze i dlaczego łączy się z widmem kosmosu

> **WERYFIKACJA (audyt, sesja 2026-08-29): twierdzenia poniżej (gęstość
> cyfr pierwszych, struktura XOR na pozycjach pierwszych) zostały
> przetestowane i OBALONE — pełny audyt z liczbami w
> `prime_position_filter.md` (ten sam pomysł, pełniejszy opis) i
> `al_filter_predictions.md` (gęstość cyfr + powiązane "predictions").
> Ten plik jest niedokończonym szkicem tej samej koncepcji — nie dopisano
> tu osobnego audytu, żeby nie duplikować tych samych liczb trzy razy.**

---

## 1. Fundament: trzy liczby i ich struktury
Filtr opiera się na trzech rozwinięciach dziesiętnych:

- √2 – struktura binarna (45°), gęstość cyfr pierwszych ≈ 36%
- √3 – struktura trójkowa (60°), gęstość cyfr pierwszych = 50%
- q = √2 + √3 – struktura mieszana, gęstość ≈ 48%

√3 dominuje filtr, √2 wprowadza asymetrię.

---

## 2. Pierwsza warstwa filtra: indeksy pierwsze
Filtr nie działa na wartości cyfr, tylko na ich pozycje.

Wybieramy cyfry na pozycjach:
2, 3, 5, 7, 11, 13, 17, 19, 23…

To są „pierwsze pozycje”.

---

## 3. Druga warstwa: XOR(√2, √3)
Dla każdej pozycji pierwszej:

