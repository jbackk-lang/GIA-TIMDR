# TIMDR — pięć własności fal (2026-11-14)

Uruchomiono skrypt `wave_properties_timdr.py`, seed 202611140807, fs=200 Hz, 10 s, nośna f=7 Hz. Pełny skrypt i stdout są dostępne jako pliki rozmowy. GitHub zawiera reprodukowalny skrypt o tych samych obliczeniach.

## 1. Interferencja
Dwie sinusoidy jednostkowe 7 Hz. Różnica faz 0°,60°,120°,180° daje amplitudy sumy 2.0,1.732051,1.0,0.0; RMS 1.414214,1.224745,.707107,0.0. Wynik wynika ze znanej superpozycji.

## 2. Dudnienia
Dwie sinusoidy 7 Hz i 7+Δf. Dla Δf=.5,1,2 Hz zmierzony z obwiedni Hilberta medianowy okres dudnień 2,1,.5 s. Zgodne z 1/Δf.

## 3. Dyspersja
Dwie składowe (k,ω)=(2,10),(2.5,13): prędkości fazowe 5 i 5.2; prędkość obwiedni (Δω/Δk)=6. To obliczenie analityczne, nie symulacja medium dyspersyjnego.

## 4. Tłumienie i faza
Fala exp(-λt)sin(2π7t+φ), 300 losowych faz na wariant, projekcja kwadraturowa na pierwszych 2 s. MAE fazy [rad] dla (λ,σ): (0,0) 0; (0,.15) .00862; (.1,0) .00073; (.1,.15) .00895; (.3,0) .00224; (.3,.15) .01152. Niewielkie błędy nawet bez szumu przy tłumieniu są błędem metody estymacji przez projekcję na skończonym oknie.

## 5. Energia dwóch pakietów
Dwa pakiety Gaussa z nośną 7 Hz, szerokość .16 s. Energia sumy / suma energii oddzielnych pakietów dla odstępu w cyklach 0,.25,.5,1 wynosi 2,1,.04860,1.81931. Wynik zależy od nakładania się obwiedni; nie jest uniwersalną zależnością wyłącznie od fazy.

## Interpretacja TIMDR
Trójki lokalne MIN/MAX/Δt należy zachować. Dodatkowe relacje warte testowania: faza względna, częstotliwość dudnień obwiedni, prędkość fazowa i grupowa, tłumienie, koherencja i opóźnienie pakietów. Wykonane eksperymenty potwierdzają znane prawa falowe w modelach syntetycznych; nie ustanawiają nowych praw fizyki ani przewagi reprezentacji TIMDR. Następny falsyfikacyjny test: szumne mieszanki fal z automatycznymi trójkami i kontrolą FFT/STFT/Hilberta, z predykcją niezależnych przyszłych obserwacji.