# CHECKPOINT — chirality and phase-memory research (2026-11-08)

**Restart protocol:** Read this checkpoint, the linked PRs, source and current CI before continuing. A conversation reset is not evidence of a code defect. Distinguish code bugs, incorrect test assumptions, model limits and lost context using commits and logs.

## GitHub state at checkpoint

- GIA-TIMDR protocol: https://github.com/jbackk-lang/GIA-TIMDR/pull/2, draft, branch `proposal/helix-chiral-memory-protocol`, base `proposal/chirality-resolving-operator`.
- Helix-Lock synthetic experiment: https://github.com/jbackk-lang/Helix-Lock/pull/2, draft, branch `experiment/chiral-memory-retention`.
- Helix-Lock chirality operator: https://github.com/jbackk-lang/Helix-Lock/pull/1, draft.
- Helix-Lock CI: https://github.com/jbackk-lang/Helix-Lock/actions/runs/42505701203, 163 tests passed on both Python 3.11 and 3.12.
- Operator branch CI: https://github.com/jbackk-lang/Helix-Lock/actions/runs/42505801696, successful.

## Established in synthetic tests, not in physical theory

- Mirror-coordinate normalization removes apparent left/right phase-memory asymmetry in the tested null model.
- Full-cycle circular averaging has smaller **mean** reference estimation error than a single transition (0.01900644 vs 0.06421710 rad across 100 seeds).
- Orientation-aware full-cycle readout recovers the two-symbol payload in all 100 trials at each of four disturbance magnitudes. Orientation-blind left-handed readout fails in all those trials because of phase-coordinate mismatch.
- Feedback is explicitly imposed using a stored reference; no result proves spontaneous recovery, an intrinsic chirality effect, or any production TSI behavior.

## Diagnosed defects

1. Missing operator helper functions and test imports: actual source/test integration error, fixed and CI validated.
2. Single-seed assertion that averaging must always outperform one sample: invalid statistical test assumption; replaced by paired 100-seed mean test.
3. JSON newline output formatting: code defect, fixed.
4. No evidence whether any defect was caused by missing conversational context after a reset. Do not speculate.

## Next research

Investigate a chirality flip during history acquisition, with per-sample orientation-aware canonicalization versus orientation-blind averaging; test pre/post flip history, matched noise, payload recovery, and phase error. Keep G5 axioms unchanged unless a justified new mechanism emerges. Link future results here and in Helix-Lock.
