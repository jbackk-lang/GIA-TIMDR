from core import TIMDR_pipeline_full

def color_psych_map(frame_bytes):
    core = TIMDR_pipeline_full(frame_bytes)
    spectral = core["operators"]["spectral"]
    return spectral
