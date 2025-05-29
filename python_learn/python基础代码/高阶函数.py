# 高阶函数，把函数作为参数传入
# 绝对值
abs(-10)
# 四舍五入计算
round(1.2)

def add_num(a,b,f):
    return f(a)+f(b)

result=add_num(-1,2,abs)
print(result)

"""内置高阶函数
1.map()，将传入的函数变量func作用到list变量的每个元素之中
2.reduce(func,lst)其中func必须有两个函数，每次func计算的结果继续和序列的下一个元素做累计计算
"""
list1=[1,2,3,4,5]
def func(x):
    return x**2

result=map(func,list1)
print(result)
print(list(result))
"""
<map object at 0x00000202FDE34E50>
[1, 4, 9, 16, 25]
"""
import functools
def func2(a,b):
    return a+b

result=functools.reduce(func2,list1)
print(result)
# 15
"""
filter()函数用于过滤序列，过滤掉不符合条件的元素，返回filter对象
"""
def func3(x):
    return x%2==0
# 调用filter
result=filter(func3,list1)
print(result)
print(list(result))
