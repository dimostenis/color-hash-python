# color-hash

ColorHash is a lightweight Python library for generating deterministic colors from any object.

By calculating a color value based on an object's hash, it ensures consistent results: the same input will always yield the same color. This is particularly useful for UI elements like user avatars or category labels where visual consistency is required.

This module is a port of the original [color-hash Javascript library](https://github.com/zenozeng/color-hash).

Key features:
- **Deterministic**: Same input always results in the same color.
- **Customizable**: Influence hue range, lightness, and saturation.
- **Zero Dependencies**: Lightweight and easy to integrate.
- **Compatibility**: Supports Python 3.8+ and is tested up to Python 3.15.

## Quick Start

```python
>>> from colorhash import ColorHash
>>> c = ColorHash('Hello World')
>>> c.hsl
(131, 0.65, 0.5)
>>> c.rgb
(45, 210, 75)
>>> c.hex
'#2dd24b'
```

## Installation

Its hosted on PyPI.

```bash
pip install colorhash
```

## Basic (intended) use

| code                                  | hex       | color                           |
|:--------------------------------------|:---------:|:-------------------------------:|
| `ColorHash('hey')` | `#782d86` | ![#782d86](./docs/782d86.png) |
| `ColorHash('oh')` | `#d29d79` | ![#d29d79](./docs/d29d79.png) |
| `ColorHash('boi')` | `#6ce072` | ![#6ce072](./docs/6ce072.png) |

## Advanced usage

You can influence every aspect of final color. **Default values** are following:

```python
ColorHash(
    obj: Any,
    lightness: Sequence[float] = (0.35, 0.5, 0.65),  # picks deterministically one
    saturation: Sequence[float] = (0.35, 0.5, 0.65),  # picks deterministically one
    min_h: Optional[int] = None,  # hue, min 0
    max_h: Optional[int] = None,  # hue, max 360
)
```

But be careful, **setting tight conditions may result in very similar colors**. See example tables.

You can fix lightness or saturation to single value(s) by using sequence with 1 element (eg. `[0.5]`). Providing more values enables wider variety of options for ColorHash to choose from (deterministically).

_Note: If you provide a single float instead of a sequence, it will be automatically wrapped in a list for convenience._

| code                                  | hex       | color                           |
|:--------------------------------------|:---------:|:-------------------------------:|
| `ColorHash('hey', lightness=[0.55])` | `#b453c6` | ![#b453c6](./docs/b453c6.png) |
| `ColorHash('hey', lightness=[0.75])` | `#d69fdf` | ![#d69fdf](./docs/d69fdf.png) |
| `ColorHash('hey', lightness=[0.95])` | `#f7ecf9` | ![#f7ecf9](./docs/f7ecf9.png) |
| `ColorHash('hey', saturation=[0.15])` | `#8d6c93` | ![#8d6c93](./docs/8d6c93.png) |
| `ColorHash('hey', saturation=[0.55])` | `#b139c6` | ![#b139c6](./docs/b139c6.png) |
| `ColorHash('hey', saturation=[0.95])` | `#d406f9` | ![#d406f9](./docs/d406f9.png) |
| `ColorHash('hey', lightness=[0.95], saturation=[0.95])` | `#fbe6fe` | ![#fbe6fe](./docs/fbe6fe.png) |
| `ColorHash('oh', lightness=[0.95], saturation=[0.95])` | `#fef0e6` | ![#fef0e6](./docs/fef0e6.png) |
| `ColorHash('boi', lightness=[0.95], saturation=[0.95])` | `#e6fee7` | ![#e6fee7](./docs/e6fee7.png) |

You can set hue range or even fix it by setting `min_h` = `max_h`.
If you set only `min_h` or `max_h`, the other will be defaulted to 0 or 360 respectively.

| code                                  | hex       | color                           |
|:--------------------------------------|:---------:|:-------------------------------:|
| `ColorHash('hey', min_h=150)` | `#2d5886` | ![#2d5886](./docs/2d5886.png) |
| `ColorHash('hey', min_h=300)` | `#862d6c` | ![#862d6c](./docs/862d6c.png) |
| `ColorHash('hey', max_h=150)` | `#866e2d` | ![#866e2d](./docs/866e2d.png) |
| `ColorHash('hey', min_h=150, max_h=360)` | `#2d5886` | ![#2d5886](./docs/2d5886.png) |
| `ColorHash('hey', min_h=150, max_h=150)  # fixed hue` | `#2d8659` | ![#2d8659](./docs/2d8659.png) |

Or you can let `ColorHash` decide between combination of many `lightness` and `saturation` options (mind `min_h` and `max_h` are equal in this example).

| code                                  | hex       | color                           |
|:--------------------------------------|:---------:|:-------------------------------:|
| `ColorHash('stick', min_h=65, max_h=65, saturation=[x/10 for x in range(1, 10)], lightness=[x/10 for x in range(1, 10)])` | `#869108` | ![#869108](./docs/869108.png) |
| `ColorHash('with', min_h=65, max_h=65, saturation=[x/10 for x in range(1, 10)], lightness=[x/10 for x in range(1, 10)])` | `#eef5a3` | ![#eef5a3](./docs/eef5a3.png) |
| `ColorHash('one', min_h=65, max_h=65, saturation=[x/10 for x in range(1, 10)], lightness=[x/10 for x in range(1, 10)])` | `#ddeb47` | ![#ddeb47](./docs/ddeb47.png) |

Finally some bad examples. When you set too strict rules, colors may be almost identical.

| code                                  | hex       | color                           |
|:--------------------------------------|:---------:|:-------------------------------:|
| `ColorHash('lets', lightness=[0.95], saturation=[0.95], min_h=300)` | `#fee6f8` | ![#fee6f8](./docs/fee6f8.png) |
| `ColorHash('break', lightness=[0.95], saturation=[0.95], min_h=300)` | `#fee6fb` | ![#fee6fb](./docs/fee6fb.png) |
| `ColorHash('it', lightness=[0.95], saturation=[0.95], min_h=300)` | `#fee6fa` | ![#fee6fa](./docs/fee6fa.png) |
| `ColorHash('here', min_h=150, max_h=150)` | `#6ce0a6` | ![#6ce0a6](./docs/6ce0a6.png) |
| `ColorHash('goes', min_h=150, max_h=150)` | `#79d2a6` | ![#79d2a6](./docs/79d2a6.png) |
| `ColorHash('color', min_h=150, max_h=150)` | `#6ce0a6` | ![#6ce0a6](./docs/6ce0a6.png) |

## Changelog

- color-hash **2.2.0** *(2026-03-12)*
  - 🐛 Fixed hue calculation range mapping to correctly use the full spectrum when `min_h` and `max_h` are provided
  - ✨ Support up to `python3.15` (tested on `3.15.0a6`)
- color-hash **2.1.0** *(2025-06-17)*
  - ✨ Support up to `python3.14`
  - ✨ Use `uv`
  - ⚰️ `python3.7` is still supported and *shall* work, but not tested any more
- color-hash **2.0.0** *(2023-09-22)*
  - ✨ Expose params to influence colors
  - ✨ Runtime validation of input params
  - 📝 Update docs for advanced usage
- color-hash **1.3.2** *(2023-09-21)*
  - ⚡️ 30%+ speedup on `hsl2rgb()`
  - ✅ Add tests for all named colors (1500+ tests)
- color-hash **1.3.1** *(2023-09-21)*
  - 🐛 Handle missing `importlib-metadata` import
- color-hash **1.3.0** *(2023-09-20)*
  - 🧑‍💻 Add `py.typed` to support type annotations (#4)
  - 📦 Changed packaging ecosystem
    - ➖ Remove `poetry`
    - ➖ Remove `tox`
    - ➕ Add `pip-tools` (manage dependencies)
    - ➕ Add `hatch` (build & test)
    - ➕ Add `twine` (publish)
  - ✨ Support `python3.11`
  - ⚰️ Drop support for `python3.6` (downloads from PyPI are under 1%)
- color-hash **1.2.2** *(2022-10-17)*
  - ✨ Add publish helper script
- color-hash **1.2.1** *(2022-10-17)*
  - 📝 Update docs
- color-hash **1.2.0** *(2022-10-17)*
  - 🧑‍💻 Use typing supporting `python3.6`
- color-hash **1.1.0** *(2022-09-01)*
  - ✅ Add tests
  - 🚸 Add installation instructions
- color-hash **1.0.4** *(2021-11-30)*
  - Support only for `python3.6+`
  - ✅ Add tests
- color-hash **1.0.3** *(2020-12-04)*
  - ⚰️ Drop support for `python2.x`
  - 🎉 Handover of project maintenance
- color-hash **1.0.2** *(2016-07-08)*
  - ✨ Add ``crc32_hash`` function and set default hashfunc to that. It's not
    fully backwards-compatible, but I don't want to bump the version a lot for
    not doing my research.
- color-hash **1.0.0** *(2016-07-07)*
  - 🎉 Initial port.

## License

Copyright (c) 2016 Felix Krull <f_krull@gmx.de>

This is a port of the 'color-hash' Javascript library which is:

Copyright (c) 2015 Zeno Zeng

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
