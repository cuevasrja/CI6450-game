from pygame import Vector2


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
    - get_x() -> int: Returns the x value of the character's position.
    - get_y() -> int: Returns the y value of the character's position.
    - get_orientation() -> float: Returns the orientation of the character.
    - get_velocity() -> Vector2: Returns the velocity of the character.
    - get_angular_velocity() -> float: Returns the angular velocity of the character.
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
    
    def get_x(self) -> int:
        return self.position.x
    
    def get_y(self) -> int:
        return self.position.y
    
    def get_orientation(self) -> float:
        return self.orientation

    def get_velocity(self) -> Vector2:
        return self.velocity
    
    def get_angular_velocity(self) -> float:
        return self.angular_velocity

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