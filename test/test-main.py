from require import require
import traceback
import sys

try:
    require("1")
    require("a")
    require("i1")
    require("r1")
    require("testimport")
    require("test-require-all")
    require("test-force")
    
    print("\n"*3)
    print("all tests passed!")
except Exception as e:
    ex_type, ex, tb = sys.exc_info()
    print(ex)
    traceback.print_tb(tb)
    
    print("\n"*3)
    print("tests failed!")