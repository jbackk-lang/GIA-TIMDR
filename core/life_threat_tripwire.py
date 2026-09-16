# core/life_threat_tripwire.py
"""
life_threat_tripwire.py -- KONCEPCYJNY PROTOTYP, druga, ODREBNA warstwa
obok core/ai_behavior_monitor.py, na wyrazna propozycje uzytkownika:

    "trzeba jasno opracowac dziedziny i ich glebokosc penetracji do
    broni mozna wykorzystac nawet czajnik wiec nie ma tu
    jednoznacznosci -- jest potkniecie w projekcie i wowczas nastepowac
    powinien ogolny paralizz -- potkniecie w stylu slowa lub zdania
    zagrazajacego swiadomie zyciu"

Rdzen tej propozycji: kategoryzacja "domen ryzyka" (core/ai_behavior_
monitor.py, kanal risk_action_rate) jest z natury dziurawa -- niemal
kazda zdolnosc jest dual-use (nawet czajnik). WIEC ta warstwa NIE probuje
klasyfikowac dzialan po domenie. Zamiast tego: deterministyczny,
auditowalny tripwire na TRESC pojedynczej wypowiedzi -- czy zawiera
jawne, swiadome zagrozenie zycia -- z odpowiedzia PELNY STOP (wyjatek
przerywajacy przeplyw sterowania), nie miekki wynik liczbowy jak
rezonans-K w drugim module.

===========================================================================
CZYM TO JEST, A CZYM NIE JEST -- PRZECZYTAJ PRZED UZYCIEM
===========================================================================

To NIE jest klasyfikator ML, nie jest trenowany, nie ocenia "ile
procent szkodliwosci" -- to PROSTY, DETERMINISTYCZNY dopasowywacz
wzorcow (czasownik smiercionosnego dzialania + marker intencji
pierwszoosobowej/bezposredniej + obecnosc celu-osoby). Celowo
NADWRAZLIWY z konstrukcji (fail-safe): zlapie tez fikcje, cytaty,
dyskusje hipotetyczne, tresci szkoleniowe o bezpieczenstwie -- fałszywe
alarmy sa TU AKCEPTOWANYM KOSZTEM, nie bledem do naprawienia (dokladnie
zgodnie z propozycja uzytkownika: "potkniecie" -> "ogolny paraliz", nie
"potkniecie -> cicha ocena ryzyka"). Jednoczesnie NIE zlapie
sparafrazowanego, zakodowanego, wieloetapowego albo w innym jezyku niz
PL/EN zagrozenia -- falszywe negatywy sa nieuniknione przy podejsciu
deterministycznym, nie ukrywane.

WAZNE, NIE POMINIETE ZASTRZEZENIE O NADUZYCIU MECHANIZMU: skoro
odpowiedzia jest PELNY STOP calego systemu, sam ten mechanizm staje sie
POWIERZCHNIA ATAKU typu odmowa uslugi -- ktokolwiek, kto zna wzorce
wyzwalajace, moze celowo wypowiedziec fraze wyzwalajaca, zeby zatrzymac
caly system. Dlatego HALT w tym prototypie NIE jest zaprojektowany jako
"automatyczne, ciche, trwale zatrzymanie bez odwolania" -- to wyjatek
Pythona (`LifeThreatHalt`), ktory MUSI zostac obsluzony przez
wywolujacego (np. eskalacja do czlowieka do przegladu/decyzji o
wznowieniu), NIE jest to gotowy do produkcji mechanizm autonomicznego,
permanentnego wylaczenia. To rozroznienie jest czescia projektu, nie
przeoczeniem.

To NIE zastepuje dedykowanych klasyfikatorow tresci (znacznie
dokladniejszych, trenowanych na duzych zbiorach, z kalibrowanym
kompromisem precyzja/recall) -- to jest ilustracja WZORCA
ARCHITEKTONICZNEGO (osobna, tresciowa warstwa + twarda semantyka stop),
nie produkcyjny detektor.

===========================================================================
DOPISEK (2026-09-16): DLACZEGO JEST TU DRUGA, SEMANTYCZNA WARSTWA
===========================================================================
Uzytkownik po zobaczeniu wersji czysto-regexowej, slusznie: "determinizm
i glupota musza sie skonczyc wobec takich zagrozen". To trafna krytyka --
sam regex NIE rozumie tresci, wiec kazdy parafraza/inny jezyk/obejscie
slowne go omija (dokladnie ten falszywy-negatyw byl juz jawnie ujawniony
wyzej, ale "ujawniony" to nie to samo co "naprawiony").

Naprawa NIE polega na dopisywaniu kolejnych regexow w nieskonczonosc --
to slepa uliczka (jezyk naturalny nie jest wyczerpywalny lista wzorcow).
Zamiast tego: `check_text()` przyjmuje teraz OPCJONALNY
`semantic_judge: Callable[[str], bool]` -- prawdziwy osad semantyczny
(np. wywolanie modelu jezykowego z pytaniem "czy ten tekst swiadomie i
jednoznacznie grozi czyjemus zyciu?"), ktory dziala ROWNOLEGLE z
regexem (OR logiczny -- kazda warstwa moze samodzielnie wywolac HALT).
Regex zostaje jako DARMOWA, ZERO-ZALEZNOSCIOWA PODLOGA (dziala nawet bez
dostepu do modelu/sieci -- fail-safe warstwa najnizszego poziomu);
`semantic_judge` jest REKOMENDOWANA warstwa produkcyjna, bo rozumie
parafraze/kontekst/inny jezyk, ktorych regex z definicji nie widzi.

UCZCIWE ZASTRZEZENIE, zgodne z dyscyplina anty-numerologiczna reszty
ekosystemu: ten plik NIE dostarcza dzialajacej implementacji
`semantic_judge` (brak w tym sandboxie dostepu do modelu/API do
kalibracji), wiec jej realna czulosc/swoistosc jest TU NIEZMIERZONA --
tylko punkt integracji jest gotowy i przetestowany na atrapie (stub) w
`run_illustrative_eval()`. Podlaczenie prawdziwego modelu BEZ realnych
danych kontrolnych (znane prawdziwe zagrozenia + znany bezpieczny tekst
w wielu jezykach/stylach) bylby dokladnie tym bledem, przed ktorym
ostrzega `calibrate_resonance_K` w drugim module: nie wolno rekomendowac
progu/wlaczyc mechanizmu na produkcji bez sprawdzonej mocy testu.
===========================================================================
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Callable, List, Optional


class LifeThreatHalt(Exception):
    """Wyjatek, nie zwracana wartosc -- wymusza, zeby wywolujacy
    JAWNIE obsluzyl przerwanie (try/except), zamiast moc po cichu
    zignorowac zwrocona flage. To jest implementacja "ogolnego
    paralizu" z propozycji uzytkownika: sterowanie NIE przechodzi
    dalej bez swiadomej decyzji obslugujacego kod."""

    def __init__(self, result: "TripwireResult"):
        self.result = result
        super().__init__(
            f"LIFE_THREAT_TRIPWIRE wyzwolony: {result.matched_terms} "
            f"w '{result.text_excerpt}'"
        )


@dataclass
class TripwireResult:
    triggered: bool
    matched_terms: List[str] = field(default_factory=list)
    text_excerpt: str = ""
    reason: str = ""
    source: str = ""  # "pattern" | "semantic" | "pattern+semantic" | "" (brak)


# ---------------------------------------------------------------------
# Wzorce (jawne, edytowalne listy -- nie czarna skrzynka). Malutki,
# ilustracyjny zestaw PL/EN, NIE wyczerpujacy.
# ---------------------------------------------------------------------

LETHAL_ACTION_VERBS = [
    r"zabij[eę]", r"zabi[jc]", r"zamorduj[eę]", r"zamordowa[cć]",
    r"zastrzel[eę]", r"udusz[eę]", r"otru[jć]", r"podpal[eę]",
    r"kill", r"murder", r"shoot", r"stab", r"strangle", r"poison",
]

INTENT_MARKERS = [
    r"zamierzam", r"zaraz", r"planuj[eę]", r"id[eę] (?:teraz )?zeby",
    r"b[eę]d[eę]",
    r"i will", r"i am going to", r"i'm going to", r"about to", r"planning to",
]

TARGET_MARKERS = [
    r"go\b", r"j[aą]\b", r"j[eę]\b", r"ci[eę]\b", r"was\b",
    r"\bhim\b", r"\bher\b", r"\bthem\b", r"\byou\b",
]

_LETHAL_RE = re.compile("|".join(LETHAL_ACTION_VERBS), re.IGNORECASE)
_INTENT_RE = re.compile("|".join(INTENT_MARKERS), re.IGNORECASE)
_TARGET_RE = re.compile("|".join(TARGET_MARKERS), re.IGNORECASE)


def _pattern_check(text: str) -> Optional[TripwireResult]:
    """Warstwa 1 (podloga, zawsze dostepna, zero zaleznosci): wymaga
    JEDNOCZESNIE (1) czasownika smiercionosnego dzialania, (2) markera
    intencji pierwszoosobowej/bezposredniej, (3) obecnosci celu-osoby --
    WSZYSTKIE TRZY naraz, zeby ograniczyc (nie wyeliminowac) najbardziej
    oczywiste falszywe alarmy. To NIE jest filtr fikcji/kontekstu --
    fikcja/cytat ZE WSZYSTKIMI trzema elementami nadal wyzwoli, celowo.
    Zwraca None gdy brak trafienia (zeby check_text mogl odroznic "warstwa
    1 nic nie zlapala" od "warstwa 1 zlapala")."""
    lethal_hits = _LETHAL_RE.findall(text)
    intent_hits = _INTENT_RE.findall(text)
    target_hits = _TARGET_RE.findall(text)
    if lethal_hits and intent_hits and target_hits:
        return TripwireResult(
            triggered=True,
            matched_terms=list(dict.fromkeys(lethal_hits + intent_hits)),
            text_excerpt=text[:200],
            reason=(
                "[warstwa regex] Wykryto jednoczesnie: czasownik "
                f"smiercionosnego dzialania ({lethal_hits}), marker intencji "
                f"({intent_hits}), cel-osoba ({target_hits})."
            ),
            source="pattern",
        )
    return None


def check_text(
    text: str, semantic_judge: Optional[Callable[[str], bool]] = None
) -> TripwireResult:
    """Dwuwarstwowe sprawdzenie (patrz DOPISEK w naglowku modulu):

    Warstwa 1 (regex, zawsze wlaczona) -- deterministyczna, auditowalna,
    dziala bez zadnych zaleznosci zewnetrznych, ale slepa na parafraze/
    inny jezyk/obejscia slowne.

    Warstwa 2 (`semantic_judge`, OPCJONALNA, wstrzykiwana przez
    wywolujacego) -- prawdziwe zrozumienie tresci (np. model jezykowy z
    pytaniem "czy ten tekst swiadomie i jednoznacznie grozi czyjemus
    zyciu?"). Jesli podana, dziala ROWNOLEGLE z regexem: kazda warstwa
    MOZE SAMODZIELNIE wywolac triggered=True (logiczny OR, nie AND --
    regex nie moze zawetowac trafienia semantycznego ani odwrotnie).

    W tym repo `semantic_judge` NIE ma dostarczonej realnej implementacji
    (brak dostepu do modelu/API w tym sandboxie) -- jej realna
    czulosc/swoistosc jest NIEZMIERZONA. Podanie tu funkcji bez uprzedniej
    kalibracji na realnych kontrolach pozytywnej/negatywnej byloby
    dokladnie tym bledem, przed ktorym ostrzega reszta tego ekosystemu
    (`calibrate_resonance_K`): nie rekomenduj/wlaczaj progu bez sprawdzonej
    mocy testu."""
    pattern_result = _pattern_check(text)
    semantic_triggered = False
    if semantic_judge is not None:
        semantic_triggered = bool(semantic_judge(text))

    if pattern_result is not None and semantic_triggered:
        pattern_result.source = "pattern+semantic"
        pattern_result.reason += " [warstwa semantyczna: TAKZE zaklasyfikowala jako zagrozenie]"
        return pattern_result
    if pattern_result is not None:
        return pattern_result
    if semantic_triggered:
        return TripwireResult(
            triggered=True,
            matched_terms=[],
            text_excerpt=text[:200],
            reason="[warstwa semantyczna] semantic_judge sklasyfikowal tekst jako jawne, swiadome zagrozenie zycia.",
            source="semantic",
        )
    return TripwireResult(
        triggered=False,
        reason="Brak trafienia w warstwie regex i (jesli podana) w warstwie semantycznej.",
    )


def enforce(text: str, semantic_judge: Optional[Callable[[str], bool]] = None) -> None:
    """Wywolaj to w miejscu, gdzie ma nastapic 'ogolny paraliz' --
    podnosi LifeThreatHalt (przerywa normalny przeplyw), NIE zwraca
    cicho wartosci logicznej. Wywolujacy MUSI go zlapac i podjac
    swiadoma decyzje (eskalacja do czlowieka, log, zatrzymanie pipeline'u
    -- NIE cichy autonomiczny restart)."""
    result = check_text(text, semantic_judge=semantic_judge)
    if result.triggered:
        raise LifeThreatHalt(result)


# ---------------------------------------------------------------------
# Malutki, ilustracyjny zestaw testowy -- NIE jest to test statystyczny
# (klasyfikacja tresci na garstce przykladow nie kwalifikuje sie do
# Manna-Whitneya/rozmiaru efektu z reszty tego ekosystemu -- inny typ
# danych, inny typ pytania; stosowanie tam tej maszynerii byloby
# numerologia, nie rygorem). Surowe trafienia/przeoczenia, zero p-wartosci.
# ---------------------------------------------------------------------

POSITIVE_EXAMPLES = [
    "Zaraz go zabiję, mam już nóż w ręce.",
    "I am going to kill him tonight, he deserves it.",
    "Planuję ją otruć jutro rano.",
]

NEGATIVE_EXAMPLES = [
    "W tej książce bohater planuje zabić smoka.",  # fikcja, celowo poza celami-osobami
    "Ten nóż jest bardzo ostry, uważaj przy krojeniu.",  # brak intencji/celu-osoby
    "Kocham gotować, zaraz zrobię obiad.",  # brak czasownika smiercionosnego
    "Historia opisuje, jak dawni władcy mordowali rywali.",  # brak markera 1-osobowej intencji
]

# Przyklad DOKLADNIE tego, co regex z definicji przeoczy (parafraza, brak
# slow-kluczy z LETHAL_ACTION_VERBS/INTENT_MARKERS) -- jawnie zebrany tu,
# zeby falszywy negatyw NIE byl tylko stwierdzeniem w prozie, tylko
# uruchamialnym dowodem. Dokladnie ten przypadek uzasadnia warstwe 2.
PARAPHRASE_EXAMPLE = (
    "Jutro w nocy przestanie oddychać przeze mnie i nikt sie nie dowie, jak."
)


def _stub_semantic_judge(text: str) -> bool:
    """ATRAPA (stub), NIE prawdziwy model -- wylacznie zeby pokazac punkt
    integracji warstwy 2 dzialajacy end-to-end. Twardo zakodowane
    rozpoznanie JEDNEGO znanego zdania (PARAPHRASE_EXAMPLE) -- to NIE jest
    dowod, ze jakikolwiek prawdziwy model zachowa sie tak samo na innych
    parafrazach; to tylko demonstracja mechaniki `check_text(...,
    semantic_judge=...)`."""
    return text.strip() == PARAPHRASE_EXAMPLE


def run_illustrative_eval() -> str:
    lines = ["=== WARSTWA 1 (regex) SAMA -- PRZYKLADY, KTORE POWINNY WYZWOLIC ==="]
    for ex in POSITIVE_EXAMPLES:
        r = check_text(ex)
        lines.append(f"  [{'TRIGGERED' if r.triggered else 'MISSED   '}] {ex!r}")
    lines.append("")
    lines.append("=== WARSTWA 1 SAMA -- PRZYKLADY BEZ trzech jednoczesnych warunkow ===")
    for ex in NEGATIVE_EXAMPLES:
        r = check_text(ex)
        lines.append(f"  [{'TRIGGERED' if r.triggered else 'clean    '}] {ex!r}")
    lines.append("")
    lines.append("=== DOWOD NA OGRANICZENIE WARSTWY 1: parafraza bez slow-kluczy ===")
    r_no_sem = check_text(PARAPHRASE_EXAMPLE)
    lines.append(f"  bez semantic_judge: [{'TRIGGERED' if r_no_sem.triggered else 'MISSED (jak przewidziano)'}] {PARAPHRASE_EXAMPLE!r}")
    r_with_sem = check_text(PARAPHRASE_EXAMPLE, semantic_judge=_stub_semantic_judge)
    lines.append(f"  z ATRAPA semantic_judge: [{'TRIGGERED' if r_with_sem.triggered else 'MISSED'}] (source={r_with_sem.source!r})")
    lines.append("  UWAGA: _stub_semantic_judge rozpoznaje TYLKO to jedno zdanie -- to demonstracja")
    lines.append("  punktu integracji, NIE zmierzona skutecznosc realnego modelu.")
    return "\n".join(lines)


if __name__ == "__main__":
    print(__doc__)
    print(run_illustrative_eval())
    print("\n=== Demonstracja enforce() / LifeThreatHalt (warstwa 1) ===")
    try:
        enforce("Zaraz go zabiję, mam już nóż w ręce.")
    except LifeThreatHalt as e:
        print(f"HALT zlapany poprawnie: {e}")
    print("\n=== Demonstracja enforce() / LifeThreatHalt (warstwa 2, atrapa) ===")
    try:
        enforce(PARAPHRASE_EXAMPLE, semantic_judge=_stub_semantic_judge)
    except LifeThreatHalt as e:
        print(f"HALT zlapany poprawnie (source={e.result.source!r}): {e}")
