import math

import pygame

import engine.settings as _S
from engine.settings import (
    WIDTH, HEIGHT, WHITE, BLACK, LIGHT_BROWN,
    SPRITE_WIDTH, SPRITE_HEIGHT, MOVEMENT_SPEED,
)
from engine.dialogue import text_box, draw_3d_box
from engine.movement import move_player
from data.dialogue import (
    SCENE_1_INTRO,
    SCENE_1_ITEMS,
    SCENE_1_MAGGIE_DIALOGUE,
    SCENE_1_COMPLETE,
)

# Interaction distances
_PICKUP_RADIUS  = 45    # px — how close Sam must be to grab an item
_BASKET_RADIUS  = 55    # px — how close Sam must be to pack the basket
_GLOW_DURATION  = 1800  # ms — total item-glow cue duration after prompt


# ── Drawing helpers ───────────────────────────────────────────────────────────

def _draw_room(screen: pygame.Surface, gs: dict) -> None:
    """Animated kitchen GIF background, falling back to black if no frames loaded."""
    frames    = gs.get("s1_bg_frames", [])
    durations = gs.get("s1_bg_durations", [])
    screen.fill(LIGHT_BROWN)
    if not frames:
        return

    now = pygame.time.get_ticks()
    idx = gs["s1_bg_frame_idx"]
    if now - gs["s1_bg_last_tick"] >= durations[idx]:
        gs["s1_bg_frame_idx"] = (idx + 1) % len(frames)
        gs["s1_bg_last_tick"] = now
        idx = gs["s1_bg_frame_idx"]

    y_off = gs.get("s1_bg_y_offset", 0)
    screen.blit(frames[idx], (0, y_off))


def _draw_scene(screen: pygame.Surface, gs: dict) -> None:
    """Draw furniture, basket, and any items still on the floor."""
    spr = gs["sprites"]
    screen.blit(spr["table"],  (gs["s1_table_pos"].x,  gs["s1_table_pos"].y))
    screen.blit(spr["basket"], (gs["s1_basket_pos"].x, gs["s1_basket_pos"].y))
    for name, data in gs["s1_items"].items():
        if not data["packed"] and not data["following"]:
            screen.blit(spr[name], (data["pos"].x, data["pos"].y))


def _draw_characters(screen: pygame.Surface, gs: dict) -> None:
    spr = gs["sprites"]
    screen.blit(spr["maggie"], (gs["maggie_pos"].x, gs["maggie_pos"].y))
    screen.blit(spr["sam"],    (gs["sam_pos"].x,    gs["sam_pos"].y))


def _draw_carried_items(screen: pygame.Surface, gs: dict) -> None:
    """Draw items Sam is carrying — on top of characters so they're visible."""
    spr = gs["sprites"]
    for name, data in gs["s1_items"].items():
        if data["following"] and not data["packed"]:
            screen.blit(spr[name], (data["pos"].x, data["pos"].y))


def _draw_item_glows(screen: pygame.Surface, gs: dict, alpha: int) -> None:
    """Draw a pulsing golden halo behind each uncollected item."""
    glow_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for data in gs["s1_items"].values():
        if data["packed"] or data["following"]:
            continue
        iw, ih = data["size"]
        cx = int(data["pos"].x + iw // 2)
        cy = int(data["pos"].y + ih // 2)
        r = max(iw, ih) // 2 + 14
        pygame.draw.circle(glow_surf, (255, 220,  50, alpha),      (cx, cy), r)
        pygame.draw.circle(glow_surf, (255, 255, 150, alpha // 2), (cx, cy), r - 6)
    screen.blit(glow_surf, (0, 0))


def _draw_prompt_box(screen: pygame.Surface) -> None:
    """Centred 'PACK THE PICNIC BASKET / press ENTER to start' box."""
    bw, bh = 520, 110
    bx = (WIDTH - bw) // 2
    by = (HEIGHT - bh) // 2
    surf = pygame.Surface((bw, bh), pygame.SRCALPHA)
    draw_3d_box(surf, 0, 0, bw, bh)
    title  = _S.FONT_SMALL.render("PACK THE PICNIC BASKET", True, BLACK)
    prompt = _S.FONT_SMALL.render("press ENTER to start",   True, BLACK)
    surf.blit(title,  ((bw - title.get_width())  // 2, 18))
    surf.blit(prompt, ((bw - prompt.get_width()) // 2, 64))
    screen.blit(surf, (bx, by))



def _full_redraw(screen: pygame.Surface, gs: dict) -> None:
    """Draw the complete scene so text_box overlays on a fresh frame."""
    _draw_room(screen, gs)
    _draw_scene(screen, gs)
    _draw_characters(screen, gs)
    _draw_carried_items(screen, gs)


# ── Main scene function ───────────────────────────────────────────────────────

async def run(screen: pygame.Surface, game_state: dict, keys, event) -> None:
    sam_pos    = game_state["sam_pos"]
    maggie_pos = game_state["maggie_pos"]

    # ── Phase 1: Opening line ─────────────────────────────────────────────────
    if not game_state.get("s1_intro_done"):
        _full_redraw(screen, game_state)
        await text_box(screen, SCENE_1_INTRO)
        game_state["s1_intro_done"] = True
        return

    # ── Phase 2: Instruction prompt (ENTER to begin) ──────────────────────────
    if not game_state.get("s1_prompt_done"):
        _full_redraw(screen, game_state)
        _draw_prompt_box(screen)
        if event and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            game_state["s1_prompt_done"] = True
        return

    # ── Phase 2.5: Item glow cue ──────────────────────────────────────────────
    if not game_state.get("s1_glow_done"):
        now = pygame.time.get_ticks()
        if "s1_glow_start" not in game_state:
            game_state["s1_glow_start"] = now
        elapsed = now - game_state["s1_glow_start"]
        if elapsed >= _GLOW_DURATION:
            game_state["s1_glow_done"] = True
        else:
            t     = elapsed / _GLOW_DURATION
            alpha = int(180 * math.sin(math.pi * t))
            _draw_room(screen, game_state)
            _draw_item_glows(screen, game_state, alpha)
            _draw_scene(screen, game_state)
            _draw_characters(screen, game_state)
            return

    # ── Phase 3: Gameplay ─────────────────────────────────────────────────────
    if not game_state.get("s1_complete"):

        # Move Sam; clamp to screen bounds
        move_player(keys, sam_pos, speed=MOVEMENT_SPEED)
        sam_pos.x = max(0, min(WIDTH  - SPRITE_WIDTH,  sam_pos.x))
        sam_pos.y = max(0, min(HEIGHT - SPRITE_HEIGHT, sam_pos.y))

        sam_rect   = pygame.Rect(sam_pos.x, sam_pos.y, SPRITE_WIDTH, SPRITE_HEIGHT)
        sam_center = pygame.Vector2(sam_pos.x + SPRITE_WIDTH  // 2,
                                    sam_pos.y + SPRITE_HEIGHT // 2)

        # Maggie collision — one dialogue line per new overlap
        maggie_rect = pygame.Rect(maggie_pos.x, maggie_pos.y, SPRITE_WIDTH, SPRITE_HEIGHT)
        if sam_rect.colliderect(maggie_rect):
            if not game_state["s1_maggie_touching"]:
                game_state["s1_maggie_touching"] = True
                _full_redraw(screen, game_state)
                await text_box(screen, SCENE_1_MAGGIE_DIALOGUE)
        else:
            game_state["s1_maggie_touching"] = False

        # Item pickup — one item per frame, closest in range
        items = game_state["s1_items"]
        for name, data in items.items():
            if data["packed"] or data["following"]:
                continue
            iw, ih = data["size"]
            item_center = pygame.Vector2(data["pos"].x + iw // 2,
                                         data["pos"].y + ih // 2)
            if sam_center.distance_to(item_center) < _PICKUP_RADIUS:
                data["following"] = True
                _full_redraw(screen, game_state)
                await text_box(screen, SCENE_1_ITEMS[name])
                break  # one pickup per frame

        # Carried items float above Sam's head, staggered if multiple
        following = [n for n, d in items.items() if d["following"] and not d["packed"]]
        for i, name in enumerate(following):
            data = items[name]
            iw, ih = data["size"]
            # Centre the row of carried items above Sam
            total_w = len(following) * iw + (len(following) - 1) * 4
            start_x = sam_pos.x + SPRITE_WIDTH // 2 - total_w // 2
            target_x = start_x + i * (iw + 4)
            target_y = sam_pos.y - ih - 6
            data["pos"].x += (target_x - data["pos"].x) * 0.3
            data["pos"].y += (target_y - data["pos"].y) * 0.3

        # Packing — Sam reaches the basket while carrying items
        bw, bh = game_state["s1_basket_size"]
        basket_center = pygame.Vector2(game_state["s1_basket_pos"].x + bw // 2,
                                       game_state["s1_basket_pos"].y + bh // 2)
        if following and sam_center.distance_to(basket_center) < _BASKET_RADIUS:
            for name in following:
                items[name]["following"] = False
                items[name]["packed"]    = True

        # Completion — all items packed
        if all(d["packed"] for d in items.values()):
            _full_redraw(screen, game_state)
            await text_box(screen, SCENE_1_COMPLETE)
            game_state["s1_complete"] = True
            game_state["scene"] = 2
            return

    # ── Draw every frame ──────────────────────────────────────────────────────
    _draw_room(screen, game_state)
    _draw_scene(screen, game_state)
    _draw_characters(screen, game_state)
    _draw_carried_items(screen, game_state)
