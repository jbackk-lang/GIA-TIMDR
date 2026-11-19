# RESULTS 013 — Walidacja lokalności i zależności od cech

Na rzeczywistych 16 nagraniach CWRU (800 okien po 2048 próbek) ponownie obliczono cztery cechy z RESULTS_012: RMS, crest factor, asymetrię przyrostów i maksymalną autokorelację obwiedni Hilberta dla opóźnień 30–400 próbek. Przeanalizowano 48 kandydatów (trzech na plik).

31/48 kandydatów miało wynik anomalii większy niż 2× mediana wyników czterech najbliższych sąsiednich okien (tam, gdzie dostępne). To opisowa reguła, nie test istotności.

Dominujące cechy wśród 48 kandydatów: RMS 12; crest factor 17; asymetria przyrostów 9; powtarzalność obwiedni 10.

| Nagranie | Okno (0-based) | Maks. odporny z | Dominująca cecha | Maks. z bez tej cechy | Pozycja po usunięciu cechy (1=top) |
|---|---:|---:|---|---:|---:|
| 121.mat | 36 | 6.8655 | crest factor | 1.9447 | 7 |
| 119.mat | 20 | 5.2692 | crest factor | 1.2716 | 24 |
| 97.mat | 7 | 4.6312 | asymetria przyrostów | 0.7393 | 41 |

Wniosek: topowe anomalie są lokalnymi odchyleniami, ale wykrycie jest mocno zależne od pojedynczej znanej cechy. Brak dowodu nowej informacji, pamięci po zdarzeniu lub struktury helikalnej. Ponieważ kandydatów wybrano i oceniono na tych samych oknach, nie podajemy p-value ani deklaracji niezależnej walidacji.

Następny test: czy fragmenty **po** impulsach zachowują przewidywalną informację o wcześniejszym zdarzeniu, z kontrolą energii, STFT, obwiedni, surogatów oraz podziałem nagrań na trening i test.
