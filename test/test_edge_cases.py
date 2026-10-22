from __future__ import annotations

import pytest

from colorhash import ColorHash


def test_hash_stability() -> None:
    """Ensure that different but string-identical objects yield same color."""
    obj1 = "test_string"
    obj2 = "".join(["test", "_", "string"])  # ruff: ignore[static-join-to-f-string]
    assert ColorHash(obj1).hex == ColorHash(obj2).hex


def test_complex_objects() -> None:
    """Test with objects that have different __str__ implementations."""

    class CustomObj:
        def __init__(self, val: int) -> None:
            self.val = val

        def __str__(self) -> str:
            return f"Custom({self.val})"

    assert ColorHash(CustomObj(1)).hex != ColorHash(CustomObj(2)).hex
    assert ColorHash(CustomObj(1)).hex == ColorHash(CustomObj(1)).hex


def test_edge_case_hue_boundaries() -> None:
    """Test min_h and max_h at absolute boundaries."""
    # Hue exactly at 0
    c1 = ColorHash("test", min_h=0, max_h=0)
    assert c1.hsl[0] == 0

    # Hue exactly at 360
    c2 = ColorHash("test", min_h=360, max_h=360)
    assert c2.hsl[0] == 360  # ruff: ignore[magic-value-comparison]


def test_very_long_input() -> None:
    """Ensure stability and no crash with very large strings."""
    large_input = "a" * 10**6
    assert isinstance(ColorHash(large_input).hex, str)


def test_non_string_primitive_types() -> None:
    """Test with ints, floats, booleans, and None."""
    types = [123, 45.67, True, False, None]
    for t in types:
        c = ColorHash(t)
        assert isinstance(c.hex, str)
        assert len(c.hex) == 7  # ruff: ignore[magic-value-comparison]


def test_argument_mutation_safety() -> None:
    """
    Ensure that modifying the input list doesn't affect ColorHash internal state.
    """
    lightness = [0.5]
    c = ColorHash("test", lightness=lightness)
    lightness.append(0.1)
    # The result should be based on the state at initialization
    assert pytest.approx(c.hsl[2]) == 0.5  # ruff: ignore[magic-value-comparison]


def test_float_precision_lightness_saturation() -> None:
    """Test with very small float differences."""
    c = ColorHash("test", lightness=[0.500000000000001])
    assert pytest.approx(c.hsl[2]) == 0.500000000000001  # ruff: ignore[magic-value-comparison]


@pytest.mark.parametrize("h_val", [0, 180, 360])
def test_hsl_to_rgb_boundaries(h_val: int) -> None:
    """Test HSL to RGB conversion at specific hue angles."""
    c = ColorHash("test", min_h=h_val, max_h=h_val, lightness=[0.5], saturation=[1.0])
    # For L=0.5, S=1.0:
    # 0 deg   -> (255, 0, 0)
    # 180 deg -> (0, 255, 255)
    # 360 deg -> (255, 0, 0)
    rgb = c.rgb
    if h_val in {0, 360}:
        assert rgb == (255, 0, 0)
    elif h_val == 180:  # ruff: ignore[magic-value-comparison]
        assert rgb == (0, 255, 255)
