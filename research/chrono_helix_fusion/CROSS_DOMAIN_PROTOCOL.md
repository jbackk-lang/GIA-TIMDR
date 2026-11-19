# CHF cross-domain signal validation — protocol v0.1

**Question:** Do CHF temporal/helix/bridge features add predictive information beyond FFT/statistics on mechanical, electrical, and plasma time series?

## Candidate source projects
- [TIMDR-Industrial-Predict](https://github.com/jbackk-lang/TIMDR-Industrial-Predict): mechanical vibration; bearing resonance sieve as an additional domain-specific comparator.
- [TIMDR-Grid-Monitor](https://github.com/jbackk-lang/TIMDR-Grid-Monitor): voltage/current, THD, power-grid events. Its README reports simulation-based fault-detection tests, not independent real-grid ground truth.
- [TIMDR-fusion-tools](https://github.com/jbackk-lang/TIMDR-fusion-tools): TCABR plasma current/voltage, real labeled shots; keep entire shot in one split group.
- [universal-state-analyzer](https://github.com/jbackk-lang/universal-state-analyzer): domain-agnostic FLOW/TWIST/anomaly controls.

## Implemented baseline
`cross_domain_eval.py` accepts a manifest of **locally supplied, labeled** recordings. It computes FFT/stats, chrono, helix, trinode and lagged bridge ablations. It performs five group-disjoint splits *within each domain*, fitting scaling and logistic regression on training data only. Optional `--rms-normalize` removes absolute amplitude differences. No data are silently downloaded.

Manifest example:

```csv
path,label,group,fs,domain
recordings/healthy_01.npy,healthy,machine01,12000,mechanical
recordings/fault_02.npy,fault,machine02,12000,mechanical
recordings/normal_01.npy,normal,shot01,100000,plasma
recordings/disruption_02.npy,disruption,shot02,100000,plasma
```

These paths are illustrative, **not included datasets**.

```bash
python research/chrono_helix_fusion/cross_domain_eval.py --manifest data/signals.csv --output cross_domain_results.json
python research/chrono_helix_fusion/cross_domain_eval.py --manifest data/signals.csv --rms-normalize --output cross_domain_rms.json
```

## Mandatory next steps before scientific claims
1. Obtain verifiable labeled electrical recordings (not just synthetic Grid-Monitor scenarios); record source, license, acquisition frequency, event definition, hashes.
2. Add explicit domain-specific baselines (voltage sag/THD, plasma quench/phase-space, bearing sieve) on exactly the same group-held-out recordings.
3. Add duration-matched windows across differing sample rates; currently windows have equal sample **counts** and different physical durations.
4. Add permutation and time-shuffle negative controls for bridges; quantify incremental gains and uncertainty.
5. Test unseen devices/sessions/shots, then true **cross-domain transfer** separately. This implementation is within-domain only.

**Status:** executable evaluation framework committed; no cross-domain data were evaluated or performance results claimed in this step.
