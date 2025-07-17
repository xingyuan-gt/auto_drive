import pytest
from unittest.mock import patch
from app.cli import SimulationCLI


def test_single_car_simulation(capsys):
    """
    Simulates a single car being added and run through a command sequence.
    Asserts the correct state updates and final posture.
    """
    mock_inputs = [
        "10 10",  # field size
        "1",  # add car
        "A",  # car name
        "1 2 N",  # initial pos
        "FFRFFFFRRL",  # commands
        "2",  # run simulation
        "2"  # exit
    ]

    with patch("builtins.input", side_effect=mock_inputs):
        SimulationCLI().start()

    captured = capsys.readouterr()
    out = captured.out

    # Assert setup
    assert "Car A added." in out
    assert "Your current list of cars are:" in out
    assert "- A, (1,2) N, FFRFFFFRRL" in out

    # Assert simulation outcome
    assert "After simulation, the result is:" in out
    assert "- A, (5,4) S" in out

    # Exit message
    assert "Thank you for running the simulation. Goodbye!" in out


def test_two_car_collision(capsys):
    """
    Simulates two cars on a collision path and asserts that the collision is detected and reported.
    """
    mock_inputs = [
        "10 10",  # field size
        "1",  # add car A
        "A",
        "1 2 N",
        "FFRFFFFRRL",
        "1",  # add car B
        "B",
        "7 8 W",
        "FFLFFFFFFF",
        "2",  # run simulation
        "2"  # exit
    ]

    with patch("builtins.input", side_effect=mock_inputs):
        SimulationCLI().start()

    captured = capsys.readouterr()
    out = captured.out

    # Assert setup
    assert "Car A added." in out
    assert "Car B added." in out
    assert "- A, (1,2) N, FFRFFFFRRL" in out
    assert "- B, (7,8) W, FFLFFFFFFF" in out

    # Assert simulation outcome
    assert "After simulation, the result is:" in out
    assert "- A, collides with B" in out or "- A, collides with B," in out
    assert "- B, collides with A" in out or "- B, collides with A," in out
    assert "at step 7" in out

    # Exit message
    assert "Thank you for running the simulation. Goodbye!" in out


def test_cli_invalid_inputs(capsys):
    """
    Test how the CLI handles:
    - non-integer field size
    - invalid direction
    - invalid menu option
    """
    mock_inputs = [
        "ten ten",             # invalid field input
        "10 10",               # valid field
        "1", "A", "1 1 Z",     # invalid direction
        "1", "A", "1 1 N",     # valid
        "FF", "3", "2", "2"    # invalid option, then run and exit
    ]
    with patch("builtins.input", side_effect=mock_inputs):
        SimulationCLI().start()

    out = capsys.readouterr().out
    assert "Invalid format" in out
    assert "Invalid direction" in out
    assert "Invalid option" in out
    assert "- A, (1,1) N, FF" in out


def test_cli_invalid_car_inputs(capsys):
    """
    Tests rejection of:
    - out-of-bounds placement
    - duplicate car name
    - invalid commands
    """
    mock_inputs = [
        "5 5",
        "1", "A", "10 10 N",        # out-of-bounds
        "1", "A", "11 N",        # poor input structure
        "1", "A", "1 1 N", "XYZ",   # invalid commands
        "1", "A", "1 1 N", "F",     # valid
        "1", "A", "2 2 N", "FL",    # duplicate name
        "1", "B", "1 1 N", "F",     # position is occupied
        "1", "B", "3 3 N", "FLR",   # valid
        "2", "2"
    ]
    with patch("builtins.input", side_effect=mock_inputs):
        SimulationCLI().start()

    out = capsys.readouterr().out
    assert "outside the field bounds" in out
    assert "Commands must only contain F, L, R." in out
    assert "already exists" in out
    assert "- B, (3,3) N, FLR" in out


def test_cli_restart_after_simulation(capsys):
    """
    Simulates running a simulation, then starting over with a new field.
    """
    mock_inputs = [
        "10 10", "1", "A", "1 2 N", "F", "2", "1",
        "5 5", "1", "B", "0 0 E", "F", "2", "2"
    ]
    with patch("builtins.input", side_effect=mock_inputs):
        SimulationCLI().start()

    out = capsys.readouterr().out
    assert "Welcome to Auto Driving Car Simulation!" in out
    assert "- A, (1,2) N, F" in out
    assert "- B, (0,0) E, F" in out
    assert "Thank you for running the simulation. Goodbye!" in out
