requests.get

```python
import requests

response = requests.get('https://www.runoob.com/')
response.encoding = 'utf-8'

# print(type(response.content))
# print(response.content)      # 请求二进制内容
print(type(response.text))     # 查看类型
print(response.text)           # 请求内容
print(response.status_code)    # 请求回应
print(response.headers)        # 表头
print(response.cookies)        # cookies
```

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

#### 菜鸟笔记

Python 3 源码文件以 **UTF-8** 编码

- Python 中单引号 **'** 和双引号 **"** 使用完全相同

- 使用三引号(**'''** 或 **"""**)可以指定一个多行字符串

- 转义符 \

- 使用 **r** 可以让反斜杠不发生转义。 如 **r"this is a line with \n"** 则 **\n** 会显示，并不是换行

- 索引方式，从左往右以 **0** 开始，从右往左以 **-1** 开始

  ![img](https://static.runoob.com/wp-content/uploads/123456-20200923-1.svg)



- 字符串的截取的语法格式如下：**变量[头下标:尾下标:步长]**

```
str='123456789'

print(str[1:5:2])          # 输出从第二个开始到第五个且每隔一个的字符（步长为2）
```

**print** 默认输出是换行的，如果要实现不换行需要在变量末尾加上 **end=""**

```python
#!/usr/bin/python3
 
x="a"
y="b"
# 换行输出
print( x )
print( y )
 
print('---------')
# 不换行输出
print( x, end=" " )
print( y, end=" " )
print()
```

在 python 用 **import** 或者 **from...import** 来导入相应的模块

> 将整个模块(somemodule)导入，格式为： **import somemodule**
>
> 从某个模块中导入某个函数,格式为： **from somemodule import somefunction**
>
> 从某个模块中导入多个函数,格式为： **from somemodule import firstfunc, secondfunc, thirdfunc**
>
> 将某个模块中的全部函数导入，格式为： **from somemodule import  ***

```python
#导入 sys 模块
import sys
print('================Python import mode==========================')
print ('命令行参数为:')
for i in sys.argv:
    print (i)
print ('\n python 路径为',sys.path)


#导入 sys 模块的 argv,path 成员
from sys import argv,path  #  导入特定的成员
 
print('================python from import===================================')
print('path:',path) # 因为已经导入path成员，所以此处引用时不需要加sys.path
```

isinstance 和 type 的区别在于：

- type()不会认为子类是一种父类类型。
- isinstance()会认为子类是一种父类类型。

```python
>>> class A:
...     pass
... 
>>> class B(A):
...     pass
... 
>>> isinstance(A(), A)
True
>>> type(A()) == A 
True
>>> isinstance(B(), A)
True
>>> type(B()) == A
False
```

可以使用del语句删除一些对象引用

```bash
del var
del var_a, var_b
```

数值运算

>数值的除法包含两个运算符：**/** 返回一个浮点数，**//** 返回一个整数

列表

```
列表是写在方括号 [] 之间、用逗号分隔开的元素列表
列表截取的语法格式 变量[头下标:尾下标]
```

![img](D:\疯狂内卷文件\云计算省赛准备\省赛记忆手册github\Provincial-competition-memory-handbook\个人问题笔记\Python笔记.assets\list_slicing1_new1.png)

元组（tuple）与列表类似，不同之处在于元组的元素不能修改。元组写在小括号 **()** 里，元素之间用逗号隔开

```
修改元组元素的操作是非法的
tup = (1, 2, 3, 4, 5, 6)
```

Set（集合）由一个或数个形态各异的大小整体组成的，构成集合的事物或对象称作元素或是成员

```
使用大括号 { } 或者 set() 函数创建集合
parame = {value01,value02,...}
或者
set(value)
创建一个空集合必须用 set() 而不是 { }

print(a - b)     # a 和 b 的差集

print(a | b)     # a 和 b 的并集

print(a & b)     # a 和 b 的交集

print(a ^ b)     # a 和 b 中不同时存在的元素
```

字典（dictionary）字典是一种映射类型，字典用 **{ }** 标识，它是一个无序的 **键(key) : 值(value)** 的集合

```python
键(key)必须使用不可变类型
dict = {}
dict['one'] = "1 - 菜鸟教程"
tinydict = {'name': 'runoob','code':1, 'site': 'www.runoob.com'}

print (dict['one'])       # 输出键为 'one' 的值
print (tinydict)          # 输出完整的字典
print (tinydict.keys())   # 输出所有键
print (tinydict.values()) # 输出所有值
```

类型转换

```
显性类型转换
隐形类型转换
```

推导式

- 列表(list)推导式

```python
#格式
[表达式 for 变量 in 列表] 
[out_exp_res for out_exp in input_list]
或者 
[表达式 for 变量 in 列表 if 条件]
[out_exp_res for out_exp in input_list if condition]

# out_exp_res：列表生成元素表达式，可以是有返回值的函数。
# for out_exp in input_list：迭代 input_list 将 out_exp 传入到 out_exp_res 表达式中。
# if condition：条件语句，可以过滤列表中不符合条件的值。
#实例1
>>> names = ['Bob','Tom','alice','Jerry','Wendy','Smith']
>>> new_names = [name.upper()for name in names if len(name)>3]
>>> print(new_names)
['ALICE', 'JERRY', 'WENDY', 'SMITH']
# .upper() 方法将字符串中的小写字母转为大写字母
# .lower()方法转换字符串中所有大写字符为小写

#实例2
>>> multiples = [i for i in range(30) if i % 3 == 0]
>>> print(multiples)
[0, 3, 6, 9, 12, 15, 18, 21, 24, 27]
#range(start, stop, step) 
```

- 字典(dict)推导式

```python
#格式
{ key_expr: value_expr for value in collection }
或
{ key_expr: value_expr for value in collection if condition }

#实例1
listdemo = ['Google','Runoob', 'Taobao']
# 将列表中各字符串值为键，各字符串的长度为值，组成键值对
>>> newdict = {key:len(key) for key in listdemo}
>>> newdict
{'Google': 6, 'Runoob': 6, 'Taobao': 6}

#实例2
>>> dic = {x: x**2 for x in (2, 4, 6)}
>>> dic
{2: 4, 4: 16, 6: 36}
>>> type(dic)
<class 'dict'>
```

- 集合(set)推导式

```

```

- 元组(tuple)推导式

```

```

