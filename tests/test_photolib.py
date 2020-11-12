import sys, os
DIRNAME = os.path.dirname(os.path.abspath(__file__))
DIRNAME_MAIN = os.path.dirname(DIRNAME)

sys.path.append(DIRNAME_MAIN)

import photolib

def test_getDirname():
    assert photolib.getDirname() == DIRNAME_MAIN

def test_listFiles():
    listed = photolib.listFiles(os.path.join(DIRNAME, "test_photolib", "test1"))
    listed = [os.path.basename(str(f)) for f in listed]

    assert len(listed) == 1
    assert listed == ["test.png"]

def test_listDirs():
    assert photolib.listDirs(os.path.join(DIRNAME, "test_photolib")) == ["test1", "test2"]
    assert photolib.listDirs(os.path.join(DIRNAME, "test_photolib"), ["test2"]) == ["test1"]
    assert photolib.listDirs(os.path.join(DIRNAME, "test_photolib"), checkFunc=lambda fn: fn != "test1") == ["test2"]
    assert photolib.listDirs(os.path.join(DIRNAME, "test_photolib"), ["test1", "test2"]) == []
    assert photolib.listDirs(os.path.join(DIRNAME, "test_photolib"), checkFunc=lambda fn: False) == []

def test_isYear():
    assert photolib.isYear("2020")
    assert photolib.isYear("1980")
    assert not photolib.isYear("202")
    assert not photolib.isYear("20202")

    assert not photolib.isYear("2020a")
    assert not photolib.isYear("a2020")
    assert not photolib.isYear("a2020a")
    assert not photolib.isYear("20z0")
