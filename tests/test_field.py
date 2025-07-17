import pytest
from app.field import Field


@pytest.mark.parametrize("x,y,expected", [
    (0, 0, True),        # Lower bound: (0, 0) is the bottom-left corner
    (9, 9, True),        # Upper inclusive bound: (width - 1, height - 1)
    (10, 10, False),     # Outside: exactly equal to width and height (out of bounds)
    (-1, 5, False),      # Negative x: invalid coordinate
    (5, -1, False),      # Negative y: invalid coordinate
])
def test_is_within_bounds(x: int, y: int, expected: bool):
    """
    Tests whether the Field correctly reports positions as within bounds.
    """
    field = Field(10, 10)
    assert field.is_within_bounds(x, y) == expected


def test_field_with_zero_size_disallows_all_positions():
    """
    A field of size (0, 0) should not allow any positions.
    """
    field = Field(0, 0)
    assert not field.is_within_bounds(0, 0), "Zero-sized field should disallow all coordinates"
