import sys

def test_version():
    if not sys.version_info[0] == 3:
        assert False
