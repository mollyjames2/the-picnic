import asyncio
import pygame
import sys

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


async def display_gif(screen, gif_path, duration=3000, center=None):
    if not HAS_PIL:
        screen.fill((0, 0, 0))
        pygame.display.flip()
        await asyncio.sleep(duration / 1000.0)
        return

    gif = Image.open(gif_path)
    frames = []
    frame_durations = []

    for frame in range(gif.n_frames):
        gif.seek(frame)
        frame_surface = pygame.image.fromstring(
            gif.tobytes(), gif.size, gif.mode
        ).convert_alpha()
        frames.append(frame_surface)
        frame_durations.append(gif.info.get("duration", 400))

    current_frame = 0
    start_time = pygame.time.get_ticks()

    if center is None:
        center = (screen.get_width() // 2, screen.get_height() // 2)

    while pygame.time.get_ticks() - start_time < duration:
        elapsed_time = pygame.time.get_ticks() - start_time
        total_duration = sum(frame_durations[: current_frame + 1])

        if elapsed_time > total_duration:
            current_frame = (current_frame + 1) % len(frames)

        screen.fill((0, 0, 0))
        gif_rect = frames[current_frame].get_rect(center=center)
        screen.blit(frames[current_frame], gif_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        await asyncio.sleep(frame_durations[current_frame] / 1000.0)
