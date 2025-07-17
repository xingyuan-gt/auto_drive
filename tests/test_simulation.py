import pytest
from app.car import Car


def test_add_and_list_single_car(simulation):
    """Simulation should allow adding and listing a single car."""
    simulation.add_car("A", 1, 2, "N", "FF")
    cars = simulation.list_cars()

    assert len(cars) == 1
    assert cars[0][0] == "A"
    assert cars[0][2] == "FF"

def test_duplicate_car_name(simulation):
    """Adding a car with an existing name should raise a ValueError."""
    simulation.add_car("A", 1, 1, "N", "FF")
    with pytest.raises(ValueError, match="Car with name 'A' already exists."):
        simulation.add_car("A", 2, 2, "E", "LR")


def test_add_car_outside_field(simulation):
    """Adding a car outside field bounds should raise a ValueError."""
    with pytest.raises(ValueError, match="outside the field bounds"):
        simulation.add_car("X", 11, 5, "N", "FF")


def test_run_all_no_collision(simulation, car):
    """Multiple cars should complete commands without colliding."""
    simulation.add_car("A", 1, 2, "N", "FF")
    simulation.add_car("B", 7, 8, "W", "FF")
    result = simulation.run_all()

    assert len(result) == 2
    for r in result:
        assert r["status"] == "completed"
        assert r["collision"] is None

    posture = [car.posture() for car in simulation.cars.values()]
    assert (1, 4, "N") in posture
    assert (5, 8, "W") in posture


def test_head_on_collision(simulation):
    """
    Cars facing each other and moving towards each other should collide.
    """
    simulation.add_car("A", 0, 0, "E", "F")
    simulation.add_car("B", 2, 0, "W", "F")
    result = simulation.run_all()

    a_result = next(r for r in result if r["name"] == "A")
    b_result = next(r for r in result if r["name"] == "B")

    assert a_result["status"] == "collided"
    assert b_result["status"] == "collided"

    assert set(a_result["collision"]["with"]) == {"B"}
    assert set(b_result["collision"]["with"]) == {"A"}

    assert simulation.cars["A"].frozen
    assert simulation.cars["B"].frozen


def test_run_all_with_collision(simulation):
    """Cars colliding at same step and position should report the same collision."""
    simulation.add_car("A", 1, 2, "N", "FFRFFFFRRL")
    simulation.add_car("B", 7, 8, "W", "FFLFFFFFFF")
    result = simulation.run_all()

    a_result = next(r for r in result if r["name"] == "A")
    b_result = next(r for r in result if r["name"] == "B")

    assert a_result["status"] == "collided"
    assert b_result["status"] == "collided"

    assert set(a_result["collision"]["with"]) == {"B"}
    assert set(b_result["collision"]["with"]) == {"A"}

    assert a_result["collision"]["step"] == b_result["collision"]["step"] == 7
    assert a_result["collision"]["at"] == b_result["collision"]["at"]


def test_start_same_position(simulation):
    """Two cars cannot start at the same coordinates."""
    simulation.add_car("A", 1, 1, "N", "F")
    with pytest.raises(ValueError):
        simulation.add_car("B", 1, 1, "E", "F")


def test_car_with_no_commands(simulation):
    """Car with no commands should not move."""
    simulation.add_car("A", 1, 1, "N", "")
    simulation.run_all()
    assert simulation.cars["A"].posture() == (1, 1, "N")


def test_uneven_commands(simulation):
    """Cars with unequal command lengths should run independently."""
    simulation.add_car("A", 0, 0, "N", "FF")  # Ends at (0,2)
    simulation.add_car("B", 1, 1, "N", "F")   # Ends at (1,2) after 1 step

    result = simulation.run_all()

    assert len(result) == 2
    assert all(r["status"] == "completed" for r in result)

    pos_A = simulation.cars["A"].posture()
    pos_B = simulation.cars["B"].posture()

    assert pos_A == (0, 2, "N")
    assert pos_B == (1, 2, "N")

    # Assert A didn't stop due to B's shorter command length
    assert pos_A[1] > pos_B[1] or pos_A[0] != pos_B[0]