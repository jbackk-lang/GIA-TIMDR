# PREREG — most Hell Bridge Test Arena: kotwica modalna K + kształt modu, v0.1

Data: 2026-09-27. Kod: `core/hbta_modal_anchor.py`. Zamrożone przed liczeniem cech na rejestracjach UDS_02 i DS1–DS8.
Oglądane przed zamrożeniem: struktura pliku, atrybuty, widmo rejestracji uczącej UDS_01 (wybór 8 kotwic).

## Dane
Svendsen i in., Hell Bridge Test Arena (stalowy kratownicowy most kolejowy, Norwegia), Zenodo 10.5281/zenodo.14028239,
plik `data_100Hz.h5`. Rejestracje „Noise mode” (szum 1–100 Hz z wibratora, pozycja P2, pionowo), 59 akcelerometrów (z),
~950 s. Stany: UDS (2 rejestracje: 2020-09-27 i 2020-09-22), DS1–DS8 (2020-09-27/28). Typy uszkodzeń wg Svendsen i in. 2022:
DS1–2 połączenia podłużnica–poprzecznica, DS3–4 poprzeczki podłużnic, DS5–7 połączenia stężeń wiatrowych, DS8 połączenie
poprzecznica–dźwigar główny. Opublikowane: najlepiej wykrywane DS1, DS2, DS8; najtrudniej stężenia i poprzeczki.

## Reguła wykonalności (przed testem)
Wymuszenie szumem → reżim pola (D wysokie) → droga przez linie K przy kotwicy. N_cyk w oknie 60 s: 400–1900 (mody 6,9–32 Hz).
Kotwica: śledzona (samokorekta ±4% w każdym oknie). Przewidywanie: droga wykonalna.

## Podział
Uczenie: okna 60 s z UDS_01. Test nieuszkodzony: UDS_02 (inny dzień — kontrola fałszywych alarmów od otoczenia).
Test uszkodzony: DS1–DS8. Miara: AUC (okna UDS_02 vs okna DSk), detektor kNN (k = 3) jak LANL v0.1.

## Hipotezy
- **H1:** średnie AUC(TIMDR) po DS1–DS8 ≥ 0,90.
- **H2 (nie gorzej niż klasyka):** średnie AUC(TIMDR) ≥ średnie AUC(AR) − 0,02.
- **H3 (fizyka zgodna z publikacją):** średnie AUC(TIMDR) dla DS1, DS2, DS8 > dla DS3–DS7.
- **H4 (fałszywe alarmy):** odsetek okien UDS_02 ponad progiem 95% (LOO na uczeniu) ≤ 0,20.
Jedno uruchomienie; wynik do README niezależnie od werdyktu.
