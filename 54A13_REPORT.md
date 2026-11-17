# 54A.13 — Alarmy zmian reżimu a kompresja

Dwa syntetyczne strumienie po 32768 bajtów: zmiany regularne co 512 bajtów i nieregularne co 300–800 bajtów. Generatory lag 1/3/64 z 2% zakłóceń. Porównano gzip, adaptacyjny EWMA, alarm błędu oraz wieloskalowy wybór predyktora. Reszty kodowano modulo 256 i gzip level 9 jednym strumieniem. Bezstratne dekodowanie zweryfikowane. Nie uwzględniono nagłówków ani kosztu przekazania alarmów.

| Dane | Granice | gzip | adaptacyjna | wieloskalowa | alarmy błędu: trafienia / fałszywe | alarmy wieloskalowe |
|---|---:|---:|---:|---:|---:|---:|
| regularne | 63 | 1958 | 2550 | 2642 | 57 / 70 | 0 |
| nieregularne | 55 | 1756 | 2318 | 2392 | 48 / 53 | 0 |

Alarm przypisano do granicy w oknie od -64 do +128 bajtów, z dopasowaniem jeden-do-jednego. Wczesne alarmy (10 i 6) mogą być przypadkowe; nie dowodzą przewidywania. Detektor używa aktualnego błędu. Alarmy nie sterowały kodowaniem. Wieloskalowy wariant nie wyzwolił alarmów przy ustalonym progu.

Wniosek: brak przewagi kompresyjnej, dużo fałszywych alarmów. To prototyp inspirowany wieloskalowością, a nie pełny Chronoproces TIMDR.

Lokalny kod: 54A13_CHANGE.py.
