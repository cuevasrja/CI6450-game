from typing import List
import pygame
from utils.physics import Kinematic


def show_menu() -> int:
    """
    ### Description
    Shows the menu of the game.

    ### Returns
    - int : The selected option.
    """
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
    print("10. Pursue and Evade")
    print("11. Look Where You're Going")
    print("12. Dynamic Wander")
    print("13. Path Following")
    print("14. Separation")

    return int(input("\033[1;92mSeleccione una opción: \033[0m"))

def check_border(screen: pygame.Surface, player: Kinematic, border: int = 0) -> None:
    """
    ### Description
    Checks if the player is out of the screen.

    ### Parameters
    - screen: pygame.Surface : The screen to check.
    - player: Kinematic : The player to check.
    - border: int : The border to consider.

    ### Returns
    - None
    """
    if player.position.y > screen.get_height() - border:
        player.position.y = screen.get_height() - border
    elif player.position.y < border:
        player.position.y = border

    if player.position.x > screen.get_width() - border:
        player.position.x = screen.get_width() - border
    elif player.position.x < border:
        player.position.x = border

def key_checker(keys: pygame.key.ScancodeWrapper, player: Kinematic, hist_pos: pygame.Vector2, const_velocity: float, dt: float) -> None:
    """
    ### Description
    Checks the keys pressed by the user.

    ### Parameters
    - keys: pygame.key.ScancodeWrapper : The keys pressed by the user.
    - player: Kinematic : The player to move.
    - hist_pos: pygame.Vector2 : The position of the player.
    - const_velocity: float : The velocity of the player.
    - dt: float : The time elapsed.

    ### Returns
    - None
    """

    # If the user presses the key, the player moves
    
    # Key D. Right
    if keys[pygame.K_d]:
        player.add_position(x=const_velocity * dt)
        hist_pos.x += const_velocity * dt
        player.set_velocity(x=const_velocity)

    # Key W. Up
    if keys[pygame.K_w]:
        player.add_position(y=-const_velocity * dt)
        hist_pos.y -= const_velocity * dt
        player.set_velocity(y=-const_velocity)

    # Key A. Left
    if keys[pygame.K_a]:
        player.add_position(x=-const_velocity * dt)
        hist_pos.x -= const_velocity * dt
        player.set_velocity(x=-const_velocity)
    
    # Key S. Down
    if keys[pygame.K_s]:
        player.add_position(y=const_velocity * dt)
        hist_pos.y += const_velocity * dt
        player.set_velocity(y=const_velocity)

    # If the user releases the key or does not press another key, the player stops
    if not(keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s]):
        player.set_velocity(x=0, y=0)

def create_square_path(screen: pygame.Surface, n_points: int = 4, border: float = 0.9) -> List[pygame.Vector2]:
    """
    ### Description
    Creates a square path.

    ### Parameters
    - screen: pygame.Surface : The screen to create the path.
    - n_points: int : The number of points in the path. (Default is 4)
    - border: float : The border to consider. (Default is 0.9)

    ### Returns
    - List[pygame.Vector2] : The square path.
    """
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