from require import *
import sys
require('b')
c = require('d/c')
print(c)
print(dir(c))

for modname in sys.modules:
    print(modname, sys.modules[modname])

print('-' * 30, "cache", '-' * 30)
print_cached_modules()