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

## Continuation: reversal control

Helix-Lock now has a follow-up synthetic experiment `experiments/helix_chiral_memory_reversal.py` and tests on branch `experiment/chiral-memory-retention`. It tests phase-coordinate handedness reversal mid-history using per-sample versus final-only versus blind normalization. CI run: https://github.com/jbackk-lang/Helix-Lock/actions/runs/42505958517 . Check the run before claiming validation. The experiment does not establish physical chirality-dependent storage.

## New CI and negative control (2026-11-08 17:39+ UTC)

Mid-history reversal Helix-Lock CI https://github.com/jbackk-lang/Helix-Lock/actions/runs/42505958517 passed 177 tests on both Python 3.11 and 3.12. At midpoint reversal, correctly labeled per-sample normalization yielded 100% two-symbol recovery and 0.01900644 rad mean reference error across 100 seeds. Labels were supplied as oracle metadata.

A new `shuffled_labels` control checks whether incorrect label/sample alignment degrades memory reconstruction. CI https://github.com/jbackk-lang/Helix-Lock/actions/runs/42506116845 was pending at checkpoint; verify before claiming results.

## 2026-11-08 17:41+ UTC — new inference experiment

Shuffled-label Helix-Lock CI https://github.com/jbackk-lang/Helix-Lock/actions/runs/42506116845 passed 179 tests on Python 3.11 and 3.12. At midpoint reversal and 100 seeds, correct per-sample labels yield 100% payload recovery (0.01900644 rad error); shuffled labels yield 5% (0.93366167 rad); final-only labels yield 5% (0.85110901 rad).

Added a synthetic phase-continuity Viterbi inference experiment on Helix-Lock branch `experiment/chiral-memory-retention`, module `experiments/helix_chiral_memory_inference.py`. It does not receive per-sample labels or flip boundary; it optionally receives the first-sample orientation as an external anchor. Without such an anchor, global sign symmetry makes absolute handedness/payload unidentifiable. CI https://github.com/jbackk-lang/Helix-Lock/actions/runs/42506276081 was pending at checkpoint.

## 2026-11-08 17:42+ UTC — phase-history inference CI and TSI boundary

Helix-Lock CI https://github.com/jbackk-lang/Helix-Lock/actions/runs/42506276081 passed 183 tests on Python 3.11 and 3.12. With 100 seeds, midpoint flip, and 0.08 rad phase noise, first-sample anchored phase-continuity inference reached 100% label and two-symbol payload accuracy, mean phase error 0.01900645 rad. At 0.4 rad noise, label accuracy fell to 93.25%, payload accuracy to 92%, mean error 0.13252048 rad.

**Do not misinterpret unanchored 100% in the start=+1 benchmark**: the algorithm's deterministic tie-breaking selects a global sign. A globally mirrored latent trajectory yields identical measurements, so absolute chirality and canonical payload are not identifiable without an external sign reference. New mirror-pair tests are pending CI after commit `ceaa942d16695b3bcb67eed3549c4aa7c03f50b2`.

For TSI, distinguish decoding a synthetic phase history from physical information storage in a helical system. A future educational simulator should explicitly expose this global-sign ambiguity and show both mirror-equivalent reconstructions.
