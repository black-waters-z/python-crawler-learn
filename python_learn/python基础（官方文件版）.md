###Match语句
####*需要python版本3.10以上*
类似于switch case语句，但只有第一个匹配的模式会被执行，并且它还可以提取值的组成部分（序列的元素或对象的属性）赋给变量。
```cython
def http_error(status):
    match status:
        case 400:
            return "Bad request"
        case 404:
            return "Not found"
        case 418:
            return "I'm a teapot"
        case _:
            return "Something's wrong with the internet"
```
“变量名” _ 被作为 通配符 并必定会匹配成功。如果没有 case 匹配成功，则不会执行任何分支。

形如解包赋值的模式可被用于绑定变量：
```cython
# point 是一个 (x, y) 元组
point=(1,3)
match point:
    case (0, 0):
        print("Origin")
    case (0, y):
        print(f"Y={y}")
    case (x, 0):
        print(f"X={x}")
    case (x, y):
        print(f"X={x}, Y={y}")
    case _:
        raise ValueError("Not a point")
```
point=(1,3)  
输出：X=1,Y=3  

####用类组织数据
```cython
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def where_is(point):
    match point:
        case Point(x=0, y=0):
            print("Origin")
        case Point(x=0, y=y):
            print(f"Y={y}")
        case Point(x=x, y=0):
            print(f"X={x}")
        case Point():
            print("Somewhere else")
        case _:
            print("Not a point")
```
我们可以为模式添加 if 作为守卫子句。如果守卫子句的值为假，那么 match 会继续尝试匹配下一个 case 块。注意是先将值捕获，再对守卫子句求值：
```
match point:
    case Point(x, y) if x == y:
        print(f"Y=X at {x}")
    case Point(x, y):
        print(f"Not on the diagonal")
```

##参数
###默认值参数
```cython
def ask_ok(prompt, retries=4, reminder='Please try again!'):
    while True:
        reply = input(prompt)
        if reply in {'y', 'ye', 'yes'}:
            return True
        if reply in {'n', 'no', 'nop', 'nope'}:
            return False
        retries = retries - 1
        if retries < 0:
            raise ValueError('invalid user response')
        print(reminder)
```
有三种传参方式：  
ask_ok('Do you really want to quit?')  
ask_ok('OK to overwrite the file?', 2)  
ask_ok('OK to overwrite the file?', 2, 'Come on, only yes or no!')
####默认值在 定义 作用域里的函数定义中求值：
```cython
i = 5
def f(arg=i):
    print(arg)
i = 6
f()##输出值为5
```
默认值只计算一次。默认值为列表、字典或类实例等可变对象时，会产生与该规则不同的结果。例如，下面的函数会累积后续调用时传递的参数：
```cython
def f(a, L=[]):
    L.append(a)
    return L
print(f(1))
print(f(2))
print(f(3))
# [1]
# [1, 2]
# [1, 2, 3]
```
如若不采用可变列表，不共享值，那么可以采用以下方案：
```cython
def f(a, L=None):
    if L is None:
        L = []
    L.append(a)
    return L
# [1]
# [2]
# [3]
```
###关键字参数
*name 元祖  
**name 字典  
如何传入参数？？  
元祖："It's very runny, sir.",
           "It's really very, VERY runny, sir."  
字典： shopkeeper="Michael Palin",
           client="John Cleese",
           sketch="Cheese Shop Sketch"
```cython
def cheeseshop(kind, *arguments, **keywords):
    print("-- Do you have any", kind, "?")
    print("-- I'm sorry, we're all out of", kind)
    for arg in arguments:
        print(arg)
    print("-" * 40)
    for kw in keywords:
        print(kw, ":", keywords[kw])
cheeseshop("Limburger", "It's very runny, sir.",
           "It's really very, VERY runny, sir.",
           shopkeeper="Michael Palin",
           client="John Cleese",
           sketch="Cheese Shop Sketch")
```
输出：
```
-- Do you have any Limburger ?
-- I'm sorry, we're all out of Limburger
It's very runny, sir.
It's really very, VERY runny, sir.
----------------------------------------
shopkeeper : Michael Palin
client : John Cleese
sketch : Cheese Shop Sketch
```
####特殊参数
默认情况下，参数可以按位置或显式关键字传递给 Python 函数。为了让代码易读、高效，最好限制参数的传递方式

/位置参数  
*关键字参数
```
def f(pos1, pos2, /, pos_or_kwd, *, kwd1, kwd2):
      -----------    ----------     ----------
        |             |                  |
        |        位置或关键字   |
        |                                - 仅限关键字
         -- 仅限位置
```
函数定义中未使用 / 和 * 时，参数可以按位置或关键字传递给函数。

###解包实参列表
####参数在元组中
```cython
list(range(3, 6))            # 附带两个参数的正常调用
# [3, 4, 5]
args = [3, 6]
list(range(*args))            # 附带从一个列表解包的参数的调用
# [3, 4, 5]
```
####参数在字典中
```
def parrot(voltage, state='a stiff', action='voom'):
    print("-- This parrot wouldn't", action, end=' ')
    print("if you put", voltage, "volts through it.", end=' ')
    print("E's", state, "!")

d = {"voltage": "four million", "state": "bleedin' demised", "action": "VOOM"}
parrot(**d)
```
##lambda表达式
lambda 关键字用于创建小巧的匿名函数。
lambda参数：表达式返回值
如下：
```cython
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
```
带判断的lambda
```cython
fun1=lambda a,b:a if a>b else b
```
嵌套函数定义一样，lambda 函数可以引用包含作用域中的变量
```cython
def make_incrementor(n):
    return lambda x: x + n

f = make_incrementor(42)
f(0)
# 42
f(1)
# 43
```
还可以把匿名函数用作传递的实参
```cython
pairs = [(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four')]
pairs.sort(key=lambda pair: pair[1])
# 输出：按照首字母序号从小到大排序的数
```

##异常处理
异常处理步骤：  
1.执行try语句，如执行错误，跳过下列句子。如果和except匹配，执行except字句  
2.如若执行成功，则跳过except
3.如果发生的异常与 except 子句 中指定的异常不匹配，则它会被传递到外层的 try 语句中；如果没有找到处理器，则它是一个 未处理异常 且执行将停止并输出一条错误消息。
```cython
while True:
    try:
        x = int(input("Please enter a number: "))
        break
    except ValueError:
        print("Oops!  That was no valid number.  Try again...")
```
except 子句 可以用带圆括号的元组来指定多个异常
```
except (RuntimeError, TypeError, NameError):
    pass
```
一个 except 子句中的类匹配的异常将是该类本身的实例或其所派生的类的实例，例如子类

