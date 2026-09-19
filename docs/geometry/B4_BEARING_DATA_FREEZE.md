# B4-Bearing data freeze — CWRU 1797 RPM / 12 kHz v0.1

## Status

**INCONCLUSIVE — geometry gate closed.**  The synchronous data and its sample
time mapping are frozen below.  Mean curvature `H_i` must not be calculated
until independently measured sensor coordinates and a valid measured mesh are
provided.

## Frozen recordings

The files are a sparse local copy of the public mirror
[`srigas/CWRU_Bearing_NumPy`](https://github.com/srigas/CWRU_Bearing_NumPy),
which documents the retained DE, FE and BA channels.  Their original source is
the CWRU Bearing Data Center.

```text
dataset_id: CWRU_B4_BEARING_1797RPM_12KHZ_v0.1
sample_rate_hz: 12000.0
sampling_interval_s: 1 / 12000
window_size: 50 samples
time_source: common acquisition sample counter inside one NPZ recording
geometry_time_mapping_source: t_i = i / 12000 for DE, FE and BA in the SAME file
```

The stored source files are:

```text
TIMDR-Industrial-Predict/data/cwru_bearing/b4_raw/source_mirror/Data/1797 RPM/
  1797_IR_21_DE12.npz     SHA-256 4FE4B0198A9EF77E2D249420EBD31C558A82F9D95DB9F9FEF1C26345D88B9C33
  1797_OR@6_21_DE12.npz  SHA-256 068D400E9FE360D6D49B188ACA568FA60A4451128D724868D63F741E1F824C8C
  1797_Normal.npz        SHA-256 4CD7F673ACED17EF1B1253159B32D6C3146BA76AF1B6034B1E18C86AED6C0E26
```

`IR_21` and `OR@6_21` contain synchronous DE/FE/BA arrays.  `Normal` contains
DE/FE only and is admissible as a META reference, not as a three-channel
geometry record.  The recorded timeline is relative to the acquisition; it
does not claim a UTC origin.  No mapping between different recordings is
allowed.

## Why the geometry gate stays closed

CWRU documents accelerometers at the drive-end and fan-end motor housing and,
for some recordings, at the base plate.  It does not provide measured 3D
coordinates or a triangular mesh of the housing in these files.  The three
available channels form at most one triangle.  The discrete Weingarten
operator requires a two-dimensional neighbourhood at every fitted vertex;
one triangle cannot provide it.

Therefore this freeze prohibits all of the following:

- inventing DE/FE/BA coordinates from a diagram;
- adding interpolated vertices to manufacture curvature;
- fitting time offsets between records;
- treating a delay embedding of one channel as branch-G geometry.

## Completion conditions

The B4-Bearing geometry side may be unlocked only with all of:

1. a same-recording measurement with at least four spatial sensor nodes;
2. measured coordinates in one declared unit system;
3. a preregistered closed triangular mesh and channel-to-node mapping;
4. finite, equal-length samples on the frozen `t_i = i / 12000` grid.

Then `timdr_geometry.b4_bearing_data_gate` may admit the record and the
existing `geometry_meta_alignment` path can compute `H_i` and blockwise
`Lambda_G` on exactly the META blocks.  Until then, `n_valid_blocks = 0` and
the B4 result remains inconclusive.
