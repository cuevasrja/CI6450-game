from pygame import Vector2

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