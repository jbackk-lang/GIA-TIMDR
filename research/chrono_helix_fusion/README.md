# CHRONO-HELIX-FUSION (CHF) — eksperymentalna gałąź badawcza GIA-TIMDR

Status: **hipoteza / prototyp**, bez potwierdzonej przewagi nad metodami standardowymi.

## Cel
Sprawdzić, czy wspólny Chronoproces Ξ=(T,x,Γ,φ), helikalna reprezentacja sygnału i sprzężenie gałęzi M/S, G, K poprawiają wykrywanie zdarzeń, zmian reżimu i anomalii względem metod klasycznych (FFT/STFT, energia, obwiednia, falki).

CHF to gałąź **badawczo-aplikacyjna**, a nie piąta niezależnie zaksjomatyzowana gałąź formalna. Nie zmienia aksjomatów M/S, G, K ani META-DYNAMICS.

## Model roboczy
Dla sygnału rzeczywistego x(t) obliczamy sygnał analityczny a(t)=x(t)+i Hilbert(x(t)), obwiednię r(t)=|a(t)| i fazę φ(t)=unwrap(arg(a(t))). Definiujemy trajektorię:
H(t)=[r(t)cosφ(t), r(t)sinφ(t), αt].
α, normalizację, filtry i skalę czasu kalibrujemy **wyłącznie na zbiorze treningowym**.

M/S: amplituda, energia, impulsy i lokalna zmienność.
G: krzywizna, skręcenie (z kontrolą niestabilności numerycznej), prędkość i odkształcenia trajektorii H.
K: faza, częstotliwość chwilowa, koherencja i synchronizacja.
Trójwęzeł: jawne, estymowane na treningu relacje opóźnione M/S↔G, G↔K, K↔M/S; weryfikujemy, czy niosą przyrost informacji poza osobnymi gałęziami.
Möbius: opcjonalna **hipoteza topologiczna**; porównanie po okresie P i 2P samo nie dowodzi nieorientowalności. Wymaga definicji transportu orientacji i kontroli modeli dwucyklowych bez topologii Möbiusa.

## Program testów
1. Dane syntetyczne kontrolne: sinusoidy, chirpy, impulsy, przejścia, szum kolorowy, zmiany fazy, sygnały o zgodnym widmie i różnej kolejności zdarzeń.
2. Dane rzeczywiste pobierane z internetu: np. ECG z SciPy datasets, Case Western Reserve University Bearing Data Center, UCR/UEA Time Series Archive. Każdy adapter musi podać źródło, licencję/warunki użycia, datę pobrania, SHA-256, próbkę i częstotliwość próbkowania. Nie publikować dużych surowych zbiorów bez uprawnienia.
3. Porównania: (A) FFT/STFT/energia, (B) sam Chronoproces, (C) + helisa, (D) + M/S,G,K, (E) + trójwęzeł, (F) + test Möbiusa.
4. Rozdział danych po **obiekcie / pacjencie / sesji / czasie**, bez przecieku między oknami tego samego pomiaru. Kalibracja i dobór progów wyłącznie na treningu; osobny zbiór walidacyjny i zamrożony test.
5. Metryki: AUROC, AUPRC, F1 przy zamrożonym progu, false alarms/hour, opóźnienie detekcji, odporność na SNR, czas CPU i pamięć; przedziały ufności bootstrap grupowany po obiekcie. Dla zadań bez etykiet raportować wyłącznie cechy i diagnostykę, nie skuteczność detekcji.
6. Ablacje: usunięcie każdej gałęzi, permutacja czasu, losowanie fazy przy zachowaniu widma, usunięcie krawędzi trójwęzła, kontrola dwucyklowa wobec Möbiusa. Testować także prostą fuzję cech o porównywalnej liczbie parametrów.
7. Prerejestracja hipotez, kryteriów sukcesu, kosztu i protokołu przed otwarciem testu. Raportować wyniki SUPPORTED / PARTIAL / NEGATIVE / INCONCLUSIVE z pełnymi parametrami.

## Hipoteza główna
CHF osiąga dodatni, powtarzalny przyrost jakości na niezależnych testach **po uwzględnieniu kosztu obliczeniowego i po porównaniu z mocną fuzją standardowych cech**. Brak przyrostu oznacza wynik negatywny, a nie powód do zmiany metryki po teście.

## Pierwszy krok
Uruchomić `python research/chrono_helix_fusion/pilot.py` po instalacji `numpy scipy`. Skrypt pobiera publiczny zapis ECG za pośrednictwem `scipy.datasets.electrocardiogram()` (pierwsze uruchomienie wymaga internetu), oblicza cechy helisy i zapisuje raport. To **eksploracja cech**, nie test przewagi diagnostycznej.
