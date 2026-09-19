"""Resumable checkpoint runner for the H-trace step of b4_kitchen_run_v0_2.

NOT part of the frozen v0.2 pipeline itself -- this is purely an execution
harness to work around a sandboxed-session constraint (each shell call is
capped at a hard wall-clock budget, well under the ~10 minutes the full
82,219-frame Weingarten trace takes on this machine's 2 CPUs). It calls
the exact same frozen `_one_h` / `_read_vertices` functions from
b4_kitchen_run_v0_2.py, unchanged, in a resumable loop, persisting partial
results to a .npy checkpoint on the mounted (persistent) filesystem
between shell calls. No analysis parameter is touched by this file.
"""
from __future__ import annotations

import json
import multiprocessing
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import b4_kitchen_run_v0_2 as mod  # noqa: E402

mod.MOCAP_ARCHIVE = Path("/sessions/blissful-focused-lamport/mnt/Downloads/S13_Brownie_Mocap.zip")
mod.AUDIO_ARCHIVE = Path("/sessions/blissful-focused-lamport/mnt/Downloads/S13_Brownie_Audio.zip")

CHECKPOINT = Path("/sessions/blissful-focused-lamport/mnt/a/GIA-TIMDR/core/_kitchen_h_checkpoint.npy")
TIME_BUDGET_S = 140.0
BATCH = 2000


def main() -> None:
    t_start = time.time()
    vertices = mod._read_vertices()
    total = vertices.shape[0]

    if CHECKPOINT.exists():
        done = np.load(CHECKPOINT)
        start_idx = done.size
        print(f"resuming at {start_idx}/{total}", flush=True)
    else:
        done = np.empty(0, dtype=float)
        start_idx = 0
        print(f"starting fresh, total={total}", flush=True)

    if start_idx >= total:
        print("ALREADY COMPLETE", flush=True)
        return

    faces = np.asarray(json.loads(mod.TRIANGULATION.read_text(encoding="utf-8"))["faces"], dtype=int)
    context = multiprocessing.get_context("spawn")
    results = [done]
    idx = start_idx
    with ProcessPoolExecutor(
        max_workers=2,
        mp_context=context,
        initializer=mod._init_geometry_worker,
        initargs=(faces,),
    ) as pool:
        while idx < total and (time.time() - t_start) < TIME_BUDGET_S:
            end = min(idx + BATCH, total)
            batch_result = np.asarray(list(pool.map(mod._one_h, vertices[idx:end], chunksize=200)), dtype=float)
            results.append(batch_result)
            idx = end
            elapsed = time.time() - t_start
            print(f"[{elapsed:.1f}s] progress {idx}/{total}", flush=True)

    combined = np.concatenate(results)
    np.save(CHECKPOINT, combined)
    print(f"checkpoint saved: {combined.size}/{total}", flush=True)
    if combined.size >= total:
        print("ALL DONE", flush=True)


if __name__ == "__main__":
    main()
