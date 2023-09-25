# Copyright (c) 2016 Felix Krull <f_krull@gmx.de>
# Released under the terms of the MIT license; see README.md.

"""
Generate a color based on an object's hash value.

Quick start:

>>> from colorhash import ColorHash
>>> c = ColorHash('Hello World')
>>> c.hsl
(131, 0.65, 0.5)
>>> c.rgb
(45, 210, 75)
>>> c.hex
'#2dd24b'
"""
from binascii import crc32
from typing import Any
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

MIN_HUE = 0
MAX_HUE = 360

IntOrFloat = Union[int, float]


def crc32_hash(obj: Any) -> int:
    """
    Generate a hash for ``obj``.

    This function first converts the object to a string and encodes it into
    UTF-8, then calculates and returns the CRC-32 checksum of the result. The
    hash is guaranteed to be as stable as the result of the object's ``__str__``
    method.
    """
    bs = str(obj).encode("utf-8")
    return crc32(bs) & 0xFFFFFFFF


def hue_to_rgb(p, q, t):
    if t < 0:
        t += 1
    elif t > 1:
        t -= 1

    if t < 1 / 6:
        return p + (q - p) * 6 * t
    if t < 1 / 2:
        return q
    if t < 2 / 3:
        return p + (q - p) * (2 / 3 - t) * 6
    return p


def hsl2rgb(hsl: Tuple[float, float, float]) -> Tuple[int, int, int]:
    h, s, l = hsl  # noqa: E741
    h /= 360
    q = l * (1 + s) if l < 0.5 else l + s - l * s
    p = 2 * l - q

    r = round(hue_to_rgb(p, q, h + 1 / 3) * 255)
    g = round(hue_to_rgb(p, q, h) * 255)
    b = round(hue_to_rgb(p, q, h - 1 / 3) * 255)

    return r, g, b


def rgb2hex(rgb: Tuple[int, int, int]) -> str:
    """
    Format an RGB color value into a hexadecimal color string.

    >>> rgb2hex((255, 0, 0))
    '#ff0000'
    """
    try:
        return "#%02x%02x%02x" % rgb
    except TypeError:
        raise ValueError(rgb)


def color_hash(
    obj: Any,
    lightness: Sequence[float] = (0.35, 0.5, 0.65),
    saturation: Sequence[float] = (0.35, 0.5, 0.65),
    min_h: Optional[int] = None,
    max_h: Optional[int] = None,
) -> Tuple[float, float, float]:
    """
    Calculate the color for the given object.

    This function takes the same arguments as the ``ColorHash`` class.

    Returns:
        A ``(H, S, L)`` tuple.
    """
    # "all([x for x ...])" is actually faster than "all(x for x ...)"
    if not all([0.0 <= x <= 1.0 for x in lightness]):
        raise ValueError("lightness params must be in range (0.0, 1.0)")
    if not all([0.0 <= x <= 1.0 for x in saturation]):
        raise ValueError("saturation params must be in range (0.0, 1.0)")

    if min_h is None and max_h is not None:
        min_h = MIN_HUE
    if min_h is not None and max_h is None:
        max_h = MAX_HUE

    hash_val = crc32_hash(obj)
    h = hash_val % 359
    if min_h is not None and max_h is not None:
        if not (
            MIN_HUE <= min_h <= MAX_HUE
            and MIN_HUE <= max_h <= MAX_HUE
            and min_h <= max_h
        ):
            raise ValueError(
                "min_h and max_h must be in range [0, 360] with min_h <= max_h"
            )
        h = (h / 1000) * (max_h - min_h) + min_h
    hash_val //= 360
    s = saturation[hash_val % len(saturation)]
    hash_val //= len(saturation)
    l = lightness[hash_val % len(lightness)]  # noqa

    return (h, s, l)


class ColorHash:
    """
    Generate a color value and provide it in several format.

    Args:
        obj: the value.
        lightness: a range of values, one of which will be picked for the
                   lightness component of the result. Can also be a single
                   number.
        saturation: a range of values, one of which will be picked for the
                    saturation component of the result. Can also be a single
                    number.
        min_h: if set, limit the hue component to this lower value.
        max_h: if set, limit the hue component to this upper value.

    Attributes:
        hsl: HSL representation of the color value.
        rgb: RGB representation of the color value.
        hex: hex-formatted RGB color value.
    """

    def __init__(
        self,
        obj: Any,
        lightness: Sequence[float] = (0.35, 0.5, 0.65),
        saturation: Sequence[float] = (0.35, 0.5, 0.65),
        min_h: Optional[int] = None,
        max_h: Optional[int] = None,
    ):
        self.hsl: Tuple[float, float, float] = color_hash(
            obj=obj,
            lightness=lightness,
            saturation=saturation,
            min_h=min_h,
            max_h=max_h,
        )

    @property
    def rgb(self) -> Tuple[int, int, int]:
        return hsl2rgb(self.hsl)

    @property
    def hex(self) -> str:
        return rgb2hex(self.rgb)
