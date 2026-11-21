"""Neighbour-Waker 3000 catalogue entry.

Reads the studio product shot (gadget.png) from this repository and writes
it as a 1024x1024 PNG to the output directory, unchanged in content.
"""

import os
from pathlib import Path

from PIL import Image

SIZE = 1024


def main() -> None:
    here = Path(__file__).resolve().parent
    src = here / "gadget.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "entry.png"

    with Image.open(src) as im:
        im = im.convert("RGB")
        # Fit inside the 1024x1024 frame, keep aspect, centre on the shot's
        # own backdrop colour (sampled from the top-left corner) so the
        # padding blends with the studio background instead of a hard white.
        bg = im.getpixel((0, 0))
        im.thumbnail((SIZE, SIZE), Image.LANCZOS)
        canvas = Image.new("RGB", (SIZE, SIZE), bg)
        x = (SIZE - im.width) // 2
        y = (SIZE - im.height) // 2
        canvas.paste(im, (x, y))
        canvas.save(out_path, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
