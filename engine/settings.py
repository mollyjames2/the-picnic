import os
import sys
import pygame

if getattr(sys, "frozen", False):
    BASE_PATH = sys._MEIPASS
else:
    BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

WIDTH, HEIGHT = 800, 600
FPS = 30

SPRITE_SCALER = 2
SPRITE_WIDTH, SPRITE_HEIGHT = int(50 * SPRITE_SCALER), int(70 * SPRITE_SCALER)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
OFF_WHITE = (245, 240, 230)
ORANGE = (255, 165, 0)
LIGHT_BROWN = (205, 170, 125)

FOLLOW_DISTANCE = 40
DELAY_FRAMES = 3
MOVEMENT_SPEED = 8

# Fonts are None until init_fonts() is called from async main()
FONT_LARGE = None
FONT_SMALL = None


def init_fonts() -> None:
    """Initialise fonts. Must be called after pygame.init() inside async main()."""
    global FONT_LARGE, FONT_SMALL
    try:
        font_path = os.path.join(BASE_PATH, "assets/fonts/Monospace.ttf")
        FONT_LARGE = pygame.font.Font(font_path, 50)
        FONT_SMALL = pygame.font.Font(font_path, 25)
    except FileNotFoundError:
        FONT_LARGE = pygame.font.SysFont("monospace", 50)
        FONT_SMALL = pygame.font.SysFont("monospace", 25)
