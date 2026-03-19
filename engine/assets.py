import json
import os
import pygame
from pathlib import Path
from engine.settings import BASE_PATH

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


def load_gif_frames(path: str, size: tuple[int, int] | None = None) -> tuple[list, list]:
    """
    Load a GIF and return its frames as pygame Surfaces plus per-frame durations.

    Tries PIL first (local dev). Falls back to pre-extracted PNG frames for
    browser/pygbag deployments where Pillow is unavailable.

    Parameters
    ----------
    path : str
        Path to the GIF file (relative to BASE_PATH or absolute).
    size : tuple[int, int] | None
        If given, scale every frame to (width, height).

    Returns
    -------
    frames : list[pygame.Surface]
    durations : list[int]
        Per-frame display time in milliseconds.
    """
    full_path = path if os.path.isabs(path) else os.path.join(BASE_PATH, path)

    if HAS_PIL:
        gif = Image.open(full_path)
        frames: list[pygame.Surface] = []
        durations: list[int] = []
        for i in range(gif.n_frames):
            gif.seek(i)
            frame_rgba = gif.convert("RGBA")
            surf = pygame.image.fromstring(frame_rgba.tobytes(), frame_rgba.size, "RGBA").convert_alpha()
            if size:
                surf = pygame.transform.scale(surf, size)
            frames.append(surf)
            durations.append(gif.info.get("duration", 100))
        return frames, durations

    # PIL unavailable (browser/WASM) — load pre-extracted PNG frames
    png_dir = Path(full_path).with_suffix("")
    manifest = png_dir / "frames.json"
    if not manifest.exists():
        return [], []

    durations = json.loads(manifest.read_text())
    frames = []
    for i, _ in enumerate(durations):
        png_path = png_dir / f"{i:04d}.png"
        surf = pygame.image.load(str(png_path)).convert_alpha()
        if size:
            surf = pygame.transform.scale(surf, size)
        frames.append(surf)

    return frames, durations

class SpriteManager:
    def __init__(self):
        self.sprites = {}

    def load(self, name, path, size=None):
        full_path = os.path.join(BASE_PATH, path)
        image = pygame.image.load(full_path).convert_alpha()
        if size:
            image = pygame.transform.scale(image, size)
        self.sprites[name] = image

    def load_with_aspect_ratio(self, name, path, target_height):
        full_path = os.path.join(BASE_PATH, path)
        image = pygame.image.load(full_path).convert_alpha()
        original_width, original_height = image.get_width(), image.get_height()
        aspect_ratio = original_width / original_height
        scaled_width = int(target_height * aspect_ratio)
        scaled_image = pygame.transform.scale(image, (scaled_width, target_height))
        self.sprites[name] = scaled_image

    def get(self, name):
        return self.sprites.get(name)
