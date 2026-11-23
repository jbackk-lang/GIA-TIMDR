# RESULTS 012 — Nienadzorowane poszukiwanie anomalii w drganiach CWRU

2026-11-19. Lokalna analiza 16 plików MAT z rzeczywistymi drganiami łożysk; kanał DE_time, 50 niepokrywających się okien po 2048 próbek na plik, łącznie 800. Nie użyto etykiet usterek do selekcji anomalii.

Miary kontrolne: RMS, crest factor, asymetria przyrostów, maksymalna autokorelacja obwiedni Hilberta dla opóźnień 30–400 próbek. Ranking: największe bezwzględne odporne z-score wewnątrz danego nagrania.

Najsilniejsze lokalne odstępstwa: 121.mat okno 36 (6.8655), 119.mat okno 20 (5.2692), 97.mat okno 7 (4.6312).

Mediany powtarzalności obwiedni: 130–133.mat = 0.796, 0.754, 0.775, 0.768; 118–121.mat = 0.115, 0.114, 0.131, 0.133. Są to różnice dynamiki, ale mogą być klasycznym efektem znanych uszkodzeń łożysk.

**Nie ma dowodu nowego zjawiska.** Nie wykonano jeszcze pełnego CHF, surogatów IAAFT, korekty wielokrotnych porównań, walidacji niezależnych maszyn ani interpretacji informacji przechowywanej przez helisę. Częstotliwość próbkowania nie została zweryfikowana dla wszystkich plików; opóźnienia podano w próbkach.

Następny krok: weryfikacja fragmentów i sąsiednich okien, stabilność parametrów, surogaty dopasowane widmem i rozkładem amplitud, pełne CHF vs STFT, obwiednia i matrix profile.