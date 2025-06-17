from __future__ import annotations

import importlib.metadata
from typing import Any

import pytest

from colorhash import ColorHash
from colorhash import get_version
from colorhash.colorhash import MAX_HUE
from colorhash.colorhash import MIN_HUE
from colorhash.colorhash import hsl2rgb
from colorhash.colorhash import rgb2hex
from test.constants import NAMED_COLORS_HEX
from test.constants import NAMED_COLORS_HSL
from test.constants import NAMED_COLORS_RGB
from test.constants import OBJECTS

MAX_SATURATION = 1.0
MAX_LIGHTNESS = 1.0


@pytest.mark.parametrize(
    "params",
    [
        {"min_h": 0, "max_h": 360},
        {"min_h": 0, "max_h": 0},
        {"min_h": 10, "max_h": 10},
        {"min_h": 10, "max_h": 20},
        {"min_h": 300, "max_h": 360},
        {"min_h": 360, "max_h": 360},
    ],
)
def test_hue_params(params: dict[str, int]):
    hsl = ColorHash(None, **params).hsl
    min_h = params.get("min_h", MIN_HUE)
    max_h = params.get("max_h", MAX_HUE)
    assert min_h <= hsl[0] <= max_h


@pytest.mark.parametrize(
    "params",
    [
        {"lightness": (0.0,)},
        {"lightness": (0.1,)},
        {"lightness": (0.5,)},
        {"lightness": (0.9,)},
        {"lightness": (1.0,)},
        {"lightness": (0.3, 0.6)},
        {"lightness": [0.0]},
        {"lightness": [0.1]},
        {"lightness": [0.5]},
        {"lightness": [0.9]},
        {"lightness": [1.0]},
        {"lightness": [0.3, 0.6]},
    ],
)
def test_lightness_param(params: dict[str, tuple[float, ...]]):
    hsl = ColorHash(None, **params).hsl
    assert hsl[2] in params.get("lightness")


@pytest.mark.parametrize(
    "params",
    [
        {"saturation": (0.0,)},
        {"saturation": (0.1,)},
        {"saturation": (0.5,)},
        {"saturation": (0.9,)},
        {"saturation": (1.0,)},
        {"saturation": (0.3, 0.6)},
        {"saturation": [0.0]},
        {"saturation": [0.1]},
        {"saturation": [0.5]},
        {"saturation": [0.9]},
        {"saturation": [1.0]},
        {"saturation": [0.3, 0.6]},
    ],
)
def test_saturation_param(params: dict[str, tuple[float, ...]]):
    hsl = ColorHash(None, **params).hsl
    assert hsl[1] in params.get("saturation")


@pytest.mark.parametrize(
    ("err", "params"),
    [
        ("min_h and max_h must be in range", {"min_h": 10, "max_h": 0}),
        ("min_h and max_h must be in range", {"min_h": 360, "max_h": 0}),
        ("min_h and max_h must be in range", {"min_h": 10_000, "max_h": 0}),
        ("min_h and max_h must be in range", {"min_h": -1}),
        ("min_h and max_h must be in range", {"max_h": 361}),
        ("min_h and max_h must be in range", {"min_h": -10, "max_h": 400}),
        ("params must be in range", {"lightness": (-0.1,)}),  # using tuple
        ("params must be in range", {"lightness": (1.1,)}),  # using tuple
        ("params must be in range", {"saturation": (-0.1,)}),  # using tuple
        ("params must be in range", {"saturation": (1.1,)}),  # using tuple
        ("params must be in range", {"lightness": [-0.1]}),  # using list
        ("params must be in range", {"lightness": [1.1]}),  # using list
        ("params must be in range", {"saturation": [-0.1]}),  # using list
        ("params must be in range", {"saturation": [1.1]}),  # using list
    ],
)
def test_unsopported_params(err: str, params: dict[str, Any]):
    with pytest.raises(ValueError, match=err):
        ColorHash(None, **params)


@pytest.mark.parametrize("obj", OBJECTS)
def test_colorhash_returns_some_color(obj):
    min_rgb = 0
    max_rgb = 255

    hex: str = ColorHash(obj).hex
    assert isinstance(hex, str)

    hsl = ColorHash(obj).hsl
    assert isinstance(hsl, tuple)
    assert len(hsl) == 3  # noqa: PLR2004
    assert hsl[0] <= MAX_HUE
    assert hsl[1] <= MAX_SATURATION
    assert hsl[2] <= MAX_LIGHTNESS

    rgb = ColorHash(obj).rgb
    assert isinstance(rgb, tuple)
    assert len(rgb) == 3  # noqa: PLR2004
    assert all(min_rgb < x <= max_rgb for x in rgb)


@pytest.mark.parametrize("obj", OBJECTS)
def test_is_deterministic(obj):
    assert ColorHash(obj).hex == ColorHash(obj).hex
    assert ColorHash(obj).hsl == ColorHash(obj).hsl
    assert ColorHash(obj).rgb == ColorHash(obj).rgb


@pytest.mark.parametrize(
    ("hsl", "rgb"),
    tuple(zip(NAMED_COLORS_HSL, NAMED_COLORS_RGB)),
)
def test_hsl2rgb(hsl: tuple[float, float, float], rgb: tuple[int, int, int]):
    assert hsl2rgb(hsl=hsl) == rgb


@pytest.mark.parametrize(
    ("rgb", "hex"),
    tuple(zip(NAMED_COLORS_RGB, NAMED_COLORS_HEX)),
)
def test_rgb2hex(rgb: tuple[int, int, int], hex: str):
    assert rgb2hex(rgb=rgb) == hex


def test_get_version():
    assert get_version(None) == importlib.metadata.version("colorhash")
