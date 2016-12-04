import sys

from require import *

require('b')
c = require('d/c')
print(c)
print(dir(c))

for modname in sys.modules:
    print(modname, sys.modules[modname])

print_cached_modules()