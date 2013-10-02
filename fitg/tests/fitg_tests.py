from sys import version_info
from nose.tools import ok_

def test_version():
    ok_(version_info[0] == 3, "Expected Python version 3.x")