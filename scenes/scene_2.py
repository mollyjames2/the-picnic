import asyncio
import sys

import pygame

import engine.settings as _S
from engine.settings import (
    WIDTH, HEIGHT, WHITE, BLACK,
    SPRITE_WIDTH, SPRITE_HEIGHT, MOVEMENT_SPEED,
)

_WALKOFF_Y = HEIGHT - SPRITE_HEIGHT
from engine.dialogue import text_box, draw_3d_box
from data.dialogue import (
    SCENE_2_SAM_NICE_DAY,
    SCENE_2_MOLLY_WHERE,
    SCENE_2_CHOICES,
    SCENE_2_MOLLY_PLAN,
)

_MOLLY_TARGET_X = 480   # x-position Molly walks to before stopping
_WALK_SPEED     = MOVEMENT_SPEED
_CAR_SPEED      = 15    # px/frame for the driving transition


# ── Drawing helpers ────────────────────────────────────────────────────────────

def _draw_kitchen(screen: pygame.Surface, gs: dict, show_basket: bool = True) -> None:
    """Kitchen background — same animated GIF as Scene 1, no floor items."""
    from engine.settings import LIGHT_BROWN
    frames    = gs.get("s1_bg_frames", [])
    durations = gs.get("s1_bg_durations", [])
    screen.fill(LIGHT_BROWN)
    if frames:
        now = pygame.time.get_ticks()
        idx = gs["s1_bg_frame_idx"]
        if now - gs["s1_bg_last_tick"] >= durations[idx]:
            gs["s1_bg_frame_idx"] = (idx + 1) % len(frames)
            gs["s1_bg_last_tick"] = now
            idx = gs["s1_bg_frame_idx"]
        screen.blit(frames[idx], (0, gs.get("s1_bg_y_offset", 0)))
    spr = gs["sprites"]
    screen.blit(spr["table"], (gs["s1_table_pos"].x, gs["s1_table_pos"].y))
    if show_basket:
        screen.blit(spr["basket"], (gs["s1_basket_pos"].x, gs["s1_basket_pos"].y))


def _draw_characters(
    screen: pygame.Surface, gs: dict, molly_pos: pygame.Vector2
) -> None:
    spr = gs["sprites"]
    screen.blit(spr["maggie"], (gs["maggie_pos"].x, gs["maggie_pos"].y))
    screen.blit(spr["sam"],    (gs["sam_pos"].x,    gs["sam_pos"].y))
    screen.blit(spr["molly"],  (molly_pos.x,        molly_pos.y))


def _full_redraw(
    screen: pygame.Surface, gs: dict, molly_pos: pygame.Vector2,
    show_basket: bool = True,
) -> None:
    _draw_kitchen(screen, gs, show_basket)
    _draw_characters(screen, gs, molly_pos)


# ── Choice menu ────────────────────────────────────────────────────────────────

async def _choice_box(screen: pygame.Surface, prompt: str, choices: list) -> int:
    """
    Render a multiple-choice menu over the current screen contents.

    Parameters
    ----------
    screen : pygame.Surface
        The display surface.
    prompt : str
        Question line shown at the top of the box.
    choices : list
        List of choice strings.

    Returns
    -------
    int
        Index of the selected option.
    """
    box_x, box_y = 50, HEIGHT - 190
    box_w, box_h = WIDTH - 100, 170
    selected = 0
    choosing = True

    while choosing:
        surf = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        draw_3d_box(surf, 0, 0, box_w, box_h)

        prompt_surf = _S.FONT_SMALL.render(prompt, True, BLACK)
        surf.blit(prompt_surf, (20, 16))

        for i, choice in enumerate(choices):
            prefix = "\u25BA " if i == selected else "  "
            text_surf = _S.FONT_SMALL.render(prefix + choice, True, BLACK)
            surf.blit(text_surf, (20, 55 + i * 36))

        screen.blit(surf, (box_x, box_y))
        pygame.display.flip()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_UP:
                    selected = (selected - 1) % len(choices)
                elif ev.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(choices)
                elif ev.key == pygame.K_RETURN:
                    choosing = False

        await asyncio.sleep(0)

    return selected


# ── Main scene function ────────────────────────────────────────────────────────

async def run(screen: pygame.Surface, game_state: dict, keys, event) -> None:
    gs        = game_state
    molly_pos = gs["s2_molly_pos"]

    # ── Phase 0: Molly enters from the right, then opening line ───────────────
    if not gs.get("s2_intro_done"):
        if molly_pos.x > _MOLLY_TARGET_X:
            molly_pos.x -= _WALK_SPEED
            _full_redraw(screen, gs, molly_pos)
            return

        # Molly has arrived — show Sam's opening line
        _full_redraw(screen, gs, molly_pos)
        await text_box(screen, SCENE_2_SAM_NICE_DAY)
        gs["s2_intro_done"] = True
        return

    # ── Phase 1: Destination choice, then Molly's reply ───────────────────────
    if not gs.get("s2_choice_done"):
        _full_redraw(screen, gs, molly_pos)
        idx = await _choice_box(screen, SCENE_2_MOLLY_WHERE, SCENE_2_CHOICES)
        gs["destinationChoice"] = ["beach", "woods", "view"][idx]
        # All choices lead to the same response
        _full_redraw(screen, gs, molly_pos)
        await text_box(screen, SCENE_2_MOLLY_PLAN)
        gs["s2_choice_done"] = True
        # Arrange characters for the walk-off: Molly leads, Sam behind, Maggie last
        molly_pos.x,        molly_pos.y        = 460, _WALKOFF_Y
        gs["sam_pos"].x,    gs["sam_pos"].y    = 370, _WALKOFF_Y
        gs["maggie_pos"].x, gs["maggie_pos"].y = 280, _WALKOFF_Y
        return

    # ── Phase 2: All three walk off screen to the right ───────────────────────
    if not gs.get("s2_walkoff_done"):
        molly_pos.x        += _WALK_SPEED
        gs["sam_pos"].x    += _WALK_SPEED
        gs["maggie_pos"].x += _WALK_SPEED

        _draw_kitchen(screen, gs, show_basket=False)

        # Basket carried by Molly — floats just above her head
        spr = gs["sprites"]
        bw, bh = gs["s1_basket_size"]
        bx = molly_pos.x + SPRITE_WIDTH // 2 - bw // 2
        by = molly_pos.y - bh - 4
        if bx < WIDTH:
            screen.blit(spr["basket"], (bx, by))

        _draw_characters(screen, gs, molly_pos)

        if gs["maggie_pos"].x > WIDTH:
            gs["s2_walkoff_done"] = True
        return

    # ── Phase 3: Driving scene ────────────────────────────────────────────────
    spr = gs["sprites"]
    screen.blit(spr["road"], (0, 0))

    gs["s2_car_x"] += _CAR_SPEED
    car_surf = spr["redcar"]
    car_y    = HEIGHT * 2 // 3 - car_surf.get_height() // 2 + 20
    screen.blit(car_surf, (int(gs["s2_car_x"]), car_y))

    if gs["s2_car_x"] > WIDTH:
        gs["scene"] = 3
