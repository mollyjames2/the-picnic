import asyncio
import sys

import pygame

import engine.settings as _S
from engine.settings import WIDTH, HEIGHT, WHITE, BLACK
from engine.dialogue import text_box, draw_3d_box
from data.dialogue import (
    SCENE_3_MOLLY_SUN,
    SCENE_3_SAM_BLOSSOMS,
    SCENE_3_MOLLY_QUESTION,
    SCENE_3_CHOICES,
    SCENE_3_CHOICE_KEYS,
    SCENE_3_FOLLOWUP,
    SCENE_3_MOLLY_ARRIVED,
    SCENE_3_MAGGIE_BOOF,
    SCENE_3_SAM_KNOWS,
    SCENE_3_MOLLY_MORON,
    SCENE_3_MAGGIE_LEGEND,
    SCENE_3_MOLLY_ALRIGHT,
)

_CAR_IMG_W, _CAR_IMG_H = 640, 352
_CAR_IMG_X = (WIDTH  - _CAR_IMG_W) // 2
_BORDER = 4
_CAR_IMG_Y = 22                            # small top gap


def _draw_car_bg(screen: pygame.Surface, bg: pygame.Surface) -> None:
    """Render the car interior image in a white-bordered box on black."""
    screen.fill(BLACK)
    pygame.draw.rect(
        screen, WHITE,
        (_CAR_IMG_X - _BORDER, _CAR_IMG_Y - _BORDER,
         _CAR_IMG_W + _BORDER * 2, _CAR_IMG_H + _BORDER * 2),
    )
    screen.blit(bg, (_CAR_IMG_X, _CAR_IMG_Y))


def _wrap_text(text: str, font: pygame.font.Font, max_width: int) -> list:
    words = text.split()
    lines, current = [], ""
    for word in words:
        test = f"{current} {word}".strip()
        if font.size(test)[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


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
    box_x = 50
    box_w  = WIDTH - 100
    inner_w = box_w - 40
    line_h = _S.FONT_SMALL.get_linesize()

    prompt_lines = _wrap_text(prompt, _S.FONT_SMALL, inner_w)
    choices_y_start = 16 + len(prompt_lines) * line_h + 8
    box_h = max(170, choices_y_start + len(choices) * 36 + 20)
    box_y = HEIGHT - box_h - 10

    selected = 0
    choosing = True

    while choosing:
        surf = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        draw_3d_box(surf, 0, 0, box_w, box_h)

        for li, line in enumerate(prompt_lines):
            prompt_surf = _S.FONT_SMALL.render(line, True, BLACK)
            surf.blit(prompt_surf, (20, 16 + li * line_h))

        for i, choice in enumerate(choices):
            prefix = "\u25BA " if i == selected else "  "
            text_surf = _S.FONT_SMALL.render(prefix + choice, True, BLACK)
            surf.blit(text_surf, (20, choices_y_start + i * 36))

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


async def run(screen: pygame.Surface, game_state: dict, keys, event) -> None:
    gs = game_state
    bg = gs["sprites"]["car_bg"]

    # ── Phase 0: opening dialogue about spring / living here ─────────────────
    if not gs.get("s3_intro_done"):
        _draw_car_bg(screen, bg)
        await text_box(screen, SCENE_3_MOLLY_SUN, SCENE_3_SAM_BLOSSOMS)
        gs["s3_intro_done"] = True
        return

    # ── Phase 1: hidden remembered choice ────────────────────────────────────
    if not gs.get("s3_choice_done"):
        _draw_car_bg(screen, bg)
        idx = await _choice_box(screen, SCENE_3_MOLLY_QUESTION, SCENE_3_CHOICES)
        gs["livingHereChoice"] = SCENE_3_CHOICE_KEYS[idx]
        gs["s3_choice_done"] = True
        return

    # ── Phase 2: follow-up + arrival ─────────────────────────────────────────
    if not gs.get("s3_arrival_done"):
        _draw_car_bg(screen, bg)
        followup = SCENE_3_FOLLOWUP[gs["livingHereChoice"]]
        await text_box(
            screen,
            followup,
            SCENE_3_MOLLY_ARRIVED,
            SCENE_3_MAGGIE_BOOF,
            SCENE_3_SAM_KNOWS,
            SCENE_3_MOLLY_MORON,
            SCENE_3_MAGGIE_LEGEND,
            SCENE_3_MOLLY_ALRIGHT,
        )
        gs["s3_arrival_done"] = True
        return

    # ── Phase 3: full-screen destination image for 2 seconds ─────────────────
    if not gs.get("s3_destination_shown"):
        dest_key = f"dest_{gs.get('destinationChoice', 'beach')}"
        screen.blit(gs["sprites"][dest_key], (0, 0))
        pygame.display.flip()
        await asyncio.sleep(2)
        gs["s3_destination_shown"] = True
        return

    gs["scene"] = 4
