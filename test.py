import asyncio
import sys
import pygame

from engine.settings import WIDTH, HEIGHT, FPS, SPRITE_WIDTH, SPRITE_HEIGHT
from engine.assets import SpriteManager
from engine.transitions import display_gif
from data.game_config import WINDOW_CAPTION
from scenes import scene_0, scene_1, scene_2, scene_3, scene_4, scene_5, scene_6

SCENES = {
    0: scene_0,
    1: scene_1,
    2: scene_2,
    3: scene_3,
    4: scene_4,
    5: scene_5,
    6: scene_6,
}

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(f"{WINDOW_CAPTION} [TEST]")
clock = pygame.time.Clock()

ITEM_SIZE   = (45, 45)
BASKET_SIZE = (70, 55)
TABLE_SIZE  = (140, 90)

sprites = SpriteManager()
sprites.load("sam",        "assets/sprites/sam.png",        (SPRITE_WIDTH, SPRITE_HEIGHT))
sprites.load("maggie",     "assets/sprites/mag.png",        (SPRITE_WIDTH, SPRITE_HEIGHT))
sprites.load("molly",      "assets/sprites/molly.png",      (SPRITE_WIDTH, SPRITE_HEIGHT))
sprites.load("road",       "assets/sprites/road.png",       (WIDTH, HEIGHT))
sprites.load_with_aspect_ratio("redcar", "assets/sprites/redcar.png", 80)
sprites.load("basket",     "assets/sprites/basket.png",     BASKET_SIZE)
sprites.load("table",      "assets/sprites/table.png",      TABLE_SIZE)
sprites.load("sandwich",   "assets/sprites/sandwich.png",   ITEM_SIZE)
sprites.load("strawberry", "assets/sprites/strawberry.png", ITEM_SIZE)
sprites.load("suncream",   "assets/sprites/suncream.png",   ITEM_SIZE)
sprites.load("blanket",    "assets/sprites/blanket.png",    ITEM_SIZE)
sprites.load("bone",       "assets/sprites/bone.png",       ITEM_SIZE)
sprites.load("car_bg",     "assets/pictures/car.png",       (700, 440))
sprites.load("spot_bg",    "assets/sprites/spot.png",       (WIDTH, HEIGHT))
sprites.load("picnic_bg",  "assets/sprites/picnic.png",     (WIDTH, HEIGHT))
sprites.load_with_aspect_ratio("ring", "assets/pictures/ring.png", 240)

game_state = {
    "scene": 0,
    "sprites": {
        "sam":        sprites.get("sam"),
        "maggie":     sprites.get("maggie"),
        "molly":      sprites.get("molly"),
        "road":       sprites.get("road"),
        "redcar":     sprites.get("redcar"),
        "basket":     sprites.get("basket"),
        "table":      sprites.get("table"),
        "sandwich":   sprites.get("sandwich"),
        "strawberry": sprites.get("strawberry"),
        "suncream":   sprites.get("suncream"),
        "blanket":    sprites.get("blanket"),
        "bone":       sprites.get("bone"),
        "car_bg":     sprites.get("car_bg"),
        "spot_bg":    sprites.get("spot_bg"),
        "picnic_bg":  sprites.get("picnic_bg"),
        "ring":       sprites.get("ring"),
    },
    "sam_pos":    pygame.Vector2(100, 290),
    "maggie_pos": pygame.Vector2(530, 380),
    "s1_intro_done":      False,
    "s1_prompt_done":     False,
    "s1_maggie_touching": False,
    "s1_complete":        False,
    "s1_items": {
        "sandwich":   {"pos": pygame.Vector2(70,  205), "size": ITEM_SIZE, "following": False, "packed": False},
        "strawberry": {"pos": pygame.Vector2(650, 205), "size": ITEM_SIZE, "following": False, "packed": False},
        "suncream":   {"pos": pygame.Vector2(700, 380), "size": ITEM_SIZE, "following": False, "packed": False},
        "blanket":    {"pos": pygame.Vector2(50,  420), "size": ITEM_SIZE, "following": False, "packed": False},
        "bone":       {"pos": pygame.Vector2(360, 490), "size": ITEM_SIZE, "following": False, "packed": False},
    },
    "s1_basket_pos":  pygame.Vector2(348, 292),
    "s1_basket_size": BASKET_SIZE,
    "s1_table_pos":   pygame.Vector2(310, 340),
    "s1_table_size":  TABLE_SIZE,
    "display_gif": display_gif,
    # Scene 5 state
    "s5_intro_done":       False,
    "s5_house_done":       False,
    "s5_home_choice_done": False,
    "s5_mike_done":        False,
    "s5_adventure_done":   False,
    "livingHereChoice":    None,
    "homeChoice":          None,
    "adventureChoice":     None,
    # Scene 2 state
    "s2_intro_done":   False,
    "s2_choice_done":  False,
    "s2_walkoff_done": False,
    "s2_molly_pos":    pygame.Vector2(WIDTH + SPRITE_WIDTH, 350),
    "s2_car_x":        -150.0,
}


async def main(start_scene: int):
    game_state["scene"] = start_scene
    running = True

    while running:
        event = None

        for current_event in pygame.event.get():
            event = current_event
            if current_event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        scene_module = SCENES.get(game_state["scene"])
        if scene_module:
            await scene_module.run(screen, game_state, keys, event)
        else:
            print(f"No scene registered for index {game_state['scene']}")
            pygame.quit()
            sys.exit()

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python test.py <scene_number>")
        print(f"Available scenes: {sorted(SCENES.keys())}")
        sys.exit(1)

    try:
        scene_num = int(sys.argv[1])
    except ValueError:
        print(f"Error: scene_number must be an integer, got '{sys.argv[1]}'")
        sys.exit(1)

    if scene_num not in SCENES:
        print(f"Error: scene {scene_num} not found. Available: {sorted(SCENES.keys())}")
        sys.exit(1)

    asyncio.run(main(scene_num))
