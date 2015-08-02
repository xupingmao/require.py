# require.py

## 功能
模仿nodejs的require方法导入模块
使用Python的时候我们有时候会遇到这样的问题：
```
src
|- init.py
|- a.py
|- dir/
   |- b.py
```
在这样的情况下在b.py里导入a.py呢？require.py的作用就是提供一个根据相对路径导入模块的解决方案。

## 使用方法
在启动文件第一行加入`from require import *`即可，其他python源文件就可以自由使用require方法导入模块了。
以上面的目录结构为例，假设init.py是启动文件，使用方法是：
在init.py中加入`from require import *`在b.py里加入`require('../a.py')`便可以导入a.py模块了。

## 关于循环导入
导入顺序和python一致，在test目录下有测试代码
例如：i1,i2是使用import语法循环导入，r1,r2是使用require语法循环导入
结果分别是
```
$ > python i1.py
i1
i2
i1
```

```
$ > python r1.py
r1
r2
r1
```

## 其他
在python中可以导入1.py吗？不行！但是require可以！
在python中，你使用`import 1`会这样
```
>>> import 1
  File "<stdin>", line 1
    import 1
           ^
SyntaxError: invalid syntax
```
但是使用require，放心，你成功导入的
```
from require import *
m2 = require('2.py')
print(m2)
```
会看到输出
```
<module '2' from 'XXXX/2.pyc'>
```
