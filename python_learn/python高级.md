##列表推导式
Python 中的 列表推导式 List Comprehension 用于 从 一个现有的列表 创建 一个新列表 , 使用一行代码 即可 实现 循环 或 条件逻辑 , 生成新的 列表 ;
```
new_list = [expression for item in iterable if condition]
```
####基础用法：
```cython
original_list = [1, 2, 3, 4, 5]
new_list = [x * 2 + 1 for x in original_list]
print(new_list)  # 输出: [3, 5, 7, 9, 11]
```
####条件表达式用法
```cython
original_list = [1, 2, 3, 4, 5]
new_list = [x * 2 + 1 for x in original_list if x > 3]
```
####列表推导式嵌套用法
```cython
original_list1 = ['a', 'b']
original_list2 = [1, 2]
# 使用 列表推导式 推导出新列表
# for x in original_list1 是外层循环
# for y in original_list2 是内层循环
new_list = [(x, y) for x in original_list1 for y in original_list2]
print(new_list)  # 输出: [('a', 1), ('a', 2), ('b', 1), ('b', 2)]
```
##Python 生成器（Generators）
####1. 什么是生成器？
生成器是一个返回迭代器的函数，它使用了 yield 关键字来返回数据。与普通函数不同的是，当生成器函数调用时，它并不会立刻执行所有的代码并返回结果，而是返回一个生成器对象。每次调用生成器的 __next__() 方法时，生成器才会继续执行代码，直到遇到 yield 语句或者结束。

通过 yield 返回的每个值都被保存在生成器的状态中，当 next() 被调用时，执行会从上次返回 yield 语句的地方继续。

####2.创建生成器
```cython
def count_up_to(max):
    count = 1
    while count <= max:
        yield count # 每次调用时返回一个新的值 
        count += 1

# 采用next（）函数or在循环中迭代
# 1.——————————————
counter = count_up_to(5)#返回生成器对象
print(next(counter)) # 输出: 1
print(next(counter)) # 输出: 2

# 2.——————————————
for num in count_up_to(5):
    print(num)
# 输出：1 2 3 4 5
```
####3.生成器表达式
除了使用 yield 关键字创建生成器，我们还可以使用生成器表达式（generator expressions），它类似于列表推导式，但使用圆括号而不是方括号：
```cython
gen = (x * x for x in range(5))
# 1.
print(next(gen)) # 输出: 0
print(next(gen)) # 输出: 1
# 2.
for value in gen:
    print(value)
# 输出：4 9 16
```
####4.生成器优点
1)生成器的一个主要优点是它们比列表、元组等数据结构更加节省内存，因为它们不会一次性生成所有数据。数据是惰性地生成的，只有在需要时才会计算。

假设我们需要生成一个非常大的序列，普通的列表可能会占用大量内存，而使用生成器就能避免这一问题。
```cython
# 使用列表

numbers = [x * x for x in range(1000000)] # 会占用大量内存

# 使用生成器

numbers = (x * x for x in range(1000000)) # 不会占用大量内存
```
2)生成器仅在迭代时计算下一个值，避免了计算不必要的元素。

3)生成器非常适合表示和处理无限序列，因为它们不会将所有值都存储在内存中。你可以创建一个无限的序列，而生成器会按需生成每个值。

####5.生成器和迭代器的关系
生成器是迭代器的一个特殊实现。一个迭代器必须实现 __iter__() 和 __next__() 方法，而生成器函数自动实现了这两个方法。

虽然二者的表现相似，但生成器更简洁、易读。
```cython
# 普通迭代器
class MyIterator:
    def __init__(self, start, end):
        self.current = start
        self.end = end
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current > self.end:
            raise StopIteration
        self.current += 1
        return self.current - 1
 
# 生成器
def my_generator(start, end):
    current = start
    while current <= end:
        yield current
        current += 1
```