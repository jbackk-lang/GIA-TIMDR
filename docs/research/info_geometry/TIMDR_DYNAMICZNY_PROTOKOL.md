# TIMDR dynamiczny zamiast klasyfikacji cech statycznych

**2026-11-14. Status:** korekta metodologii po uwadze autora. Projekt eksperymentu, nie potwierdzony wynik.

## Błąd poprzedniego uproszczenia

W pilocie A/B i `multibranch_receiver_test.py` różnice cech pomiędzy dwiema połówkami przebiegu zostały spłaszczone do wektora, po czym klasyfikator najbliższego centroidu przypisywał etykietę. To jest **cząstkowy opis statyczny**. Nie odtwarza dynamicznego działania TIMDR ani sprzężeń i sekwencji zmian. Uzyskane wyniki (w tym 100% w konfiguracji AB+ALL) są wynikiem klasyfikatora na uproszczonej syntetyce, nie walidacją dynamicznego TIMDR.

## Nowa jednostka analizy: trajektoria procesu

Nie `F(y_before), F(y_after)` i pojedyncza różnica, lecz chronologiczny ciąg stanów:

```text
T = (t0,...,tn)
Ξ(t) = (x(t), Γ(t,s), φ(t))   [tylko gdy konstrukcje są zdefiniowane]
z(t) = (e_MS(t), e_G(t), e_K(t), e_META(t), q(t))
```

`q(t)` zawiera jakość obserwacji, kalibrację, opóźnienie, niepewność i maski dostępności. `e_G` nie jest domyślnie operatorem G: gdy nie mamy kongruencji powierzchniowej, oznaczyć `G_PROXY` lub `NOT_APPLICABLE`. Podobnie `K_PROXY` nie jest rezonansem K.

Wymagane jest jawne rozróżnienie **ewolucji opisu** od **ewolucji badanego układu**. To, że zmienia się `z(t)`, nie przesądza o zmianie generatora.

## Dynamika i mosty

1. **M/S:** okna przesuwne i strumień detekcji zdarzeń, trend, zmiana reżimu, nie tylko jedna różnica przed/po.
2. **K:** trajektorie widma/fazy i synchronizacji z jawnym warunkiem próbkowania; bez automatycznego nazywania pików rezonansem.
3. **G:** ewolucja dopuszczalnej rodziny trajektorii, jeśli mamy poprawnie zdefiniowaną `Γ(t,s)`; osobno oznaczone proxy geometrii opóźnieniowej.
4. **META:** dynamiczna agregacja z jawnymi wejściami i historią, nie jednorazowa konkatenacja.
5. **Mosty:** badanie opóźnień i następstwa zdarzeń między ścieżkami; jawne mapy i warunki zgodności, nie założenie równoważności gałęzi.
6. **Dwa odbiorniki:** porównanie sekwencji zmian `z_A(t)` i `z_B(t)`, ich synchronizacji, przesunięć i rozbieżności; wspólna zmiana nadal nie odróżnia S od wspólnego H.

## Pytania dynamiczne

- Czy pierwsza wykrywalna zmiana pojawia się w M/S, K, czy G_PROXY?
- Czy relacja czasowa między ścieżkami jest stabilna przy zmianie odbiornika?
- Czy efekt jest przejściowy, narastający, cykliczny, czy trwały?
- Czy stan wraca do poprzedniej konfiguracji po usunięciu zakłócenia?
- Czy przy identycznym końcowym rozkładzie cech różne historie prowadzą do odmiennych wniosków?
- Kiedy wynik musi pozostać `UNKNOWN`?

## Następny eksperyment: przełączenie, narastanie i powrót

Wygenerować sekwencje z czterema fazami:
`BASE → RAMP → PERTURBATION → RECOVERY`.
Manipulować osobno generatorem, kanałem wspólnym, odbiornikiem A i B. Dodać scenariusze z identycznym stanem końcowym, lecz różną historią zmian.

**Porównanie kontrolne:** (a) dotychczasowy klasyfikator statyczny, (b) klasyfikator trajektorii zachowujący porządek okien, (c) wariant z losową permutacją kolejności okien, (d) dwie ścieżki odbioru, (e) opcjonalna referencja przed kanałem. Dla uczciwości porównać pojemność modeli i liczbę cech.

**Metryki:** czas do detekcji, opóźnienie przypisania przyczyny, macro-F1 na sesję, fałszywe alarmy na jednostkę czasu, błędne przypisanie SOURCE↔COMMON_CHANNEL, odsetek UNKNOWN, wykrycie powrotu, stabilność na nieznanych parametrach. Podział train/calibration/test według całych sesji.

**Kontrole:** permutacja czasu, zmiana zegara odbiornika, filtracji, szumu i długości okien; test przy zamienionych rolach A/B. Parametry i progi zamrozić przed testem odłożonym.

## Ograniczenia

Dynamika obserwacji może być indukowana przez dynamiczny odbiornik. Dwa odbiorniki bez referencji nie rozwiązują ogólnej nieidentyfikowalności źródła i wspólnego kanału. Nawet wykazanie dodatkowej wartości trajektorii nie dowodzi ontologicznej natury informacji.

## Źródła TIMDR do zachowania

- [Specyfikacja gałęzi](../../theory/TIMDR_Branch_Specification.md)
- [Chronoproces](../../theory/TIMDR_Chronoprocess.md)
- [Konstrukcja odwzorowań TRM/GIA](../../theory/TIMDR_EventGraph_Branch_Construction.md)

Nie wprowadzać nowych aksjomatów przez nazewnictwo prototypu. Najpierw poprawność operatorów i testy mostów.
