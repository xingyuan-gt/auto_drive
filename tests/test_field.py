import pytest
from field import Field

def test_field_initialization():
    field = Field(10, 8)
    assert field.width == 10
    assert field.height == 8

@pytest.mark.parametrize("x, y, expected", [
    (0, 0, True),
    (9, 7, True),
    (10, 0, False),   # x at right edge
    (0, 8, False),    # y at top edge
    (-1, 5, False),   # x too low
    (5, -1, False),   # y too low
])
def test_field_bounds_check(x, y, expected):
    field = Field(10, 8)
    assert field.is_within_bounds(x, y) == expected
