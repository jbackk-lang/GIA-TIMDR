from core import TIMDR_pipeline_full

def detect_overlay(frame_bytes):
    core = TIMDR_pipeline_full(frame_bytes)
    return core["operators"]["spectral"]
