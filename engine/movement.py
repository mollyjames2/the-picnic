import asyncio
import pygame

def move_player(keys, pos, speed=5):
    if keys[pygame.K_UP]:
        pos.y -= speed
    if keys[pygame.K_DOWN]:
        pos.y += speed
    if keys[pygame.K_LEFT]:
        pos.x -= speed
    if keys[pygame.K_RIGHT]:
        pos.x += speed

def follow_leader(leader_pos, follower_pos, follow_distance=40, follow_speed=3):
    if abs(follower_pos.x - (leader_pos.x - follow_distance)) > 5:
        if follower_pos.x < leader_pos.x - follow_distance:
            follower_pos.x += follow_speed
        elif follower_pos.x > leader_pos.x - follow_distance:
            follower_pos.x -= follow_speed

    if abs(follower_pos.y - leader_pos.y) > 5:
        if follower_pos.y < leader_pos.y:
            follower_pos.y += follow_speed
        elif follower_pos.y > leader_pos.y:
            follower_pos.y -= follow_speed

async def apply_idle_sway_with_follow(
    leader_pos,
    follower_pos,
    sway_timer,
    sway_direction,
    sway_magnitude,
    sway_frequency,
    keys,
    follow_speed=2.5,
):
    sway_timer += 1
    if sway_timer > sway_frequency:
        sway_timer = 0
        sway_direction *= -1

    sway = sway_direction * sway_magnitude

    if keys[pygame.K_UP]:
        leader_pos.y += follow_speed
        leader_pos.x -= sway
    if keys[pygame.K_DOWN]:
        leader_pos.y -= follow_speed
        leader_pos.x += sway
    if keys[pygame.K_LEFT]:
        leader_pos.x += follow_speed
    if keys[pygame.K_RIGHT]:
        leader_pos.x -= follow_speed

    if not any(keys[key] for key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]):
        leader_pos.x += sway

    dx = leader_pos.x - follower_pos.x
    dy = leader_pos.y - follower_pos.y
    distance = (dx**2 + dy**2) ** 0.5
    if distance > 40:
        follower_pos.x += follow_speed * (dx / distance)
        follower_pos.y += follow_speed * (dy / distance)

    await asyncio.sleep(0)
    return leader_pos, follower_pos, sway_timer, sway_direction
