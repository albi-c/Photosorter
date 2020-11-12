import sys, os
DIRNAME = os.path.dirname(os.path.abspath(__file__))
DIRNAME_MAIN = os.path.dirname(DIRNAME)

sys.path.append(DIRNAME_MAIN)

import strings

def test_Strings():
    s = strings.Strings("test")

    assert s["test1"] == "test1"
    assert s["test2.text"] == "test2"

    s["test1"] = "test"
    assert s["test1"] == "test"

    del s["test2.text"]

    val = 0
    try:
        s["test2.text"]
    except KeyError:
        val = 1
    
    assert val == 1
