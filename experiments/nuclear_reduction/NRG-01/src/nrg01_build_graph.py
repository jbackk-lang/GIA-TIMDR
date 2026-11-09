#!/usr/bin/env python3
"""Build reproducible nuclide decay graphs from the IAEA LiveChart CSV API.

This is a data-ingestion/reduction experiment, not a nuclear-physics predictor.
Unknown or non-ground-state channels are retained as unresolved edges rather
than guessed. Requires Python 3.10+ and network access when downloading.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import time
import urllib.parse
import urllib.request
from collections import deque
from datetime import datetime, timezone
from pathlib import Path

API = "https://nds.iaea.org/relnsd/v1/data"
SEEDS = ("238u", "232th", "237np")
FIELDS = "ground_states"


def parse_nuclide(label: str) -> tuple[int, int, str]:
    import re
    m = re.fullmatch(r"(\d+)([a-zA-Z]{1,3})", label.strip())
    if not m:
        raise ValueError(f"Invalid nuclide label: {label}")
    a, symbol = int(m.group(1)), m.group(2).capitalize()
    z_by_symbol = {
        "H":1,"He":2,"Li":3,"Be":4,"B":5,"C":6,"N":7,"O":8,"F":9,"Ne":10,
        "Na":11,"Mg":12,"Al":13,"Si":14,"P":15,"S":16,"Cl":17,"Ar":18,"K":19,"Ca":20,
        "Sc":21,"Ti":22,"V":23,"Cr":24,"Mn":25,"Fe":26,"Co":27,"Ni":28,"Cu":29,"Zn":30,
        "Ga":31,"Ge":32,"As":33,"Se":34,"Br":35,"Kr":36,"Rb":37,"Sr":38,"Y":39,"Zr":40,
        "Nb":41,"Mo":42,"Tc":43,"Ru":44,"Rh":45,"Pd":46,"Ag":47,"Cd":48,"In":49,"Sn":50,
        "Sb":51,"Te":52,"I":53,"Xe":54,"Cs":55,"Ba":56,"La":57,"Ce":58,"Pr":59,"Nd":60,
        "Pm":61,"Sm":62,"Eu":63,"Gd":64,"Tb":65,"Dy":66,"Ho":67,"Er":68,"Tm":69,"Yb":70,
        "Lu":71,"Hf":72,"Ta":73,"W":74,"Re":75,"Os":76,"Ir":77,"Pt":78,"Au":79,"Hg":80,
        "Tl":81,"Pb":82,"Bi":83,"Po":84,"At":85,"Rn":86,"Fr":87,"Ra":88,"Ac":89,"Th":90,
        "Pa":91,"U":92,"Np":93,"Pu":94,"Am":95,"Cm":96,"Bk":97,"Cf":98,"Es":99,"Fm":100,
        "Md":101,"No":102,"Lr":103
    }
    if symbol not in z_by_symbol:
        raise ValueError(f"Unknown element symbol: {symbol}")
    z = z_by_symbol[symbol]
    if a < z:
        raise ValueError(f"Mass number A={a} is smaller than Z={z}")
    return z, a-z, symbol


def daughter_for(z: int, n: int, mode: str) -> tuple[int, int] | None:
    """Return daughter (Z,N) for unambiguous ground-state modes only."""
    m = mode.strip().upper().replace(" ", "")
    if m in {"A", "ALPHA"}:
        return (z-2, n-2) if z >= 2 and n >= 2 else None
    if m in {"B-", "BM", "BETA-", "BETA−"}:
        return (z+1, n-1) if n >= 1 else None
    if m in {"B+", "BP", "BETA+", "BETA+"}:
        return (z-1, n+1) if z >= 1 else None
    if m in {"EC", "E.C.", "ELECTRONCAPTURE"}:
        return (z-1, n+1) if z >= 1 else None
    # IT, SF, p, n, cluster, double-beta and mixed/unknown labels need
    # level/channel-specific information. Do not invent a daughter here.
    return None


def fetch_ground_state(label: str, timeout: int = 30) -> dict:
    params = urllib.parse.urlencode({"fields": FIELDS, "nuclides": label.lower()})
    req = urllib.request.Request(
        f"{API}?{params}",
        headers={"User-Agent": "GIA-TIMDR-NRG01/0.1 (reproducible research)"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        raw = response.read()
    text = raw.decode("utf-8-sig")
    rows = list(csv.DictReader(io.StringIO(text)))
    if not rows:
        raise RuntimeError(f"No IAEA LiveChart ground-state record for {label}")
    # API may return more than one row in future; keep the ground state if idx exists.
    row = next((r for r in rows if str(r.get("idx", "0")).strip() in {"", "0"}), rows[0])
    row["_raw_sha256"] = hashlib.sha256(raw).hexdigest()
    row["_raw_csv"] = text
    return row


def finite_float(value):
    try:
        v = float(value)
        return v if v == v and abs(v) != float("inf") else None
    except (TypeError, ValueError):
        return None


def build_graph(seeds=SEEDS, max_depth=80, delay=0.15):
    nodes, edges, unresolved, sources, raw_csv = {}, [], [], [], {}
    queue = deque((s.lower(), 0) for s in seeds)
    seen = set()
    while queue:
        label, depth = queue.popleft()
        if label in seen or depth > max_depth:
            continue
        seen.add(label)
        row = fetch_ground_state(label)
        raw_csv[label.lower()] = row.pop("_raw_csv")
        z, n, symbol = parse_nuclide(label)
        canonical = f"{z+n}{symbol}"
        node = {
            "id": canonical, "a": z+n, "z": z, "n": n, "symbol": symbol,
            "half_life_sec": finite_float(row.get("half_life_sec")),
            "half_life_raw": row.get("half_life"),
            "half_life_unit": row.get("unit_hl"),
            "decay_modes": [], "stability_status": "not_determined_from_mode_list",
            "source_cutoff": row.get("ENSDFpublicationcut-off") or row.get("ENSDF_publication_cut-off"),
            "source_authors": row.get("ENSDFauthors") or row.get("ENSDF_authors"),
        }
        for i in range(1, 4):
            mode = (row.get(f"decay_{i}") or "").strip()
            pct = finite_float(row.get(f"decay_{i}_%"))
            if not mode:
                continue
            node["decay_modes"].append({"mode": mode, "branching_percent": pct})
            daughter = daughter_for(z, n, mode)
            if daughter is None:
                unresolved.append({
                    "parent": canonical, "mode": mode, "branching_percent": pct,
                    "reason": "Requires evaluated channel/daughter data; no daughter inferred."
                })
                continue
            dz, dn = daughter
            if dz < 0 or dn < 0:
                unresolved.append({"parent": canonical, "mode": mode, "reason": "Nonphysical daughter under simple balance rule."})
                continue
            dsym = symbol_for_z(dz)
            if not dsym:
                unresolved.append({"parent": canonical, "mode": mode, "reason": "Daughter Z outside supported symbol table."})
                continue
            daughter_label = f"{dz+dn}{dsym}"
            edges.append({
                "source": canonical, "target": daughter_label, "mode": mode,
                "branching_percent": pct, "balance_rule": "ground-state A/Z/N bookkeeping"
            })
            if daughter_label.lower() not in seen and depth < max_depth:
                queue.append((daughter_label.lower(), depth+1))
        if node["decay_modes"]:\n            node["stability_status"] = "decay_mode_listed"\n        else:\n            node["stability_status"] = "no_decay_mode_listed_not_assumed_stable"
        nodes[canonical] = node
        sources.append({"nuclide": canonical, "raw_sha256": row["_raw_sha256"]})
        time.sleep(delay)
    return {
        "schema": "gia-timdr-nrg01-graph-v0.1",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "source": API,
        "seeds": list(seeds),
        "scope_note": "Ground-state decay-mode graph; unsupported channels are unresolved, not guessed.",
        "nodes": list(nodes.values()), "edges": edges,
        "unresolved_edges": unresolved, "source_records": sources,
        "metrics": graph_metrics(nodes, edges, unresolved),
    }


def symbol_for_z(z: int) -> str | None:
    # Reverse lookup intentionally shares parse_nuclide's validated table.
    for a in range(max(1, z), max(1, z)+1):
        pass
    symbols = [
        "H","He","Li","Be","B","C","N","O","F","Ne","Na","Mg","Al","Si","P","S","Cl","Ar","K","Ca",
        "Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr","Rb","Sr","Y","Zr",
        "Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I","Xe","Cs","Ba","La","Ce","Pr","Nd",
        "Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg",
        "Tl","Pb","Bi","Po","At","Rn","Fr","Ra","Ac","Th","Pa","U","Np","Pu","Am","Cm","Bk","Cf","Es","Fm",
        "Md","No","Lr"
    ]
    return symbols[z-1] if 1 <= z <= len(symbols) else None


def graph_metrics(nodes, edges, unresolved):
    out_degree, in_degree = {}, {}
    for e in edges:
        out_degree[e["source"]] = out_degree.get(e["source"], 0) + 1
        in_degree[e["target"]] = in_degree.get(e["target"], 0) + 1
    return {
        "node_count": len(nodes), "resolved_edge_count": len(edges),
        "unresolved_edge_count": len(unresolved),
        "branching_nodes_outdegree_gt_1": sum(v > 1 for v in out_degree.values()),
        "terminal_nodes_no_resolved_outgoing": sum(k not in out_degree for k in nodes),
        "max_resolved_outdegree": max(out_degree.values(), default=0),
        "note": "Terminal here means no resolved outgoing edge in this partial graph, not experimentally stable."
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", nargs="+", default=list(SEEDS))
    parser.add_argument("--max-depth", type=int, default=80)
    parser.add_argument("--delay", type=float, default=0.15)
    parser.add_argument("--out", default="experiments/nuclear_reduction/NRG-01/raw/graph.json")
    args = parser.parse_args()
    graph = build_graph(args.seeds, args.max_depth, args.delay)
    target = Path(args.out)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(graph, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(graph["metrics"], indent=2))
    print(f"Wrote {target}")


if __name__ == "__main__":
    main()
