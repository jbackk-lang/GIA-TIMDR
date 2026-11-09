# WYNIK: zachowanie fazy i chiralności przy transformacji sygnału do pola

**Data:** 2026-11-09  
**Status:** test syntetyczny PASS (3/3), CI run 42584118204  
**Zakres:** reprezentacja sygnału fazowego w polu; bez twierdzeń o fizycznym sprzężeniu helisy.

## 1. Pytanie testowe

Czy transformacja sygnału z fazą do regularnego pola może zachować znak skrętu, a zwykła interpolacja kąta jako skalaru może go utracić?

## 2. Metoda

Zastosowano wzorzec interpolacji Synoptyk-v3: próbki rozproszone 9×9 → regularna siatka 81×81 przez `scipy.interpolate.griddata(method="cubic")`, z uzupełnieniem poza otoczką metodą nearest.

Wygenerowano dwa pola o przeciwnym znaku chiralności:
[
\phi(x,y)=+\operatorname{atan2}(y,x),\qquad
\phi(x,y)=-\operatorname{atan2}(y,x).
]

Porównano dwie reprezentacje:
- **kontrola poprawna:** interpolacja dwóch składowych `cos(φ)` i `sin(φ)`, a następnie odtworzenie `atan2(sin,cos)`;
- **kontrola błędna:** interpolacja zawiniętego kąta `φ` jako zwykłej wartości skalarnej.

Miarą zachowania topologicznego jest liczba nawinięć (winding number) fazy na zamkniętej pętli otaczającej centrum. To test przejścia przez nieciągłość ±π.

## 3. Wyniki CI

| Prawdziwa chiralność | Reprezentacja cos/sin: winding | Kąt interpolowany wprost: winding | MAE fazy cos/sin |
|---:|---:|---:|---:|
| +1 | +1.000 | ≈ 0 | 0.826° |
| −1 | −1.000 | ≈ 0 | 0.826° |

Dla rekonstrukcji cos/sin 95. percentyl błędu fazy wyniósł **3.846°**. Mediana normy pola `sqrt(cos²+sin²)` wyniosła 0.9995; minimum w analizowanym obszarze 0.3253. CI: **3/3 testy PASS**.

## 4. Dodatkowa obserwacja: które cechy zachowują orientację?

W Synoptyk-v3:
- radialne widmo mocy `|FFT|²` po binowaniu promieniowym jest niezmiennicze względem odbicia lustrzanego — usuwa kierunek/orientację;
- moduł gradientu `|∇f|` również nie zachowuje znaku orientacji;
- wirowość `dv/dx-du/dy` jest wielkością ze znakiem i może zachować informację o orientacji rotacji;
- dla pola fazowego odpowiednią bezpośrednią miarą jest znak liczby nawinięć, nie sam moduł gradientu ani radialne widmo.

Dla dwóch lustrzanych pól kontrolnych suma radialnego widma mocy i średni/modułowy rozkład gradientu były identyczne numerycznie. To potwierdza, że te dwie cechy same nie wystarczą do rozróżniania chiralności.

## 5. Wniosek

**W tym teście reprezentacja fazy jako pary składowych (cosφ, sinφ) zachowała znak nawinięcia +1/−1; bezpośrednia interpolacja zawiniętego kąta wyzerowała wykrywane nawinięcie.**

To wspiera konkretną wskazówkę z Synoptyk-v3: transformować reprezentację cykliczną przez składowe, nie interpolować samego kąta. Dla helisy TIMDR należy zachować parę fazorową/kwadraturową i osobno monitorować znak chiralności. Nie redukować jej wcześnie do modułu, wartości bezwzględnej, radialnego widma ani modułu gradientu.

## 6. Granice wyniku

To syntetyczny test interpolacji i reprezentacji, nie pomiar rzeczywistej helisy. Nie testuje:
- fizycznego kanału informacji → helisa;
- mechanicznej odpowiedzi G-Rezonansu;
- pamięci, adaptacji lub samonaprawy helisy;
- odporności na szum, rzadkie próbkowanie, różne topologie, defekty i niejednorodne warunki brzegowe.

Dodatkowo faza jest niezdefiniowana w centrum, gdzie norma pary kwadraturowej zanika/ma defekt — dlatego miarę nawinięcia liczono na pętli omijającej centrum.

## 7. Decyzja dla następnego kroku

Zachować pole jako kandydata na warstwę transformacji, ale minimalny kontrakt danych dla dalszej integracji powinien przechowywać:
1. dwie składowe kwadraturowe (nie sam kąt);
2. amplitudę/normę pola;
3. znak nawinięcia/chiralność;
4. informację o obszarach, gdzie norma jest bliska zeru i faza staje się nieokreślona;
5. oryginalny sygnał do kontroli rekonstrukcji i strat.

Następnie testować odporność tej reprezentacji na szum i rozdzielczość próbkowania. Dopiero potem mapować pole do S w GS-Matrix. Nie łączyć jeszcze bezpośrednio z mechanicznym G-Rezonansem.
