from require import require, set_entry_file, getabspath
import traceback
import sys

try:
    set_entry_file(__file__)

    path, parent, fname = getabspath("/root", "home/../name")
    print(path, parent, fname)
    assert "/root/name" == path

    require("1")
    require("a")
    require("i1")
    require("r1")
    require("testimport")
    require("test-require-all")
    require("test-force")

    t1 = require("tween")
    t2 = require("dup/tween")
    print(t1)
    print(t2)
    assert t1.name == "outside"
    assert t2.name == "inside"

    print("\n"*3)
    print("all tests passed!")
except Exception as e:
    # ex_type, ex, tb = sys.exc_info()
    print("\n"*3)
    print("tests failed!")
    raise e
