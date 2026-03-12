from __future__ import annotations

import pytest

from colorhash import ColorHash


@pytest.mark.parametrize(
    "lightness",
    [
        0.5,  # float
        0,  # int
        1,  # int
        (0.2, 0.8),  # tuple
        [0.3, 0.7],  # list
        range(1),  # other sequence (though values must be 0-1)
    ],
)
def test_lightness_types(lightness):
    c = ColorHash("test", lightness=lightness)
    if isinstance(lightness, (int, float)):
        assert pytest.approx(c.hsl[2]) == float(lightness)
    else:
        assert c.hsl[2] in lightness


@pytest.mark.parametrize(
    "saturation",
    [
        0.5,  # float
        0,  # int
        1,  # int
        (0.2, 0.8),  # tuple
        [0.3, 0.7],  # list
    ],
)
def test_saturation_types(saturation):
    c = ColorHash("test", saturation=saturation)
    if isinstance(saturation, (int, float)):
        assert pytest.approx(c.hsl[1]) == float(saturation)
    else:
        assert c.hsl[1] in saturation


def test_invalid_types():
    # Test with something that is not numbers or sequence of numbers
    with pytest.raises(TypeError):
        ColorHash("test", lightness="invalid")

    with pytest.raises(TypeError):
        ColorHash("test", lightness=None)


def test_empty_sequence():
    # If passed empty sequence, it should fail when trying to index or get len
    with pytest.raises(ZeroDivisionError):
        ColorHash("test", lightness=[])
