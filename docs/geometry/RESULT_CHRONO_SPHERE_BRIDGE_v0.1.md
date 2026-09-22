# Wynik: chrono_sphere_bridge v0.1 — ODRZUCONY na etapie kontroli syntetycznej

> Zgodnie z `PREREG_CHRONO_SPHERE_BRIDGE_v0.1.md` §5: jeśli kontrola
> pozytywna/negatywna nie przejdzie zgodnie z przewidywaniem —
> zatrzymanie, zgłoszenie na etapie kontroli, BEZ dotykania danych
> CWRU. Dokładnie to się stało tutaj. Kod: `core/chrono_sphere_bridge.py`
> (commit lokalny, patrz status repo). Uruchomione: 2026-09-22.

## Wynik bramki sanity (§5, kontrola (c))

Trzy kopie tego samego sygnału + znikomy szum (`SYN_GATE_NOISE_EPS=0.05`)
— bramka niezależności (`λ_1/Σλ<0.9`) odrzuciła **100% okien (30/30)**
na wszystkich trzech rozmiarach okna (500, 1000, 2000 próbek). Bramka
działa zgodnie z przewidywaniem — **PASSED**.

## Wynik testu głównego (§5, kontrola (a) vs (b))

| window_size | p | r (rank-biserial) | mediana (a) skok | mediana (b) szum | kierunek |
|---|---|---|---|---|---|
| 500 | 3.02e-11 | -1.000 | 0.1758 | 0.6628 | **odwrotny** |
| 1000 | 3.02e-11 | -1.000 | 0.1760 | 0.6622 | **odwrotny** |
| 2000 | 3.02e-11 | -1.000 | 0.1749 | 0.6657 | **odwrotny** |

Przewidywanie z preregu: `median(a) > median(b)` (skok kierunku daje
wyższe `Ω_win` niż czysty szum). **Wynik: dokładnie odwrotny, ze
skrajnie silnym, idealnie stabilnym efektem (`r=-1.000` na wszystkich
trzech rozmiarach okna)** — nie jest to słaby/niejednoznaczny wynik,
tylko jednoznacznie sprzeczny z przewidywaniem, stabilny między
rozmiarami okna.

## Diagnoza mechanizmu (uczciwa, nie post-hoc retuning metryki)

Kontrola negatywna (b): każda próbka to świeży niezależny szum na
wszystkich trzech kanałach — kierunek `u(t)` zmienia się losowo na
KAŻDYM kroku, dając dużo małych, ale ciągłych `ω(t)` przez cały czas
trwania okna.

Kontrola pozytywna (a), zdefiniowana w v0.1: JEDEN skok w połowie okna
(trwały offset dodany do jednego kanału od połowy okna do końca). Po
skoku sygnał "zamarza" w nowym kierunku — duży, stały offset dominuje
nad szumem, więc `u(t)` przestaje się poruszać. Jeden duży `ω(t)` w
momencie skoku, otoczony DŁUGIM odcinkiem niemal zerowej prędkości
kątowej, ale z WYSOKĄ wagą `r(t)` (offset zwiększa też promień). Ważona
średnia `Ω_win` jest ciągnięta w dół przez ten długi, spokojny,
wysoko ważony odcinek.

**Wniosek**: `Ω_win`, tak jak zdefiniowane w v0.1, mierzy "jak bardzo
CIĄGLE drga kierunek, ważone chwilową siłą sygnału" — nie "czy
zdarzył się gdziekolwiek pojedynczy duży skok". Konstrukcja metryki
nie jest zła sama w sobie — generator kontroli pozytywnej v0.1 (jeden
skok + zamrożenie) był złym modelem tego, co metryka faktycznie
wykrywa. To jest wynik na temat NIEDOPASOWANIA profilu kontroli do
metryki, nie na temat samej metryki będącej bezużyteczną.

## Status

**v0.1 ODRZUCONY** na etapie kontroli syntetycznej — nie uruchomiono
żadnego testu na danych CWRU (zgodnie z protokołem, ta sama dyscyplina
co `chrono_cone_bridge` v0.3). Kod, generatory i wyniki liczbowe
zostają w repozytorium jako część historii, NIE nadpisane ani
przemianowane po fakcie.

Decyzja właściciela projektu: nie poprawiać generatora post-hoc, tylko
zaprojektować **v0.2** z jawnie innym, z góry zdefiniowanym profilem
kontroli pozytywnej (powtarzające się/cykliczne zaburzenie kierunku,
bliższe fizyce uszkodzenia łożyska — powtarzające się uderzenia, nie
jednorazowy krok) — patrz `PREREG_CHRONO_SPHERE_BRIDGE_v0.2.md`.
