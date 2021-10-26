import os

from typing import Union
from pathlib import Path

VIDEO_SOURCE: Union[str, int] = os.environ["VIDEO_SOURCE"]
DETECT_HUMAN: bool = bool(os.environ["DETECT_HUMAN"])
HOOK_URL: str = os.environ["HOOK_URL"]
CLIP_DURATION: int = int(os.environ["CLIP_DURATION"])
OUTPUT_DIR = os.environ["OUTPUT_DIR"] == "null"

try:
    VIDEO_SOURCE = int(VIDEO_SOURCE)
except ValueError:
    VIDEO_SOURCE = VIDEO_SOURCE
finally:
    if OUTPUT_DIR:
        OUTPUT_DIR = Path(Path(__file__).parent.parent, "output/")

        if not OUTPUT_DIR.exists():
            OUTPUT_DIR.mkdir()

        OUTPUT_DIR = str(OUTPUT_DIR)
