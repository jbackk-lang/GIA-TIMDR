# Wynik — topologia TIMDR uzupełnia klasyczne cechy drgań, Paderborn, v0.1 (2026-09-26): SUPPORTED

Pre-rejestracja: `PREREG_PADERBORN_VIBRATION_COMPLEMENT_v0.1.md` (commit f17ad16, przed obliczeniem cech). Liczby:
`RESULT_PADERBORN_VIBRATION_COMPLEMENT_v0.1.json`. Bez zmian po zamrożeniu. Holdout podziału AI-Core nieotwierany.
Kontrole: pozytywna F1 1,00, negatywna 0,25 — przeszły. Sufit nie wystąpił (klasyczne ≥ 0,97 w 0 z 4 warunków).

**Kryterium główne — w obrębie warunku pracy** (uczenie na pomiarach `train`, test na innych pomiarach `calibration`
tego samego warunku; macro-F1, 3 klasy):

| Warunek | klasyczne (4 cechy) | TIMDR (3 cechy topologii) | klasyczne + TIMDR | zysk |
|---|---|---|---|---|
| N15_M07_F10 | 0,81 | 0,94 | **1,00** | +0,19 |
| N09_M07_F10 | 0,78 | 0,79 | **0,86** | +0,09 |
| N15_M01_F10 | 0,96 | 0,92 | **0,99** | +0,03 |
| N15_M07_F04 | 0,91 | 0,90 | **0,97** | +0,06 |

Średni zysk +0,091, dodatni w 4/4 warunkach → **SUPPORTED**. Po fakcie (bootstrap po 48 pomiarach testowych,
`POSTHOC_PADERBORN_VIBRATION_COMPLEMENT_v0.1.json`): 95% CI średniego zysku [+0,051; +0,126], zysk ≤ 0 w 0 z 2000 prób.

Opisowo, przeniesienie na nowy warunek: klasyczne 0,92 / 0,65 / 0,90 / 0,85, klasyczne + TIMDR 0,98 / 0,79 / 0,98 / 0,99;
sam TIMDR przy zmianie warunku słaby (0,30–0,47).

**Co to znaczy.** Pierwsze pre-rejestrowane potwierdzenie z góry zapisanej hipotezy (z SEU gearset) na innej maszynie:
trzy metryki topologii TIMDR (winding, crossing, phase winding) niosą informację o uszkodzeniu łożyska, której nie mają
klasyczne cechy statystyczne, i razem z nimi poprawiają rozpoznanie. Sam TIMDR nie zastępuje klasycznych cech.

**Granice:** jedno łożysko na klasę i sztuczne uszkodzenia EDM (nie naturalne); kanał drgań był wcześniej czytany w AI-Core
(inne cechy); baseline to 4 proste cechy, nie pełna analiza obwiedni. Kolejny krok: Paderborn z uszkodzeniami naturalnymi
i kilkoma łożyskami na klasę oraz baseline z widmem obwiedni.
