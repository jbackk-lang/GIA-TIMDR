from core import TIMDR_pipeline_full

def analyze_rhythm(frame_bytes):
    core = TIMDR_pipeline_full(frame_bytes)
    return core["operators"]["prime"]
