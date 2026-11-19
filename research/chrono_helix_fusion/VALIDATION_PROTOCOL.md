# CHF: automated validation protocol

Workflow: `.github/workflows/chf-validation.yml`. Trigger on changes to CHF files in a pull request, or manually via Actions > CHF bridge validation > Run workflow (once workflow is available on the default branch, depending on GitHub Actions policy).

Output: `validation_bridges.json` in the workflow artifact `chf-bridge-validation`. GitHub Actions run logs are the source of truth for successful execution.

The synthetic test uses 20 grouped holdouts. It compares FFT+statistics, unbridged fusion, original zero-lag trinode, and new lagged bridges. All fitted scaling and classification parameters use training data only. **Interpretation remains exploratory**: repeated holdouts overlap and synthetic labels are not independent field measurements.

## Real-data plan: CWRU
Official data portal: https://engineering.case.edu/bearingdatacenter/download-data-file

CWRU offers 12 kHz and 48 kHz accelerometer recordings with healthy and fault conditions. Use 12 kHz drive-end files consistently. Record filename, URL, SHA256, sample rate, channel, fault type, motor load, and measurement session. Split by recording and, where possible, physical bearing or operating condition; never put windows of one recording in both train and test. Evaluate a leave-one-load-out design separately from random grouped holdout. CWRU recordings can be confounded by load and experimental fault construction. Do not treat a single CWRU score as proof of generalization.

Before any automatic download, verify the dataset access terms. Do not commit raw data to Git.
