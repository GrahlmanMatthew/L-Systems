import os

FPS_TARGET: int = int(os.environ.get("FPS_TARGET", 60))
SEGMENTS_PER_FRAME: int = int(os.environ.get("SEGMENTS_PER_FRAME", 8))
