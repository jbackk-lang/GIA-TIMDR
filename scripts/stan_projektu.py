"""Odswieza czesc automatyczna STAN_PROJEKTU.md: bilans testow i liste wynikow od najnowszego.

Zrodlo prawdy to tabela wynikow w README.md (kazdy test ma tam wiersz z linkiem do RESULT_*.md) -- protokol
i tak wymaga tego wiersza, wiec po dopisaniu testu wystarczy uruchomic:

    python scripts/stan_projektu.py        (albo dwuklik na aktualizuj_stan.bat)

Reczne czesci STAN_PROJEKTU.md (poza znacznikami AUTO) nie sa ruszane. Tylko biblioteka standardowa.
"""
from __future__ import annotations

import re
import subprocess
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
STAN = ROOT / "STAN_PROJEKTU.md"
START, END = "<!-- AUTO:START -->", "<!-- AUTO:END -->"
LINK = re.compile(r"\[wynik\]\(([^)]+)\)")
ORDER = [("NOT SUPPORTED", "NIE"), ("SUPPORTED", "TAK"), ("MIXED", "MIESZANY"), ("MIESZANY", "MIESZANY"),
         ("INCONCLUSIVE", "NIEROZSTRZYGNIĘTY"), ("brak wartości", "NIE"), ("remis", "MIESZANY"),
         ("replikacja częściowa", "MIESZANY")]
ICON = {"TAK": "✅", "MIESZANY": "🟡", "NIE": "❌", "NIEROZSTRZYGNIĘTY": "⚪"}


def verdict(cell: str) -> str:
    """Pierwszy werdykt w komorce (wg pozycji); 'NOT SUPPORTED' ma pierwszenstwo przed 'SUPPORTED' w tym samym miejscu."""
    best = None
    for key, name in ORDER:
        i = cell.find(key)
        if key == "SUPPORTED":                       # pomin trafienie bedace czescia "NOT SUPPORTED"
            i = next((m.start() for m in re.finditer("SUPPORTED", cell) if not cell[:m.start()].endswith("NOT ")), -1)
        if i >= 0 and (best is None or i < best[0]):
            best = (i, name)
    return best[1] if best else "NIEROZSTRZYGNIĘTY"


def git_date(path: Path) -> str:
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", str(path)], cwd=ROOT, capture_output=True,
                             text=True, timeout=20).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        out = ""
    return out or date.today().isoformat()


def rows() -> list[dict]:
    out = []
    for line in README.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or "[wynik](" not in line:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        link = LINK.search(line).group(1)
        name = re.sub(r"\*\*", "", cells[0])
        out.append({"name": name, "verdict": verdict(cells[-1]), "link": link,
                    "date": git_date(ROOT / link) if not link.startswith("http") else "", "detail": cells[-1]})
    return out


def short(detail: str, n: int = 160) -> str:
    d = re.sub(r"\(\[wynik\]\([^)]+\)\)", "", detail)
    d = re.sub(r"\*\*", "", d).strip(" ;,")
    return d if len(d) <= n else d[: n - 1].rsplit(" ", 1)[0] + "…"


def render(rs: list[dict]) -> str:
    c = Counter(r["verdict"] for r in rs)
    rs = sorted(rs, key=lambda r: r["date"], reverse=True)
    L = [START, "", f"_Część automatyczna — odświeżona {date.today().isoformat()} skryptem `scripts/stan_projektu.py` "
                    f"z tabeli wyników w README._", "",
         f"**Bilans pre-rejestrowanych testów: {len(rs)}** — "
         f"{ICON['TAK']} potwierdzone {c['TAK']} · {ICON['MIESZANY']} mieszane {c['MIESZANY']} · "
         f"{ICON['NIE']} niepotwierdzone {c['NIE']} · {ICON['NIEROZSTRZYGNIĘTY']} nierozstrzygnięte {c['NIEROZSTRZYGNIĘTY']}.",
         "", "Werdykt w kolumnie to pierwsza hipoteza główna testu; szczegóły (hipotezy poboczne, ograniczenia) — w pliku wyniku.",
         "", "| Data | Test | Werdykt | Wynik |", "|---|---|---|---|"]
    for r in rs:
        L.append(f"| {r['date']} | [{r['name']}]({r['link']}) | {ICON[r['verdict']]} {r['verdict'].lower()} | "
                 f"{short(r['detail'])} |")
    L += ["", END]
    return "\n".join(L)


def main() -> None:
    text = STAN.read_text(encoding="utf-8")
    if START not in text or END not in text:
        raise SystemExit(f"{STAN.name}: brak znaczników {START} / {END}")
    a, b = text.index(START), text.index(END) + len(END)
    rs = rows()
    text = text[:a] + render(rs) + text[b:]
    text = re.sub(r"(?m)^_Stan na: .*_$", f"_Stan na: {date.today().isoformat()}_", text)
    STAN.write_text(text, encoding="utf-8")
    print(f"{STAN.name}: {len(rs)} testów odświeżonych")


if __name__ == "__main__":
    main()
