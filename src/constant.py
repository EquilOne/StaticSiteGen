import re

CODE_FENCE_RE = re.compile(r"^```([a-zA-Z0-9]+)?\n")
OL_NUM_RE = re.compile(r"^(\d+)\. ")
