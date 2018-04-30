import os
import sys

'''
require function for python
    
    2018-04-30 : Add set_entry_file to set programe entry path, the root will be cwd by default.

    2016-12-04 : Add require parameter to force update module

@author xupingmao
@modified 2018/04/30 15:30:08
'''

FILE_SEP = os.sep

class M:
    '''just call it `M`'''
    def __init__(self):
        self.cache = {}
        self.cwd = os.getcwd()
        # self.cwd = os.path.dirname(__file__)
        self.root = self.cwd

# makesure there is only one `M`
if '_modules' not in globals():
    _modules = M()

def set_entry_file(fpath):
    fpath = os.path.abspath(fpath)
    _modules.root = os.path.dirname(fpath)
    _modules.cwd = _modules.root


def split_path(path):
    """split path to list of directories
        
        >>> split_path("home/usr")
        ['home', 'usr']
    """
    path = path.replace("\\", "/")
    return path.split("/")

def join_path(path_list):
    """join a list of string to a valid path

        >>> join_path(['home', 'usr'])
        'home/usr'
    """
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
    """

        >>> getabspath("/root", "home")
        '/root/home'
        >>> getabspath("/root", "home/../name")
        '/root/name'
    """
    fs1 = split_path(cwd)
    fs2 = split_path(path)
    abspath = join_path(fs1 + fs2)
    parent = os.path.dirname(abspath)
    file   = os.path.basename(abspath)
    return abspath, parent, file
    
class RModule:
    
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return "<RModule from %s>" % self.path


def require(path, globals = None, force=False):
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

    if not force and abspath in _modules.cache:
        # find module in cached_modules
        m = _modules.cache[abspath]
        # print("hit cache", path, abspath)
    else:
        # print("miss cache", path, abspath)
        _modules.cache[abspath] = RModule(abspath)
        # print("put cache", path, abspath)
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
            if force and abspath in _modules.cache:
                oldm = _modules.cache[abspath]
                modulescopy = sys.modules.copy()
                for key in modulescopy:
                    value = sys.modules[key]
                    if value == oldm:
                        # print("del %s, %s" % (key, sys.modules[key]))
                        del sys.modules[key]
                        break
            if file in sys.modules:
                # remove file
                print("remove module", file)
                del sys.modules[file]
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
        
        _modules.cache[abspath] = m
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
    for path in _modules.cache:
        mod = _modules.cache[path]
        print("%-50s%s" % (path, mod))


