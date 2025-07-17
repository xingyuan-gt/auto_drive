import pytest
from unittest.mock import patch
from app.main import start_simulation

def test_single_car_simulation(capsys):
    # Mock user input sequence (simulate typing in the CLI)
    mock_inputs = [
        "10 10",            # field size
        "1",                # add car
        "A",                # car name
        "1 2 N",            # initial pos
        "FFRFFFFRRL",       # commands
        "2",                # run simulation
        "2"                 # exit
    ]

    with patch("builtins.input", side_effect=mock_inputs):
        start_simulation()

    captured = capsys.readouterr()
    out = captured.out

    # Assert expected output substrings are present
    assert "Car A added." in out
    assert "Your current list of cars are:" in out
    assert "- A, (1,2) N, FFRFFFFRRL" in out
    assert "After simulation, the result is:" in out
    assert "- A, (5,4) S" in out


def test_multiple_car_collision(capsys):
    mock_inputs = [
        "10 10",            # field size
        "1",                # add car A
        "A",
        "1 2 N",
        "FFRFFFFRRL",
        "1",                # add car B
        "B",
        "7 8 W",
        "FFLFFFFFFF",
        "2",                # run simulation
        "2"                 # exit
    ]

    with patch("builtins.input", side_effect=mock_inputs):
        start_simulation()

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