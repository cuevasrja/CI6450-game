from typing import List
from pygame import Vector2
from utils.physics import Kinematic, Static, SteeringOutput
from utils.seek import Seek
from utils.trigonometry import magnitude

class Path:
    """
    ### Description
    A class to represent a path.

    ### Attributes
    - `points` : List[Vector2] : The points that make up the path.
    - `cur` : int : The current point in the path.
    - `offset` : float : The offset to consider the point as reached.

    ### Methods
    - `get_param(position: Vector2, current_param: int) -> int` : Returns the next point in the path.
    - `get_position(param: int) -> Vector2` : Returns the position of the point in the path.
    - `set_param(param: int)` : Sets the current point in the path.
    """
    def __init__(self, points: List[Vector2] = Vector2(0,0), cur: int = 0, offset: float = 0):
        self.points: List[Vector2] = points
        self.cur: int = cur
        self.offset: float = offset

    def get_param(self, position: Vector2, current_param: int) -> int:
        direction: Vector2 = self.points[current_param] - position
        return current_param + 1 if magnitude(direction) < self.offset else current_param

    def get_position(self, param: int) -> Vector2:
        return self.points[param]
    
    def set_param(self, param: int):
        if param < len(self.points):
            self.cur = param
        else:
            self.cur = 0

class FollowPath(Seek):
    """
    ### Description
    A class to represent a path following behavior.

    ### Attributes
    - `character` : Kinematic : The character to move.
    - `target` : Static : The target to follow.
    - `max_speed` : float : The maximum speed of the character.
    - `path` : Path : The path to follow.
    - `path_ofset` : float : The offset to consider the point as reached.
    - `current_param` : int : The current point in the path. (default 0)

    ### Methods
    - `get_steering() -> SteeringOutput` : Returns the steering to follow the path.
    """
    def __init__(self, character: Kinematic, target: Static, max_speed: float, path: List[Vector2], path_ofset: float, current_param: int = 0):
        super().__init__(character, target, max_speed)
        self.path: Path = Path(path, current_param, path_ofset)


    def get_steering(self) -> SteeringOutput:
        # The target is set to the current point in the path.
        target_param: float = self.path.get_param(self.character.position, self.path.cur)
        # The current point in the path is updated.
        self.path.set_param(target_param)

        # The target position is set to the position of the current point in the path.
        target_position: Vector2 = self.path.get_position(self.path.cur)

        # The target is set to the target position.
        self.target = self.target.copy()
        self.target.position = Vector2(target_position.x, target_position.y)

        # The steering is calculated.
        return super().get_steering()