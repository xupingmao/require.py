import os
import sys

FILE_SEP = os.sep

class M:
    '''just call it `M`'''
    def __init__(self):
        self.cached_pathes = []
        self.cached_modules = []
        self.cwd = os.getcwd()

# makesure there is only one `M`
if '_modules' not in globals():
    _modules = M()

# split path to list of directories
# eg. home/usr => ['home', 'usr']
def split_path(path):
    cached_pathes = []
    name = ''
    for c in path:
        if c == '/' or c == '\\':
            cached_pathes.append(name)
            name = ''
        else:
            name += c
    if name != '':cached_pathes.append(name)
    return cached_pathes

# join a list like ['home', 'usr'] to a dir "home/usr"
# also handle pathes like 'home/usr/../proc' to "home/proc"
def join_path(path_list):
    if len(path_list) == 0: return ""
    else: lastdir = path_list.pop()
    path = ''
    cleanpath = []
    for item in path_list:
        if item == '..':
            cleanpath.pop()
        elif item == '.':
            pass
        else:
            cleanpath.append(item)
    for item in cleanpath:
        path += item + FILE_SEP
    return path + lastdir

def getabspath(cwd, path):
    fs1 = split_path(cwd)
    fs2 = split_path(path)
    file = fs2.pop()
    parent = join_path(fs1 + fs2)
    abspath = os.path.join(parent, file)
    return abspath, parent, file
    
    
def require(path, globals = None):
    '''require python module from relative path'''
    syspath_modified = False
    cwd = _modules.cwd
    exc = None # exception
    if '/' not in path:
        parent = None
        file = path
        abspath = os.path.join(cwd, path)
    else:
        abspath, parent, file = getabspath(cwd, path)

    if abspath in _modules.cached_pathes:
        # find module in cached_modules
        idx = _modules.cached_pathes.index(abspath)
        m = _modules.cached_modules[idx]
    else:
        if parent != None:
            # change current working directory
            # to the directory of the module.
            _modules.cwd = parent
            os.chdir(parent)
            # make sure the module can be loaded by default python importer
            if parent not in sys.path:
                sys.path.insert(0, parent)
                syspath_modified = True
        try:
            m = __import__(file)
        except Exception as e:
            exc = e # restore environment and raise Exception
        # restore `sys.path`
        if syspath_modified:
            del sys.path[0]
        if parent != None:
            # switch back current working directory
            os.chdir(cwd)
            _modules.cwd = cwd
        if exc is not None:
            raise exc
        _modules.cached_modules.append(m)
        _modules.cached_pathes.append(abspath)
        # print 'loadlib', abspath
    # import attributes to target globals.
    if globals:
        for key in dir(m):
            if key[0] != '_':
                globals[key] = getattr(m, key)
    return m

# make `require` to be a builtin-in function
def add_builtin(name, func):
    # when imported, __builtins__ is a dict
    # but when evaluated, it becomes a module.
    if isinstance(__builtins__, dict):
        __builtins__[name] = func
    else:
        setattr(__builtins__, name, func)
add_builtin('require', require)

def print_cached_modules():
    for path in _modules.cached_pathes:
        print(path)