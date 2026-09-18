# GEOMETRY_LAMBDA_FREEZE — Λ_G v0.1

## Status

Operator implementation frozen at code level. This file does **not** claim that the geometry trace is already temporally aligned to META; that mapping remains OPEN until the upstream geometry/time-index pipeline is identified.

## 1. Operator

For a one-dimensional window of mean-curvature samples H:

```text
Λ_G = std(H) / (std(H) + |mean(H)| + eps_G)
```

Implementation:

```text
`TIMDR-Geometry-Formalism/timdr_geometry/weingarten.py::mean_curvature_dispersion`
```

## 2. Exact conventions

- `sigma(H)` = `np.std(H)` with default `ddof=0` (population standard deviation).
- `Hbar` = `np.mean(H)`.
- no hidden normalization of H;
- no clipping;
- no NaN filtering;
- NaNs therefore propagate to the result;
- empty H input raises `ValueError`;
- `eps_G` must be finite and strictly positive;
- frozen implementation value: `EPS_GEOMETRY = 1e-9`.

`eps_G` is an operator parameter and must not be tuned against bridge results.

## 3. H source

`H` is the mean curvature obtained from the discrete Weingarten shape operator:

```text
H = (kappa1 + kappa2) / 2
```

with principal curvatures returned by `discrete_shape_operator`.

## 4. Block handling

The geometry operator does not invent its own time partition.

```text
`TIMDR-Geometry-Formalism/timdr_geometry/weingarten.py::mean_curvature_dispersion_blocks(H_trace, block_slices)`
```

accepts explicit `(start, end)` blocks supplied by the caller and computes one Λ_G per supplied block.

For a valid B bridge comparison, those `block_slices` must be the exact same disjoint blocks used on the META side, and `H_trace` must already be aligned to the same sample index.

## 5. What is CLOSED

- Algebraic form: CLOSED.
- `std`: CLOSED.
- `mean`: CLOSED.
- `eps_G`: CLOSED in implementation (`1e-9`).
- H definition: CLOSED.
- No hidden preprocessing inside the operator: CLOSED.
- Reuse of caller-supplied blocks: CLOSED.

## 6. What remains OPEN

- empirical mapping of geometry observations/timestamps to the META sample index;
- proof that the produced H trace has the same sampling grid as the META trace;
- real-data validation of the complete Λ_G pipeline.

Those are bridge-pipeline questions, not unresolved algebra inside Λ_G itself.
