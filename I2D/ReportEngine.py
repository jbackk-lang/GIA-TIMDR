from core import TIMDR_pipeline_full

def generate_report(frame_bytes):
    core = TIMDR_pipeline_full(frame_bytes)
    return {
        "pipeline": core["pipeline"],
        "diagnostic": core["diagnostic"],
        "operators": core["operators"]
    }
