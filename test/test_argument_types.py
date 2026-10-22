from __future__ import annotations

from typing import Any

import pytest

from colorhash import ColorHash
from colorhash.colorhash import ScalarOrSequence
from colorhash.colorhash import color_hash


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
def test_lightness_types(lightness: ScalarOrSequence) -> None:
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
def test_saturation_types(saturation: ScalarOrSequence) -> None:
    c = ColorHash("test", saturation=saturation)
    if isinstance(saturation, (int, float)):
        assert pytest.approx(c.hsl[1]) == float(saturation)
    else:
        assert c.hsl[1] in saturation


def test_invalid_types() -> None:
    # Test with something that is not numbers or sequence of numbers
    invalid_string: Any = "invalid"
    with pytest.raises(TypeError):
        ColorHash("test", lightness=invalid_string)

    invalid_none: Any = None
    with pytest.raises(TypeError):
        ColorHash("test", lightness=invalid_none)


@pytest.mark.parametrize(
    ("lightness", "saturation", "message"),
    [
        ([], [0.5], "lightness must not be empty"),
        ([0.5], [], "saturation must not be empty"),
    ],
)
def test_empty_sequences_raise_value_error(
    lightness: list[float],
    saturation: list[float],
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        ColorHash("test", lightness=lightness, saturation=saturation)


@pytest.mark.parametrize(
    ("lightness", "saturation", "message"),
    [
        ([], [0.5], "lightness must not be empty"),
        ([0.5], [], "saturation must not be empty"),
    ],
)
def test_empty_sequences_in_color_hash_raise_value_error(
    lightness: list[float],
    saturation: list[float],
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        color_hash("test", lightness=lightness, saturation=saturation)
