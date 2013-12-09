from sys import version_info
from nose.tools import ok_

def test_version():
    ok_(version_info[0] == 2, "Expected Python version 2.x")
