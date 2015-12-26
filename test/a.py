
from require import *

require('b')
c = require('d/c')
print(c, dir(c))
print_cached_modules()