# NRG-01 data ingestion

This folder contains the first executable stage of the preregistered NRG-01 experiment.

## Source and provenance

The downloader uses the IAEA LiveChart CSV API, whose documented endpoint is
`https://nds.iaea.org/relnsd/v1/data`. It requests `fields=ground_states`
for the seed nuclides U-238, Th-232 and Np-237, then follows daughters for
simple, unambiguous ground-state channels. The IAEA notebook documents the
CSV API, the `ground_states` fields (including `z`, `n`, `decay_1` and
branching percentages), and the requirement to supply a nuclide selector for
ground-state data.

The upstream data are based primarily on ENSDF. See:
- IAEA LiveChart API notebook: https://iaea-nds.github.io/lc_api_notebook/
- NNDC ENSDF API: https://www.nndc.bnl.gov/ensdf-api/
- NNDC NuDat 3: https://www.nndc.bnl.gov/nudat3/

## Run

From this directory:

```bash
python src/nrg01_build_graph.py --out results/graph.json
```

The program writes:
- `results/graph.json`: nodes, resolved edges, unresolved channels, graph metrics and source provenance;
- `results/source_csv/*.csv`: exact CSV payloads returned by IAEA for each queried nuclide.

The JSON stores a SHA-256 hash for each raw response. Do not discard the CSV files.

## Important scientific limits

- This is a **ground-state decay-mode graph**, not a complete level-by-level decay scheme.
- Daughter bookkeeping is inferred only for alpha, beta-minus, beta-plus and electron-capture modes.
- IT, spontaneous fission, proton/neutron emission, cluster decay, double-beta and ambiguous channels remain unresolved until channel-specific evaluated data are ingested.
- A nuclide with no decay mode listed is **not automatically labelled stable**. The graph records this as unknown/no mode listed.
- The graph can be incomplete at the selected maximum depth. A terminal graph node is not necessarily a stable nuclide.
- Four graph vertices are not a four-component topological knot. Graph reduction and knot topology remain separate mathematical objects.
- Do not fit the archive's `tau_nuc` hypothesis until this empirical graph has been validated and a preregistered train/test split exists.

## Tests

```bash
python -m unittest discover -s tests -v
```

The tests validate nuclide identity, alpha/beta bookkeeping, and the rule that
unsupported channels are not guessed. They do not validate nuclear data from
the remote API.
