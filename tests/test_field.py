import pytest
from app.field import Field

@pytest.mark.parametrize("x,y,expected", [
    # why these test cases
    (0, 0, True),
    (9, 9, True),
    (10, 10, False),
    (-1, 5, False),
    (5, -1, False),
])
def test_is_within_bounds(x, y, expected):
    field = Field(10, 10)
    assert field.is_within_bounds(x, y) == expected

def test_zero_size_field():
    field = Field(0, 0)
    assert not field.is_within_bounds(0, 0)