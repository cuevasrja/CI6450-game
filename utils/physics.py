import math
import random
from typing import List, Tuple
from pygame import Vector2, Surface
from utils.trigonometry import atan2, magnitude, normalize

class Static:
    """
    ### Description
    A class to represent a static object.

    ### Attributes
    - position: Vector2 - The position of the object.
    - orientation: float - The orientation of the object.

    ### Methods
    - set_position(x: int, y: int) -> None: Sets the position of the object.
    - set_orientation(angle: float) -> None: Sets the orientation of the object.
    - get_position() -> Vector2: Returns the position of the object.
    - get_orientation() -> float: Returns the orientation of the object.
    - copy() -> Static: Returns a copy of the object.

    ### Example
    ```python
    from pygame import Vector2

    static = Static(Vector2(0, 0), 0)
    static.set_position(10, 10)
    static.set_orientation(1.57)
    print(static.get_position()) # Output: Vector2(10, 10)
    print(static.get_orientation()) # Output: 1.57
    print(static.copy()) # Output: Static(Vector2(10, 10), 1.57)
    ```
    """

    def __init__(self, position: Vector2 = Vector2(0, 0), orientation: float = 0):
        self.position: Vector2 = position
        self.orientation: float = orientation

    def set_position(self, x: int, y: int) -> None:
        self.position = (x, y)

    def set_orientation(self, angle: float):
        self.orientation = angle

    def get_position(self) -> Vector2:
        return self.position
    
    def get_orientation(self) -> float:
        return self.orientation
    
    def copy(self) -> 'Static':
        return Static(self.position, self.orientation)

class SteeringOutput:
    """
    ### Description
    A class to represent the steering output of a character.

    ### Attributes
    - linear: Vector2 - The linear steering output.
    - angular: float - The angular steering output. 

    ### Methods
    - __init__(linear: Vector2 = Vector2(0, 0), angular: float = 0): Constructor for the SteeringOutput class.

    ### Example
    ```python
    from pygame import Vector2

    steering_output = SteeringOutput(Vector2(0, 0), 0)
    ```
    """
    def __init__(self, linear: Vector2 = Vector2(0, 0), angular: float = 0):
        self.linear: Vector2 = linear
        self.angular: float = angular

class KinematicSteeringOutput:
    """
    ### Description
    A class to represent the steering output of a character.

    ### Attributes
    - linear: Vector2 - The linear steering output.
    - rotation: float - The rotation steering output.

    ### Methods
    - __init__(linear: Vector2 = Vector2(0, 0), rotation: float = 0): Constructor for the KinematicSteeringOutput class.

    ### Example
    ```python
    from pygame import Vector2

    steering_output = KinematicSteeringOutput(Vector2(0, 0), 0)
    ```
    """
    def __init__(self, velocity: Vector2 = Vector2(0, 0), rotation: float = 0):
        self.velocity: Vector2 = velocity
        self.rotation: float = rotation

class Kinematic:
    """
    ### Description
    A class to represent the kinematic properties of a character.

    ### Attributes
    - position: Vector2 - The position of the character.
    - orientation: float - The orientation of the character.
    - velocity: Vector2 - The velocity of the character.
    - angular_velocity: float - The angular velocity of the character.

    ### Methods
    - set_position(x: int, y: int) -> None: Sets the position of the character.
    - set_orientation(angle: float) -> None: Sets the orientation of the character.
    - set_velocity(x: int|None = None, y: int|None = None) -> None: Sets the velocity of the character.
    - set_angular_velocity(angular_velocity: float) -> None: Sets the angular velocity of the character.
    - get_position() -> Vector2: Returns the position of the character.
    - get_orientation() -> float: Returns the orientation of the character.
    - get_velocity() -> Vector2: Returns the velocity of the character.
    - get_angular_velocity() -> float: Returns the angular velocity of the character.
    - update(steering: SteeringOutput, dt: float) -> None: Updates the character's position and orientation based on the steering output.
    - update_with_max_speed(steering: KinematicSteeringOutput, dt: float, max_speed: float) -> None: Updates the character's position and orientation based on the steering output with a maximum speed.
    - add_position(x: int = 0, y: int = 0) -> None: Adds a value to the character's position.
    - copy() -> Kinematic: Returns a copy of the character.

    ### Example
    ```python
    from pygame import Vector2

    kinematic = Kinematic(Vector2(0, 0), 0, Vector2(0, 0), 0)
    kinematic.set_position(10, 10)
    kinematic.set_orientation(1.57)
    kinematic.set_velocity(5, 5)
    kinematic.set_angular_velocity(0.5)
    print(kinematic.get_position()) # Output: Vector2(10, 10)
    print(kinematic.get_orientation()) # Output: 1.57
    print(kinematic.get_velocity()) # Output: Vector2(5, 5)
    print(kinematic.get_angular_velocity()) # Output: 0.5
    print(kinematic.copy()) # Output: Kinematic(Vector2(10, 10), 1.57, Vector2(5, 5), 0.5)
    ```
    """
    def __init__(self, position: Vector2 = Vector2(0, 0), orientation: float = 0, velocity: Vector2 = Vector2(0, 0), angular_velocity: float = 0):
        self.position: Vector2 = position
        self.orientation: float = orientation
        self.velocity: Vector2 = velocity
        self.angular_velocity: float = angular_velocity

    def set_position(self, x: int, y: int):
        self.position.x = x
        self.position.y = y

    def set_orientation(self, angle: float):
        self.orientation = angle

    def set_velocity(self, x: int|None = None, y: int|None = None):
        if x is not None:
            self.velocity.x = x
        if y is not None:
            self.velocity.y = y

    def set_angular_velocity(self, angular_velocity: float):
        self.angular_velocity = angular_velocity

    def get_position(self) -> Vector2:
        return self.position
    
    def get_orientation(self) -> float:
        return self.orientation

    def get_velocity(self) -> Vector2:
        return self.velocity
    
    def get_angular_velocity(self) -> float:
        return self.angular_velocity

    def update(self, steering: SteeringOutput, dt: float):
        """
        ### Description
        Updates the character's position and orientation based on the steering output.

        ### Parameters
        - steering: SteeringOutput - The steering output.
        - dt: float - The time step.

        ### Returns
        - None
        """
        self.position += self.velocity * dt
        self.orientation += self.angular_velocity * dt

        self.velocity += steering.linear * dt
        self.angular_velocity += steering.angular * dt

    def update_with_max_speed(self, steering: KinematicSteeringOutput, dt: float, max_speed: float):
        """
        ### Description
        Updates the character's position and orientation based on the steering output with a maximum speed.

        ### Parameters
        - steering: KinematicSteeringOutput - The steering output.
        - dt: float - The time step.
        - max_speed: float - The maximum speed.

        ### Returns
        - None
        """
        self.position += self.velocity * dt
        self.orientation += self.angular_velocity * dt

        if magnitude(self.velocity) > max_speed:
            self.velocity = normalize(self.velocity) * max_speed

        self.angular_velocity += steering.rotation * dt

    def add_position(self, x: int = 0, y: int = 0):
        """
        ### Description
        Adds a value to the character's position.

        ### Parameters
        - x: int - The x value. (optional)
        - y: int - The y value. (optional)

        ### Returns
        - None
        """
        self.position.x += x
        self.position.y += y

    def copy(self) -> 'Kinematic':
        return Kinematic(self.position, self.orientation, self.velocity, self.angular_velocity)

def random_npc(screen: Surface) -> Kinematic:
    """
    ### Description
    Generates a random NPC.

    ### Parameters
    - screen: Surface - The screen.

    ### Returns
    - Kinematic: The random NPC.
    """
    random_x: int = random.randint(0, screen.get_width())
    random_y: int = random.randint(0, screen.get_height())
    random_orientation: float = random.uniform(0, 2 * math.pi)
    return Kinematic(Vector2(random_x, random_y), random_orientation)

def list_of_random_npcs(screen: Surface, n: int) -> List[Kinematic]:
    """
    ### Description
    Generates a list of random NPCs.

    ### Parameters
    - screen: Surface - The screen.
    - n: int - The number of NPCs.

    ### Returns
    - List[Kinematic]: The list of random NPCs.
    """
    return [random_npc(screen) for _ in range(n)]

def center_npc(screen: Surface) -> Kinematic:
    """
    ### Description
    Generates a NPC in the center of the screen.

    ### Parameters
    - screen: Surface - The screen.

    ### Returns
    - Kinematic: The NPC in the center of the screen.
    """
    pos_x: int = screen.get_width()//2 + random.randint(-50, 50)
    pos_y: int = screen.get_height()//2 + random.randint(-50, 50)
    random_orientation: float = random.uniform(0, 2 * math.pi)
    return Kinematic(Vector2(pos_x, pos_y), random_orientation)

def list_of_center_npcs(screen: Surface, n: int) -> List[Kinematic]:
    """
    ### Description
    Generates a list of NPCs in the center of the screen.

    ### Parameters
    - screen: Surface - The screen.
    - n: int - The number of NPCs.

    ### Returns
    - List[Kinematic]: The list of NPCs in the center of the screen.
    """
    return [center_npc(screen) for _ in range(n)]