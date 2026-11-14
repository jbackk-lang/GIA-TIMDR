# Odbiór bez założonej kategorii — mosty gałęzi TIMDR

**Data:** 2026-11-14. **Status:** propozycja architektury badawczej, nie nowy aksjomat TIMDR.

## Zasada

Nie wiemy z góry, czy cechy odebranego sygnału najlepiej opisuje gałąź M/S, G, K, META, czy kombinacja. Nie wymuszamy klasyfikacji ontologicznej informacji. Wykonujemy **równoległe, niezależne rzuty** i porównujemy ich wyniki przez jawne mosty, zachowując rozdzielność domen matematycznych.

Punkty odniesienia w repo:
- [Specyfikacja gałęzi](../../theory/TIMDR_Branch_Specification.md): gałęzie nie są redukcjami siebie; skręt M/S nie jest skrętem G.
- [Chronoproces](../../theory/TIMDR_Chronoprocess.md): wspólny indeks czasu `T`, ale odrębne rzuty `x`, `Γ`, `φ`.
- [Konstrukcja TRM/GIA → gałęzie](../../theory/TIMDR_EventGraph_Branch_Construction.md): jawne odwzorowania tracące część informacji, nie ogólnie odwracalne.
- [Mapa repozytorium](../../../REPOZYTORIUM.md): statusy i odnośniki do istniejących mostów.

## Schemat odbioru

```text
źródło S -- kanał H -- odbiornik R --> obserwacja y(t) + metadane toru
                                      |
                    +-----------------+------------------+
                    |                 |                  |
                 M/S: x(t)         K: (f,φ,A)       G: Γ(t,s)*
                    |                 |                  |
                    +-----------------+------------------+
                                      |
                      kandydaci mostów + META
                                      |
                       raport wielohipotezowy:
                 źródło / kanał / odbiornik / nierozstrzygalne
```

`*` **G wymaga jawnej konstrukcji domeny geometrycznej**. Pojedyncza krzywa opóźnieniowa w R³ może mieć krzywiznę Freneta, ale sama nie jest powierzchnią 2D z operatorem kształtu z aksjomatów G. Aby zastosować pełny rzut G Chronoprocesu, trzeba zdefiniować rodzinę trajektorii `Γ(t,s)` i sprawdzić regularność. W przeciwnym razie wynik podpisujemy `geometria pomocnicza / proxy`, nie `operator G`.

## Ścieżki równoległe

| Ścieżka | Obserwacja | Czego nie wolno wnioskować |
|---|---|---|
| M/S | anomalia, trend, koincydencja progowa, okna | że wykryty skręt jest skrętem powierzchni G |
| K | widmo, faza, modalność, synchronizacja | że maksimum widma samo dowodzi rezonansu |
| G | jawna krzywa lub rodzina trajektorii, zgodna z definicją operatora | że każda trajektoria 1D ma operator kształtu |
| META | agregat z udokumentowanymi wejściami Λ–τ–ρ–J | że agregat stanowi nowy niezależny pomiar |
| Mosty | zgodność, rozbieżność i komplementarność gałęzi | że most jest twierdzeniem bez osobnego testu |

## Zasada „nieznanej kategorii”

Wynik ma postać wektora dowodów `E=(E_MS,E_G,E_K,E_META,E_bridges)`, z maską brakujących/nieadekwatnych rzutów i informacją o kalibracji. Nie normalizujemy go automatycznie do rozkładu prawdopodobieństwa „prawdziwych kategorii informacji”. Opcjonalna klasyfikacja operacyjna wymaga etykiet, kalibracji i możliwości abstencji `UNKNOWN`.

## Mosty do rozważenia

1. **M/S ↔ G**: zgodność zdarzeń sygnałowych z poprawnie skonstruowanymi obiektami G. Istniejące w repo mosty i ich statusy sprawdzić w specyfikacji; nie przenosić automatycznie walidacji z łożysk na nową domenę.
2. **M/S ↔ K**: zgodność zmian czasowych z fazą i widmem; zachować różnicę między koincydencją progową M a rezonansowym operatorem K.
3. **G ↔ K**: hipoteza powiązania geometrii kongruencji z modalnością, wymagająca osobnej mapy i kontroli.
4. **Gałęzie ↔ META**: jawna agregacja po zamrożeniu wejść i parametrów; test ablacyjny sprawdzający, czy META wnosi wartość ponad swoje składowe.

To **lista kandydatów badawczych**, nie deklaracja, że wszystkie mosty zostały dowiedzione lub zaimplementowane.

## Źródło / kanał / odbiornik

Dla dwóch odbiorników `y_A`, `y_B` uruchamiamy każdą ścieżkę osobno i porównujemy:
- zgodność zdarzeń między odbiornikami w obrębie tej samej gałęzi;
- zgodność między gałęziami w obrębie jednego odbiornika;
- zgodność po uwzględnieniu opóźnień, różnic próbkowania i filtracji;
- porównanie z referencją przed kanałem, jeśli istnieje.

Zgodność wszystkich gałęzi w obu odbiornikach **nadal nie rozdziela generatora od wspólnego kanału**. Wspólne błędy kalibracji mogą tworzyć pozorny konsensus.

## Kryteria następnego eksperymentu

- Dla scenariuszy G/H/R/COMMON_CHANNEL/UNKNOWN liczyć skuteczność osobno dla M/S, K, proxy geometrii i ich połączeń.
- Porównać z baseline'em surowych cech i prostym modelem wieloczujnikowym.
- Wprowadzić etykietę `UNKNOWN` i mierzyć fałszywe przypisanie źródła.
- Zamrozić mosty i progi przed odłożonym testem; raportować kalibrację, ablacje, niepewność i przypadki sprzeczności.
- Jeśli brak danych do poprawnej konstrukcji G lub META, oznaczyć `NOT_APPLICABLE`, zamiast udawać kompletność.

## Kluczowa hipoteza

Możliwe, że informacja obserwowana jest relacyjna: zależy od źródła, kanału, odbiornika i wybranego opisu. **Hipoteza relacyjności** nie jest w tym dokumencie dowodem na ontologiczną naturę informacji.
