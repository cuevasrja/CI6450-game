# Example file showing a circle moving on screen
import math
from typing import List
import pygame
from utils.trigonometry import atan2, normalize

# pygame setup
pygame.init()
screen: pygame.Surface = pygame.display.set_mode((1280, 720))
clock: pygame.time.Clock = pygame.time.Clock()
running: bool = True
dt: int = 0
hist_pos: List[float] = [0, 0]
orientation: float = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)



while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    pygame.draw.polygon(screen, "red", [(player_pos.x + math.cos(orientation) * 20, player_pos.y + math.sin(orientation) * 20), (player_pos.x + math.cos(orientation + 2.5) * 20, player_pos.y + math.sin(orientation + 2.5) * 20), (player_pos.x + math.cos(orientation - 2.5) * 20, player_pos.y + math.sin(orientation - 2.5) * 20)])

    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt
        hist_pos[0] += 300 *dt

    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
        hist_pos[1] -= 300 * dt

    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
        hist_pos[0] -= 300 * dt
        
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
        hist_pos[1] += 300 * dt

    orientation = atan2(hist_pos[0], hist_pos[1])

    if hist_pos[0] >= 10000 or hist_pos[1] >= 10000:
        hist_pos = normalize(hist_pos[0], hist_pos[1])

    if player_pos.y > screen.get_height():
        player_pos.y = 0
    elif player_pos.y < 0:
        player_pos.y = screen.get_height()
        
    if player_pos.x > screen.get_width():
        player_pos.x = 0
    elif player_pos.x < 0:
        player_pos.x = screen.get_width()

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()