from typing import List
import pygame
from utils.physics import Kinematic


def show_menu() -> int:
    print("\033[1;93mBienvenido al simulador de algoritmos de movimiento\033[0m")
    print("\033[1;92mSeleccione una opción: \033[0m")
    print("1. Kinematic Arrive")
    print("2. Kinematic Flee")
    print("3. Kinematic Wandering")
    print("4. Dynamic Seek")
    print("5. Dynamic Flee")
    print("6. Dynamic Arrive")
    print("7. Align")
    print("8. Velocity Match")
    print("9. Face")
    print("10. Look Where You're Going")
    print("11. Dynamic Wander")
    print("12. Path Following")

    return int(input("\033[1;92mSeleccione una opción: \033[0m"))

def check_border(screen: pygame.Surface, player: Kinematic, border: int = 0) -> None:
    if player.position.y > screen.get_height() - border:
        player.position.y = screen.get_height() - border
    elif player.position.y < border:
        player.position.y = border

    if player.position.x > screen.get_width() - border:
        player.position.x = screen.get_width() - border
    elif player.position.x < border:
        player.position.x = border

def key_checker(keys: pygame.key.ScancodeWrapper, player: Kinematic, hist_pos: pygame.Vector2, const_velocity: float, dt: float) -> None:
    if keys[pygame.K_d]:
        player.add_position(x=const_velocity * dt)
        hist_pos.x += const_velocity * dt
        player.set_velocity(x=const_velocity)

    if keys[pygame.K_w]:
        player.add_position(y=-const_velocity * dt)
        hist_pos.y -= const_velocity * dt
        player.set_velocity(y=-const_velocity)

    if keys[pygame.K_a]:
        player.add_position(x=-const_velocity * dt)
        hist_pos.x -= const_velocity * dt
        player.set_velocity(x=-const_velocity)
        
    if keys[pygame.K_s]:
        player.add_position(y=const_velocity * dt)
        hist_pos.y += const_velocity * dt
        player.set_velocity(y=const_velocity)

    if not(keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s]):
        player.set_velocity(x=0, y=0)

def create_square_path(screen: pygame.Surface, n_points: int = 4, border: float = 0.9) -> List[pygame.Vector2]:
    width: int = screen.get_width()
    height: int = screen.get_height()
    padding_width: int = width * (1 - border) / 2
    padding_height: int = height * (1 - border) / 2

    return [
        pygame.Vector2(padding_width, padding_height), 
        pygame.Vector2(width - padding_width, padding_height), 
        pygame.Vector2(width - padding_width, height - padding_height), 
        pygame.Vector2(padding_width, height - padding_height)
        ]