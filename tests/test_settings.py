import sys, os
DIRNAME = os.path.dirname(os.path.abspath(__file__))
DIRNAME_MAIN = os.path.dirname(DIRNAME)

sys.path.append(DIRNAME_MAIN)

import settings

def test_getDirname():
    assert settings.getDirname() == DIRNAME_MAIN

def test_getStringsFile():
    assert settings.getStringsFile("test1") == "test1"
