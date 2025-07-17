import pytest
from app.car import Car

def test_initial_position(car):
    assert car.posture() == (1, 2, "N")

def test_turn_left(car):
    car.execute("L")
    assert car.posture()[2] == "W"

def test_turn_right(car):
    car.execute("R")
    assert car.posture()[2] == "E"

def test_invalid_command_ignored(car):
    car.execute("X")  # unknown command
    assert car.posture() == (1, 2, "N")

def test_forward_move_within_bounds(car):
    car.execute("F")
    assert car.posture() == (1, 3, "N")

def test_forward_blocked_out_of_bounds(field):
    car = Car("X", 0, 0, "S", field)
    car.execute("F")
    assert car.posture() == (0, 0, "S")

