import pytest
from app.car import Car


def test_initial_position(car):
    """Car should be at (1, 2) facing North initially."""
    assert car.posture() == (1, 2, "N"), "Initial posture incorrect"


@pytest.mark.parametrize("start_dir, command, expected_dir", [
    ("N", "L", "W"),
    ("N", "R", "E"),
    ("E", "L", "N"),
    ("S", "R", "W"),
])
def test_car_turning(start_dir, command, expected_dir, field):
    """Car should turn correctly based on command."""
    car = Car("A", 1, 2, start_dir, field)
    car.execute(command)
    assert car.posture()[2] == expected_dir, f"Expected {expected_dir} but got {car.posture()[2]}"


def test_invalid_command_ignored(car):
    """Invalid command should not change the car's state."""
    car.execute("X")  # unknown command
    assert car.posture() == (1, 2, "N"), "Invalid command changed posture"


def test_forward_move_within_bounds(car):
    """Car should move one step north when facing North and not at boundary."""
    car.execute("F")
    assert car.posture() == (1, 3, "N"), "Car did not move correctly"


def test_forward_blocked_out_of_bounds(field):
    """Car should not move forward out of the field boundary."""
    car = Car("X", 0, 0, "S", field)
    car.execute("F")
    assert car.posture() == (0, 0, "S"), "Car moved out of bounds"


def test_set_command_updates_car_commands(car):
    """
    set_command() should correctly update the car's command queue.
    """
    car.set_commands("RRRR")
    car.execute_next()
    car.set_commands("LRFF")
    assert car.commands == "LRFF", "Expected command list to be updated to ['L', 'R', 'F', 'F']"
    assert car.command_index == 0, "Index not reset"
