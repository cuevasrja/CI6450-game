from pygame import Vector2

class Static:
    """
    ### Description
    A class to represent a static object.

    ### Attributes
    - `position`: Vector2
        The position of the object.
    - `orientation`: float
    """
    def __init__(self, position: Vector2, orientation: float):
        self.position: Vector2 = position
        self.orientation: float = orientation
        self.x: int = position.x
        self.y: int = position.y
