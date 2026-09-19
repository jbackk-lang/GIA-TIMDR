"""Frozen B4-Kitchen v0.2 execution for CMU Kitchen S13 Brownie.

Implements exactly docs/geometry/PREREG_B4_KITCHEN_v0.2.md. Reuses the
geometry/audio extraction and Lambda-block construction from
core/b4_kitchen_run.py (v0.1) UNCHANGED. The only change is the null
distribution: circular block permutation (block length L=12, frozen via
L=round(n**(1/3)), PREREG Section 3) instead of full independent
permutation, because v0.1's own negative control showed the full
permutation test is invalid for autocorrelated Lambda series.

It intentionally has no tuning switches: all analysis choices are frozen
in docs/geometry/PREREG_B4_KITCHEN_v0.2.md.
"""
from __future__ import annotations

import csv
import io
import json
import math
import multiprocessing
import sys
import wave
import zipfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
MOCAP_ARCHIVE = Path(r"C:\Users\jback\Downloads\S13_Brownie_Mocap.zip")
AUDIO_ARCHIVE = Path(r"C:\Users\jback\Downloads\S13_Brownie_Audio.zip")
TRIANGULATION = REPO / "docs" / "geometry" / "kitchen_triangulation.json"
RESULT_PATH = REPO / "docs" / "geometry" / "B4_KITCHEN_RESULT_v0.2.json"
WINDOW_SIZE = 50
EPS = 1e-9
N_PERMUTATIONS = 10_000
SEED = 20_260_919
ALPHA = 0.05
BLOCK_LENGTH = 12  # frozen: round(1645 ** (1/3)) -- PREREG v0.2 Section 3
GEOMETRY_WORKERS = 4
_WORKER_FACES: np.ndarray | None = None


def _init_geometry_worker(faces: np.ndarray) -> None:
    global _WORKER_FACES
    sys.path.insert(0, str(REPO / "TIMDR-Geometry-Formalism"))
    _WORKER_FACES = faces


def _one_h(points: np.ndarray) -> float:
    # This calls the repository's frozen Weingarten adapter unchanged.
    from timdr_geometry.geometry_meta_alignment import mesh_snapshot_to_mean_curvature
    from timdr_geometry.weingarten import Mesh

    volume = abs(float(np.linalg.det(np.stack((points[1] - points[0], points[2] - points[0], points[3] - points[0]))) / 6.0))
    if not np.all(np.isfinite(points)) or volume <= 1e-10:
        raise ValueError("invalid frozen geometry")
    if _WORKER_FACES is None:
        raise RuntimeError("geometry worker is not initialized")
    return mesh_snapshot_to_mean_curvature(Mesh(points, _WORKER_FACES))


def _seconds(value: str) -> float:
    hour, minute, second, fraction = value.split("_")
    return int(hour) * 3600 + int(minute) * 60 + int(second) + int(fraction) / 1e7


def _lambda(values: np.ndarray) -> float:
    values = np.asarray(values, dtype=float)
    if values.ndim != 1 or values.size == 0 or not np.all(np.isfinite(values)):
        raise ValueError("invalid Lambda input")
    std = float(np.std(values))
    mean = float(np.mean(values))
    return std / (std + abs(mean) + EPS)


def _rank(values: np.ndarray) -> np.ndarray:
    order = np.argsort(values, kind="mergesort")
    ranks = np.empty(values.size, dtype=float)
    ranks[order] = np.arange(values.size, dtype=float)
    sorted_values = values[order]
    start = 0
    while start < values.size:
        end = start + 1
        while end < values.size and sorted_values[end] == sorted_values[start]:
            end += 1
        if end - start > 1:
            ranks[order[start:end]] = (start + end - 1) / 2.0
        start = end
    return ranks


def _spearman(x: np.ndarray, y: np.ndarray) -> float:
    rx, ry = _rank(np.asarray(x, dtype=float)), _rank(np.asarray(y, dtype=float))
    rx -= rx.mean()
    ry -= ry.mean()
    denom = float(np.linalg.norm(rx) * np.linalg.norm(ry))
    if denom == 0.0:
        raise ValueError("constant series has undefined Spearman rho")
    return float(np.dot(rx, ry) / denom)


def _circular_block_permutation_test(x: np.ndarray, y: np.ndarray, seed: int, block_length: int = BLOCK_LENGTH) -> dict[str, float | int]:
    """Circular block permutation test (PREREG v0.2 Section 3).

    Ranks do not change under a permutation of y, so we precompute ranks
    once. The null is built by circularly shifting y by a random offset,
    cutting it into contiguous blocks of `block_length`, and reassembling
    those blocks in random order (permuting block ORDER, not contents) --
    this preserves within-block autocorrelation while destroying the
    pairing between x and y, unlike full independent permutation.
    """
    rx = _rank(np.asarray(x, dtype=float))
    ry_full = _rank(np.asarray(y, dtype=float))
    rx -= rx.mean()
    n = rx.size
    denom_x = float(np.linalg.norm(rx))

    def _rho_for(ry_arranged: np.ndarray) -> float:
        ry = ry_arranged - ry_arranged.mean()
        denom = denom_x * float(np.linalg.norm(ry))
        if denom == 0.0:
            raise ValueError("constant series has undefined Spearman rho")
        return float(np.dot(rx, ry) / denom)

    observed = _rho_for(ry_full)

    rng = np.random.default_rng(seed)
    n_blocks = math.ceil(n / block_length)
    exceedances = 0
    for _ in range(N_PERMUTATIONS):
        offset = int(rng.integers(0, n))
        y_shifted = np.concatenate((ry_full[offset:], ry_full[:offset]))
        block_order = rng.permutation(n_blocks)
        pieces = [y_shifted[b * block_length : (b + 1) * block_length] for b in block_order]
        y_perm = np.concatenate(pieces)[:n]
        rho = _rho_for(y_perm)
        if abs(rho) >= abs(observed):
            exceedances += 1
    return {
        "rho": observed,
        "pvalue": (exceedances + 1) / (N_PERMUTATIONS + 1),
        "permutations": N_PERMUTATIONS,
        "exceedances": exceedances,
        "block_length": block_length,
        "method": "circular_block_permutation",
    }


def _ar1(n: int, phi: float, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    result = np.empty(n, dtype=float)
    result[0] = rng.normal()
    for i in range(1, n):
        result[i] = phi * result[i - 1] + rng.normal()
    return result


def _read_times() -> np.ndarray:
    with zipfile.ZipFile(MOCAP_ARCHIVE) as archive:
        lines = archive.read("mocapTime-sync.txt").decode("ascii").splitlines()
    values = []
    for line in lines:
        frame, stamp = line.split()
        if int(frame.split(":")[1]) != len(values) + 1:
            raise ValueError("non-contiguous source frame numbering")
        values.append(_seconds(stamp))
    return np.asarray(values, dtype=float)


def _read_vertices() -> np.ndarray:
    config = json.loads(TRIANGULATION.read_text(encoding="utf-8"))
    wanted = [column for vertex in config["vertices"] for column in vertex["coordinate_columns"]]
    with zipfile.ZipFile(MOCAP_ARCHIVE) as archive, archive.open("brownie_1.V.global") as raw:
        rows = csv.reader(line.decode("utf-8") for line in raw)
        header = [cell.strip().strip('"') for cell in next(rows)]
        indices = [header.index(name) for name in wanted]
        values = [np.asarray([float(row[index]) for index in indices], dtype=float).reshape(4, 3) for row in rows]
    if len(values) != 82_221:
        raise ValueError(f"unexpected V.global row count: {len(values)}")
    return np.asarray(values[1:82_220], dtype=float)


def _read_q(times: np.ndarray) -> np.ndarray:
    with zipfile.ZipFile(AUDIO_ARCHIVE) as archive:
        blob = archive.read("AudioTrack.wav")
        sync = archive.read("recording-synch.log").decode("ascii")
    start_line = next(line for line in sync.splitlines() if "opened at:" in line)
    audio_start = _seconds(start_line.rsplit(":", 1)[1].strip())
    with wave.open(io.BytesIO(blob), "rb") as wav:
        if wav.getnchannels() != 1 or wav.getsampwidth() != 2 or wav.getframerate() != 44_100:
            raise ValueError("AudioTrack.wav does not match frozen audio format")
        samples = np.frombuffer(wav.readframes(wav.getnframes()), dtype="<i2").astype(float)
        fs = wav.getframerate()
    q = np.empty(times.size - 1, dtype=float)
    for i, (begin, end) in enumerate(zip(times[:-1], times[1:])):
        lo = math.ceil((begin - audio_start) * fs)
        hi = math.ceil((end - audio_start) * fs)
        if lo < 0 or hi > samples.size or hi <= lo:
            raise ValueError(f"invalid audio interval for source frame {i + 1}")
        q[i] = float(np.sqrt(np.mean(np.square(samples[lo:hi]))))
    return q


def _h_trace(vertices: np.ndarray) -> np.ndarray:
    faces = np.asarray(json.loads(TRIANGULATION.read_text(encoding="utf-8"))["faces"], dtype=int)
    context = multiprocessing.get_context("spawn")
    with ProcessPoolExecutor(
        max_workers=GEOMETRY_WORKERS,
        mp_context=context,
        initializer=_init_geometry_worker,
        initargs=(faces,),
    ) as pool:
        return np.asarray(list(pool.map(_one_h, vertices, chunksize=250)), dtype=float)


def _blocks(values: np.ndarray) -> np.ndarray:
    return np.asarray([_lambda(values[start : start + WINDOW_SIZE]) for start in range(0, values.size, WINDOW_SIZE)])


def _controls(n: int) -> dict[str, object]:
    positive = np.arange(n, dtype=float)
    positive_test = _circular_block_permutation_test(positive, positive, SEED)
    negative_test = _circular_block_permutation_test(_ar1(n, 0.8, 20_260_917), _ar1(n, 0.8, 20_260_918), SEED)
    return {
        "positive": positive_test,
        "negative": negative_test,
        "passed": positive_test["pvalue"] < ALPHA and negative_test["pvalue"] >= ALPHA,
    }


def main() -> None:
    times = _read_times()
    vertices = _read_vertices()
    if vertices.shape[0] != times.size - 1:
        raise ValueError("geometry/Q source-grid length mismatch")
    q = _read_q(times)
    h = _h_trace(vertices)
    lambda_g, lambda_meta = _blocks(h), _blocks(q)
    if lambda_g.size != lambda_meta.size or lambda_g.size != 1645:
        raise ValueError("unexpected frozen block count")
    controls = _controls(lambda_g.size)
    if not controls["passed"]:
        verdict = "INCONCLUSIVE"
        main_test = None
    else:
        main_test = _circular_block_permutation_test(lambda_g, lambda_meta, SEED)
        verdict = "SUPPORTED" if main_test["pvalue"] < ALPHA else "NOT SUPPORTED"
    report = {
        "dataset_id": "CMU_KITCHEN_S13_BROWNIE_v0.1",
        "prereg_version": "B4_KITCHEN_v0.2",
        "method": "circular_block_permutation",
        "block_length": BLOCK_LENGTH,
        "verdict": verdict,
        "n_geometry_frames": int(h.size),
        "n_blocks": int(lambda_g.size),
        "h_summary": {"min": float(h.min()), "max": float(h.max()), "mean": float(h.mean())},
        "q_summary": {"min": float(q.min()), "max": float(q.max()), "mean": float(q.mean())},
        "lambda_g_summary": {"min": float(lambda_g.min()), "max": float(lambda_g.max()), "mean": float(lambda_g.mean())},
        "lambda_meta_summary": {"min": float(lambda_meta.min()), "max": float(lambda_meta.max()), "mean": float(lambda_meta.mean())},
        "controls": controls,
        "main_test": main_test,
        "alpha": ALPHA,
        "seed": SEED,
    }
    RESULT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2), flush=True)


if __name__ == "__main__":
    main()
