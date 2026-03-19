import asyncio
import sys

import pygame

import engine.settings as _S
from engine.settings import WIDTH, HEIGHT, BLACK, SPRITE_WIDTH, SPRITE_HEIGHT
from engine.dialogue import text_box, draw_3d_box
from data.dialogue import (
    SCENE_5_SAM_SPOT,
    SCENE_5_HOUSE_QUESTION,
    SCENE_5_HOUSE_CHOICES,
    SCENE_5_HOUSE_FOLLOWUP,
    SCENE_5_HOME_QUESTION,
    SCENE_5_HOME_CHOICES,
    SCENE_5_HOME_CHOICE_KEYS,
    SCENE_5_HOME_FOLLOWUP,
    SCENE_5_MIKE_MOLLY,
    SCENE_5_MIKE_SAM,
    SCENE_5_ADV_MOLLY_1,
    SCENE_5_ADV_SAM,
    SCENE_5_ADV_MOLLY_2,
    SCENE_5_ADV_CHOICES,
    SCENE_5_ADV_CHOICE_KEYS,
    SCENE_5_ADV_FOLLOWUP,
)

# Character and basket positions — upper-left quartile of the 800×600 screen
_MOLLY_POS  = (125, 235)
_SAM_POS    = (240, 225)
_MAGGIE_POS = (610, 110)
_BASKET_POS = (400, 380)


def _draw_scene(screen: pygame.Surface, gs: dict) -> None:
    """Render the static picnic scene: background, basket, then characters."""
    spr = gs["sprites"]
    screen.blit(spr["picnic_bg"], (0, 0))
    screen.blit(spr["basket"],   _BASKET_POS)
    screen.blit(spr["molly"],    _MOLLY_POS)
    screen.blit(spr["sam"],      _SAM_POS)
    screen.blit(spr["maggie"],   _MAGGIE_POS)


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
    box_x   = 50
    box_w   = WIDTH - 100
    inner_w = box_w - 40
    line_h  = _S.FONT_SMALL.get_linesize()

    prompt_lines    = _wrap_text(prompt, _S.FONT_SMALL, inner_w)
    choices_y_start = 16 + len(prompt_lines) * line_h + 8
    box_h  = max(170, choices_y_start + len(choices) * 36 + 20)
    box_y  = HEIGHT - box_h - 10

    selected = 0
    choosing = True

    while choosing:
        surf = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        draw_3d_box(surf, 0, 0, box_w, box_h)

        for li, line in enumerate(prompt_lines):
            prompt_surf = _S.FONT_SMALL.render(line, True, (0, 0, 0))
            surf.blit(prompt_surf, (20, 16 + li * line_h))

        for i, choice in enumerate(choices):
            prefix    = "\u25BA " if i == selected else "  "
            text_surf = _S.FONT_SMALL.render(prefix + choice, True, (0, 0, 0))
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

    # ── Phase 0: settling-in line ─────────────────────────────────────────────
    if not gs.get("s5_intro_done"):
        _draw_scene(screen, gs)
        await text_box(screen, SCENE_5_SAM_SPOT)
        gs["s5_intro_done"] = True
        return

    # ── Phase 1: house flavor choice (not stored) + follow-up ────────────────
    if not gs.get("s5_house_done"):
        _draw_scene(screen, gs)
        await text_box(screen, SCENE_5_HOUSE_QUESTION)
        _draw_scene(screen, gs)
        await _choice_box(screen, "", SCENE_5_HOUSE_CHOICES)
        _draw_scene(screen, gs)
        await text_box(screen, SCENE_5_HOUSE_FOLLOWUP)
        gs["s5_house_done"] = True
        return

    # ── Phase 2: homeChoice (stored) + follow-up ─────────────────────────────
    if not gs.get("s5_home_choice_done"):
        _draw_scene(screen, gs)
        await text_box(screen, SCENE_5_HOME_QUESTION)
        _draw_scene(screen, gs)
        idx = await _choice_box(screen, "", SCENE_5_HOME_CHOICES)
        gs["homeChoice"] = SCENE_5_HOME_CHOICE_KEYS[idx]
        _draw_scene(screen, gs)
        await text_box(screen, SCENE_5_HOME_FOLLOWUP[gs["homeChoice"]])
        gs["s5_home_choice_done"] = True
        return

    # ── Phase 3: Mike dialogue ────────────────────────────────────────────────
    if not gs.get("s5_mike_done"):
        _draw_scene(screen, gs)
        await text_box(screen, SCENE_5_MIKE_MOLLY, SCENE_5_MIKE_SAM)
        gs["s5_mike_done"] = True
        return

    # ── Phase 4: adventure lead-in + adventureChoice (stored) + follow-up ────
    if not gs.get("s5_adventure_done"):
        _draw_scene(screen, gs)
        await text_box(screen, SCENE_5_ADV_MOLLY_1, SCENE_5_ADV_SAM, SCENE_5_ADV_MOLLY_2)
        _draw_scene(screen, gs)
        idx = await _choice_box(screen, "", SCENE_5_ADV_CHOICES)
        gs["adventureChoice"] = SCENE_5_ADV_CHOICE_KEYS[idx]
        _draw_scene(screen, gs)
        await text_box(screen, *SCENE_5_ADV_FOLLOWUP[gs["adventureChoice"]])
        gs["s5_adventure_done"] = True
        return

    # ── Transition to scene 6 ─────────────────────────────────────────────────
    gs["scene"] = 6
