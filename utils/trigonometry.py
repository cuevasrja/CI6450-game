import math
from typing import Tuple

def atan2(x: float, y: float) -> float:
    """
    ### Description
    Get the angle in radians from the x-axis to the point (x, y).

    ### Parameters
    - x: float - The x-coordinate of the point.
    - y: float - The y-coordinate of the point.

    ### Returns
    - float - The angle in radians from the x-axis to the point (x, y).
    """
    if x == 0:
        if y > 0:
            return math.pi / 2
        elif y < 0:
            return -math.pi / 2
        else:
            return 0
    else:
        angle = math.atan(y / x)
        return angle if x > 0 else angle + math.pi

def new_orientation(orientation: float, velocity: Tuple[int, int]) -> float:
    if velocity[0] == 0 and velocity[1] == 0:
        return orientation
    else:
        return atan2(velocity[1], velocity[0])