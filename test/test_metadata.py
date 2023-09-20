def test_version_from_metadata():
    """
    This test makes sense only if importlib.metadata or importlib_metadata is avail.
    Otherwise its a test of "colorhash.get_version" vs. "colorhash.get_version" :)
    """
    import colorhash

    version = colorhash.get_version(__package__)
    assert colorhash.__version__ == version
