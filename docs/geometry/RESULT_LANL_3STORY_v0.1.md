# Wynik — TIMDR na drganiach budynku (rama trzykondygnacyjna LANL), v0.1 (2026-09-26)

Pre-rejestracja: `PREREG_LANL_3STORY_v0.1.md` (commit e2afd26). Liczby: `RESULT_LANL_3STORY_v0.1.json`.
**Poprawka techniczna po zamrożeniu:** w kontrolach cechy liczyły się osobno dla każdej nazwy cechy (41× za dużo pracy),
co przekroczyło limit czasu przed zapisaniem czegokolwiek; zmieniono tylko to, by liczyć je raz na pomiar.

- Kontrole: pozytywna AUC 1,00 (impulsy), negatywna 0,47 — **przeszły**.
- **H-główna (wartość dodana): INCONCLUSIVE (sufit)** — klasyczne cechy (AR(5), kurtoza, crest) AUC 0,995 / 0,993;
  z TIMDR 0,992 / 0,994 (zysk −0,003 / +0,001). **TIMDR sam: AUC 0,45 / 0,53 — poziom losowy.**
- **H-ciężkość:** B ρ = 0,97; T ρ = 0,50 (p = 0,0002, formalnie na progu SUPPORTED); BT ρ = 0,98.
- **Sztywność/masa vs uszkodzenie (alarmy przy progu 95%):** B alarmuje na 90–100% pomiarów uszkodzonych i 0–20% pomiarów
  ze zmianą sztywności; T alarmuje na 0% uszkodzonych (poza stanem 14: 15%).

**Wniosek:** na drganiach budynku cechy TIMDR nie wykrywają uszkodzenia (nieliniowości zderzaka) i nic nie dodają do
klasycznych cech SHM, które rozwiązują to zadanie niemal perfekcyjnie. Słaba zależność od ciężkości (ρ = 0,50) jest jedynym
śladem sygnału. Test wartości dodanej jest formalnie nierozstrzygnięty z powodu sufitu baseline'u, ale sam TIMDR na poziomie
losowym zamyka ten kierunek dla tej klasy problemów.
