import sys

def test_version():
    if not sys.version_info['major'] == (3):
        assert False