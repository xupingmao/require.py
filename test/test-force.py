from require import *
import os
import time

code1 = '''
msg = "This is old code"
print(msg)
'''

code2 = '''
msg = "This is new code"
print(msg)
'''

def save(name, code):
    fp=open(name,"w")
    fp.write(code)
    fp.flush()
    fp.close()

save("test-force-item.py", code1)
m = require("test-force-item")
assert m.msg == "This is old code"

# wait pycache to refresh
time.sleep(1)

save("test-force-item.py", code2)
m2 = require("test-force-item", force=True)
assert m2.msg == "This is new code"

os.remove("test-force-item.py")