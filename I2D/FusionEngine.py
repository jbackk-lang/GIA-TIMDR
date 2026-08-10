from core import TIMDR_pipeline_full

def fuse(frame_bytes):
    core = TIMDR_pipeline_full(frame_bytes)
    return {
        "twist": core["operators"]["M"],
        "prime": core["operators"]["prime"],
        "spectral": core["operators"]["spectral"],
        "defects": core["operators"]["deltaS"]
    }
