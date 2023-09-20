def get_version():
    """
    Fast (dev time) way to get version.
    """
    with open("pyproject.toml") as f:
        for line in f.readlines():
            if line.startswith("version = "):
                ver = line.split("=")[1].strip().strip('"')
                return ver


def test_version_from_metadata():
    import colorhash

    version = get_version()
    assert colorhash.__version__ == version
