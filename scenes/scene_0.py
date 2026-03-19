import asyncio
import pygame

from engine.settings import BLACK, WHITE, WIDTH, HEIGHT, FONT_LARGE, FONT_SMALL
from data.dialogue import INTRO_TITLE, INTRO_SUBTITLE


async def run(screen, game_state, keys, event):
    screen.fill(BLACK)

    title_text = FONT_LARGE.render(INTRO_TITLE, True, WHITE)
    subtitle_text = FONT_SMALL.render(INTRO_SUBTITLE, True, WHITE)
    prompt_text = FONT_SMALL.render("Press ENTER to start", True, WHITE)

    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(subtitle_text, (WIDTH // 2 - subtitle_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT // 2 + 50))

    if event and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        await asyncio.sleep(0.15)
        game_state["scene"] = 1
