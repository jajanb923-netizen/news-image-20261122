#!/usr/bin/env python3
"""Copy the pre-drawn entry image to the grader output directory.

Python 3.13 standard library only; no network. The image itself was drawn
by draw.py (Pillow) in this same session and is shipped in the repository
as entry.png, so both runs write byte-identical output.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / "entry.png", out_dir / "entry.png")


if __name__ == "__main__":
    main()
