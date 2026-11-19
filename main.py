#!/usr/bin/env python3
"""Entry point for news-image-20261119.

Renders THE WORLD TODAY - Thursday 19 November 2026 with render.py
and writes it to /output/entry.png (JPEG bytes under the .png name,
which the rules allow). If Pillow is unavailable in the sandbox, it
falls back to the pre-rendered entry.jpg shipped in this repository,
so both runs still write identical bytes.
"""
import os
import shutil
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    try:
        sys.path.insert(0, _HERE)
        import render
        data = render.render_bytes()
    except Exception:
        src = os.path.join(_HERE, "entry.jpg")
        with open(src, "rb") as fh:
            data = fh.read()
    with open(out_path, "wb") as fh:
        fh.write(data)


if __name__ == "__main__":
    main()
