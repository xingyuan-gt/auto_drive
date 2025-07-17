from typing import Tuple

from app.field import Field
from app.constants import DIRECTIONS, MOVES


class Car:
    """
    Car Class that define the individual car
    """

    def __init__(self, name: str, x: int, y: int, direction: str, field: Field) -> None:
        """
        Initiation with mandatory
        - (x, y) starting position
        - facing direction
        - field it is supposed to be in
                """
        self.name: str = name
        self.x: int = x
        self.y: int = y
        self.direction: str = direction
        self.field: Field = field

        self.commands: str = ""
        self.command_index: int = 0
        self.frozen: bool = False

    def set_commands(self, cmd_string: str) -> None:
        """
        Set the command, reset command index after new command issued
        """
        self.commands = cmd_string
        self.command_index = 0

    def has_remaining_commands(self) -> bool:
        """
        Function to determine if the car need to be stopped
        """
        return self.command_index < len(self.commands)

    def execute_next(self) -> None:
        """
        function to iterate the execution of command
        """
        if not self.has_remaining_commands():
            return
        command = self.commands[self.command_index]
        self.execute(command)
        self.command_index += 1

    def execute(self, command: str) -> None:
        """
        The core logic to move the car

        Having a significant responsibility by Car class to check if the movement is valid seems grey
        """
        if command == 'L':
            idx = (DIRECTIONS.index(self.direction) - 1) % 4
            self.direction = DIRECTIONS[idx]
        elif command == 'R':
            idx = (DIRECTIONS.index(self.direction) + 1) % 4
            self.direction = DIRECTIONS[idx]
        elif command == 'F':
            dx, dy = MOVES[self.direction]
            new_x = self.x + dx
            new_y = self.y + dy
            if self.field.is_within_bounds(new_x, new_y):
                self.x, self.y = new_x, new_y

    def position(self) -> Tuple[int, int]:
        """
        Mainly used for collision checking
        return the position (x, y) only
        """
        return self.x, self.y

    def posture(self) -> Tuple[int, int, str]:
        """
        An older function mainly use for testing

        return position in addition to the attitude of the car
        """
        return self.x, self.y, self.direction
