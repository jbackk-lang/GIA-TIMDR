from core import TIMDR_pipeline_full

def detect_twist(frame_bytes):
    core = TIMDR_pipeline_full(frame_bytes)
    return core["operators"]["M"]
