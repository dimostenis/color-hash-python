import pytest

from colorhash import ColorHash


@pytest.fixture
def objs():
    return (
        "foo",
        "bar",
        None,
        {1, 2},
        [0, 1],
        ["a", "list"],
        {"a": 0},
        {"a": "dict"},
        ("a", "tuple"),
        {"a", "set"},
        ColorHash("w00t"),
    )


def test_colorhash_returns_some_color(objs):

    for obj in objs:
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


def test_colorhash_is_deterministic(objs):

    for obj in objs:
        assert ColorHash(obj).hex == ColorHash(obj).hex
        assert ColorHash(obj).hsl == ColorHash(obj).hsl
        assert ColorHash(obj).rgb == ColorHash(obj).rgb


@pytest.mark.parametrize(
    ["hsl", "rgb"],
    (
        ((0, 1.0, 0.5), (255, 0, 0)),  # red
        ((240, 1.0, 0.5), (0, 0, 255)),  # blue
        ((0, 0.0, 0.0), (0, 0, 0)),  # black
    ),
)
def test_hsl2rgb(hsl, rgb):
    from colorhash.colorhash import hsl2rgb

    assert hsl2rgb(hsl=hsl) == rgb


@pytest.mark.parametrize(
    ["rgb", "hex"],
    (
        ((255, 0, 0), "#ff0000"),  # red
        ((0, 0, 255), "#0000ff"),  # blue
        ((0, 0, 0), "#000000"),  # black
    ),
)
def test_rgb2hex(rgb, hex):
    from colorhash.colorhash import rgb2hex

    assert rgb2hex(rgb=rgb) == hex
