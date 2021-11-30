from pytest import fixture

from colorhash import ColorHash


@fixture
def objs():
    return (
        "foo",
        "bar",
        None,
        [0, 1],
        {1, 2},
        {"a": 0},
        ColorHash("w00t"),
    )


def test_colorhash_returns_some_color(objs):

    for obj in objs:
        assert isinstance(ColorHash(obj).hex, str)


def test_colorhash_is_deterministic(objs):

    for obj in objs:
        assert ColorHash(obj).hex == ColorHash(obj).hex
