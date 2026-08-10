from core import TIMDR_pipeline_full

def split_layers(frame_bytes):
    core = TIMDR_pipeline_full(frame_bytes)
    return core["pipeline"]["I"], core["pipeline"]["M"]
