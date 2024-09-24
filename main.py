# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
orientation = 'left'

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # pygame.draw.circle(screen, "red", player_pos, 40)
    # pygame.draw.rect(screen, "red", pygame.Rect(player_pos.x, player_pos.y, 40, 40))
    # pygame.draw.polygon(screen, "red", [(player_pos.x, player_pos.y), (player_pos.x + 40, player_pos.y + 20), (player_pos.x + 40, player_pos.y - 20)])
    if orientation == 'up':
        pygame.draw.polygon(screen, "red", [(player_pos.x, player_pos.y), (player_pos.x + 20, player_pos.y + 40), (player_pos.x - 20, player_pos.y + 40)])
    elif orientation == 'down':
        pygame.draw.polygon(screen, "red", [(player_pos.x, player_pos.y), (player_pos.x + 20, player_pos.y - 40), (player_pos.x - 20, player_pos.y - 40)])
    elif orientation == 'left':
        pygame.draw.polygon(screen, "red", [(player_pos.x, player_pos.y), (player_pos.x + 40, player_pos.y + 20), (player_pos.x + 40, player_pos.y - 20)])
    else:
        pygame.draw.polygon(screen, "red", [(player_pos.x, player_pos.y), (player_pos.x - 40, player_pos.y + 20), (player_pos.x - 40, player_pos.y - 20)])

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
        orientation = 'up'
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
        orientation = 'down'
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
        orientation = 'left'
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt
        orientation = 'right'

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