输入

```
str = input("请输入:");
print("输入的内容是:",str)
```

读写文件

```
open(filename,mode)   #会返回一个file对象

f = open("/tmp/foo.txt","w")
f.write("python")
f.close()
```

OS

```
文件目录方法
```

面向对象

```
__init__方法的第一个参数永远是 self 
使用了 __init__方法，在创建实例的时候就不能传入 空的参数了
```

