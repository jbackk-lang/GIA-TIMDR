# Wynik — SEU gearset, potwierdzenie „klasyczne + topologia TIMDR”, v0.2 (2026-09-26): MIESZANY

Pre-rejestracja: `PREREG_SEU_GEARSET_CONFIRM_v0.2.md` (commit 93ccda3, przed pobraniem danych). Liczby:
`RESULT_SEU_GEARSET_CONFIRM_v0.2.json`. Bez zmian po zamrożeniu. Kontrole przeszły (negatywna F1 0,20 / 0,10; bramka 6/6).

| macro-F1 (5 klas, losowo 0,2) | klasyczne B | TIMDR T | B + T | B + topologia |
|---|---|---|---|---|
| nowy warunek 20_0 → 30_2 | 0,52 | 0,46 | **0,57** | 0,56 |
| nowy warunek 30_2 → 20_0 | 0,59 | 0,37 | **0,60** | 0,63 |
| w obrębie warunku 20_0 (opisowo) | 0,70 | 0,72 | **0,86** | 0,83 |
| w obrębie warunku 30_2 (opisowo) | 0,66 | 0,68 | **0,80** | 0,82 |

Zysk B+T nad B przy zmianie warunku: +0,052 i +0,005 (średnio 0,029 < 0,05) → **MIESZANY** wg kryterium.

**Co to znaczy.** Na danych, których wcześniej nie oglądaliśmy, dołożenie cech TIMDR do klasycznych ani razu nie
pogorszyło wyniku, ale przy zmianie warunków pracy zysk jest mały i niestabilny — hipoteza z v0.1 (0,95 vs 0,66) była
w dużej mierze dopasowaniem. W obrębie tego samego warunku (opisowo, poza kryterium) zysk jest duży i spójny (+0,16 / +0,14),
a TIMDR sam jest na poziomie klasycznych cech — to pierwszy wynik, w którym topologia TIMDR wnosi informację
komplementarną do klasycznej na świeżych danych. Potwierdzenie wymaga osobnej pre-rejestracji z tym kryterium jako głównym
i innej maszyny.
