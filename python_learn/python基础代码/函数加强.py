# 学员管理系统
# 递归
# lambda表达式
# 高阶函数

# 1.1系统简介
# global 声名全局变量

# lambda应用场景，如果一个函数有一个返回值，并且只有一句代码，可以使用lambda简化
# 语法

# lambda 参数列表:表达式
# 函数
def fn1():
    return 200

print(fn1)
print(fn1())
"""
<function fn1 at 0x0000019A84875DC0>
200"""
# lambda表达式
fn2=lambda :100
print(fn2)
print(fn2())
"""
<function <lambda> at 0x0000019A84875700>
100
"""

def add(a,b):
    return a+b

add1=lambda a,b:a+b

func1=lambda a:a
# 定义参数
func2=lambda a,b,c=100:1+b+c
# 可变参数*args，返回值为元组
func3=lambda *args:args
print(func3(10,20,30))
# 可变参数**kwargs关键字参数，返回字典
func4=lambda **kwargs:kwargs
print(func4(name='python',age=20))


"""带判断的lambda"""
fun1=lambda a,b:a if a>b else b

# 列表数据按字典key值排序
students=[
    {'name':'tom','age':20},
    {'name':'ROSE','age':19}
]
# 按照name升序排序
students.sort(key=lambda x:x['name'])
# 降序排序
students.sort(key=lambda x:x['name'],reverse=True)
