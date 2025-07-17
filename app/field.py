
class Field:
    """
    Just a simple class to define the field. Could expand easily, like adding of wall, if need.
    """
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    def is_within_bounds(self, x: int, y: int) -> bool:
        """
        Mostly use by car to check if the move is valid
        """
        return 0 <= x < self.width and 0 <= y < self.height
