#!/usr/bin/env python3
"""Temporal Fourier-phase history test on MAGE's committed UCSD Ped2 frames.

Tests whether a sequence of complex Fourier frames can be represented by an
initial phase plus ordered inter-frame phase increments. This is a signal
representation test, not a claim that an image field is a physical helix.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import cv2
import numpy as np


def wrap(a):
    return (a + np.pi) % (2*np.pi) - np.pi


def load_sequence(root: Path, clip="Test001", limit=180):
    folder = root / "data" / "ucsd_ped2" / "Test" / clip
    paths = sorted(folder.glob("*.png"))[:limit]
    if len(paths) < 20:
        raise RuntimeError(f"Need >=20 frames; found {len(paths)} in {folder}")
    frames=[]
    for p in paths:
        im=cv2.imread(str(p), cv2.IMREAD_GRAYSCALE)
        if im is None: raise RuntimeError(f"Could not read {p}")
        im=cv2.resize(im, (180,120), interpolation=cv2.INTER_AREA)
        frames.append(im.astype(np.float32))
    return paths, np.stack(frames)


def analyze(frames, seed=20261109):
    # Remove per-frame mean only; retain spatial structure and full complex FFT.
    centered=frames-frames.mean(axis=(1,2), keepdims=True)
    F=np.fft.fftshift(np.fft.fft2(centered, axes=(1,2)), axes=(1,2))
    phase=np.angle(F)
    amp=np.abs(F)
    # Stable bins: exclude DC and retain bins with meaningful average energy.
    h,w=phase.shape[1:]
    valid=np.ones((h,w),bool); valid[h//2-2:h//2+3,w//2-2:w//2+3]=False
    mean_amp=amp.mean(axis=0)
    threshold=np.quantile(mean_amp[valid],0.50)
    mask=valid & (mean_amp>=threshold)
    d=wrap(phase[1:]-phase[:-1])
    # Per-transition activity: mean absolute phase increment across valid bins.
    transition_activity=np.mean(np.abs(d[:,mask]),axis=1)
    # Reconstruct phase history from initial phase + ordered phase increments.
    rec=np.empty_like(phase)
    rec[0]=phase[0]
    for t in range(1,len(phase)):
        rec[t]=rec[t-1]+d[t-1]
    err=np.abs(wrap(rec-phase))
    weighted=np.broadcast_to(mask,err.shape)
    exact_mae=float(np.mean(err[weighted]))
    exact_p95=float(np.quantile(err[weighted],.95))
    # Shuffle time order of increments while keeping their marginal distribution.
    rng=np.random.default_rng(seed)
    perm=rng.permutation(len(d))
    ds=d[perm]
    shuffled=np.empty_like(phase); shuffled[0]=phase[0]
    for t in range(1,len(phase)):
        shuffled[t]=shuffled[t-1]+ds[t-1]
    sherr=np.abs(wrap(shuffled-phase))
    shuffled_mae=float(np.mean(sherr[weighted]))
    shuffled_p95=float(np.quantile(sherr[weighted],.95))
    # Reversal identity: reverse the frames, recompute increments; should equal
    # negative original increments in reverse temporal order.
    revphase=phase[::-1]
    drev=wrap(revphase[1:]-revphase[:-1])
    expected=wrap(-d[::-1])
    reversal_error=np.abs(wrap(drev-expected))
    # Temporal history strength and increment diversity.
    d_valid=d[:,mask]
    return {
      "frames":int(len(frames)), "fft_shape":[int(h),int(w)],
      "valid_frequency_bins":int(mask.sum()),
      "phase_increment_abs_median_rad":float(np.median(np.abs(d_valid))),
      "phase_increment_abs_p95_rad":float(np.quantile(np.abs(d_valid),.95)),
      "ordered_reconstruction_mae_rad":exact_mae,
      "ordered_reconstruction_p95_rad":exact_p95,
      "shuffled_history_reconstruction_mae_rad":shuffled_mae,
      "shuffled_history_reconstruction_p95_rad":shuffled_p95,
      "reverse_time_identity_max_error_rad":float(reversal_error.max()),
      "shuffle_to_ordered_mae_ratio":float(shuffled_mae/max(exact_mae,1e-15)),
      "transition_activity_mean_rad":float(transition_activity.mean()),
      "transition_activity_std_rad":float(transition_activity.std()),
      "transition_activity_series_rad":transition_activity.tolist(),
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mage-root",type=Path,required=True)
    ap.add_argument("--out",type=Path,default=Path("phase_history_result.json"))
    ap.add_argument("--clip",default="Test001")
    args=ap.parse_args()
    paths,frames=load_sequence(args.mage_root,args.clip)
    gt={"Test001":[61,180],"Test002":[95,180],"Test003":[1,146]}
    result={
      "schema":"gia-timdr-mage-temporal-phase-history-v1",
      "dataset":"MAGE-IN-IMAGE-DECODER/data/ucsd_ped2/Test/"+args.clip,
      "dataset_ground_truth_anomaly_frames":gt.get(args.clip),
      "status":"real_image_sequence_representation_test_not_physical_helix_validation",
      "method":"complex 2D FFT; ordered inter-frame wrapped phase increments; deterministic temporal shuffle control",
      "result":analyze(frames),
    }
    # Compare phase activity in transitions wholly inside normal/anomalous intervals.
    lo,hi=gt.get(args.clip,(None,None))
    activity=np.asarray(result["result"]["transition_activity_series_rad"])
    normal_idx=[]; anomalous_idx=[]
    for i in range(len(activity)):
        f0=i+1; f1=i+2
        is_anom=(lo is not None and f0>=lo and f0<=hi and f1>=lo and f1<=hi)
        if is_anom: anomalous_idx.append(i)
        elif lo is not None and (f0<lo or f0>hi) and (f1<lo or f1>hi): normal_idx.append(i)
    result["phase_activity_by_ground_truth"]={
      "normal_transition_count":len(normal_idx),
      "anomalous_transition_count":len(anomalous_idx),
      "normal_mean_rad":float(activity[normal_idx].mean()) if normal_idx else None,
      "anomalous_mean_rad":float(activity[anomalous_idx].mean()) if anomalous_idx else None,
      "interpretation":"descriptive only; no significance claim; intervals from dataset annotations"
    }
    result["result"].pop("transition_activity_series_rad",None)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__": main()
