# color-hash

**Generate a color based on a value**

This module generates a color based on an object, by calculating a color value
based on a hash value for the object. This means the result is deterministic:
the same value will always result in the same color (so long as the hash
function remains deterministic).

This module is a port of the [color-hash Javascript library](https://github.com/zenozeng/color-hash).

It supports Python 3.7+ and it has no dependencies.

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

## Changelog

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
  - ⚰️ Drop support for `python3.6`
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
