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
以上面的目录结构为例，使用方法是：
在init.py中加入`from require import *`

