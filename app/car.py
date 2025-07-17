from typing import Tuple

from app.field import Field

DIRECTIONS = ['N', 'E', 'S', 'W']
MOVES = {'N': (0, 1), 'E': (1, 0), 'S': (0, -1), 'W': (-1, 0)}

class Car:
    def __init__(self, name: str, x: int, y: int, direction: str, field: Field) -> None:
        self.name: str = name
        self.x: int = x
        self.y: int = y
        self.direction: str = direction
        self.field: Field = field
        self.commands: str = ""
        self.command_index: int = 0
        self.frozen: bool = False

    def set_commands(self, cmd_string: str) -> None:
        self.commands = cmd_string
        self.command_index = 0

    def has_remaining_commands(self) -> bool:
        return self.command_index < len(self.commands)

    def execute_next(self) -> None:
        if not self.has_remaining_commands():
            return
        command = self.commands[self.command_index]
        self.execute(command)
        self.command_index += 1

    def execute(self, command: str) -> None:
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
        return self.x, self.y

    def posture(self) -> Tuple[int, int, str]:
        return self.x, self.y, self.direction