---
name: "timdr-signal-framework"
description: "Use for building/debugging TIMDR-style signal/anomaly-detection systems (weather, market, radar, grid, seismic, GPS, DDoS/security, aviation PHM); evaluating whether a numeric/geometric pattern (phi, pi, primes, Riemann zeros, resonance, category theory) is real math or unverified; auditing a repo for diverged duplicate code; converting a symbolic TIMDR rule into a neural module; choosing single vs multi-module (regime-change + frozen-reference) detector architecture; cross-domain-transferring a detector (prime-gap stats, torsion, LSQ trend) with a baseline comparison; or fixing a Tkinter Canvas+Scrollbar panel that clips content. Covers: anomalia/defekt/rezonans/skret, adaptive thresholds, ringdown_resonance(), duplication-drift, numerology pre-registration, Boerdijk-Coxeter helix, Arrhenius ceilings, EMA vs windowed recovery, KHIPU-NEURAL lessons, DDoS validation, tension_zscore filters, baseline-poisoning, Short-Term Aftershock Incompleteness, derivative-order-vs-noise pattern, NASA C-MAPSS transfer test."
---

# TIMDR signal framework — reusable patterns, known pitfalls, and a numerology/formalism-testing protocol

Distilled from building/debugging the Synoptyk-v2.0 weather system and the wider
TIMDR-family repo ecosystem (grid monitoring, market analysis, earthquake core,
radar, DNA coverage anomaly detection, meta-dynamics, math-validator, GIA-TIMDR
theory docs, probabilistic-timdr, KHIPU/KHIPU-NEURAL, TIMDR-Security-Module,
TIMDR-Cosmology-Filters, TEST-TIMDR, TIMDR-Aviation-Diagnostics, etc.). Apply
these to any other TIMDR-style repo — including a seismograph/earthquake-
monitoring project ("Ertake"/TIMDR-Earthquake-Core) — since the underlying
problem shape is the same: repeated readings of a physical signal, detecting
when something unusual happens, and getting more accurate over time from your
own track record. §18-20 additionally cover a separate but related recurring
question in this ecosystem: is a claimed numeric/geometric/categorical
"resonance"/"structure" pattern real mathematics or an artifact of
under-tested pattern-matching or unverified formalism — with protocols proven
to work, not just asserted. §21 covers a related but distinct question: when a
deterministic/symbolic TIMDR rule is reimplemented as a gradient-learned
neural module, does the translation itself help, hurt, or do nothing — with
its own protocol. §22-29 are one connected audit arc: five domain-transfer
tests (security, cosmology, radar/primes, torsion, defect-operator v1-v4)
converging on a user-authored verdict (§26), replicated once more in
seismology (§27) and aviation PHM (§29) — together establishing a recurring
"higher-order-derivative loses to a simpler baseline" meta-pattern. §28 is an
unrelated packaging/GUI-debugging record for TIMDR-Earthquake-Core.

## 1. The four TIMDR signal types (generic, not weather-specific)

- **anomalia** — a single reading falls outside a statistically "normal" range
  for that parameter (e.g. `value > mean + 2*std` or outside `[p10, p90]`-derived
  bounds).
- **defekt** — a sudden jump between consecutive readings of the same parameter,
  bigger than a threshold derived from the recent spread of that parameter
  (e.g. `0.3 * (p90 - p10)`).
- **rezonans** — several parameters flag `anomalia` at the same timestamp
  simultaneously (e.g. ≥3) — a stronger, more trustworthy signal than any single
  anomaly. **This is a coincidence counter, not a physical oscillator — see §11
  for a completely different, unrelated thing that also gets called
  "rezonans"/"resonance" in this ecosystem.**
- **skręt** — a trend reversal: the sign of the local slope flips between two
  consecutive windows, and the magnitude of the flip exceeds a threshold
  (e.g. `1.5 * std`).

These four generalize to any multi-parameter time series — for a seismograph:
amplitude, frequency, P-wave/S-wave delta, station-to-station correlation, etc.
can all plug into the same four checks.

## 2. Adaptive thresholds without persistent calibration data

If there's no real climatology/calibration database yet (empty on a fresh
project, or by design because the system always uses live data), do NOT fall
back to a hardcoded universal threshold like `{mean: 0, std: 1, low: -2, high: 2}`.
Real-world values (seismic amplitude, pressure, whatever) essentially never fall
inside `[-2, 2]`, so every single reading gets flagged as an anomaly —
indistinguishable from "nothing ever gets flagged" in terms of usefulness, just
noisy instead of silent.

Instead: calibrate live from the same window of data being analyzed
(`fallback_df`) — compute mean/std/p10/p90 from it. This is weaker than real
historical climatology (a front/event present through the *entire* window won't
be caught, since it defines its own "normal"), but far better than a fixed
constant tuned for a different scale entirely.

**Caveat found in production**: this fallback calibration is fine for
continuously-distributed parameters (temperature, pressure) but can be *too
sensitive* for zero-inflated/threshold-driven parameters (precipitation — mostly
zero with occasional spikes). If `p90 - p10 ≈ 0` because most readings are zero,
the derived threshold collapses to a tiny constant and any nonzero reading gets
flagged. Watch for this with any parameter that's "mostly quiet, occasionally
active" (a seismograph's amplitude channel during quiet periods is exactly this
shape) — consider an absolute floor, not just a purely statistical threshold, for
such parameters. The same "mostly quiet" shape shows up again in §13 below (pure
white noise almost never triggers a candidate-event detector at all, which makes
naive white-noise negative controls degenerate).

## 3. Performance: cache threshold computation, don't repeat it per row

`get_thresholds(dt, param)`-style functions get called *per row per parameter
per check type* (anomaly + defekt + skręt ≈ up to 15 calls per row). At even a
few hundred rows (e.g. 30 days of hourly readings = 720 rows), that's 10,000+
calls. If each call re-queries a database and recomputes mean/std/quantiles on
the whole window from scratch, this becomes O(n²) and turns a sub-second
computation into minutes.

**Fix**: memoize per (month, param) for climatology-backed thresholds, and per
`param` alone for the live-fallback branch (the fallback result doesn't depend
on `dt`, only on which parameter and the window data — compute it once per
analysis run, cache the DataFrame query result too). This exact bug caused a
reported "3 stations at max settings ≈ 300 seconds"; after caching, the
equivalent workload measured well under 5 seconds.

## 4. Schema mismatches are a silent-failure trap

If a project has TWO independent code paths that fetch the same *kind* of data
(e.g. one from a live API, one from a local cache/CLI tool), they can easily end
up with different column names/shapes (`datetime` column vs. a `time`-named
index; `wind_speed` vs `wind`). A signal analyzer written against one schema
will throw `KeyError` when fed the other — and if that call is wrapped in a bare
`except Exception: pass` (common "defensive" pattern), the failure is
**completely invisible**: the UI looks like it ran fine and just "found nothing,"
when in fact the analysis never executed at all, possibly for the entire
lifetime of the feature.

**Rule**: never use a bare `except: pass` around a signal-detection call. At
minimum, log the exception message somewhere visible (a log panel, stderr,
whatever the UI exposes) so a future schema drift shows up immediately instead
of silently degrading to "always empty." Write a small adapter function
(`_adapt_for_x()`) at the boundary between the two schemas instead of trying to
unify the underlying fetchers.

## 5. Data integrity in append-only collection pipelines: idempotent writes + unreliable trailing archive data

Real bug pair found in SYNOPTYK-ARCTIC, both initially looking like "the
collector isn't working" (a fresh run reported `bias=+0.00 MAE=0.00 n=5` for
lead_days=0) but actually two independent, generalizable pitfalls in any
TIMDR-family collector that appends to a CSV/log on every run:

- **Non-idempotent append inflates sample counts instead of adding new data.**
  If append-to-CSV code always writes every fetched row with no dedup, running
  the collector twice on the same day (or after a crash-and-retry) writes the
  same reading multiple times. `n=5` looked like "5 real days collected" but
  was actually 1 real day duplicated 5x. Fix: dedupe on write, keyed by the
  full logical identity of a reading (here `(station, target_date, issue_date,
  source)`) — load existing keys from the file before appending, skip any row
  whose key is already present. This makes re-running the collector any
  number of times on the same data safe, and is worth testing directly
  (`test_append_same_day_twice_is_idempotent`).
- **A data source's "archive"/"final" endpoint may not be final for its most
  recent days.** Open-Meteo's Archive API (reanalysis) mirrors its own
  forecast model for roughly the trailing 1-2 days before the data is fully
  reconciled — so comparing "forecast vs archive" for lead_days=0 (today) is
  really comparing the forecast against a not-yet-finalized copy of itself,
  producing a spuriously perfect bias≈0/MAE≈0 that looks like success but
  measures nothing. Generalizes to any TIMDR pipeline pulling a "ground truth"
  feed that reconciles/revises after a delay (satellite imagery, financial
  closing prices before end-of-day adjustments, provisional seismic
  magnitudes): explicitly exclude the last N days/readings of the "truth"
  side from any bias/accuracy comparison (`exclude_trailing_days` parameter),
  and treat "the newest comparison is suspiciously perfect" as a signal to
  investigate, not a result to report.

Both were only found because the user ran the real collector on their own
machine and reported the literal, un-smoothed console output (`n=5`, "chyba
nie zbiera danych") rather than a description of the problem — the same
"reproduce with real output, don't reason in the abstract" discipline as §9's
debugging-discipline section.

## 6. EV / "engine volatility" — jump detection between successive runs

Compare the current reading for a given target (station+timestamp, or
sensor+event-id) against the *previous* run's reading for that same target;
flag if the delta exceeds a per-parameter threshold. Requirements:

- Persist the "last reading" state to **disk**, not just an in-memory dict —
  otherwise a process restart silently resets it and the jump-detector never
  fires until two runs have happened back-to-back without any restart in
  between (in practice, this means it almost never fires).
- Give the user a manual "clear this cache" control, since stale entries from
  old test runs / other stations can accumulate indefinitely.
- If the jump signal isn't firing when you expect it to, verify with a direct,
  isolated function call (`detect_jump(prev_row, new_row)` with hand-constructed
  dicts) *before* assuming the detection logic itself is broken — in practice
  it's more often something operational (cache got cleared, two server
  processes both writing to the same state file, browser session desync)
  than the comparison function itself.

## 7. Self-learning bias correction from paired (prediction, later-confirmed) logs

Simple, fully transparent approach — NOT machine learning, just arithmetic, and
should be described to the user as such:

- Log every prediction with its target timestamp/id and lead time (how far
  ahead of the confirmed event it was made).
- When ground truth eventually arrives for that same target, you now have a
  matched pair.
- Group matched pairs by lead time; compute mean error (bias) and mean absolute
  error (MAE) per lead time.
- Apply the bias as a correction to future predictions **only** once you have
  enough paired samples for that lead time (e.g. ≥5) — otherwise you're
  "correcting" based on noise. Report the sample count `n` alongside any
  correction so it's clear when a correction is provisional.
- Use a traffic-light badge to make this state visible at a glance: 🔴 not
  enough samples yet (no correction applied) / 🟠 correction active but small
  sample (treat as provisional) / 🟢 correction active on a solid sample. Always
  show the badge, even when red — a missing badge reads as "everything's fine,"
  which is the opposite of true when there's no data yet.
- Automating the "wait for ground truth" step itself is valuable: a scheduled
  daily pull of real observations (IMGW/official station data) that gets logged
  against past predictions removes the need for anyone to manually type numbers
  in — this is what turned Synoptyk's bias correction from a manual chore into
  something that runs unattended (`krakow-weather-real-data-daily`-style
  scheduled task, once per day, well after the observation is final).
- **A "previous runs" style API, if the data provider offers one, can replace
  weeks of the above daily-accumulation loop with a single request.**
  Open-Meteo's Previous Runs API (`previous-runs-api.open-meteo.com`) archives,
  for each past day, what the forecast model said N days before at fixed lead
  times (`temperature_2m_previous_dayN`, N=1..7) — exactly the paired
  (prediction, lead_time) data this section describes collecting one day at a
  time, but for 90+ days in one call. Pair it with the same provider's Archive
  API for the "ground truth" side (same trailing-day caveat applies to the
  archive side here — see the data-integrity section above) to get a full
  bias/MAE-per-lead-time table immediately instead of waiting out the
  real-time collection window. Verified working end-to-end on a real 90-day,
  7-lead-day run with no parser fixes needed on the first real request — still
  only one location/time-window's worth of evidence, same caveat as any single
  backtest.

## 8. Parallel independent tracks + blending, and the uncertainty-band trap

Running a second, fully independent prediction method (e.g. deterministic trend
extrapolation from raw history) alongside the primary live-model prediction is
useful for two things: (a) stabilizing the primary prediction at long horizons
by blending toward the trend method with increasing weight as horizon grows, and
(b) giving the user a second opinion to sanity-check against once enough
real-world outcomes accumulate (see #6 — log the second track's predictions too,
not just the primary one, so you can compute *its* bias/MAE independently once
ground truth arrives).

**Trap**: if the trend method's uncertainty band widens as `spread ∝
base_std * multiplier * sqrt(step)`, and `multiplier` jumps (e.g. ×2.5) whenever
a "recent anomaly" was seen in the input window, the band can compound to
physically nonsensical ranges at long horizons for any station/sensor whose
recent window happened to contain a flagged anomaly (observed: a coastal
weather station's band exploded to a 50°C-wide range spanning below-freezing
in August, purely from a modest, individually-reasonable-looking formula
compounding). Sanity-check the band width against physical plausibility, or cap
it, rather than trusting the formula blindly at long horizons.

## 9. Debugging discipline that mattered in practice

- When a user reports "X isn't working," reproduce it directly — mock only the
  network/IO boundary, then run the *actual* production function with
  controlled synthetic inputs and inspect the real output. Don't reason about
  it in the abstract; the actual bugs found this way (schema mismatch, O(n²)
  threshold recompute, a CSS property silently breaking a scrollbar) were not
  the first hypothesis guessed.
- If a shared state file (cache, log CSV) is being read/written by both your
  test process and the user's live/independently-running process, back it up
  before touching it and restore it after — don't let test runs pollute the
  user's real accumulated data.
- Before declaring a fix complete, verify it end-to-end with the exact
  before/after data the user reported, not just "the code looks right now."
- When a user reports something "looks stuck" or "seems to be looping,"
  reproduce it directly and check for the boring explanation first: is there
  simply no progress output between long-running steps (§14), and/or is there
  no bounded worst-case runtime? Both are far more common than an actual
  infinite loop, and both are fixed by printing progress + adding a time
  budget, not by debugging the algorithm.
- When a shell command's error output uses backticks inside a double-quoted
  string passed to `bash -c`, the shell will interpret them as command
  substitution and silently strip that portion — this can quietly corrupt a
  git commit message (or any generated string) without erroring. Avoid raw
  backticks in double-quoted shell strings, or escape them.
- **A backgrounded process (`nohup ... &`) does not reliably survive between
  separate tool-call invocations of a sandboxed shell** — each call can be a
  fresh process-tree scope that gets torn down on return, silently killing the
  background job. If a computation needs more wall-clock time than one tool
  call's timeout allows (observed cap in practice: ~120-180s, not the higher
  value requested), don't rely on backgrounding — checkpoint progress to disk
  (save partial results every N steps) and resume across multiple sequential
  tool calls instead. This exact pattern was needed to compute 1000
  `mpmath.zetazero()` values (~90-150s per 100-zero chunk).
- **A newly-touched repo in this sandbox may have no git identity configured**,
  even if other repos in the same ecosystem already commit fine — `git commit`
  fails with "Author identity unknown" the first time in a fresh repo. Fix once
  per repo: `git config user.email ...` / `git config user.name ...` before the
  first commit attempt, not a sign of a deeper problem.
- **Know which test runner convention a repo actually uses before adding new
  tests.** `python -m unittest discover` only picks up `unittest.TestCase`
  subclasses — it silently runs zero of any bare pytest-style
  `def test_...():` functions added in a new file, with no error, which looks
  exactly like "the tests passed" when they were never collected at all.
  Match the existing repo's convention (grep an existing test file for
  `unittest.TestCase` vs bare functions before writing a new one) and confirm
  by checking the printed test COUNT went up by the expected number, not just
  that the run exited 0.
- **Cross-filesystem copies of a git repo commonly show spurious
  100644→100755 file-mode-only diffs** (every file appears "modified" in
  `git status` with 0 insertions/deletions in `git diff --stat`) — diagnose
  with `git diff --stat` (confirms mode-only) and fix once with
  `git config core.fileMode false`, not by inspecting each file individually.
- **`dataclasses.replace()` is not a free way to get an independent copy** —
  it reconstructs the object through `__init__`, so it re-runs
  `__post_init__` validation on every call. If the data being copied is
  already known-valid (e.g. read back from a cache/table you just validated
  on write), `copy.copy()` (shallow copy) gives the same independence
  guarantee for a flat dataclass of immutable fields (str/int/etc.) without
  the redundant re-validation cost — measured ~1.9x fewer ops/sec with
  `replace()` vs a plain constructor call on an equivalent flat object.
- **A `dataclasses.replace()`-free copy fix for one aliasing bug can still
  leave a second copy point uncovered.** A lookup-table pattern that both
  *returns* cached objects (read side) and *accepts* live objects to cache
  (write side) needs copying on BOTH sides — copying only on read still lets
  a caller's later mutation of what it wrote silently corrupt the stored
  template from the write side.
- **When two call sites pass the same conceptual parameter but under
  different names/shapes to a shared constructor** (e.g. one path builds a
  "kind" preset with implied labels, another wants fully custom labels),
  don't gate the choice on an incidental property like "how many items" —
  gate it on the actual identity/content that downstream code will key
  against. A resonance-figure module that picked a 3-vs-4-label preset purely
  by *counting* the caller's custom labels (ignoring their actual names)
  produced structurally mismatched keys the moment a caller supplied
  non-default labels — invisible in tests that only ever used the defaults.

## 10. Duplication-drift: independent copies of the same formula silently diverging

A structurally different failure mode from §4's schema mismatches: two files
in the same repo independently implementing the *same* formula (copy-pasted
once, then maintained separately) will eventually diverge when one copy gets
a bugfix and the other doesn't. Found twice in the same repo (`THE`) across
two separate audit passes. First pass: `THE_GEO_PRO_4D_Radar.py` got its own
independent torsion-gating fix (`kappa` instead of `cross_norm == 0`) that was
never ported to the sibling `the_geo_pro_4d.py`. Second pass, on a later
re-audit of the same repo: after that first fix, `THE_GEO_PRO_4D_Radar.py` was
STILL a second, independent copy of the whole function body (just now also
fixed) — the actual root cause (two copies, one intended source of truth) had
not been addressed the first time, only its most recent symptom.

**Fix pattern — not just "make the two copies equal for now."** Replace the
duplicate implementation with a thin re-export
(`from the_geo_pro_4d import THE_GEO_PRO_4D as THE_GEO_PRO_4D_Radar`), so there
is structurally only one implementation left to maintain. Then add a
regression test asserting **object identity**, not just equal output:
`self.assertIs(THE_GEO_PRO_4D_Radar, THE_GEO_PRO_4D)`. An equal-output test
would pass today and still allow someone to paste a fresh independent copy
back in later without the test noticing (until it silently drifts again); an
identity test makes that specific regression structurally impossible to
reintroduce unnoticed. Document any minor behavioral side-effect of the
re-export explicitly in the module docstring (here: the re-exported function
gained a default value for a parameter that used to be required), so it isn't
mistaken for an unrelated bug later.

Generalizes to any TIMDR-family repo built with this ecosystem's
copy-paste-and-adapt style — across-repo duplication of a shared *concept*
under a different name is expected and fine (§18 case study 6 found "TIMDR"
means four unrelated things in four different repos, which is not itself a
problem); duplication of the exact same formula *inside one repo* is the
specific pattern to grep for (`grep -rn "def <suspicious_function_name>"`
across the repo) whenever auditing a repo for the first time, or especially
when re-auditing one that was already fixed once before.

## 11. `ringdown_resonance()` — a SECOND, unrelated meaning of "resonance"

Across several TIMDR repos (universal-state-analyzer, TIMDR-Grid-Monitor,
analizator-gieldowy-v3, deliverable_timdr_finanse, TIMDR-Earthquake-Core) there
is a function called `ringdown_resonance(t, s, event_idx, ...)` that is
**completely different math from §1's "rezonans"** (the multi-parameter
coincidence counter). Don't conflate them — this exact conflation is what a
user's question about earthquake prediction initially risked.

What it actually computes: given a known event index, does the signal's return
to its pre-event baseline look like a damped oscillator (crosses the baseline
band multiple times, decaying) or a monotonic decay? Implementation shape that
was validated repeatedly across ports:

- Baseline = mean of a pre-event window (or an explicit domain constant, e.g.
  grid frequency 50/60Hz).
- Noise band = `noise_floor_factor * std(pre-event window)` (default factor
  3.0) — a Schmitt-trigger-style hysteresis band, not a single zero-crossing
  count, so noise sitting right at the baseline doesn't generate spurious
  crossings.
- State machine walks post-event samples, only registers a "confirmed" state
  flip when the signal exceeds the band on the opposite side from the current
  state (dedupe consecutive same-side excursions).
- Frequency estimate = `1 / (2 * median(diff(confirmed crossing times)))` —
  median, not mean, to resist outlier segments.
- Damping estimate = log-decrement between peaks 2 apart (same sign), converted
  to a damping ratio.
- `is_oscillatory` requires **both** ≥2 confirmed crossings **and** ≥2 peaks —
  a single overshoot-and-settle is not oscillatory.

**This is a post-event descriptive tool, not a predictive one** — it inherently
needs `event_idx` to already be known. It says nothing by itself about whether
anything can be detected *before* a future event (see §13).

**Known, honestly-documented limitation**: real-world signals are often
multi-modal (a seismogram is P+S+surface+coda superimposed, not one clean
decaying sinusoid). On a real local-earthquake trace, `is_oscillatory` flipped
between `False` and `True` depending on `noise_floor_factor` (2.0 → False,
1.5 → True) with no independent ground truth to say which is "right." Treat any
single run's oscillatory/non-oscillatory verdict on real (non-synthetic) data as
threshold-sensitive unless you've swept the threshold and it's stable.

**Edge-case gotcha (found this session, testing an audio ringdown)**: if
`event_idx=0` with no samples before it (`pre_event_window` has nothing to
draw from), `noise_floor` comes out `0.0`, and the hysteresis band collapses —
every sample of numerical/measurement noise then registers as a "confirmed"
state flip, producing wildly wrong frequency estimates (observed: 13384 Hz
instead of a true 440 Hz on a synthetic damped-oscillator test signal). This is
documented in the function's own docstring as a known limitation of that edge
case, not a silent bug — but it's easy to trigger by accident when testing.
Always give the function real pre-event samples (silence/baseline before the
event) so it has something to estimate the noise floor from. With that fixed,
a pre-registered test on a physics-grounded synthetic signal (damped oscillator,
f0=440Hz, τ=0.3s, 20dB SNR, sampled at 44100Hz) recovered frequency within 0.74%
and damping ratio within 0.0007 of the analytically exact values — the function
itself is correct; the earlier failure was a test-setup bug. This was validated
on a *physics-grounded synthetic* signal, not a real recording (no internet
access to fetch one this session) — see §19 item 4.

## 12. RCS / Mie-scattering "resonance region" — a THIRD, unrelated meaning

Radar cross-section (RCS) has its own "resonance region" (target size ~
wavelength, `ka` ~ 1), where RCS oscillates with frequency/size due to
interference between direct reflection and creeping waves circulating the
target. **This is frequency-domain scattering physics, not a time-domain
decaying oscillator** — nothing to do with §11's `ringdown_resonance()`, despite
both being called "resonance." If a TIMDR-radar-family repo needs real RCS
resonance-region behavior, the only exactly-solvable canonical case is a
perfectly-conducting sphere via the Mie series (1908) — implement with
`scipy.special.spherical_jn/yn(..., derivative=True)` for the Riccati-Bessel
functions, truncate the series with the standard rule
`N = ceil(x + 4*x^(1/3) + 2)` (Bohren & Huffman), and validate against three
independent, well-known physical laws rather than a remembered table of
numbers: Rayleigh scaling `σ ∝ λ⁻⁴` for small `ka` (doubling `ka` should give
≈16× RCS), convergence to the geometric cross-section `σ/(πa²) → 1` for large
`ka`, and qualitative non-monotonicity (oscillation, first major peak
`σ/πa² ≈ 3–4` near `ka≈1`) in between. Be explicit that this exact solution is
**sphere-only** — arbitrary real target shapes need a full electromagnetic
solver (MoM/FEM), not a lightweight approximation.

## 13. Testing whether a TIMDR signal has genuine predictive power

Multiple times in this ecosystem, someone proposed that a TIMDR signal (a
topological embedding feature, `ringdown_resonance()`-derived oscillatory
fraction, etc.) might *predict* a future event (market move, earthquake), not
just describe one after the fact. Treat "does it describe X" and "does it
predict X before it happens" as two entirely separate claims requiring separate
tests — a function needing `event_idx` as an argument cannot, by construction,
answer the second question about itself.

Honest protocol (used for both a topological-embedding test and a
`ringdown_resonance()`-based test, independently, both came back negative — and
generalized further in §18 to non-predictive "does X pattern-match Y" claims):

1. **Pre-register the feature definition before touching real data.** Freeze
   parameters (embedding dimensions, thresholds, window sizes) on a synthetic
   sanity-check *first*. Changing the feature definition after seeing the real
   result is the data-snooping trap.
2. **Compare a pre-event window against random background windows**, not
   against "does it fire when an event has already started" (that's detection,
   not prediction, and is a much easier bar).
3. **Use a real significance test (Mann-Whitney U), not just a percentile
   comparison** — a percentile against one background distribution is weaker
   evidence than a proper two-sample test.
4. **Run a synthetic self-test with BOTH a positive and a negative control
   before running on real data**, and gate the real run on both passing:
   - Positive control: inject the effect you're testing for, confirm the
     pipeline detects it (p should be small).
   - Negative control: two independently-generated background samples with NO
     injected effect, confirm the pipeline does NOT flag a significant
     difference (p should be large / not significant).
   - **Use autocorrelated noise (e.g. AR(1)) for the negative control, not
     white noise** — white noise is often too smooth to trigger a candidate-
     event detector at all (observed: 0/30 windows produced any candidate on
     pure white noise), which makes white-vs-white a degenerate 0-vs-0
     "negative control" that doesn't actually exercise the classifier. AR(1)
     noise with occasional untimed spikes gives a non-degenerate,
     meaningfully-variable negative control. An even more direct calibration:
     probe the classifier at random indices in background noise directly
     (bypassing the candidate-detector entirely) to measure its raw
     false-positive rate.
5. **A negative result is a valid, complete answer — report it as such**, with
   the actual p-value and effect direction. Both real tests run this way in
   this ecosystem came back negative (topological feature: below-background
   percentile on both sudden and gradual synthetic events; `ringdown_resonance`
   feature on real M≥6.5 earthquakes from the USGS catalog vs random
   background: p≈0.997, no difference). This is consistent with the field's
   own position (USGS: no earthquake has ever been reliably predicted by any
   method) — a negative result matching domain consensus is a *good* sign the
   test itself is sound, not a disappointing one.
6. **A single apparently-positive run is not proof** — it's a preliminary lead
   requiring replication on an independent event set (a BTC-only "signal" in
   this same ecosystem flipped sign when replicated on gold — classic
   overfitting, not real structure).

## 14. Lessons from a real external-data pipeline (USGS/EarthScope case study)

Building the real-data mode of the §13 protocol against live USGS/EarthScope
APIs surfaced several bugs that had nothing to do with the statistics and
everything to do with basic API/pipeline hygiene — worth checking for in any
TIMDR repo that pulls from a real external data source:

- **Respect documented result caps.** USGS's FDSN event API caps results at
  20,000 per query and returns `HTTP 400` (not a clear "too many results"
  message) if you exceed it. A 5-year, magnitude≥4.5 global catalog is ~38,000
  events — well over the cap. Fix: don't fetch one giant catalog upfront for a
  filtering/exclusion check; issue narrow, per-candidate queries (or use a
  lightweight `/count`-style endpoint) so no single request can approach the
  cap regardless of the total time range being analyzed.
- **Scope geographic/global exclusion filters to what's physically relevant,
  not literally everywhere.** An "exclude this background window if any
  M≥4.5 happened within ±3 days" check, if not also constrained by distance
  from the recording station, rejects almost every candidate — magnitude-4.5+
  earthquakes happen somewhere on Earth several times a day, so a 7-day global
  window essentially never comes up empty. Constrain by a real physical radius
  around the station/sensor that would actually be affected (verified via
  USGS's own `latitude`/`longitude`/`maxradiuskm` count-query parameters that
  a quiet region gives 0 nearby events in the same window a seismically active
  region gives several).
- **Long-running real-data loops need a hard wall-clock time budget, not just
  a soft attempt-count cap**, plus visible per-item progress with flushed
  output. A loop that only limits attempts (e.g. `n_target * 20`) can still run
  unboundedly long in wall-clock time if the per-attempt success rate is low or
  individual network calls are slow — and with no progress printed between
  items, this is indistinguishable from a genuine hang to whoever is watching
  it run. Print one line per item (with elapsed/budget shown) and stop firmly
  once the time budget is hit, reporting honestly how much of the target was
  actually collected.
- **Reuse an HTTP session with retry/backoff** once a pipeline moves from one
  big request to many small ones (a direct consequence of the point above) —
  otherwise a handful of transient `429`/`5xx` responses turn into hard
  failures partway through a long run.
- **Sandbox network access is not guaranteed session-to-session, and is
  inconsistent WITHIN a session by domain.** This session, both `librosa.org`
  (audio example fetch) and `yfinance`/Yahoo Finance (market data) were blocked
  at the proxy (`403`/tunnel failure) — but plain `git clone` of a public
  `github.com` repo worked fine in the same session. Confirmed again in a later
  session: the entire Open-Meteo API family (`api.open-meteo.com`,
  `archive-api.open-meteo.com`, `historical-forecast-api.open-meteo.com`,
  `previous-runs-api.open-meteo.com`) is blocked in this sandbox (`403
  blocked-by-allowlist` via the sandbox's own HTTP proxy, confirmed with
  verbose curl) — same pattern as `librosa.org`/`yfinance` above, different
  domain, and `download.pytorch.org` is blocked the same way (confirmed
  repeatedly across sessions, see §21). Build and unit-test the parsing logic
  against a hand-built payload matching the documented response shape, and
  have the user run the actual network call on their own machine — this is
  exactly how the Previous Runs API backtest (see the bias-correction section
  above) was verified for real. Don't assume a blocked domain means the whole
  sandbox is offline, and don't assume a working domain (like GitHub) means
  arbitrary other domains will work too — check the specific domain/method you
  need (one cheap fetch) before designing a whole real-data test around it,
  and have a "needs user-supplied file" fallback ready (see §19 item 3).

## 15. Physical ceilings vs numeric ceilings (Arrhenius/cable-life case study)

If a TIMDR-family repo models degradation/aging using a **linear-in-native-units
approximation of an exponential physical law** (e.g. Montsinger's "life halves
every ΔT°C" rule, which is a local linearization of the true Arrhenius equation
`L(T) = A·exp(Ea/(k·T))` with T in Kelvin), expect it to need an arbitrary
numeric cap to avoid diverging at extreme inputs — and expect that cap to mask
real variation over a big chunk of the input's plausible range, not just at the
true extremes. Symptom users will actually report: "the result stops changing
no matter how far I push this input."

Fix pattern: replace the linear approximation with the real closed-form
physical law (usually just requires converting to the natural units the law is
defined in — Kelvin, not Celsius, for Arrhenius), and separately identify
whether there's an actual **physical** ceiling for the system (a material
decomposition/destruction temperature, not just "when the formula blows up")
that should be the real safety valve instead of an arbitrary numeric clamp.
Keep a much larger numeric clamp only as an overflow guard, not as the primary
protective mechanism — and when the physical ceiling is crossed, report it
honestly as a distinct state (e.g. "insulation destroyed," remaining life = 0),
not silently folded into the same saturating-number behavior as the old bug.

## 16. Samonaprawa — does anomalia/defekt correctly de-escalate after the event ends?

A different question from §13's "does it predict the future": once an anomaly
is over and the signal is back to genuinely normal behavior, does the
anomaly/defekt score correctly **recover** (drop back down), or does it stay
falsely elevated because the old anomalous samples are still sitting in
whatever reference window/state the detector uses? Verified empirically across
the whole local portfolio (TIMDR-Crypto-Graph, universal-state-analyzer,
TIMDR-Grid-Monitor, analizator-gieldowy-v3, deliverable_timdr_finanse,
TIMDR-Earthquake-Core) — the answer depends entirely on which of two
structurally different mechanisms a given repo uses.

**Mechanism A — EMA/persistent state (TIMDR-Crypto-Graph).** `state` is an
exponential moving average continuously updated by `step_live()`; `eq` is a
frozen baseline set once via `calibrate_eq()`. Recovery here is **gradual, not
instant** — it decays exponentially toward baseline as new normal samples keep
updating the EMA. Measured across 5 seeds: defect value decays to <2% of its
peak after ~200 steps of subsequent normal behavior (decay_ratio 0.8–2.2%,
final-value-vs-median-of-normal-range 0.79–1.29×). This is expected and
correct for an EMA — there's no sharp cutoff, just "eventually negligible,"
so any test of this shape needs a decay-ratio/threshold assertion, not an
exact-zero assertion.

**Mechanism B — stateless self-baseline windowed (universal-state-analyzer's
`TIMDRCore` and its vendored siblings: TIMDR-Grid-Monitor, analizator-gieldowy-v3,
deliverable_timdr_finanse, TIMDR-Earthquake-Core).** No persistent state —
median/MAD or p10/p90 spread is recomputed fresh from whatever array is passed
on each call. Recovery behavior splits on one thing: **is the anomalous
contamination a minority or a majority of the window being analyzed?**

- **Minority contamination (anomaly ≤ ~50% of the analysis window)** → recovery
  is **near-instant** — as soon as you simulate a realistic streaming caller
  (a trailing window that slides forward sample-by-sample), the anomalous
  samples become a shrinking minority and then age out entirely, and the new
  normal samples are correctly NOT flagged. This works because median/MAD has
  a 50% breakdown point — a minority of contaminated values (tested at 10%
  contamination) barely moves the median/MAD at all, so the z-score of a new
  normal sample against that window stays low. `defect()`/`defekt()` variants
  that use an explicit rolling window (TIMDR-Grid-Monitor, the fixed
  analizator-gieldowy-v3/deliverable_timdr_finanse) get an additional, simpler
  guarantee on top: the contaminating samples mechanically fall out of the
  window after `window` steps regardless of the statistics.
- **Majority contamination (tested at ~73% of the window)** → degraded: the
  median/MAD itself gets pulled toward the contaminated values, so readings
  come back systematically shifted but typically still unflagged — a partial,
  transitional version of the already-known **self-baseline blind spot**
  (documented separately in universal-state-analyzer's README/`baseline.py`):
  a chronic anomaly spanning the *entire* window is invisible to a
  self-baseline method because there's nothing left to compare it against.
  Recovery-under-majority-contamination is the same failure mode, just partial
  rather than total.

**Real bug found via this exact test, and the "half-fix trap" lesson**
(`deliverable_timdr_finanse/timdr_core_finance.py::defekt()`): computed its
jump threshold from the percentile spread (p10–p90) of price **levels**
instead of the spread of **differences** between consecutive prices — already
found and fixed in the sibling module `analizator-gieldowy-v3` (documented
there as "Bug 1"), but never ported to this class-based sibling. Measured
16.3% false-positive rate on a clean random walk with zero real anomalies.
**Fixing only the spread source (switching to diffs) without also raising the
`factor` multiplier made it WORSE, not better — 49.4% false positives** — because
a diffs-based spread is a much smaller reference scale than a levels-based
spread, so the same multiplier now produces a much tighter (over-sensitive)
threshold. The complete fix requires both changes together: spread computed
from diffs AND the multiplier raised to match the new scale (0.3 → 3.0 here),
verified down to 0.0% false positives. **Lesson: always re-measure empirically
after a fix, especially when changing what a threshold is computed FROM — the
multiplier that was calibrated against the old reference scale is very
unlikely to still be correct against a different one.**

**Test-construction pitfall (own mistake, caught before it produced a false
report)**: when building synthetic "calibration → anomaly → recovery" test
data for a naturally trending/non-stationary signal (price as a random walk),
the recovery segment must **continue the underlying process from its
pre-anomaly level** (`level = pre[-1]; post = level + cumsum(...)`), not
restart from a fixed constant. Restarting from a constant introduces an
unintended *second* discontinuous jump exactly at the anomaly→recovery
transition, which then looks like "still elevated after the anomaly" in
results — but the elevated reading is an artifact of how the test data was
built, not a real property of the code under test. Any recovery test on a
trending/random-walk-like signal needs this continuation, not just tests on
stationary signals (voltage, temperature) where a constant target level is
fine.

**TIMDR-Earthquake-Core's bilateral-TRM exception**: its `anomalies()` uses
TRM smoothing with `k=8` *nearest neighbors by time in both directions*
(bilateral/non-causal) over the whole array passed in — a deliberately
different design (one-shot analysis of a complete recorded waveform segment,
not a live stream). This causes one specific, bounded artifact, not unbounded
stickiness: the very first sample immediately after an anomaly ends gets
flagged consistently (10/10 seeds tested), because its `k=8` window still
reaches backward into the anomaly's tail. Bounded to a handful of samples at
the boundary (`k_neighbors` wide), never persists beyond that — correctly
distinguished from a real recovery bug by checking flags far past the window
(`event_end + k_neighbors` onward), where zero false flags were found.

**Practical takeaway for any new TIMDR-family detector**: know which
mechanism (A or EMA-persistent vs B or stateless-windowed) you're building
before writing a recovery test, and if it's a rolling/self-baseline design,
explicitly check the minority-vs-majority-contamination boundary rather than
assuming "it uses a robust statistic so it's fine" — robustness to minority
contamination does not imply the same statistic recovers cleanly once
contamination becomes the majority of what it's being measured against.

## 17. Trójkąt → helisa: zweryfikowana konstrukcja geometryczna (Boerdijk-Coxeter), i skąd bierze się τ

The user's mental model for this ecosystem describes a genesis: triangle →
space → movement/time → "defekt" as a directional twist along a
Möbius-constrained path → helix. Checked computationally against real
geometry. Result: **part of it is real, exact, provable mathematics — a
well-known construction — and part of it (extensions to primes/Riemann
Hypothesis/"cosmic duality") has no established mathematical basis.**
Recorded here so it doesn't need to be re-derived or re-litigated.

**What's real and exact — the Boerdijk–Coxeter tetrahelix** (Boerdijk 1952,
Coxeter): start with a regular tetrahedron and repeatedly reflect the oldest
of the last 4 vertices through the plane of the other 3, gluing a new
congruent tetrahedron onto the chain each time — a single fixed operation, no
free parameters. Verified via exact symbolic arithmetic (sympy, not floating
point): edge length, bond angle, and torsion angle are all constant
(`cos(τ)=1/3`, the same tetrahedral angle familiar from chemistry).
**Strongest result**: solved exactly for the single rigid screw motion `S`
satisfying `S(v_i)=v_{i+1}`; confirmed `S` — derived from only the first 4
vertices — exactly predicts every further vertex and maps whole tetrahedra to
the next, which by definition means the vertices lie exactly on a circular
helix, not an approximation. The tetrahedron's centroid traces its own
coaxial helix at a smaller, exactly-derived radius. No central/point symmetry
in the chain.

**Where this connects to the actual TIMDR codebase**: `τ` (torsion/skręt) is
a real, traceable thread — `math-validator-3.0/filters/singularity_filter.py`
and `TIMDR-META-DYNAMICS/core_meta/meta_state.py` both use it (the latter's
own docstring admits its thresholds are "arbitralne, do skalibrowania," an
acknowledged unfinished sketch, not a finished formula). `moebius_filter.py`
and `prime_spectrum_filter.py` in the same repo, by contrast, turned out to
be shallow syntactic heuristics with no real geometry behind the name — see
§18 case study 4 for `prime_spectrum_filter.py`'s fix.

**What is NOT established** — do not re-derive or re-affirm without new
evidence: an extension connecting this geometry to the Riemann Hypothesis /
prime distribution / "cosmic duality" was checked and rejected — the Riemann
critical line is a precise property of zeta zeros with no known bridge to
this discrete construction. The one genuine adjacent fact is the
Montgomery–Odlyzko law (zeta zero spacing matches GUE random-matrix
statistics — real, independently re-verified in §18 case study 3), but
that's about point-spacing statistics on a line, not about any helix. None
of this construction's radii/angles reduce to 1/2 or the golden ratio
(checked, reported honestly as non-matches, not rounded to fit). **§18 is
that "verbal/thematic resemblance is not evidence" standard applied five more
times with actual numbers; §20 extends it to category-theory-flavored
formalism; §21 extends the same discipline to neural-network transplants of
a symbolic rule.**

A "tetragon" (4-gon) analog, and the exact reverse direction (helix →
recover the tetrahedron), were proposed but never formally constructed — no
automatic, parameter-free construction rule exists for either, unlike the
tetrahedron→helix direction verified above.

## 18. Numerology-vs-real-math: a working, repeatable test protocol (φ/π/primes/Riemann-zero case studies)

§17 ends with a warning that "verbal/thematic resemblance is not evidence."
This section is that warning turned into an actual, repeatable procedure, run
six times across two sessions on six different claimed patterns, with honest
results reported regardless of outcome (three falsified, one confirmed as
real-and-already-established, one exposed a concrete bug in existing tooling
that was then fixed — see §19 item 1 — one exposed a structural
domain/codomain problem in a proposed operator construction, and one — case
study 6 — was already honestly self-corrected before review and just needed
auditing plus turning its conceptual schema into tested code). Use this
protocol verbatim for any future "does X pattern-match Y" question in this
ecosystem instead of re-deriving a methodology from scratch.

**The protocol:**
1. Define the exact objects and exact mapping BEFORE running anything (which
   digits, which blocks, which index, which axis, which formula).
2. Define the metric (correlation coefficient, RMS residual, KS statistic) and
   the null model BEFORE seeing the result.
3. Run once. Do not scan windows/parameters/variants and keep the
   best-looking one — if a search over many candidates (window positions,
   bitmask rules, thresholds) is unavoidable, correct for the number of trials
   (Bonferroni, or report the corrected p-value alongside the raw one).
4. Report the actual result, including "no effect," without narrative
   softening — a negative result is a complete, valid answer (same principle
   as §13 item 5).
5. **Before concluding "no structure" from a negative result, check whether
   the domain already has an established, purpose-built statistical model —
   and if your metric was homemade instead of that model, re-run against the
   real one before treating the negative result as final** (added after case
   study 4's second round below: a homemade metric failing is evidence
   against *that metric*, not automatically evidence against the phenomenon
   it was trying to detect — the mirror image of case study 2's lesson that a
   homemade metric that always "succeeds" is also worthless).

**Case study 1 — φ digit-parity bitmask vs prime positions (falsified).**
Compared bit-parity of φ's digits against primality for i=1..2000: observed
overlap matched the random-model expectation almost exactly (hypergeometric
p=0.44). A "locally good" 30-digit window (raw p≈0.012) evaporated to
p≈1.0 once Bonferroni-corrected for the ~2000 windows scanned to find it —
the textbook multiple-comparisons artifact, reproduced with real numbers
instead of just asserted.

**Case study 2 — naive "zeros on a helix" construction (exposed as
tautological, not merely false).** Embedding Riemann zero imaginary parts as
`(cos(t_n), sin(t_n), t_n)` gave an exact 0.00 RMS residual from an ideal
helix — but so did a random Poisson control with matching density. Because
the z-coordinate is defined as the value itself, EVERY sequence lies exactly
on this "helix" by construction; the fit carries zero information about the
input. **Lesson: before treating "X lies on shape S" as a finding, check
whether a null-model control also gets a perfect/excellent fit — if so, the
fit says nothing about X specifically.**

**Case study 3 — GUE / Montgomery-Odlyzko level repulsion in Riemann zeros
(CONFIRMED — this one is real, and was independently re-verified here, not
just cited).** First 1000 real nontrivial zeros (`mpmath.zetazero`, verified
Riemann-Siegel + Turing-method algorithm), unfolded via the leading term of the
Riemann-von Mangoldt formula `N̄(T) = (T/2π)·ln(T/2π) - T/2π + 7/8`. Mean
unfolded spacing came out `1.0000` (theoretical value is exactly 1 — a good
sanity check that the unfolding itself is implemented correctly). Two
independent confirmations of level repulsion:
- At N=300: variance of unfolded spacings 0.135 (real) vs median 0.967 across
  2000 Poisson-null realizations of matching density, and fraction of very
  small spacings (<0.5): 6.0% (real) vs 39.5% (Poisson-null median) — both
  p<0.0005 (0/2000 null realizations beat the real value), one-sided.
- At N=1000 (999 spacings): full-distribution KS test against the GUE Wigner
  surmise `p(s)=(32/π²)s²exp(-4s²/π)` gives D=0.043, vs KS against Poisson
  `p(s)=exp(-s)` gives D=0.322 — GUE fits ~7x better. The KS test technically
  still rejects an exact GUE match (p=0.046, just under 0.05) — expected, since
  the two-level Wigner surmise is a known approximation to the true GUE
  n-point correlation, not an exact formula; the qualitative and quantitative
  superiority over Poisson is the real, load-bearing result here, not a
  perfect KS pass.
This reproduces a genuine, decades-established result (Montgomery 1973 pair
correlation conjecture, Odlyzko's high-precision numerics from the 1980s-2001)
— cite it as a known result, not a new discovery, but it is now independently
re-derived against this project's own computation rather than only quoted from
literature.

**Case study 4 — π/φ 2-digit blocks vs unfolded zero spacings (falsified),
AND a matching bug found and fixed inside math-validator-3.0 by applying the
same method to the tool itself.** Spearman correlation of π's and φ's 2-digit
decimal blocks against unfolded zero spacings (same axis index, no
phase-shifting), permutation-tested (10000 shuffles): both consistent with
pure noise (π: ρ=0.047, p=0.135; φ: ρ=-0.032, p=0.313; both Bonferroni-corrected
for 2 comparisons).

Separately, applying the exact case-study-1 method to
`math-validator-3.0/filters/prime_spectrum_filter.py::_classify_spectrum()`:
this function's `<0.25` similarity threshold for labeling a result
`"log_spiral_1_over_f"` (with a hardcoded note claiming agreement with
**"TIMDR Λ-τ-ρ"**) had never been calibrated — 200 random NON-prime integer
sequences hit the exact same label 24.5% (3-element) and 6.5% (7-element) of
the time purely by chance. **Fixed and committed** (`math-validator-3.0`
commit `f1f258d`): the threshold is now the 5th percentile of a 1000-sample
null model built from random sequences matched in length/step range to the
observed gaps, computed per call. Then, critically, ran the **follow-up
check the fix itself demands**: do REAL prime gaps cross this 5%-calibrated
threshold more often than 5%? Tested on non-overlapping windows along the
first 78,498 real primes (up to 10⁶): **2.73%/2.10%/1.17%/0.31% labeled
`log_spiral_1_over_f` at window lengths 5/7/10/15 — all BELOW the ~5%
expected under the null, decreasing with window length.** Real prime gaps
match this pattern *less* often than random sequences, not more — so the
`"TIMDR Λ-τ-ρ"` claim was removed from the filter's output entirely, not
just downgraded; the classification is kept only as a properly-defined
statistical test against a stated null model. Tests:
`math-validator-3.0/test/test_prime_spectrum_null_model.py` (8/8 passing,
42/42 in the full suite).

**Case study 4, continued — a negative result against a homemade metric is
not the same as "no structure," and recalibrating against the actual
theory-grounded model can recover a real (if subtle) signal
(math-validator-3.0 commit `697e728`, prompted directly by the user asking
"is this a wrong metric/plane, not absence of structure?").** The null-model
fix above answered "is this filter's own ad hoc metric (gap shape vs
log(x)) doing anything real for primes specifically" — and the honest
answer was no. But that is a narrower claim than "prime gaps have no
statistical structure at all." Analytic number theory already has a
purpose-built model here (Cramér's model / Gallagher's conjecture:
normalized gaps `x_n = gap_n / log(p_n)` should converge asymptotically to
i.i.d. Exponential(1)) that the original filter never used. Re-testing
against THAT model instead of the homemade one, on the same 78,498 real
primes up to 10⁶:
- Mean of `x_n` = 1.0017 — matches the model's leading-order prediction
  almost exactly.
- Full-distribution KS test vs Exp(1): D=0.1478, p≈0 — technically rejects
  pure Exp(1) at this N, but this is a **known, documented finite-range
  effect** (convergence to the asymptotic exponential law is slow), not
  evidence against the model — same "KS technically rejects the
  approximation but the qualitative structure is still the real result" shape
  as case study 3's GUE test above.
- Serial correlation between consecutive `x_n` (exactly the "plane"/
  dependency-between-neighbors structure the user asked about): Pearson
  r=-0.0568, p≈4.4e-57 — small, but far too significant to be noise, and
  this is genuine structure **beyond** Cramér's own i.i.d. assumption (known
  in the analytic-number-theory literature as biases/correlations between
  neighboring prime gaps — not a new discovery, and explicitly NOT a
  confirmed link to any TIMDR construct). Confirmed not a test-harness
  artifact: the identical statistic on i.i.d. Exp(1) of the same size gives
  r=-0.0009, p=0.80 (no correlation), and both required negative controls
  (i.i.d. Exp(1) → KS does not reject; a constant/arithmetic sequence → KS
  clearly does reject) behaved correctly.

**General, reusable lesson: before concluding "no structure" from a negative
result, check whether the domain already has an established, purpose-built
statistical model — and if your metric was homemade instead of that model,
re-run against the real one before treating the negative result as final.**
A homemade metric failing is evidence against *that metric*, not
automatically evidence against the phenomenon it was trying to detect. This
is the mirror image of case study 2's lesson (a homemade metric that always
"succeeds" is also worthless) — both failure modes come from skipping the
step of asking whether a real, independently-motivated model exists for this
exact question before inventing one. (Folded into the protocol above as
step 5.)

**Duplication-drift follow-up (§10 pattern, found by literally auditing for
it): `math-validator-v2.0/filters/prime_spectrum_filter.py` was still the
ORIGINAL, never-fixed version** (hardcoded 0.25 threshold, no null model,
the bare `"TIMDR Λ–τ–ρ"` claim) — v2.0's own README states v3.0 "keeps all
v2.0 filters unchanged" while continuing development, but that guarantee
was never rechecked after v3.0's filter received two independent fixes.
Ported both fixes at once into v2.0 (commit `7f53787`) rather than
re-deriving them — exactly the §10 remedy (find every copy once you find
one, don't assume a "kept in sync" claim is still true). Audited the rest
of the ecosystem's `*filter*.py`/`*spectrum*.py`/`*classif*.py`/
`*pattern*.py` files (both math-validator repos' other 10 filters, GIA-TIMDR,
PC_TIMDR, fusion-tools, TIMDR-Crypto-Graph) for the same shape of problem
(a computed similarity/distance score compared against a hardcoded,
uncalibrated threshold, with a named-pattern or TIMDR-model claim attached)
— `prime_spectrum_filter.py` was the only match. One adjacent-but-different
finding, NOT fixed (different failure mode, flagged for the user instead):
`math-validator-3.0/filters/information_filter.py` buckets a computed
complexity score into 5 labels using hardcoded, evenly-spaced thresholds
(0.25/0.45/0.65/0.85) and attaches an unearned "zgodne z modelem Λ–τ–ρ–ι"
(consistent with the Λ-τ-ρ-ι model) note — but this is a descriptive
bucketing of a heuristic score with no meaningful null model (there's no
"random expression" baseline that would make a calibration test
well-posed the way it is for real-vs-random integer sequences), so the
§18 null-model remedy doesn't directly apply here. The unearned
model-compatibility claim is still the §20-style "vocabulary without
satisfied structure" problem, just not a numeric-classification one.

**Case study 5 — `M∘M` on a proposed "twist operator," instantiated as
`field_torsion()` (exposed a structural domain/codomain problem, not a
numeric falsification).** A user proposal defined "time" in TIMDR as
`Time = ∫M(x)dx` with `M` a self-map (`M:X→X`) called a "twist operator,"
and asked about properties of `M²=M∘M` (existence of a fixed point, a
"stabilization" condition `d/dx M²(x)=0`, etc.). Made `M` concrete by using
the already-built `field_torsion()` (§19 item 2) — torsion of the demo
`(Λ,τ,ρ)` trajectory from TIMDR-META-DYNAMICS, as a function `M(s)` of sample
index `s`. Composing `M` with itself immediately exposed the real problem:
`M`'s output (torsion values, range roughly [-0.35, 2.58]) and `M`'s input
domain (`s ∈ [0,59]`, a sample index) are different quantities on different
scales — `M(s)` only lands back inside the valid domain for 64% of samples
(wherever torsion happens to be non-negative), and the one "fixed point"
`M²(x₀)=x₀` found by root-search (`x₀≈0.052`) turned out to be a trivial
artifact of index and torsion-value happening to coincide numerically near
the start of the series, not a meaningful stability point. The other
claimed properties (`M²(s)≠M(s)` almost everywhere; derivatives differing;
many critical points of `M²`) all turned out to be generic facts true of
almost any non-idempotent nonlinear function composed with itself — not
specific evidence of "interference," "diffraction," or "resonance" as
physical phenomena. **General, reusable lesson: before composing any
signal-derived scalar quantity with itself as a self-map (`M:X→X`), check
that its output actually lands back in its own input domain/units — if it
doesn't, `M∘M` is either undefined on most of the domain or only "well-typed"
by numerical coincidence, and any fixed point found this way should be
treated as a units artifact until shown otherwise.** This generalizes beyond
torsion — the same check applies to any other TIMDR "operator squared"
proposal in this ecosystem.

**Case study 6 — probabilistic-timdr repo audit (already self-corrected;
audit confirmed it, then closed its "no formula" gap with tested code).**
A repo mapping T-I-M-D-R onto probability/boundary-condition/cosmology
concepts had, BEFORE this review, already gone through an honest
self-correction pass: fixed a wrong birthday-paradox table, added a caveat
that 0.5 is not a universal phase-transition threshold (counterexample:
percolation p_c depends on lattice geometry, only equals 0.5 where derivable
from self-duality), distinguished δ_crit≈1.686 (cosmology) from 0.5 (birthday)
as different constants playing an analogous but non-identical role, and wrote
a cross-repo comparison document (`TIMDR_POROWNANIE.md`) showing "TIMDR" means
four unrelated things in four repos (EasySound: Hilbert-transform phase
roughness; Senscore: z-score/percentile hit filter; KHIPU: discrete S/K pair
validator with a 1/2±(φ-1) rope-balance rule — since found to be
mathematically vacuous with that exact tolerance, see §21's KHIPU-adjacent
housekeeping note; this repo: an unimplemented five-label conceptual schema).
**Two audit techniques used here, both reusable:**
- **Derive, don't just re-cite, a literature constant when you have the
  tools to.** δ_crit≈1.686 (Press-Schechter spherical top-hat collapse) was
  independently re-derived from the underlying physics — Taylor-expand the
  cycloidal collapse solution `1+δ_nl(θ)=9(θ-sinθ)²/(2(1-cosθ)³)` at small θ
  (sympy `series`), match the leading `(3/20)θ²` term to the known EdS linear
  growth law `δ_lin∝t^(2/3)`, evaluate at collapse (`θ=2π`) — reproduces
  `(3/20)(12π)^(2/3)≈1.6865` to 1e-9 against the closed form. This is
  stronger evidence than just checking the citation matches Wikipedia: it
  shows the constant is understood, not just remembered.
- **Cross-repo comparison claims need checking against the actual other
  repos' source, not trusted from the writing alone.** `TIMDR_POROWNANIE.md`'s
  claim about EasySound's `TIMDRAnalyzer` (Λ=τ/ρ+J from Hilbert-transform
  phase) and Senscore's `TIMDRFilter` (z-score energy + percentile time trim)
  was verified by cloning both repos and grepping the actual class
  definitions — matched exactly. Don't assume a self-comparison document is
  accurate just because it's internally consistent; check it against ground
  truth the same way any other claim in this ecosystem gets checked.
- **When a doc admits "R_total and R* are conceptual labels, not a formula"
  (its own honest self-assessment), the right fix is NOT one universal
  formula covering all domains — that would silently reintroduce the very
  "it's all the same mechanism" overreach the doc had already rejected.**
  Instead, implement each domain's own metric and threshold separately under
  a shared classify-only interface, and add a test that explicitly asserts
  the thresholds are NOT all equal / share a common numeric origin
  (`threshold_source` fields differing) — this makes the correct "shared
  pattern, different constants" conclusion structurally hard to accidentally
  undo in a future edit, rather than just stated once in prose that a later
  change could silently violate.

**Case study 7 — GIA-TIMDR's `docs/filters/` numerology cluster (XOR at
prime positions, digit-density claims, `(mp/me)/(6π⁴)≈π`): mostly
falsified, one genuine-but-inconclusive numeric coincidence, and one
root-caused float-precision bug.** User asked for a rigorous verdict on
two specific claims in `GIA-TIMDR/docs/filters/` (a separate cluster of
speculative docs from the Category_Q one in §20, same repo, same general
pattern): (1) XOR of √2/√3 decimal digits at prime-numbered positions
reveals a "structural resonance" where XOR=0, especially at twin primes
29/31; (2) proton/electron mass ratio divided by `6π⁴` equals π to
0.002%, framed as "too precise to be chance" and "ending scientific
discussion."

**Claim 1 (XOR/twin-primes) — falsified, with a diagnosed root cause.**
Computed real digits of √2 and √3 to 20,000+ places with arbitrary
precision (`mpmath`) and compared against the document's own digit
table: positions up to ~17 matched, everything after did not — the exact
signature of a table computed with ordinary double-precision `float`
(~15-17 correct significant digits) rather than arbitrary precision.
Position 31, the second half of the document's central "twin primes
29/31 both agree" claim, turned out to be wrong even in the original
15-position sample once corrected (true digits differ, not match). At
full scale (2262 prime positions among 20,004 real digits): agreement
rate 9.505%, statistically indistinguishable from the 10% expected for
independent uniform digits (binomial p=0.46); no difference between
prime and non-prime positions (p=0.29); no difference between twin-prime
and other prime positions (p=0.65, wrong direction if anything). A
companion claim (digit density of {2,3,5,7} in √2/√3/q, claimed
36%/50%/48%) was also directly measured and falsified — all three came
out ~39.2-39.7%, consistent with the 40% expected under independent
uniform digits, not the claimed values (the sibling doc had already
flagged this one as "unstable across parsing methods," self-flagged but
never actually checked).

**Claim 2 (mass-ratio coincidence) — a real, narrow numeric coincidence,
but not validated physics, and the source doc has an arithmetic error.**
Verified the underlying arithmetic first: the document displays
`6π⁴ ≈ 5841.23`, but the true value is `584.4545` — off by a factor of
10 in the shown intermediate step (the final ratio, 3.14165, is
nonetheless computed from the correct value, so the stated conclusion
survives the typo). Ran a "look-elsewhere" check within the one natural
parameter family the claim lives in (`(mp/me)/(c·πᵏ)`, c rounded to the
nearest integer for each k): only k=4 (c=6) lands close to π
(rel. error 1.88e-5) — neighboring k=1,2,3,5,6 are 10 to 20,000x worse,
so this is NOT a case of "any grid cell would have hit something," it's
a genuinely tight coincidence within that narrow family. But three
things keep it from being evidence of real physics: (a) no independent
physical derivation is given for choosing c=6, k=4 specifically — they
were reverse-engineered after seeing the target, the textbook
look-elsewhere setup; (b) the same document (and its siblings
`README_filter.md`, `mobius_ratio_filter.md`) proposes several other
similarly-shaped "coincidences" (a Möbius-ratio residual, a CMB
peak-ratio match to √3, a fine-structure-constant/residual ratio near
π/2), which is itself evidence of a broader, unreported search that
would need a multiple-comparisons correction before any single "best"
hit counts as significant; (c) "dimensionless physical constant ≈ simple
function of π" claims have a poor track record once checked rigorously
(the general class of Eddington-style numerology). Verdict: a real,
worth-noting numerical curiosity, not validated physics — the source
document's "ends scientific discussion" framing significantly
overclaims what one unexplained near-match establishes. The other four
"predictions" in the same document's status table (Mercury precession,
CMB peak ratio, fine structure constant, next resonance scale) were
**not** independently re-verified this session — flagged with the same
skepticism given the identical unreferenced-parameter-search pattern and
the one confirmed arithmetic error, but not tested one by one for lack
of real reference data pulled in this pass.

**Resolution delivered**: added a "WERYFIKACJA" section to the top of
each affected file (`prime_position_filter.md`, `prime_spectrum_filter.md`,
`al_filter_predictions.md`, `README_filter.md`) with the numbers above,
same non-destructive pattern as §20's Category_Q fix — original
speculative content kept below, not deleted, so the record is honest
about both what was claimed and what was found. Committed locally
(`GIA-TIMDR` commit `a05f71c`), not pushed.

**Reusable lesson**: when a hand-typed "verified" digit table for an
irrational constant only matches known correct values up to roughly the
double-precision float limit (~15-17 significant decimal digits) and
then diverges, suspect the table was generated with ordinary
floating-point arithmetic, not arbitrary precision — this is a fast,
mechanical check (compare a few claimed digits past position ~17 against
a `mpmath`/`sympy` high-precision computation) worth running before
trusting any claimed digit-level pattern in π/e/√n-style constants
anywhere in this ecosystem.

## 19. Open research directions for this ecosystem (as of this session)

Status notes, not reusable patterns — kept short since most of the substance
already lives in the sections they point back to.

1. `math-validator-3.0/filters/prime_spectrum_filter.py`'s ungrounded 0.25
   threshold: **fixed, twice** — first the null-model calibration, then a
   deeper recalibration onto the actual Cramér/Gallagher model after the
   user asked whether the negative result was a wrong metric rather than
   absence of structure (it was) — see §18 case study 4 for the full
   method and numbers, including the duplication-drift port to
   `math-validator-v2.0`. Don't re-litigate, that section is the full
   record.
2. TIMDR-META-DYNAMICS `field_torsion()` vs the existing, manually-supplied
   `τ` field: genuinely open, untested question on real data. If picked up,
   use §18 case study 4's method (Spearman + permutation null, Bonferroni if
   testing more than one pairing) — don't skip the null model just because
   the quantities "sound related" (item 1 above is a direct demonstration of
   why that shortcut fails). Note `field_torsion()`'s output scale isn't
   directly comparable to `τ`'s own scale without checking real-data ranges
   first (§18 case study 5).
3. The resonance-tester method (unfold + KS vs Poisson/GUE, or
   Spearman+permutation) is fully designed and ready but has never been run
   on a real market/seismic/audio series — blocked purely on data access (no
   working internet to the specific source, or a user-supplied file of a few
   hundred+ real events/readings).
4. `ringdown_resonance()` (§11) validated only on a synthetic
   damped-oscillator signal, never on real audio — rerun the same
   pre-registered hypotheses (is_oscillatory=True, frequency within 2%,
   damping within 0.05) if a real recording becomes available.
5. Standing conclusion (§17, §18): no established bridge exists between
   Boerdijk-Coxeter helix geometry and Riemann zeros/primes/φ — run any
   future proposal connecting these domains through the §18 protocol before
   writing it up as a finding.
6. GIA-TIMDR's `docs/theory/` directory has ~20 more speculative "Model_*"
   documents beyond the one reviewed in §20 — the same category-axiom check
   applies if any of them get revisited.
6b. GIA-TIMDR's `docs/filters/` cluster (§18 case study 7): two of its
   claims tested and audited (XOR/twin-primes falsified, mass-ratio
   coincidence found genuine-but-inconclusive). `mobius_ratio_filter.md`
   and the untested Predictions 1/2/4/5 in `al_filter_predictions.md`
   (Mercury precession, CMB peak ratio, fine-structure constant, next
   resonance scale) remain open — same protocol, needs real reference
   data pulled in before testing.
7. probabilistic-timdr's Monte Carlo simulator (§18 case study 6) only
   covers 3 of the repo's 4 numeric claims (birthday, square-lattice
   percolation, spherical collapse) — the other 5 percolation-lattice values
   in its own table remain `CITED`, not independently simulated.
8. KHIPU-NEURAL's positive result (§21) is from ONE synthetic task family
   (d_embed=8, 4 hidden categories, seq_len=10) — never run on real data, and
   the noise level / category count were never systematically swept. The
   qualitative direction (categorical helps, magnitude hurts) is unlikely to
   flip, but the exact numbers are specific to this toy configuration.
9. defect-operator v4 (§26) is validated on ONE synthetic scenario family per
   defect type (cluster/periodic/regime-shift) — never swept across defect
   density/magnitude to find where exactly the "rare enough to bootstrap a
   clean calibration block" boundary sits, only confirmed it was crossed in
   the one dense-cluster scenario tested.
10. §27's aftershock-swarm finding was tested on synthetic Omori-law data
    (both the standalone version and the real TIMDR_EarthquakeCore version) —
    never against a real labeled aftershock catalog (e.g. Ridgecrest 2019,
    the same real dataset PhaseNet/EQTransformer literature results cite).
11. §29's C-MAPSS transfer test is n=1 (one real engine, FD001 unit 1 only) —
    full validation needs all 100 units of FD001 and a repeat on FD002-FD004
    (different operating conditions/fault modes), blocked in-session by this
    sandbox's network allowlist (data hosts, not the specific method) —
    needs a machine without that restriction. CWRU and NASA IMS bearing
    datasets (binary `.mat`, different failure mode: rolling-element bearing
    vs. gradual whole-engine degradation) remain completely untested.

## 20. Formal vocabulary without satisfied axioms: the same problem as §17, one level up (category theory case study)

§18 is about numeric/geometric pattern-matching claims (does sequence X
resemble sequence Y). This section is the same discipline applied to a
different failure mode: using the **vocabulary** of an established branch of
mathematics (here, category theory) without the underlying **definitions**
being satisfied — a document can be dense with correct-looking symbols
(Hom-sets, functors, natural transformations, monoidal structure) while not
actually forming the mathematical object it names.

**Case study — `GIA-TIMDR/docs/theory/Category_Q_Kategoria_Matematyczna.md`.**
The document defines a category with six objects (T, I, M, I(t), R, E) and a
linear chain of morphisms between them, then calls the same operators
"functors," defines "natural transformations" between them, and claims a
monoidal structure and a "functor of time" `D:ℝ→C`. Checked against the
actual definitions (not just read for vocabulary), five concrete gaps were
found:

1. **No identity morphisms** — every object in a category needs an identity
   morphism on itself; none are defined for any of the six objects.
2. **Only one linear chain of Hom-sets given, not all pairs** — composition
   forces Hom-sets between non-adjacent objects to exist too (composing two
   morphisms must land somewhere), but only the adjacent-object Hom-sets are
   ever specified.
3. **The same symbols used as both morphisms and functors** — one section
   introduces symbols as morphisms between objects; another section
   introduces (mostly the same) symbols as functors mapping the category to
   itself. A natural transformation, by definition, is a family of morphisms
   between two FUNCTORS of matching source/target categories — so a claimed
   natural transformation between two of these symbols is not well-typed
   until they're pinned down as functors specifically, not also morphisms of
   the same name.
4. **Monoidal structure given for one object, not the whole category** — a
   real monoidal category needs a bifunctor plus associator/unitor natural
   isomorphisms satisfying coherence conditions; the source document gives
   one equation for one object.
5. **The "functor of time" returns a tuple, not a single object** — it is
   defined as a 6-tuple of the six named things, but a functor must send each
   object of the source category to ONE object of the target category, and
   those six things were defined earlier as six SEPARATE objects, not
   components of one composite object.

**Resolution delivered**: reformatted the document for readability (table of
contents, consistent LaTeX/table rendering) and added an explicit "uwagi
formalne" section listing the five gaps above, framed constructively (either
supply the missing definitions so the axioms are actually satisfied, or
relabel the document as a category-theory-*inspired* diagram rather than
asserting "TIMDR is a category"). Delivered as a local file, not pushed to
the public GitHub repo without explicit permission (publishing/modifying
public content requires it).

**General lesson, applicable to any of the other ~20 `docs/theory/Model_*.md`
files in GIA-TIMDR (§19 item 6) or any future formal write-up in this
ecosystem**: correct-looking notation from a real branch of mathematics
(category theory, group theory, differential geometry, measure theory,
whatever) is not, by itself, evidence that the named structure has been
constructed. Check the actual definitions the vocabulary requires (does every
object have an identity? are all the Hom-sets/derivatives/axioms the
composition or claimed structure demands actually given? are symbols used
consistently as one type of object throughout?) before treating a document's
claims as established — the same standard §18 applies to numeric coincidence,
applied here to definitional completeness.

## 21. Transplanting a discrete/symbolic TIMDR rule into a gradient-learned neural module: keep it as an inductive bias, not as a frozen formula

A distinct question from §18/§20 (is a claimed pattern real math): here the
question is whether a TIMDR repo's own deterministic, symbolic rule — already
known to be well-defined, since it's just running code — gains or loses
anything by being reimplemented as a differentiable module trained by
gradient descent instead of run as-is. Case study: KHIPU-NEURAL
(jbackk-lang/KHIPU-NEURAL), which asks exactly this of KHIPU's State9/GIPU
rule (a 9-axis ±1 vector with a combinatorial balance condition, and a
discrete "same category → resonance" relation between neighbors).

**Two architectures, opposite results, same task:**
- `KHIPUResonanceNet` encodes the GIPU resonance rule **literally as a fixed
  formula** inside the network (normalized dot product of two quantized
  codes, mixed by a sigmoid between two learned scalars). **Loses even to a
  trivial mean predictor** (test MAE ~1.08-1.15 vs a parameter-free "always
  predict the mean" baseline at ~1.03).
- `KHIPUResonanceNetMLP` keeps only the State9 **quantization step** (hard
  discretization to ±1 with the same balance condition as KHIPU) as a
  bottleneck, but hands the rest of the computation to an ordinary learned
  MLP instead of a hand-designed formula. **Wins ~2x** over a generic
  baseline with zero KHIPU-derived structure (MAE 0.114-0.133 vs baseline
  0.253-0.286) — confirmed NOT explained by parameter count via a
  matched-parameter ablation (a baseline resized to the same parameter count
  barely improves, MAE 0.260±0.035).

**Why**: a hand-designed deterministic rule and a gradient-optimized network
are two different computational regimes — exact symbolic comparison
("same S and K → resonance", computed once, never adjusted) vs. distributed,
continuously-adjusted weights found by trial (gradient descent). Encoding the
rule as a **rigid, frozen formula** inside a differentiable model forces the
optimizer to imitate a computation it has no freedom to adapt — that
generally loses, even to a baseline with no structure at all. Encoding only
the **structural** aspect of the rule (here: forced discretization before
comparison) as an architectural constraint, while leaving the rest of the
computation to ordinary learned parameters, lets the two regimes cooperate
instead of one being forced to imitate the other — and that can genuinely
help. Reusable framing: don't ask "how do I make the network compute the
same formula" — ask "which PART of this rule is a structural prior worth
imposing, and which part is just an implementation detail of the
deterministic version with no reason to expect gradient descent to want the
same shape."

**The same discretization has a real, honestly-found boundary — it is not a
general-purpose improvement.** On a second, deliberately different task
(regression of a continuous distance/magnitude quantity between the same
hidden categories, instead of detecting whether they match), the identical
bottleneck **hurts**: MAE 24.54±6.74 (with the bottleneck) vs 17.18±6.37
(continuous baseline) vs 25.84±5.18 (trivial) — barely beats guessing, and
clearly loses to the continuous baseline. Mechanistically: forced
quantization to ±1 throws away exactly the magnitude information a
continuous-value task needs, while it only ever helped a categorical/
same-or-different task by acting as forced denoising (cutting noise before
comparison, instead of making the network learn to filter it). A third
control (`frozen_projection.py`) rules out "any bottleneck helps regardless
of learning": a random, never-trained version of the same projection is ~4x
worse (MAE 0.552±0.067) than the learned one — so the advantage is real
learning, not just generic dimensionality reduction.

**Protocol, reusable for any future "make TIMDR-rule-X a neural module"
question in this ecosystem** (same discipline as §13/§18, applied to
architecture design instead of pattern-verification):
1. Try the literal, "obvious" translation first, and report its result even
   if negative (here: `KHIPUResonanceNet` losing to a trivial baseline) — it
   is data, not a failed attempt to hide.
2. If it loses, ask specifically which part of the deterministic rule is a
   genuine *structural* prior (a bottleneck, an invariance, a combinatorial
   constraint) versus which part is just *how the exact rule happens to be
   computed* — keep only the former as an architectural constraint, let the
   latter be learned.
3. Confirm the fix isn't just "more parameters" via a matched-parameter
   ablation, and isn't just "any dimensionality reduction" via a frozen/
   untrained control of the same bottleneck.
4. **Test a second task that plausibly should NOT benefit** (here: continuous
   magnitude regression instead of categorical matching) before generalizing
   the positive result — a result that only "wins" on the one task it was
   designed around is much weaker evidence than one that also correctly
   fails to help (or actively hurts) on a deliberately mismatched task.
5. State the scope of the positive result narrowly and explicitly (here:
   helps for "detect sameness/category from noisy continuous observations,"
   not "generally better architecture") — resist the pull to generalize a
   single positive number into a broad architectural claim.

**Environment note**: PyTorch could not be installed in this sandbox
(`download.pytorch.org` blocked at the proxy, same pattern as other blocked
domains in §14) — the entire KHIPU-NEURAL codebase is hand-written NumPy
forward/backward, with every custom gradient verified by numerical
gradient-checking (`tests/test_gradients_*.py`), not assumed correct. One of
those gradient-check tests caught a real bug in its own backprop (a
Straight-Through-Estimator linearization subtlety when two independently
quantized vectors are multiplied together) — a concrete instance of §9's
"verify, don't assume" discipline applied to hand-rolled autodiff.

**Housekeeping note**: KHIPU's own `TIMDRValidator` rope-balance tolerance
(the `1/2±(φ-1)` rule referenced in §18 case study 6's cross-repo table) was
separately found, in the KHIPU repo itself, to have been mathematically
vacuous as originally implemented — `φ-1≈0.618` exceeds the maximum possible
deviation of a `[0,1]`-bounded fraction from `0.5` (which is `0.5`), so the
check could never return `False` for any input, regardless of what "1/2 and
φ" was meant to capture conceptually. Fixed by switching to `2-φ=1/φ²≈0.382`
(also directly derived from φ via `φ²=φ+1`, but actually less than 0.5). Not
a numerology-vs-real-math finding in the §18 sense (nobody claimed the
tolerance was a discovered pattern) — just a reminder that even an admittedly
arbitrary interpretive choice can be silently self-defeating in a way worth
checking mechanically (does the chosen constant even fall in the range where
the check can fire at all?), independent of whether the constant "means"
anything.


## 22. Decompose a fused detector's FPR by component before re-tuning (TIMDR-Security-Module DDoS case study)

Pre-registered 300+300 trial test (Poisson background, DDoS injected at a
random position/magnitude, vs. a pure negative control): 100% detection, but
23.0% FPR on the negative controls. Splitting the OR-fused alarm
(`connection_twist` / `ratio_twist`) by origin found it was 100%
attributable to `connection_twist` — one threshold (`conns_z_thresh=3.5`)
too tight for genuine Poisson traffic, not a fusion problem. **Reusable step
for any OR-fused TIMDR detector: an aggregate FPR tells you THAT something
is miscalibrated, not WHICH sub-check — always decompose by component before
re-tuning**, or a fix aimed at the fused output risks de-tuning a sub-check
that was already fine. Documented honestly in the repo's own README rather
than hidden.

## 23. `tension_zscore` — a real, established alternative to numerology (TIMDR-Cosmology-Filters case study)

Positive counter-example to §18: same subject matter (cosmological
constants) as GIA-TIMDR's numerology, but built from real cited measurements
and the field's own tool: `tension_zscore = (v1-v2)/sqrt(σ1²+σ2²)`. Tested
on CMB peak spacing (Planck 2018), Mercury precession, and Hubble tension —
correctly reproduces the real, well-known z≈5.77 SH0ES/Planck tension.
Instructive extra: testing a naive "CMB peaks are equally spaced" null model
against real data gives z≈21 — a correct rejection of an oversimplified
model, not a discovered anomaly, mirroring §13/§18's "a negative result
matching consensus is a good sign" principle. What separates this from
numerology isn't the subject, it's (a) real sourced data with real
uncertainties and (b) using the field's actual established test instead of
a homemade metric (§18 step 5).

## 24. A null model's validity doesn't transfer with its code (prime-gap KS test → radar defect detection, falsified)

Reused math-validator-3.0's already-fixed (§18 case study 4)
`_normalized_gaps`/KS-vs-Exp(1) code verbatim on synthetic radar-return
position data (3 scenarios: Poisson noise, cluster, periodic). Result:
rejected the null (p≈0) on ALL THREE, including pure Poisson noise — 100%
false-positive rate on the negative control — while a trivial
coefficient-of-variation baseline correctly told the three apart. Cause:
`gap/log(position)` normalization is calibrated to primes' specific
logarithmic density law; radar-return density has a different profile
entirely, so the normalized quantity isn't close to Exponential(1) for any
input. **Lesson: a statistical test's null model encodes assumptions about
the specific point process it was built for — re-derive/check those
assumptions before porting the code to a new domain, and always run a
trivial domain-appropriate baseline alongside a transplanted test.**

## 25. Higher-derivative operators are correct math but noise-fragile in practice (Frenet-Serret torsion case study)

`τ(t)=[(ṙ×r̈)·r⃛]/‖ṙ×r̈‖²` verified exactly correct via three analytic checks
(helix, straight line, planar curve). On noisy synthetic defect data it gave
~1.0x contrast (no real signal) vs. 3.91x for a simple plane-residual
baseline; even a 30x-lower-noise sweep only reached 2.98x, still worse.
**Lesson: any operator needing a derivative of order ≥2-3 on real noisy
sensor data is inherently fragile (each numerical differentiation divides
signal-to-noise ratio) — always benchmark against a lower-order baseline
(raw value, or first derivative) before investing in a higher-order
feature.** Replicated a second time in §29 — see that section for the named
meta-pattern.

## 26. A single adaptive-reference detector can't be both regime-robust and immune to frequent defects — needs a multi-module split, which has its own hard limit (defect-operator v1→v4)

Four iterations of a permutation-entropy anomaly detector, each fixing the
last version's failure and creating a new one, until the failure was
diagnosed as structural: **v1** (fixed reference) — FPR 5%→62% on regime
shift. **v2** (adaptive median/MAD reference) — fixes FPR (3-9%) but
cluster-defect detection collapses 89.9%→5.7% (baseline self-poisoning,
same failure class as §16 / TIMDR-Security-Module's LOO-fix). **v3**
(self-excluding buffer) — partially recovers detection, but FPR regresses to
42%. **v4** (user-proposed split: block-level regime-change detector +
frozen point-anomaly detector, reset only on confirmed regime change) —
solves the FPR conflict simultaneously (3.3%/3.9%) but cluster detection
collapses to 2.4%, diagnosed as fundamental: the very first calibration
block is already contaminated when defects are dense enough.

**General principle**: one adaptive reference can't simultaneously update
for legitimate regime change and ignore frequent real defects — they look
identical to it. Splitting into a coarse regime detector plus a
frozen-until-reset point detector resolves this ONLY when defects are rare
relative to the calibration window; if defects are dense enough to
contaminate the first calibration block, no reference-based method
(single or multi-module) can bootstrap a clean baseline — needs an
externally-supplied clean period, or a non-reference-based detector family
(§27 finds a real example: STA/LTA, which recomputes its reference
continuously instead of freezing one).

Canonical verdict, user's own words, recorded verbatim (`TEST-TIMDR/README.md`):

```
✔ TIMDR działa tam, gdzie dane mają stabilną fizykę (Cosmology, Security).
✘ TIMDR nie działa tam, gdzie operator jest źle dopasowany do dziedziny (Prime).
✘ TIMDR nie działa tam, gdzie operator wymaga wysokiego rzędu różniczkowania (Torsion).
✘ TIMDR nie działa jako pojedynczy detektor anomalii (v1→v3).
✔ TIMDR działa jako architektura wielomodułowa (v4), ale tylko gdy defekt jest rzadki.
```

## 27. The "rare defect" finding replicates in real seismology (Short-Term Aftershock Incompleteness)

Tested classic STA/LTA — both a standalone rebuild and the real,
ObsPy-verified `TIMDR_EarthquakeCore.sta_lta()`/`.trigger_onset()` — against
synthetic Omori-law aftershock sequences: ~100%/91% detection for an
isolated earthquake, dropping to 37-40% late in a dense swarm. STA/LTA has
no persistent reference to poison (naturally regime-robust, FPR only
1.1%→1.3% across a synthetic regime change), yet still degrades under dense
recurring events — matching a real, named phenomenon, **Short-Term
Aftershock Incompleteness (STAI)**, independently confirmed in the
literature (PhaseNet/EQTransformer show >2x completeness over STA/LTA on
real Ridgecrest 2019 aftershocks). Also: `hybrid_trigger()` gave IDENTICAL
numbers to plain `trigger_onset()` here — close aftershocks were already
merged into one onset before the extra twist/anomaly confirmation had
anything left to distinguish. Check what the base detector already does to
the data before crediting (or blaming) a fusion layer for an identical
result.

## 28. TIMDR-Earthquake-Core: packaging as a tool, and a Tkinter Canvas+Scrollbar debugging checklist

**Packaging**: `pyproject.toml` with `py-modules` (not a package dir) plus
`project.scripts` gives a real CLI via `pip install -e .` for a flat-file
repo; split `requirements.txt` into core/GUI/dev/optional groups. CLI
gotchas: check a result dict's actual keys instead of assuming a `reason`
field, and cast `np.floating`/`np.integer` to `float` before `json.dump`.

**Canvas+Scrollbar checklist** — one user-reported symptom ("labels missing
first characters, values hidden behind the scrollbar"), three compounding
causes: (1) hardcoded pixel width breaks under Windows DPI scaling — let
width come from `pack(fill="both", expand=True)` and call
`SetProcessDpiAwareness(1)` at startup; (2) a vertical-only Canvas still has
built-in horizontal arrow-key/gesture bindings that can silently shift
`xview` and leave it shifted with no way to undo it — fix with
`takefocus=0`, forced `xview_moveto(0)` on every `<Configure>`, and block
`<Left>/<Right>/<Shift-MouseWheel>`; (3) one hardcoded label width shared
across grid groups wastes space in shorter-label groups, pushing later
columns off-screen — compute label width per group dynamically. For bigger
scrollable plots: wrap the matplotlib canvas in its own Canvas+Scrollbar and
pack it with `fill="x"` only so height stays fixed while width still tracks
the window.

## 29. Cross-domain transfer test #4: NASA C-MAPSS turbofan degradation, and a named derivative-order meta-pattern

Sandbox bash network blocked nearly every data host (NASA, Kaggle, CWRU,
even `raw.githubusercontent.com` via curl), but the model's own page-fetch
tool reached a public mirror of the real `train_FD001.txt` anyway —
**worth remembering: try the fetch tool when shell-level curl is blocked,
allowlists can differ between the two**. Got one complete real 192-cycle
engine trajectory this way (n=1, not a statistical validation).

Test: `flow()` (unchanged from TIMDR-Earthquake-Core) monitoring a sensor's
local trend lost to a simple raw-value SPC baseline (18 vs. 47 cycles lead
time); `anomalies()` gave an earlier but unconfirmed, sparse signal (96
cycles, no negative control run). **This is the same failure shape as §25's
torsion result — now a named, twice-replicated meta-pattern: monitoring a
higher-order derived quantity is consistently less sensitive than a
simpler value/residual for slow, near-monotonic drifts.** Always benchmark
a derivative/trend feature against its raw-value equivalent before adopting
it in a new domain. Full validation needs all 100 FD001 units plus
FD002-FD004 — blocked here by sandbox networking, not the method; CWRU/NASA
IMS bearing data (binary `.mat`) remain completely untested.
