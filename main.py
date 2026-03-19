import asyncio
import os
import sys
import pygame

from engine.settings import WIDTH, HEIGHT, FPS, SPRITE_WIDTH, SPRITE_HEIGHT, init_fonts
from engine.assets import SpriteManager, load_gif_frames
from engine.transitions import display_gif
from data.game_config import WINDOW_CAPTION
from scenes import scene_0, scene_1, scene_2, scene_3, scene_4, scene_5, scene_6

# Item and furniture sizes for Scene 1
ITEM_SIZE   = (60, 60)
BASKET_SIZE = (90, 75)
TABLE_SIZE  = (170, 100)

_KITCHEN_BAND = 60  # px band at top and bottom of screen


async def main():
    pygame.init()
    init_fonts()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(WINDOW_CAPTION)
    clock = pygame.time.Clock()

    sprites = SpriteManager()
    sprites.load("sam",        "assets/sprites/sam.png",        (SPRITE_WIDTH, SPRITE_HEIGHT))
    sprites.load("maggie",     "assets/sprites/mag.png",        (SPRITE_WIDTH, SPRITE_HEIGHT))
    sprites.load("basket",     "assets/sprites/basket.png",     BASKET_SIZE)
    sprites.load("table",      "assets/sprites/table.png",      TABLE_SIZE)
    sprites.load("onigiri",   "assets/sprites/onigiri.png",     ITEM_SIZE)
    sprites.load("strawberry", "assets/sprites/strawberry.png", ITEM_SIZE)
    sprites.load("suncream",   "assets/sprites/suncream.png",   ITEM_SIZE)
    sprites.load("blanket",    "assets/sprites/blanket.png",    ITEM_SIZE)
    sprites.load("bone",       "assets/sprites/bone.png",       ITEM_SIZE)
    sprites.load("molly",      "assets/sprites/molly.png",      (SPRITE_WIDTH, SPRITE_HEIGHT))
    sprites.load("road",       "assets/sprites/road.png",       (WIDTH, HEIGHT))
    sprites.load_with_aspect_ratio("redcar", "assets/sprites/redcar.png", 80)
    sprites.load("car_bg",     "assets/pictures/car.png",        (640, 352))
    sprites.load("dest_beach", "assets/sprites/beach.png",       (WIDTH, HEIGHT))
    sprites.load("dest_woods", "assets/sprites/woods.png",       (WIDTH, HEIGHT))
    sprites.load("dest_view",  "assets/sprites/view.png",        (WIDTH, HEIGHT))
    sprites.load("spot_bg",    "assets/sprites/spot.png",         (WIDTH, HEIGHT))
    sprites.load("picnic_bg",  "assets/sprites/picnic.png",       (WIDTH, HEIGHT))
    sprites.load_with_aspect_ratio("ring", "assets/pictures/ring.png", 240)

    _kitchen_gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/GIFs/kitchen.gif")
    _kitchen_frames, _kitchen_durations = load_gif_frames(_kitchen_gif_path, size=(WIDTH, HEIGHT - 2 * _KITCHEN_BAND))

    game_state = {
        "scene": 0,
        "sprites": {
            "sam":        sprites.get("sam"),
            "maggie":     sprites.get("maggie"),
            "basket":     sprites.get("basket"),
            "table":      sprites.get("table"),
            "onigiri":   sprites.get("onigiri"),
            "strawberry": sprites.get("strawberry"),
            "suncream":   sprites.get("suncream"),
            "blanket":    sprites.get("blanket"),
            "bone":       sprites.get("bone"),
            "molly":      sprites.get("molly"),
            "road":       sprites.get("road"),
            "redcar":     sprites.get("redcar"),
            "car_bg":     sprites.get("car_bg"),
            "dest_beach": sprites.get("dest_beach"),
            "dest_woods": sprites.get("dest_woods"),
            "dest_view":  sprites.get("dest_view"),
            "spot_bg":    sprites.get("spot_bg"),
            "picnic_bg":  sprites.get("picnic_bg"),
            "ring":       sprites.get("ring"),
        },
        # Character starting positions
        "sam_pos":   pygame.Vector2(100, HEIGHT - SPRITE_HEIGHT),
        "maggie_pos": pygame.Vector2(530, HEIGHT - SPRITE_HEIGHT),
        # Scene 1 animated background
        "s1_bg_frames":    _kitchen_frames,
        "s1_bg_durations": _kitchen_durations,
        "s1_bg_frame_idx": 0,
        "s1_bg_last_tick": 0,
        "s1_bg_y_offset":  _KITCHEN_BAND,
        # Scene 1 state
        "s1_intro_done":     False,
        "s1_prompt_done":    False,
        "s1_maggie_touching": False,
        "s1_complete":       False,
        "s1_items": {
            "onigiri":    {"pos": pygame.Vector2(400,  280), "size": ITEM_SIZE, "following": False, "packed": False},
            "strawberry": {"pos": pygame.Vector2(520, 250), "size": ITEM_SIZE, "following": False, "packed": False},
            "suncream":   {"pos": pygame.Vector2(700, 80), "size": ITEM_SIZE, "following": False, "packed": False},
            "blanket":    {"pos": pygame.Vector2(35,  515), "size": ITEM_SIZE, "following": False, "packed": False},
            "bone":       {"pos": pygame.Vector2(160, 280), "size": ITEM_SIZE, "following": False, "packed": False},
        },
        "s1_basket_pos":  pygame.Vector2(345, 470),
        "s1_basket_size": BASKET_SIZE,
        "s1_table_pos":   pygame.Vector2(310, 500),
        "s1_table_size":  TABLE_SIZE,
        "display_gif": display_gif,
        # Scene 2 state
        "s2_intro_done":   False,
        "s2_choice_done":  False,
        "s2_walkoff_done": False,
        "s2_molly_pos":    pygame.Vector2(WIDTH + SPRITE_WIDTH, HEIGHT - SPRITE_HEIGHT),
        "s2_car_x":        -150.0,
        # Scene 3 state
        "s3_intro_done":   False,
        "s3_choice_done":  False,
        "s3_arrival_done": False,
        "s3_destination_shown": False,
        "livingHereChoice": None,   # "sea" | "town" | "house" — stored for proposal scene
        # Scene 5 state
        "s5_intro_done":       False,
        "s5_house_done":       False,
        "s5_home_choice_done": False,
        "s5_mike_done":        False,
        "s5_adventure_done":   False,
        "homeChoice":          None,  # "comfort" | "memories" | "people"
        "adventureChoice":     None,  # "destination" | "journey" | "together"
    }

    running = True

    while running:
        event = None

        for current_event in pygame.event.get():
            event = current_event
            if current_event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if game_state["scene"] == 0:
            await scene_0.run(screen, game_state, keys, event)
        elif game_state["scene"] == 1:
            await scene_1.run(screen, game_state, keys, event)
        elif game_state["scene"] == 2:
            await scene_2.run(screen, game_state, keys, event)
        elif game_state["scene"] == 3:
            await scene_3.run(screen, game_state, keys, event)
        elif game_state["scene"] == 4:
            await scene_4.run(screen, game_state, keys, event)
        elif game_state["scene"] == 5:
            await scene_5.run(screen, game_state, keys, event)
        elif game_state["scene"] == 6:
            await scene_6.run(screen, game_state, keys, event)

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)


asyncio.run(main())
