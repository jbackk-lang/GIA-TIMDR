# 54A.2 — Helix-Lock × pamięć różnicowa: test kontrolny

Data 2026-11-17. Przejrzano `jbackk-lang/Helix-Lock`: README, `helix_pro/cipher.py`, `docs/TIMDR_INTEGRATION.md` i `helix_pro/airp_history_memory.py`.

**Ustalenie architektoniczne:** Helix-Lock używa gzip przed AES-256-GCM w formacie nazwanym. TIMDR jest na razie projektem integracji diagnostycznej i historii zdarzeń; AIRPHistoryMemory przechowuje wyłącznie podsumowania metadanych, nie payloady. Nie jest gotowym kompresorem TIMDR.

**Wykonany eksperyment lokalny:** Python, seed 5402, 128 bloków po 1024 bajty; wariant badawczy: pierwszy blok jako anchor, XOR względem anchor, zlib na każdym residualu, długości zapisane w nagłówkach. Pełne bezstratne roundtrip sprawdzone asercją. To **nie** jest wykonanie właściwego operatora TIMDR ani kodu Helix-Lock.

| Dane | gzip (bajty) | Anchor+XOR+zlib (bajty) |
|---|---:|---:|
| podobne bloki, 8 losowych zmian/b | 5247 | 9928 |
| identyczne | 1850 | 3718 |
| losowe | 131130 | 133004 |

**Wniosek:** wariant anchor+XOR przegrywa z gzip we wszystkich trzech konfiguracjach. AES-GCM nie był uruchamiany; jego narzut nie zmienia porównania payloadów o tej samej długości nagłówka, ale pełna integracja formatowa wymaga osobnego testu. Nie wolno przedstawiać tego jako negatywnego testu operatora TIMDR.

**Dalszy warunek wejścia:** wskazać konkretny operator TIMDR, jego wejście/wyjście, odwracalność i koszty metadanych. Dopiero wtedy porównać rzeczywistą implementację z gzip/zstd na holdoucie. Nie zmieniać AES ani polityk AIRP.
