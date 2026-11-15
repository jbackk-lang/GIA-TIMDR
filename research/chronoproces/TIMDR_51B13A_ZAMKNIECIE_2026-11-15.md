# TIMDR / Chronoproces — formalne zamknięcie 51B.13a

Data: 2026-11-15
Status: checkpoint zatwierdzający zakres twierdzeń i problemów otwartych; punkt startowy 51B.13b.
Gałąź badań: geometria informacyjna, GIA-TIMDR.

## Twierdzenie 51B.13a — informacyjna istotność chronologii

Rozpatrujemy rodzinę C_n złożoną z n rozłącznych kontenerów, każdy zawiera dokładnie jedno wystąpienie typu A lub B. Ciągi typów mają postać b∈{0,1}^n.

Sygnatury:
R_A = {Contains, Type}
R_B = {Contains, Type, Prec}
R_A ⊊ R_B.

Prec jest porządkiem chronologicznym kontenerów. Izomorfizmy zachowują wszystkie symbole rozpatrywanej sygnatury.

Wtedy:
|C_n/≅_{R_A}| = n+1,
|C_n/≅_{R_B}| = 2^n.

Dowód: bez Prec kontenery można permutować, więc klasa zależy wyłącznie od liczby kontenerów typu A (0,...,n). Z Prec porządek liniowy wymusza zachowanie pozycji, zatem każda z 2^n sekwencji A/B stanowi odrębną klasę.

Status: DOWIEDZIONE dla zdefiniowanej rodziny, przy zachowaniu predykatu Type. Bez Type formuła n+1 nie wynika z samego Contains.

Wniosek: Prec jest informacyjnie istotna względem przejścia R_A -> R_B. Istnieją procesy izomorficzne po usunięciu Prec, ale nieizomorficzne po jej dodaniu (dla n≥2). Nie dowodzi to pierwotności Prec ani jej przynależności do każdego możliwego rdzenia TIMDR.

## Robocza ontologia

Kandydaci:
- Next(a,b): bezpośrednie następstwo zdarzeń; do rozstrzygnięcia, czy chodzi o faktyczne następstwo wystąpień, czy krawędź możliwej dynamiki.
- Contains(a,b): zawieranie/hierarchia; do rozstrzygnięcia, czy relacja bezpośrednia czy przechodnia.
- Attr(a)=(MIN(a),MAX(a),Delta t(a)): lokalne atrybuty; MIN≤MAX, Delta t>0; nie zakładamy Delta t=MAX−MIN bez dodatkowego aksjomatu.
- Prec(a,b): chronologia globalna; status otwarty.

Jeżeli Next jest bezpośrednim następstwem na skończonym śladzie liniowym, Prec jest jego dodatnim domknięciem przechodnim i jest odtwarzalna. Jeżeli Next opisuje tylko możliwe przejścia, Prec nie musi być odtwarzalna. Odtwarzalność grafowa nie jest automatycznie definiowalnością pierwszego rzędu.

## Definicja rdzenia i test minimalności — program 51B.13b

Dla ustalonej klasy procesów C i pełnej sygnatury R_full szukamy R_core⊆R_full takiej, że dla dowolnych C1,C2∈C:
C1≅_{R_core}C2  iff  C1≅_{R_full}C2.

Minimalność inkluzyjna: dla każdego R∈R_core istnieją C1,C2∈C:
C1≅_{R_core\{R}}C2,
ale
C1 nie≅_{R_core}C2.

To dowodzi niezbędności symbolu w wybranym rdzeniu, nie jego ontologicznej pierwotności. Rdzeń minimalny inkluzyjnie może nie być jedyny.

## Bilans badań 51B

1. Sama geometria pierwotna nie wyznacza ogólnie historii zależnej dynamiki H.
2. Minimalizacja względem przyszłych obserwacji prowadzi do S_H i grafu prognostycznego G_H.
3. G_H nie wyznacza ogólnie pełnej geometrii relacyjnej.
4. Zachowanie relacji i przejść prowadzi do ilorazu S_Phi, zależnego od wybranej sygnatury.
5. Koszt geometrii eta może być nieograniczony w rodzinach bez ograniczeń strukturalnych.
6. Pamięć operacyjna i archiwalna mają różne wymagania; lokalna kompresowalność nie implikuje pełnej rekonstrukcji.
7. Identyfikowalność zależy od sygnatury i poziomu rekonstrukcji (oznaczona vs do izomorfizmu).
8. Prec jest informacyjnie istotna w rodzinie 51B.12, lecz jej status jako relacji pierwotnej TIMDR pozostaje nierozstrzygnięty.

## Następny etap

51B.13b: zamrozić semantykę Next/Contains/Attr/Prec, określić R_full i klasę dopuszczalnych Chronoprocesów, a następnie konstruować świadków niezbędności i badać redundancje relacyjne. Dopiero po tym przypisywać kanoniczne znaczenie eta_{R_core}, kappa_{R_core}, kappa^{iso}_{R_core}.
