import asyncio
import sys

import pygame

from engine.settings import WIDTH, HEIGHT, BLACK, WHITE, OFF_WHITE, FONT_LARGE, FONT_SMALL
from engine.dialogue import text_box, draw_3d_box
from data.dialogue import (
    SCENE_6_SAM_WHAT,
    SCENE_6_MOLLY_OPEN,
    SCENE_6_BEEN_THINKING,
    SCENE_6_LIVING_HERE_TEXT,
    SCENE_6_HOME_TEXT,
    SCENE_6_ADVENTURE_TEXT,
    SCENE_6_LIVING_FALLBACK,
    SCENE_6_HOME_FALLBACK,
    SCENE_6_ADVENTURE_FALLBACK,
    SCENE_6_CLOSING,
    SCENE_6_PROPOSAL,
    SCENE_6_PRESS_ENTER,
    SCENE_6_ENDING_LINE,
    SCENE_6_ENDING_TITLE,
)

# Same character/basket positions as scene 5
_MOLLY_POS  = (125, 235)
_SAM_POS    = (240, 225)
_MAGGIE_POS = (610, 110)
_BASKET_POS = (400, 380)
_BASKET_W, _BASKET_H = 90, 75


def _draw_scene(screen: pygame.Surface, gs: dict) -> None:
    """Render the static picnic scene: background, basket, characters."""
    spr = gs["sprites"]
    screen.blit(spr["picnic_bg"], (0, 0))
    screen.blit(spr["basket"],    _BASKET_POS)
    screen.blit(spr["molly"],     _MOLLY_POS)
    screen.blit(spr["sam"],       _SAM_POS)
    screen.blit(spr["maggie"],    _MAGGIE_POS)


def _draw_scene_with_glow(screen: pygame.Surface, gs: dict) -> None:
    """Render scene with a warm golden glow around the basket."""
    _draw_scene(screen, gs)
    cx = _BASKET_POS[0] + _BASKET_W // 2
    cy = _BASKET_POS[1] + _BASKET_H // 2
    glow_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for r in range(5, 0, -1):
        alpha = 25 + r * 18
        pygame.draw.ellipse(
            glow_surf,
            (255, 215, 60, alpha),
            (cx - _BASKET_W // 2 - r * 12,
             cy - _BASKET_H // 2 - r * 9,
             _BASKET_W + r * 24,
             _BASKET_H + r * 18),
        )
    screen.blit(glow_surf, (0, 0))


def _draw_scene_with_ring(screen: pygame.Surface, gs: dict) -> None:
    """Render ring centred on a black background with a white border."""
    screen.fill(BLACK)
    spr = gs["sprites"]
    ring = spr.get("ring")
    if ring:
        rw, rh = ring.get_width(), ring.get_height()
        rx = WIDTH  // 2 - rw // 2
        ry = HEIGHT // 2 - rh // 2
        border = 6
        pygame.draw.rect(screen, WHITE, (rx - border, ry - border,
                                         rw + border * 2, rh + border * 2))
        screen.blit(ring, (rx, ry))
    else:
        ph_w, ph_h = 240, 160
        ph_x = WIDTH  // 2 - ph_w // 2
        ph_y = HEIGHT // 2 - ph_h // 2
        pygame.draw.rect(screen, WHITE, (ph_x, ph_y, ph_w, ph_h), 6)
        label = FONT_SMALL.render("[ring.png]", True, WHITE)
        screen.blit(label, (ph_x + ph_w // 2 - label.get_width() // 2,
                             ph_y + ph_h // 2 - label.get_height() // 2))


def _build_speech_lines(gs: dict) -> tuple:
    """Build personalized proposal speech from the player's remembered choices."""
    living_text = SCENE_6_LIVING_HERE_TEXT.get(
        gs.get("livingHereChoice"), SCENE_6_LIVING_FALLBACK)
    home_text   = SCENE_6_HOME_TEXT.get(
        gs.get("homeChoice"), SCENE_6_HOME_FALLBACK)
    adv_text    = SCENE_6_ADVENTURE_TEXT.get(
        gs.get("adventureChoice"), SCENE_6_ADVENTURE_FALLBACK)
    return (
        SCENE_6_BEEN_THINKING,
        f"About how the best part of living here is {living_text}!",
        f"And how home is really about {home_text}!",
        f"And that it's {adv_text} that makes everything worth it!",
        *SCENE_6_CLOSING,
    )


async def _pump_events() -> None:
    """Drain the event queue for one frame without blocking."""
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    await asyncio.sleep(0)


async def _fade_to_black(screen: pygame.Surface) -> None:
    """Gradually overlay the current frame with black."""
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill(BLACK)
    for alpha in range(0, 256, 6):
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.flip()
        await _pump_events()


async def _wait_for_enter(screen: pygame.Surface) -> None:
    """Block until the player presses ENTER."""
    waiting = True
    while waiting:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN:
                waiting = False
        await asyncio.sleep(0)


async def run(screen: pygame.Surface, game_state: dict, keys, event) -> None:
    gs = game_state

    # ── Phase 0: basket glows — Sam notices something ────────────────────────
    if not gs.get("s6_intro_done"):
        _draw_scene_with_glow(screen, gs)
        await text_box(screen, SCENE_6_SAM_WHAT)
        gs["s6_intro_done"] = True
        return

    # ── Phase 1: Molly's opening beat ─────────────────────────────────────────
    if not gs.get("s6_opening_done"):
        _draw_scene(screen, gs)
        await text_box(screen, *SCENE_6_MOLLY_OPEN)
        gs["s6_opening_done"] = True
        return

    # ── Phase 2: personalized proposal speech ────────────────────────────────
    if not gs.get("s6_speech_done"):
        _draw_scene(screen, gs)
        await text_box(screen, *_build_speech_lines(gs))
        gs["s6_speech_done"] = True
        return

    # ── Phase 3: fade to black, then reveal ring ─────────────────────────────
    if not gs.get("s6_ring_shown"):
        _draw_scene(screen, gs)
        pygame.display.flip()
        await _fade_to_black(screen)
        _draw_scene_with_ring(screen, gs)
        pygame.display.flip()
        start = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start < 1000:
            await _pump_events()
        gs["s6_ring_shown"] = True
        return

    # ── Phase 4: proposal line (ring still visible behind dialogue box) ───────
    if not gs.get("s6_proposal_done"):
        _draw_scene_with_ring(screen, gs)
        await text_box(screen, SCENE_6_PROPOSAL)
        gs["s6_proposal_done"] = True
        return

    # ── Phase 5: press ENTER prompt ───────────────────────────────────────────
    if not gs.get("s6_continue_done"):
        _draw_scene_with_ring(screen, gs)
        prompt      = FONT_SMALL.render(SCENE_6_PRESS_ENTER, True, BLACK)
        box_w       = prompt.get_width() + 48
        box_h       = 46
        box_x       = WIDTH  // 2 - box_w // 2
        box_y       = HEIGHT - 68
        box_surf    = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        draw_3d_box(box_surf, 0, 0, box_w, box_h)
        box_surf.blit(prompt, (24, box_h // 2 - prompt.get_height() // 2))
        screen.blit(box_surf, (box_x, box_y))
        pygame.display.flip()
        await _wait_for_enter(screen)
        gs["s6_continue_done"] = True
        return

    # ── Phase 6: fade to black ────────────────────────────────────────────────
    if not gs.get("s6_faded"):
        _draw_scene_with_ring(screen, gs)
        await _fade_to_black(screen)
        gs["s6_faded"] = True
        return

    # ── Ending title card (stays here) ────────────────────────────────────────
    screen.fill(BLACK)
    line1 = FONT_SMALL.render(SCENE_6_ENDING_LINE,  True, WHITE)
    title = FONT_LARGE.render(SCENE_6_ENDING_TITLE, True, WHITE)
    screen.blit(line1, (WIDTH // 2 - line1.get_width() // 2, HEIGHT // 2 - 55))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 + 10))
