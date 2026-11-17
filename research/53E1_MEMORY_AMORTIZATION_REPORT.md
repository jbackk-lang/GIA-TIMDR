# 53E.1 — amortyzacja kosztu dzięki pamięci

Data: 2026-11-17. Uruchomiono lokalnie model `research/53E1_MEMORY_AMORTIZATION.py` w Pythonie. Status: `ACCOUNTING_MODEL_PASS`; 15 konfiguracji.

**Wielkość mierzona:** umowne jednostki operacyjne, **nie energia fizyczna w J**. Przyjęte koszty: obliczenie 100, odczyt 2, zapis 25, utrzymanie 0.05 na wpis i krok.

| Liczba kluczy | Powtórzenia | Oszczędność |
|---:|---:|---:|
| 1 | 1 | -27.00% |
| 1 | 5 | 72.96% |
| 1 | 50 | 95.451% |
| 10 | 5 | 72.555% |
| 100 | 5 | 68.505% |
| 100 | 50 | 90.5505% |

Pamięć oszczędza pracę, gdy wynik jest używany wielokrotnie. Nie ma tutaj fizycznej akumulacji energii ani dowodu, że pamięć jest magazynem energii. Model zakłada poprawność identycznego wyniku i stałe koszty.

**Dwa rozdzielne kierunki dalszych badań:**
1. Informatyczny: rzeczywisty pomiar J/operację (liczniki energii CPU/GPU, identyczna jakość przewidywania, kontrola temperatury i obciążenia), amortyzacja kosztów zapisu, odczytu i utrzymania.
2. Fizyczny: zdefiniować konkretny nośnik pamięci i mierzyć zmianę jego energii wewnętrznej po zapisie oraz energię możliwą do odzyskania. Samo zachowanie informacji nie dowodzi magazynowania odzyskiwalnej energii.

**Warunek falsyfikacji:** po uwzględnieniu wszystkich kosztów i przy stałej jakości predykcji pamięć nie daje oszczędności energii w J lub koszt utrzymania przewyższa korzyść z ponownego użycia.
