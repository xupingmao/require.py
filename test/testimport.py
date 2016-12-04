import testimport2
import copy

prev_globals = copy.copy(globals())
prev_globals['prev_globals'] = prev_globals

print('************************')
print('testimport2 attributes:')
print('************************')
for item in dir(testimport2):
    print(item)

from testimport2 import *
print('*************************')
print('imported global variables')
print('*************************')
prev_globals['item'] = None
for item in globals():
    if item not in prev_globals:
        print(item)