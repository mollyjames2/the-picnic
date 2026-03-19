"""Scene 4 — Choosing the perfect picnic spot."""
import asyncio
import os
import sys

import pygame

from engine.assets import load_gif_frames
from engine.dialogue import draw_3d_box, text_box
from engine.movement import follow_leader, move_player
import engine.settings as _S
from engine.settings import (
    BASE_PATH,
    BLACK,
    HEIGHT,
    MOVEMENT_SPEED,
    SPRITE_HEIGHT,
    SPRITE_WIDTH,
    WIDTH,
)
from data.dialogue import (
    SCENE_4_FLOWERS_MOLLY,
    SCENE_4_FLOWERS_REPEAT,
    SCENE_4_FLOWERS_SAM,
    SCENE_4_INTRO_MAGGIE,
    SCENE_4_INTRO_MOLLY,
    SCENE_4_INTRO_SAM,
    SCENE_4_LAKE_MAGGIE,
    SCENE_4_LAKE_MOLLY,
    SCENE_4_LAKE_REPEAT,
    SCENE_4_LAKE_SAM,
    SCENE_4_SUNNY_MOLLY,
    SCENE_4_SUNNY_REPEAT,
    SCENE_4_SUNNY_SAM,
    SCENE_4_TREE_EARLY_MOLLY,
    SCENE_4_TREE_EARLY_SAM,
    SCENE_4_TREE_SUCCESS_MAGGIE,
    SCENE_4_TREE_SUCCESS_MOLLY,
    SCENE_4_TREE_SUCCESS_SAM,
    SCENE_4_TREE_SUCCESS_SAM_2,
)

# Hotspot rectangles matching the background layout (priority order: tree first).
# x-ranges are kept non-overlapping: tree(60-245), sunny(255-410), flowers(420-575), lake(590-775)
_HOTSPOTS = {
    "tree":    pygame.Rect(60,  270, 185, 250),
    "sunny":   pygame.Rect(255, 300, 155, 220),
    "flowers": pygame.Rect(460, 220, 200, 130),
    "lake":    pygame.Rect(590, 340, 185, 220),
}

_SPOT_LABELS = {
    "tree":    "under the tree",
    "lake":    "by the lake",
    "flowers": "flower patch",
    "sunny":   "open sunny area",
}

_BAD_SPOTS = {"lake", "flowers", "sunny"}

_GIF_SOLAR    = os.path.join(BASE_PATH, "assets/GIFs/hot-solar-flare.gif")
_GIF_HAYFEVER = os.path.join(BASE_PATH, "assets/GIFs/hay-fever-sick.gif")
_IMG_SWAMP    = os.path.join(BASE_PATH, "assets/pictures/swamp.png")


# ── Init ──────────────────────────────────────────────────────────────────────

def _init_s4(gs: dict) -> None:
    """Set up all scene-4 state on first entry."""
    gs["s4_spots_visited"] = set()           # bad spots triggered at least once
    gs["s4_visit_counts"]  = {k: 0 for k in _HOTSPOTS}
    gs["s4_intro_done"]    = False
    gs["s4_complete"]      = False
    # Character starting positions for this scene — grouped near centre
    gs["sam_pos"]          = pygame.Vector2(370, HEIGHT - SPRITE_HEIGHT-250)
    gs["s4_molly_pos"]     = pygame.Vector2(270, HEIGHT - SPRITE_HEIGHT-250)
    gs["s4_maggie_pos"]    = pygame.Vector2(470, HEIGHT - SPRITE_HEIGHT-250)


# ── Drawing ───────────────────────────────────────────────────────────────────

def _draw_scene(screen: pygame.Surface, gs: dict) -> None:
    """Blit the background then all three characters."""
    screen.blit(gs["sprites"]["spot_bg"], (0, 0))
    spr = gs["sprites"]
    screen.blit(spr["molly"],  (gs["s4_molly_pos"].x,  gs["s4_molly_pos"].y))
    screen.blit(spr["maggie"], (gs["s4_maggie_pos"].x, gs["s4_maggie_pos"].y))
    screen.blit(spr["sam"],    (gs["sam_pos"].x,        gs["sam_pos"].y))


def _draw_spot_prompt(screen: pygame.Surface, spot: str, ready: bool) -> None:
    """Bottom-centre 'press ENTER' prompt when Sam stands in a hotspot."""
    if spot == "tree" and ready:
        label = "Press ENTER  —  this is the one!"
    else:
        label = f"Press ENTER to try: {_SPOT_LABELS[spot]}"
    bw, bh = 560, 56
    bx = (WIDTH - bw) // 2
    by = HEIGHT - bh - 8
    surf = pygame.Surface((bw, bh), pygame.SRCALPHA)
    draw_3d_box(surf, 0, 0, bw, bh)
    ts = _S.FONT_SMALL.render(label, True, BLACK)
    surf.blit(ts, ((bw - ts.get_width()) // 2, (bh - ts.get_height()) // 2))
    screen.blit(surf, (bx, by))


# ── Asset helpers ─────────────────────────────────────────────────────────────

def _get_gif(gs: dict, key: str, path: str) -> tuple:
    """Lazy-load and cache GIF frames scaled to full screen."""
    if key not in gs:
        frames, durs = load_gif_frames(path, size=(WIDTH, HEIGHT))
        gs[key] = (frames, durs)
    return gs[key]


def _get_swamp(gs: dict) -> pygame.Surface:
    """Lazy-load and cache the swamp image scaled to full screen."""
    if "s4_swamp_img" not in gs:
        img = pygame.image.load(_IMG_SWAMP).convert_alpha()
        gs["s4_swamp_img"] = pygame.transform.scale(img, (WIDTH, HEIGHT))
    return gs["s4_swamp_img"]


# ── GIF playback ──────────────────────────────────────────────────────────────

async def _play_gif_timed(
    screen: pygame.Surface,
    frames: list,
    durations: list,
    total_ms: int,
) -> None:
    """Animate GIF frames for total_ms milliseconds, then return."""
    if not frames:
        await asyncio.sleep(total_ms / 1000.0)
        return
    start = pygame.time.get_ticks()
    fi, last = 0, start
    while pygame.time.get_ticks() - start < total_ms:
        now = pygame.time.get_ticks()
        if durations and now - last >= durations[fi]:
            fi = (fi + 1) % len(frames)
            last = now
        screen.blit(frames[fi], (0, 0))
        pygame.display.flip()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        await asyncio.sleep(0)


# ── Vignettes ─────────────────────────────────────────────────────────────────

async def _vignette_lake(screen: pygame.Surface, gs: dict) -> None:
    _draw_scene(screen, gs)
    await text_box(screen, SCENE_4_LAKE_MOLLY, SCENE_4_LAKE_MAGGIE)
    # Full-screen swamp splash for 1.5 s
    screen.blit(_get_swamp(gs), (0, 0))
    pygame.display.flip()
    await asyncio.sleep(1.5)
    _draw_scene(screen, gs)
    await text_box(screen, SCENE_4_LAKE_SAM)


async def _vignette_sunny(screen: pygame.Surface, gs: dict) -> None:
    _draw_scene(screen, gs)
    await text_box(screen, SCENE_4_SUNNY_MOLLY)
    frames, durs = _get_gif(gs, "s4_solar_gif", _GIF_SOLAR)
    await _play_gif_timed(screen, frames, durs, 1500)
    _draw_scene(screen, gs)
    await text_box(screen, SCENE_4_SUNNY_SAM)


async def _vignette_flowers(screen: pygame.Surface, gs: dict) -> None:
    _draw_scene(screen, gs)
    await text_box(screen, SCENE_4_FLOWERS_MOLLY)
    frames, durs = _get_gif(gs, "s4_hayfever_gif", _GIF_HAYFEVER)
    await _play_gif_timed(screen, frames, durs, 1500)
    _draw_scene(screen, gs)
    await text_box(screen, SCENE_4_FLOWERS_SAM)


_VIGNETTES = {
    "lake":    _vignette_lake,
    "sunny":   _vignette_sunny,
    "flowers": _vignette_flowers,
}

_REPEAT_DIALOGUE = {
    "lake":    SCENE_4_LAKE_REPEAT,
    "sunny":   SCENE_4_SUNNY_REPEAT,
    "flowers": SCENE_4_FLOWERS_REPEAT,
}


# ── Main scene function ───────────────────────────────────────────────────────

async def run(screen: pygame.Surface, game_state: dict, keys, event) -> None:
    gs = game_state

    # First entry — set up state
    if "s4_spots_visited" not in gs:
        _init_s4(gs)

    # ── Phase 0: opening dialogue ──────────────────────────────────────────────
    if not gs["s4_intro_done"]:
        _draw_scene(screen, gs)
        await text_box(screen, SCENE_4_INTRO_MOLLY, SCENE_4_INTRO_SAM, SCENE_4_INTRO_MAGGIE)
        gs["s4_intro_done"] = True
        return

    # ── Phase 1: exploration ───────────────────────────────────────────────────
    if not gs["s4_complete"]:
        move_player(keys, gs["sam_pos"], speed=MOVEMENT_SPEED)
        gs["sam_pos"].x = max(0, min(WIDTH  - SPRITE_WIDTH,  gs["sam_pos"].x))
        gs["sam_pos"].y = max(0, min(HEIGHT - SPRITE_HEIGHT, gs["sam_pos"].y))
        # Molly trails Sam; Maggie trails Molly
        follow_leader(gs["sam_pos"],       gs["s4_molly_pos"],  follow_distance=55, follow_speed=4)
        follow_leader(gs["s4_molly_pos"],  gs["s4_maggie_pos"], follow_distance=55, follow_speed=4)

        sam_rect = pygame.Rect(gs["sam_pos"].x, gs["sam_pos"].y, SPRITE_WIDTH, SPRITE_HEIGHT)

        # Detect hotspot — tree checked first to win any overlap
        current_spot = None
        for name in ("tree", "sunny", "flowers", "lake"):
            if sam_rect.colliderect(_HOTSPOTS[name]):
                current_spot = name
                break

        all_explored = _BAD_SPOTS.issubset(gs["s4_spots_visited"])

        # React to ENTER press
        if (
            current_spot
            and event
            and event.type == pygame.KEYDOWN
            and event.key == pygame.K_RETURN
        ):
            count = gs["s4_visit_counts"][current_spot]
            gs["s4_visit_counts"][current_spot] += 1

            if current_spot == "tree":
                if not all_explored:
                    # Gentle nudge to explore the other spots first
                    _draw_scene(screen, gs)
                    await text_box(screen, SCENE_4_TREE_EARLY_MOLLY, SCENE_4_TREE_EARLY_SAM)
                else:
                    # All spots seen — this is the winner
                    _draw_scene(screen, gs)
                    await text_box(
                        screen,
                        SCENE_4_TREE_SUCCESS_MOLLY,
                        SCENE_4_TREE_SUCCESS_SAM,
                        SCENE_4_TREE_SUCCESS_MAGGIE,
                        SCENE_4_TREE_SUCCESS_SAM_2,
                    )
                    gs["s4_complete"] = True
                    gs["scene"] = 5
                    return
            else:
                # Mark as visited (for the "all explored" check)
                gs["s4_spots_visited"].add(current_spot)
                if count == 0:
                    await _VIGNETTES[current_spot](screen, gs)
                else:
                    # Repeat visit — short reaction, no full vignette
                    _draw_scene(screen, gs)
                    await text_box(screen, _REPEAT_DIALOGUE[current_spot])

        # ── Draw ──────────────────────────────────────────────────────────────
        _draw_scene(screen, gs)
        if current_spot:
            ready = all_explored and current_spot == "tree"
            _draw_spot_prompt(screen, current_spot, ready)
