import re
from pathlib import Path

CODE_FENCE_RE = re.compile(r"^```([a-zA-Z0-9]+)?\n")
OL_NUM_RE = re.compile(r"^(\d+)\. ")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "static"
DST_DIR = PROJECT_ROOT / "docs"
CONTENT_DIR = PROJECT_ROOT / "content"
PUBLIC_DIR = PROJECT_ROOT / "public"
