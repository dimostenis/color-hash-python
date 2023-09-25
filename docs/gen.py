from pathlib import Path

from PIL import Image

# needed for eval()
from colorhash import ColorHash  # noqa

NEW_TABLE_SEPARATOR = object()  # sentinel

lst = [
    NEW_TABLE_SEPARATOR,
    "ColorHash('hey')  # default",
    "ColorHash('hey', lightness=[0.55])",
    "ColorHash('hey', lightness=[0.75])",
    "ColorHash('hey', lightness=[0.95])",
    "ColorHash('hey', saturation=[0.15])",
    "ColorHash('hey', saturation=[0.55])",
    "ColorHash('hey', saturation=[0.95])",
    "ColorHash('hey', lightness=[0.95], saturation=[0.95])",
    "ColorHash('oh', lightness=[0.95], saturation=[0.95])",
    "ColorHash('boi', lightness=[0.95], saturation=[0.95])",
    NEW_TABLE_SEPARATOR,
    "ColorHash('hey', min_h=150)",
    "ColorHash('hey', min_h=300)",
    "ColorHash('hey', max_h=150)",
    "ColorHash('hey', min_h=150, max_h=360)",
    "ColorHash('hey', min_h=150, max_h=150)  # fixed hue",
    NEW_TABLE_SEPARATOR,
    "ColorHash('stick', min_h=65, max_h=65, saturation=[x/10 for x in range(1, 10)], lightness=[x/10 for x in range(1, 10)])",  # noqa
    "ColorHash('with', min_h=65, max_h=65, saturation=[x/10 for x in range(1, 10)], lightness=[x/10 for x in range(1, 10)])",  # noqa
    "ColorHash('one', min_h=65, max_h=65, saturation=[x/10 for x in range(1, 10)], lightness=[x/10 for x in range(1, 10)])",  # noqa
    NEW_TABLE_SEPARATOR,
    "ColorHash('lets', lightness=[0.95], saturation=[0.95], min_h=300)",
    "ColorHash('break', lightness=[0.95], saturation=[0.95], min_h=300)",
    "ColorHash('it', lightness=[0.95], saturation=[0.95], min_h=300)",
    "ColorHash('here', min_h=150, max_h=150)",
    "ColorHash('goes', min_h=150, max_h=150)",
    "ColorHash('almost', min_h=150, max_h=150)",
    "ColorHash('same', min_h=150, max_h=150)",
    "ColorHash('color', min_h=150, max_h=150)",
]

WIDTH = 120
HEIGHT = 25
OUT = Path("docs")
HEADER = "| code                                  | hex       | color                           |\n|:--------------------------------------|:---------:|:-------------------------------:|"  # noqa

# delete old tiles
[x.unlink() for x in OUT.glob("*.png")]

# gen tiles + docs table text
for code in lst:
    # start new table
    if code == NEW_TABLE_SEPARATOR:
        print("\n")
        print(HEADER)
        continue

    hex_color = eval(code).hex
    tile = Image.new("RGB", (WIDTH, HEIGHT), hex_color)

    filename = f"{hex_color[1:]}.png"  # eg. "eafbf6.png"
    tile.save(OUT / filename)

    s: str = f"| `{code}` | `{hex_color}` | ![{hex_color}](./docs/{filename}) |"
    print(s)
