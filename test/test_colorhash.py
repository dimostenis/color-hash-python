from __future__ import annotations

from typing import Any

import pytest

from colorhash import ColorHash
from colorhash.colorhash import HUE_BUCKET_COUNT
from colorhash.colorhash import MAX_HUE
from colorhash.colorhash import MAX_HUE_BUCKET_INDEX
from colorhash.colorhash import crc32_hash
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
def test_hue_params(params: dict[str, int]) -> None:
    hsl = ColorHash(None, **params).hsl
    min_h = params["min_h"]
    max_h = params["max_h"]
    assert min_h <= hsl[0] <= max_h


def test_default_hue_uses_hash_bucket_directly() -> None:
    bucket = crc32_hash("hey") % HUE_BUCKET_COUNT

    assert ColorHash("hey").hsl[0] == bucket


@pytest.mark.parametrize(
    ("params", "min_h", "max_h"),
    [
        ({"min_h": 150}, 150, 360),
        ({"max_h": 150}, 0, 150),
        ({"min_h": 20, "max_h": 80}, 20, 80),
    ],
)
def test_hue_bounds_map_across_the_inclusive_interval(
    params: dict[str, int],
    min_h: int,
    max_h: int,
) -> None:
    bucket = crc32_hash("hey") % HUE_BUCKET_COUNT
    expected_hue = min_h + bucket / MAX_HUE_BUCKET_INDEX * (max_h - min_h)

    assert ColorHash("hey", **params).hsl[0] == pytest.approx(expected_hue)


@pytest.mark.parametrize(
    ("obj", "expected_bucket"),
    [
        ("hue-bucket-631", 0),
        ("hue-bucket-60", MAX_HUE_BUCKET_INDEX),
    ],
)
def test_hue_range_can_reach_both_endpoints(obj: str, expected_bucket: int) -> None:
    bucket = crc32_hash(obj) % HUE_BUCKET_COUNT
    min_h = 20
    max_h = 80
    expected_hue = min_h + bucket / MAX_HUE_BUCKET_INDEX * (max_h - min_h)

    assert bucket == expected_bucket
    assert ColorHash(obj, min_h=min_h, max_h=max_h).hsl[0] == pytest.approx(
        expected_hue,
    )


def test_full_circle_endpoints_have_the_same_rgb_color() -> None:
    lower_endpoint = ColorHash(
        "hue-bucket-631",
        lightness=[0.5],
        saturation=[1.0],
        min_h=0,
        max_h=360,
    )
    upper_endpoint = ColorHash(
        "hue-bucket-60",
        lightness=[0.5],
        saturation=[1.0],
        min_h=0,
        max_h=360,
    )

    assert lower_endpoint.hsl[0] == 0
    assert upper_endpoint.hsl[0] == 360  # ruff: ignore[magic-value-comparison]
    assert lower_endpoint.rgb == upper_endpoint.rgb == (255, 0, 0)


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
def test_lightness_param(params: dict[str, Any]) -> None:
    hsl = ColorHash(None, **params).hsl
    assert hsl[2] in params["lightness"]


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
def test_saturation_param(params: dict[str, Any]) -> None:
    hsl = ColorHash(None, **params).hsl
    assert hsl[1] in params["saturation"]


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
def test_unsopported_params(err: str, params: dict[str, Any]) -> None:
    with pytest.raises(ValueError, match=err):
        ColorHash(None, **params)


@pytest.mark.parametrize("obj", OBJECTS)
def test_colorhash_returns_some_color(obj: Any) -> None:
    min_rgb = 0
    max_rgb = 255

    hex: str = ColorHash(obj).hex
    assert isinstance(hex, str)

    hsl = ColorHash(obj).hsl
    assert isinstance(hsl, tuple)
    assert len(hsl) == 3  # ruff: ignore[magic-value-comparison]
    assert hsl[0] <= MAX_HUE
    assert hsl[1] <= MAX_SATURATION
    assert hsl[2] <= MAX_LIGHTNESS

    rgb = ColorHash(obj).rgb
    assert isinstance(rgb, tuple)
    assert len(rgb) == 3  # ruff: ignore[magic-value-comparison]
    assert all(min_rgb < x <= max_rgb for x in rgb)


@pytest.mark.parametrize("obj", OBJECTS)
def test_is_deterministic(obj: Any) -> None:
    assert ColorHash(obj).hex == ColorHash(obj).hex
    assert ColorHash(obj).hsl == ColorHash(obj).hsl
    assert ColorHash(obj).rgb == ColorHash(obj).rgb


@pytest.mark.parametrize(
    ("hsl", "rgb"),
    tuple(zip(NAMED_COLORS_HSL, NAMED_COLORS_RGB)),
)
def test_hsl2rgb(
    hsl: tuple[float, float, float],
    rgb: tuple[int, int, int],
) -> None:
    assert hsl2rgb(hsl=hsl) == rgb


@pytest.mark.parametrize(
    ("rgb", "hex"),
    tuple(zip(NAMED_COLORS_RGB, NAMED_COLORS_HEX)),
)
def test_rgb2hex(rgb: tuple[int, int, int], hex: str) -> None:
    assert rgb2hex(rgb=rgb) == hex
