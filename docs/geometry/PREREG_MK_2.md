# PREREG MK-2

## M/S ↔ K — Zero-Mode Suppression ↔ Fundamental-Mode Alignment

**Status:** prerejestracja kandydata; nie jest aksjomatem TIMDR.
**Gałęzie:** wyłącznie M/S + K.
**Cel:** niezależny test, czy zdefiniowany operator mostu wykazuje przewidywaną zmianę w warunkach tłumienia składowej średniej sygnału.

---

## 1. Obiekt M/S

Dla okna \(T\):

$$
\bar x=\frac{1}{|T|}\sum_{t\in T}x(t).
$$

\(\bar x\) jest tutaj **średnią składową sygnału M/S** i nie jest utożsamiana z kanonicznym \(Z_0\) używanym w innych konstrukcjach TIMDR.

Do operatora używana jest wartość bezwzględna:

$$
|\bar x|.
$$

W celu usunięcia jednostki amplitudy stosowana jest prerejestrowana normalizacja:

$$
\tilde x=\frac{|\bar x|}{A_{\mathrm{ref}}},
$$

gdzie \(A_{\mathrm{ref}}\) jest wyznaczane wyłącznie z prerejestrowanego zbioru tła i pozostaje zamrożone dla całego testu.

**Decyzja prerejestracyjna:** \(A_{\mathrm{ref}}\) nie może być dobierane na podstawie danych testowych ani wyników separacji.

---

## 2. Obiekt K

Z dostępnego widma/modalnego zbioru kandydatów wybierane są wyłącznie składowe:

* niebędące DC,
* spełniające prerejestrowane kryterium minimalnej energii/amplitudy,
* nieoznaczone jako artefakty zgodnie z wcześniej ustaloną procedurą jakościową.

Pierwsza istotna modalność:

$$
\omega_1=
\min\{\omega_k:\omega_k\ \text{spełnia wszystkie prerejestrowane kryteria}\}.
$$

Żadne kryterium wyboru \(\omega_1\) nie może zostać zmienione po obejrzeniu wyniku głównego.

---

## 3. Operator mostu

Kandydat definiuje:

$$
\boxed{
M_{M/S\leftrightarrow K}
=
\frac{\omega_1}{\tilde x+\epsilon}
}
$$

gdzie:

$$
\epsilon>0
$$

jest stabilizatorem w tej samej bezwymiarowej skali co \(\tilde x\).

Operator nie jest interpretowany przyczynowo na etapie prerejestracji.

### Przewidywanie kierunkowe

Jeżeli:

$$
\tilde x\rightarrow0,
$$

to:

$$
M_{M/S\leftrightarrow K}\rightarrow
\frac{\omega_1}{\epsilon},
$$

czyli przy pozostałych warunkach porównywalnych operator rośnie.

Jest to **predykcja konstrukcji operatora**, a nie jeszcze twierdzenie fizyczne o systemie.

---

## 4. Hipoteza główna

**H1:** okna charakteryzujące się prerejestrowanym tłumieniem składowej średniej M/S będą wykazywały większą wartość \(M_{M/S\leftrightarrow K}\) niż odpowiadające im okna kontrolne bez tego tłumienia.

**H0:** rozkład operatora w grupie tłumienia nie różni się od rozkładu w odpowiedniej grupie kontrolnej w zakresie określonym przez prereg.

Test jest jednostronny zgodnie z kierunkiem H1.

---

## 5. Kontrola pozytywna

Kontrola pozytywna ma zawierać syntetyczne realizacje, w których:

1. składowa średnia sygnału jest kontrolowanie tłumiona,
2. istotna modalność \(\omega_1\) pozostaje obecna,
3. zależność pomiędzy tłumieniem \(\tilde x\) a wzrostem względnego znaczenia \(\omega_1\) jest określona **przed** analizą.

Kontrola pozytywna służy do wykazania, że implementacja operatora potrafi wykryć skonstruowany efekt.

Nie jest traktowana jako dowód działania mostu na danych rzeczywistych.

---

## 6. Kontrola negatywna

Kontrola negatywna ma zachować:

* taki sam schemat generowania szumu,
* taki sam zakres amplitud,
* taki sam sposób wyznaczania \(\bar x\),
* taki sam sposób wyznaczania \(\omega_1\),

ale bez prerejestrowanego sprzężenia pomiędzy tłumieniem średniej a modalnością.

Jeżeli kontrola negatywna wykazuje podobny efekt jak pozytywna, interpretacja mostu zostaje osłabiona lub odrzucona.

---

## 7. Liczebność

Formalny test główny:

$$
N\ge30
$$

niezależnych realizacji/okien na klasę testową.

Warunki początkowe oraz prerejestrowane nuisance-parameters mają być losowane niezależnie pomiędzy realizacjami.

Mała eksploracja \(N<30\) nie może zostać przedstawiona jako walidacja formalna.

---

## 8. Baseline i kalibracja

Wszystkie progi oraz parametry zależne od skali, w szczególności:

* \(A_{\mathrm{ref}}\),
* próg istotności modalnej,
* kryterium odrzucenia artefaktów,
* \(\epsilon\),

muszą być określone z danych tła lub z prerejestrowanej procedury syntetycznej **przed testem głównym**.

Baseline nie może być dostrajany tak, aby zwiększyć separację grup.

---

## 9. Metoda statystyczna

Podstawowym testem porównującym grupę badaną i kontrolną jest:

$$
\text{Mann–Whitney U}.
$$

Raportowany obowiązkowo jest również rozmiar efektu:

$$
r.
$$

Samo \(p\) nie jest wystarczające.

W przypadku wielu niezależnych okien/porównań stosowana jest jedna prerejestrowana korekta Bonferroniego.

Jedno główne uruchomienie analizy jest rozstrzygające.

---

## 10. Warunek interpretacyjny

Wynik może być uznany za zgodny z H1 wyłącznie wtedy, gdy jednocześnie:

1. kierunek efektu jest zgodny z prerejestrowaną hipotezą,
2. test Mann–Whitneya spełnia prerejestrowane kryterium,
3. rozmiar efektu \(r\) jest raportowany,
4. kontrola pozytywna działa,
5. kontrola negatywna nie wykazuje analogicznego efektu,
6. liczba kwalifikujących się obserwacji zapewnia wymaganą moc testu.

Wysokie \(p\) przy zerowej liczbie zdarzeń kwalifikujących się do analizy nie będzie interpretowane jako dowód braku efektu.

---

## 11. Test wielodomenowy

Test real-world zostanie wykonany na trzech niezależnych domenach wybranych przed obejrzeniem wyników.

Dla każdej domeny stosowany będzie ten sam prerejestrowany pipeline:

$$
x(t)
\rightarrow
\bar x
\rightarrow
\tilde x
$$

oraz

$$
x(t)
\rightarrow
\omega_1
\rightarrow
M_{M/S\leftrightarrow K}.
$$

Wyniki domenowe będą raportowane osobno.

Sukces w jednej domenie nie będzie automatycznie uogólniany na pozostałe.

---

## 12. Kryterium zakresu

Nawet jeśli test syntetyczny przejdzie, wynik będzie klasyfikowany jako:

**„poprawność konstrukcji/operatora na kontroli syntetycznej”**

i nie będzie automatycznie oznaczał:

**„użyteczność mostu na danych rzeczywistych”.**

Jeżeli działanie wystąpi tylko w części domen lub tylko w określonym zakresie amplitud/częstotliwości, zakres ważności zostanie odpowiednio zawężony.

---

## 13. Zasada anty-tuningu

Po rozpoczęciu testu nie wolno zmieniać:

* definicji \(\bar x\),
* \(A_{\mathrm{ref}}\),
* definicji \(\omega_1\),
* progów istotności,
* \(\epsilon\),
* kierunku hipotezy,
* kryterium statystycznego,

na podstawie uzyskanych wyników.

Zmiana konstrukcji po wyniku oznacza rozpoczęcie nowej prerejestracji.

---

## 14. Status końcowy

Przed uruchomieniem testu:

**Candidate M/S↔K #2 — preregistered, not established.**

Po teście możliwe są wyłącznie klasyfikacje:

* zgodny z prerejestrowaną hipotezą,
* częściowy,
* wynik negatywny,
* niediagnostyczny z powodu niewystarczającej liczby zdarzeń.

Żadna z tych klasyfikacji nie tworzy automatycznie nowego aksjomatu.

## 15. Implementacja referencyjna

```python
def mc_ms_k(zero_mode, omega_1, eps):
    """
    Candidate M/S ↔ K #2:
    Zero-Mode Suppression ↔ Fundamental-Mode Alignment.

    zero_mode : |x̄| po prerejestrowanej normalizacji
    omega_1   : pierwsza istotna modalność K
    eps       : prerejestrowany stabilizator w tej samej skali co zero_mode
    """
    if zero_mode < 0:
        raise ValueError("zero_mode must be non-negative")
    if omega_1 < 0:
        raise ValueError("omega_1 must be non-negative")
    if eps <= 0:
        raise ValueError("eps must be strictly positive")

    return omega_1 / (zero_mode + eps)
```

**Ten kod implementuje kandydata. Nie stanowi sam przez się jego walidacji.**
