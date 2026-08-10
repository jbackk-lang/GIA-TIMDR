from core import TIMDR_pipeline_full

def scan_defects(frame_bytes):
    core = TIMDR_pipeline_full(frame_bytes)
    return core["operators"]["deltaS"]
