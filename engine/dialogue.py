import asyncio
import pygame
import sys

from engine.settings import WIDTH, HEIGHT, WHITE, BLACK, OFF_WHITE, FONT_SMALL


def draw_3d_box(surf: pygame.Surface, x: int, y: int, w: int, h: int, depth: int = 3) -> None:
    """Draw a raised 3D-effect off-white box with highlight/shadow edges."""
    pygame.draw.rect(surf, OFF_WHITE, (x, y, w, h))
    for i in range(depth):
        hi = max(255 - i * 30, 180)
        sh = min(80 + i * 30, 160)
        pygame.draw.line(surf, (hi, hi, hi), (x+i, y+i), (x+w-1-i, y+i))            # top
        pygame.draw.line(surf, (hi, hi, hi), (x+i, y+i+1), (x+i, y+h-1-i))          # left
        pygame.draw.line(surf, (sh, sh, sh), (x+i, y+h-1-i), (x+w-1-i, y+h-1-i))   # bottom
        pygame.draw.line(surf, (sh, sh, sh), (x+w-1-i, y+i), (x+w-1-i, y+h-1-i))   # right


def _wrap_pixel(text: str, font: pygame.font.Font, max_width: int) -> list:
    """Wrap text by pixel width rather than character count."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = (current + " " + word).strip()
        if font.size(test)[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


async def text_box(screen, *lines, font=FONT_SMALL):
    line_height = 40
    box_x, box_y = 50, HEIGHT - 150
    box_width, box_height = WIDTH - 100, 100
    # Max text width: from x=20 in the box up to the arrow at x=(box_width-40)
    max_text_width = box_width - 70

    dialog_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)

    processed_boxes = []
    for line in lines:
        wrapped = _wrap_pixel(line, font, max_text_width)
        for i in range(0, len(wrapped), 2):
            processed_boxes.append(wrapped[i:i + 2])

    current_box_index = 0
    box_active = True

    while box_active:
        dialog_surface.fill((0, 0, 0, 0))
        draw_3d_box(dialog_surface, 0, 0, box_width, box_height)

        if current_box_index < len(processed_boxes):
            current_box = processed_boxes[current_box_index]
            for i, line in enumerate(current_box):
                text_surface = font.render(line, True, BLACK)
                dialog_surface.blit(text_surface, (20, 20 + i * line_height))

        down_arrow = font.render("\u25BC", True, BLACK)
        dialog_surface.blit(down_arrow, (box_width - 40, box_height - 35))

        screen.blit(dialog_surface, (box_x, box_y))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if current_box_index + 1 < len(processed_boxes):
                        current_box_index += 1
                    else:
                        box_active = False
                elif event.key == pygame.K_UP and current_box_index > 0:
                    current_box_index -= 1

        await asyncio.sleep(0)
