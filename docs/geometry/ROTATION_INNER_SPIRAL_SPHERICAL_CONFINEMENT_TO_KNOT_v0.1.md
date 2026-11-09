# Helisa wymuszona obrotem i skręcana przez kuliste otoczenie — model osi wewnętrznej v0.1

**Data:** 2026-11-09  
**Status:** formalizacja hipotezy autora; model do zbudowania i falsyfikacji.

## 1. Interpretacja konstrukcji

Doprecyzowanie autora: obrót kolejnych modułów trójkątnych (w tym ich odbić) wymusza powstawanie helisy. Oś nie jest prostą, nieruchomą osią zewnętrzną — jest wewnętrzną spiralą / krzywą prowadzącą. Otoczenie kuliste ogranicza możliwe położenia i orientacje modułów; w wyniku tego ograniczenia tor osi oraz helisa uzyskują dodatkowy skręt. Przy odpowiednim domknięciu i sprzężeniu gałęzi struktura może przejść w węzeł.

To jest hipoteza geometryczna. Nie zakładamy, że sama kula automatycznie tworzy węzeł: potrzebne są warunki brzegowe, reguła sprzężenia i test topologiczny.

## 2. Rozdzielenie trzech obiektów

Nie utożsamiamy:
1. **Modułu** (M_n): trójkątny element konstrukcyjny z orientacją i stanem odbicia.
2. **Osi wewnętrznej** (A(s)): krzywej prowadzącej, której przebieg jest spiralny / helikalny wskutek kolejnych obrotów modułów.
3. **Gałęzi helikalnej** (H_i(s)): toru elementu względem osi wewnętrznej, następnie ograniczanego przez kulistą powierzchnię.

Kula jest otoczeniem / ograniczeniem geometrycznym, nie osią helisy.

## 3. Minimalna parametryzacja

Wewnętrzną oś opisujemy jako krzywą przestrzenną:
[
A(s)inmathbb R^3,qquad |A(s)|le R-ho,
]
gdzie (R) to promień otaczającej kuli, a (ho) jest maksymalnym zasięgiem modułu od osi.

Lokalna rama osi:
[
F(s)=(T(s),N(s),B(s))
]
lub — w punktach o małej krzywiźnie — stabilniejsza rama Bishop/Fermi-Walker. Nie wolno polegać wyłącznie na ramie Freneta, która jest nieokreślona przy zerowej krzywiźnie.

Obrót modułu zapisujemy fazą:
[
	heta(s)=	heta_0+int_0^sOmega(u),du.
]
Odbicie modułu jest osobną zmienną dyskretną (m_nin{+1,-1}), a nie tym samym co obrót ani znak torsji.

Gałąź helikalna:
[
H_i(s)=A(s)+r_i(s)left[
cos(	heta_i(s))N(s)+sin(	heta_i(s))B(s)
ight].
]
Dla kilku gałęzi (	heta_i(s)=	heta(s)+delta_i(s)). Nie narzucamy równych przesunięć fazowych, dopóki nie wynikną z modułu i warunków styku.

## 4. Rola kuli

Kula ogranicza położenie modułów i gałęzi. Dla każdego punktu sprawdzamy:
[
|H_i(s)|le R.
]
Przy kontakcie z powierzchnią (|H_i(s)|=R) pojawia się reakcja ograniczenia, która może zmienić krzywiznę osi, fazę lub orientację modułu. W modelu mechanicznym trzeba określić prawo reakcji / energię; w modelu czysto geometrycznym — operator projekcji lub warunek styczności do sfery.

Istotne: projekcja punktów na kulę sama w sobie nie dowodzi powstania skrętu. Dodatkowy obrót ramy (holonomia), torsja osi lub skręt gałęzi musi być obliczony osobno.

## 5. Rozróżnione wielkości skrętu

Rejestrować oddzielnie:
- obrót modułu (Omega(s)=d	heta/ds);
- krzywiznę osi (kappa_A(s));
- torsję Freneta osi (	au_A(s)), jeśli jest określona;
- obrót ramy / holonomię po obiegu;
- skręt własny gałęzi względem ramy (twist);
- writhe krzywej osi;
- znak odbicia modułu (m_n);
- znak orientacji parametryzacji.

Nie wolno utożsamiać tych wielkości. W szczególności obrót modułu nie jest automatycznie torsją osi.

## 6. Od helisy do węzła — warunki konieczne

Aby mówić o węźle, trzeba otrzymać zamkniętą krzywą lub zdefiniowany układ rozłącznych krzywych zamkniętych, z jawną regułą połączeń. Wymagane są:
1. domknięcie położenia;
2. zgodność stycznej na szwie (jeśli ma być gładka);
3. zgodność ramy i fazy albo jawny skok fazowy;
4. brak niedozwolonych samoprzecięć w osadzeniu;
5. dla splotu — jawne rozdzielenie składowych i obliczenie linking;
6. dla węzła jednej krzywej — obliczenie niezmiennika rozróżniającego klasę węzła.

Samo zawinięcie krzywej wokół osi lub kontakt z kulą nie wystarcza. Węzeł powstaje wtedy, gdy zamknięte osadzenie ma nietrywialną strukturę topologiczną, a nie tylko wizualnie skręcony kształt.

## 7. Powiązanie z progiem czterech, pięciu i sześciu modułów

Nowa interpretacja licznika:
- cztery moduły tworzą aktualną konfigurację czterowęzłową;
- piąty moduł może zostać włączony bez naruszenia ograniczeń;
- szósty moduł może wymusić kontakt z granicą kuli, zmianę krzywizny osi lub konflikt fazowo-orientacyjny;
- reorganizacja do trzech gałęzi jest hipotezą wyniku, nie założeniem.

Warunek do testowania:
[
g(H_5)ge0,qquad g(H_6^*)<0.
]
Funkcja (g) musi mierzyć rzeczywisty luz do granicy, kolizje, niezgodność fazy/stycznej lub energię deformacji. Nie może być jedynie progiem liczby modułów.

## 8. Eksperymenty rozstrzygające

### E1 — obrót bez kuli
Wygenerować ciąg modułów trójkątnych z odbiciem i obrotem. Wyznaczyć oś wewnętrzną i sprawdzić, czy powstaje helisa bez zewnętrznego ograniczenia.

### E2 — ta sama konstrukcja w kuli
Dodać warunek (|H_i(s)|le R). Porównać krzywiznę osi, torsję, obrót ramy, fazę i odległości między modułami z E1.

### E3 — pięć kontra sześć modułów
Dla tej samej reguły modułu i tych samych warunków początkowych porównać luz brzegowy, kolizje, naprężenie/deformację i ciągłość ramy. Sprawdzić, czy piąty jest dopuszczalny, a szósty wymusza reorganizację.

### E4 — test topologiczny
Po uzyskaniu zamkniętej krzywej / splotu obliczyć odpowiedni niezmiennik. Nie nazywać struktury węzłem przed tym testem.

### E5 — kula kontra jajko
Kula jest bazą. Jajo jest kontrolą wpływu asymetrii otoczenia. Porównać, które efekty wynikają z samego ograniczenia, a które z symetrii sferycznej.

## 9. Przewidywania falsyfikowalne

- Jeśli obrót modułów nie generuje osi spiralnej w E1, mechanizm „obrót wymusza helisę” wymaga dodatkowego stopnia swobody lub innej reguły łączenia.
- Jeśli E2 nie zmienia krzywizny/holonomii/fazy względem E1, kula nie jest źródłem postulowanego dodatkowego skrętu w danym modelu.
- Jeśli sześć modułów mieści się równie dobrze jak pięć, próg 5→6 nie jest potwierdzony.
- Jeśli po reorganizacji krzywa jest topologicznie trywialna, mamy skręconą helisę, ale nie węzeł.
- Jeśli zmiana odbicia (m_n) nie zmienia orientacji ramy lub niezmienników, odbicie nie steruje postulowanym skrętem.

## 10. Zasada robocza

**Obrót modułów generuje helisę; wewnętrzna oś jest spiralna; kula ogranicza i może wymuszać dodatkowe skręcenie; dopiero warunki domknięcia i sprzężenia mogą przekształcić helisę w węzeł.**