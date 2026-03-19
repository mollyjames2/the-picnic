"""
One-time script to pre-extract GIF frames as PNGs + a duration manifest.
Run locally before committing: python extract_gif_frames.py
Output: assets/GIFs/<gif_name>/ with 0000.png, 0001.png, ..., frames.json
"""

import json
import os
from pathlib import Path

from PIL import Image

GIF_DIR = Path("assets/GIFs")

for gif_path in sorted(GIF_DIR.glob("*.gif")):
    out_dir = GIF_DIR / gif_path.stem
    out_dir.mkdir(exist_ok=True)

    gif = Image.open(gif_path)
    durations = []

    for i in range(gif.n_frames):
        gif.seek(i)
        frame = gif.convert("RGBA")
        frame.save(out_dir / f"{i:04d}.png")
        durations.append(gif.info.get("duration", 100))

    (out_dir / "frames.json").write_text(json.dumps(durations))
    print(f"{gif_path.name}: {gif.n_frames} frames → {out_dir}/")
