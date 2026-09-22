# Wynik: chrono_modal_geometry_bridge v0.1 — NIESTABILNY na etapie kontroli syntetycznej, zatrzymany przed danymi CWRU

> Zgodnie z `PREREG_CHRONO_MODAL_GEOMETRY_BRIDGE_v0.1.md` §7: dane
> CWRU dotykane WYŁĄCZNIE, jeśli §5.2 da "jednoznaczny, stabilny
> kierunek". Nie dał — zatrzymanie tutaj. Kod:
> `core/chrono_modal_geometry_bridge.py`. Uruchomione: 2026-09-22.

## Sanity implementacji (przed kontrolami)

Wzory Freneta-Serreta zweryfikowane analitycznie na helisie
`γ(t)=(a·cos t, a·sin t, b·t)`, `a=2.0`, `b=0.5` — wynik numeryczny
zgodny z wartością analityczną `κ=a/(a²+b²)=0.470588`,
`τ=b/(a²+b²)=0.117647` co do 6 cyfr znaczących. Krzywizna/skręt są
niezmiennicze względem parametryzacji (indeks próbki vs czas fizyczny),
więc decymacja obwiedni nie zniekształca wyniku.

## Wynik bramki sanity (c)

100% odrzuconych okien (30/30) na wszystkich trzech rozmiarach okna —
**PASSED**.

## Wynik testu głównego (a: dominujący rezonans, vs b: tło) — DWUSTRONNY

| window_size | κ: p | κ: r | κ: kierunek | κ: SUPPORTED? | τ: p | τ: r |
|---|---|---|---|---|---|---|
| 250 | 0.0083 | -0.398 (średni) | saturacja | **tak** | 0.297 | -0.158 |
| 500 | 0.1761 | -0.204 (mały) | — | nie | 0.830 | -0.033 |
| 1000 | 0.0436 | -0.304 (średni, na granicy) | saturacja | **tak** (granica) | 0.446 | -0.116 |

`τ_win` bez istotnego efektu na żadnym rozmiarze okna — spójnie zerowy
wynik, nie niestabilny, po prostu brak wykrywalnego efektu na skręcie.

## Interpretacja

`κ_win` NIE jest stabilne w sensie ustalonym w tym projekcie (istotność
i kierunek zgodne na 2/3 rozmiarów okna, nieistotne na jednym) — to
JEST inny profil niż `chrono_sphere_bridge` (tam `r=-1.000` na
wszystkich trzech oknach, efekt idealny i totalny). Tutaj, gdy efekt
jest istotny, kieruje się konsekwentnie w stronę "saturacji"
(dominujący rezonans → NIŻSZA krzywizna, nie wyższa) — czyli TA SAMA
JAKOŚCIOWA hipoteza konkurencyjna z PREREG §5.2 ("dominacja spłaszcza
geometrię") ponownie wygrywa nad hipotezą "dominacja wzbogaca
geometrię", ale efekt jest znacznie słabszy i mniej jednoznaczny niż
przy sferze — nie idealna separacja, tylko średni rozmiar efektu,
niestabilny między oknami.

**To NIE jest ani czyste potwierdzenie mechanizmu saturacji (bo brak
stabilności), ani czyste "brak efektu" (bo 2/3 okien istotne, w tym
samym kierunku, nie losowo naprzemiennym)** — uczciwie NIESTABILNY,
zgłoszony jako taki, bez podciągania w żadną stronę.

## Status

**v0.1 ZATRZYMANY na etapie kontroli — dane CWRU NIE zostały
dotknięte**, zgodnie z regułą preregu wymagającą jednoznacznego,
stabilnego kierunku przed przejściem do danych realnych. Trzeci
niezależny sygnał (po `chrono_cone` v0.1-v0.3 i `chrono_sphere` v0.1-
v0.2) sugerujący, że konstrukcje oparte na "jeden wymiar zaczyna
dominować → miara geometryczna oparta na kierunku/krzywiźnie spada"
mają systematyczną tendencję w tę stronę, choć siła tej tendencji
różni się mocno między konstrukcjami (od idealnej separacji przy
sferze do słabej/niestabilnej tutaj). `τ` pozostaje bez wykrytego
efektu w tej konstrukcji.
