import pytest
from app.field import Field
from app.car import Car
from app.simulation import Simulation

@pytest.fixture
def field():
    return Field(10, 10)

@pytest.fixture
def car(field):
    return Car("A", 1, 2, "N", field)

@pytest.fixture
def simulation(field):
    return Simulation(field)
