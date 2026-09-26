# Wynik — orbita prądów silnika α–β, Paderborn, v0.1 (2026-09-26): H1 i H2 NOT SUPPORTED

Pre-rejestracja: `PREREG_PADERBORN_CURRENT_ORBIT_v0.1.md` (commit f81aab5, przed odczytem prądów). Liczby:
`RESULT_PADERBORN_CURRENT_ORBIT_v0.1.json`. Holdout zamrożonego podziału AI-Core nie był otwierany. Bez poprawek po zamrożeniu.

- Kontrole: syntetyczna F1 = 1,00, winding orbity zrównoważonej 6,40 (oczekiwane 6,4); negatywna średni F1 0,34 — **przeszły**.
- Macro-F1, średnio z 4 foldów „nowy warunek pracy” (losowo ≈ 0,33):
  klasyczne (wektor Parka + cechy fazowe) **0,74**; TIMDR na orbicie α–β **0,29**; TIMDR na osadzeniu jednego kanału **0,40**;
  wszystkie TIMDR 0,38; klasyczne + TIMDR 0,73; klasyczne + orbita 0,74.
- **H1 (wartość dodana): NOT SUPPORTED** — Δ = −0,005 … −0,016 we wszystkich 4 foldach.
- **H2 (prawdziwa orbita lepsza niż osadzenie): NOT SUPPORTED** — orbita 0,29 (poziom losowy) < osadzenie 0,40.

**Wniosek:** hipoteza „TIMDR widzi, gdy sygnał wiruje” nie potwierdziła się na fizycznie wirującym wektorze prądów.
Winding orbity mierzy w praktyce liczbę obrotów pola (prędkość), która po standaryzacji w obrębie warunku nie niesie
informacji o łożysku; crossing orbity też nie. Klasyczna metoda wektora Parka działa (0,74) i TIMDR nic do niej nie dodaje.
