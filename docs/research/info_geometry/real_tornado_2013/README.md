# Real NEXRAD observations — Moore tornado, 2013-05-20

This folder records **10 actual user-uploaded KTLX Level II radar files**, spanning 20:03:56–20:42:15 UTC (97,646,751 bytes total). The JSON manifest lists the exact file names, sizes, SHA-256 hashes and public download URLs. These are observational inputs, not simulation output.

**Status:** source files verified locally by name, size and SHA-256. The raw binary files are **not stored in GitHub**. No observed TIMDR MIN–MAX–Δt triples have yet been extracted. Download the files using the script and verify checksums before processing.

**Reproduce:** `python download_ktlx.py` (requires Internet access). The script downloads the files from the public archive, verifies hashes, and saves them to `data/`. To preserve reproducibility, do not modify the files.

The archive is external and its future availability is not guaranteed. This manifest allows verification against independently retained copies.
