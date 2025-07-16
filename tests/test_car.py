import pytest
from car import Car
from field import Field

@pytest.fixture
def field():
    return Field(5, 5)

def test_car_initial_position(field):
    car = Car("A", 1, 2, "N", field)
    assert car.position() == (1, 2, "N")

def test_car_rotates_left(field):
    car = Car("A", 1, 1, "N", field)
    car.execute("L")
    assert car.position() == (1, 1, "W")

def test_car_rotates_right(field):
    car = Car("A", 1, 1, "N", field)
    car.execute("R")
    assert car.position() == (1, 1, "E")

def test_car_moves_forward_within_bounds(field):
    car = Car("A", 1, 2, "N", field)
    car.execute("F")
    assert car.position() == (1, 3, "N")

def test_car_does_not_move_out_of_bounds(field):
    car = Car("A", 0, 0, "S", field)
    car.execute("F")
    assert car.position() == (0, 0, "S")