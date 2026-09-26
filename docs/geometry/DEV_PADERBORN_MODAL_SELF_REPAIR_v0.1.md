# Rozwój (nie test formalny) — samonaprawiający się model modalny na Paderborn, 2026-09-27

Kod: `core/real_paderborn_self_repair.py`, konstrukcja: `docs/theory/TIMDR_Modal_Self_Repair.md` (parametry jak tam,
niezmieniane). Dane rozwojowe: pomiary 1–5, 15 łożysk, 5 foldów łożysk (jak test sita).

| Zestaw | macro-F1 |
|---|---|
| sito Q (model nominalny) | **0,687** |
| sito przy naprawionej prędkości (QR) | 0,600 |
| same cechy naprawy (REP: przesunięcie, jakość przed/po, przyrost, hipoteza) | 0,582 |
| Q + REP | 0,615 |
| QR + REP | 0,605 |

Mediana naprawy |s − 1|: zdrowe 0,65%, bieżnia zewnętrzna 0,42%, wewnętrzna 0,82%; mediana przyrostu jakości
synchronizacji ≈ 0.

**Wniosek rozwojowy.** Stanowisko Paderborn utrzymuje prędkość napędem (1500 / 900 obr/min), więc model nominalny jest
już zsynchronizowany: samonaprawa nie ma czego naprawiać, a drobne „naprawy” gonią szum i pogarszają sito (0,60 wobec 0,69).
Cechy naprawy same niosą informację (0,58 — poziom klasycznych cech; głównie jakość synchronizacji i wybór hipotezy),
ale nie dodają jej do sita. Rezerwa 16–20 nieużyta.

**Gdzie samonaprawa powinna mieć znaczenie:** maszyny o zmiennej lub niepewnej prędkości (rozruch, wybieg, turbiny
wiatrowe, napędy bez regulacji), gdzie model nominalny jest rozstrojony — test wymaga takich danych.
