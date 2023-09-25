from test.constants import NAMED_COLORS_HEX
from test.constants import NAMED_COLORS_HSL
from test.constants import NAMED_COLORS_RGB
from test.constants import OBJECTS

import pytest

from colorhash import ColorHash


@pytest.mark.parametrize("obj", OBJECTS)
def test_colorhash_returns_some_color(obj):
    hex = ColorHash(obj).hex
    assert isinstance(hex, str)

    hsl = ColorHash(obj).hsl
    assert isinstance(hsl, tuple)
    assert len(hsl) == 3
    assert hsl[0] <= 360
    assert hsl[1] <= 100
    assert hsl[2] <= 100

    rgb = ColorHash(obj).rgb
    assert isinstance(rgb, tuple)
    assert len(rgb) == 3
    assert all([0 < x <= 255 for x in rgb])


@pytest.mark.parametrize("obj", OBJECTS)
def test_colorhash_is_deterministic(obj):
    assert ColorHash(obj).hex == ColorHash(obj).hex
    assert ColorHash(obj).hsl == ColorHash(obj).hsl
    assert ColorHash(obj).rgb == ColorHash(obj).rgb


@pytest.mark.parametrize(
    ["hsl", "rgb"],
    tuple(zip(NAMED_COLORS_HSL, NAMED_COLORS_RGB)),
)
def test_hsl2rgb(hsl, rgb):
    from colorhash.colorhash import hsl2rgb

    assert hsl2rgb(hsl=hsl) == rgb


@pytest.mark.parametrize(
    ["rgb", "hex"],
    tuple(zip(NAMED_COLORS_RGB, NAMED_COLORS_HEX)),
)
def test_rgb2hex(rgb, hex):
    from colorhash.colorhash import rgb2hex

    assert rgb2hex(rgb=rgb) == hex
