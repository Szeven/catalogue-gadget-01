#!/usr/bin/env python3
"""The Neighbour-Waker 3000: fit the catalogue shot into a 1024x1024 entry."""
import os
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main() -> None:
    shot = Image.open(HERE / "gadget.png").convert("RGB")
    pad = shot.getpixel((0, 0))
    canvas = Image.new("RGB", (1024, 1024), pad)
    shot.thumbnail((1024, 1024), Image.LANCZOS)
    x = (1024 - shot.width) // 2
    y = (1024 - shot.height) // 2
    canvas.paste(shot, (x, y))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / "entry.png"
    canvas.save(out, format="PNG", optimize=True)
    # The gate caps entry.png at 1 MiB: fall back to JPEG if PNG runs over.
    if out.stat().st_size > 1_048_576:
        canvas.save(OUT_DIR / "entry.jpg", format="JPEG", quality=92)
        out.unlink()
        (OUT_DIR / "entry.jpg").rename(OUT_DIR / "entry.png")


if __name__ == "__main__":
    main()
