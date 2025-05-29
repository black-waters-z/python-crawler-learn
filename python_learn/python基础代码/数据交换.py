#第一个方法：定义中间变量
# 第二个方法，没见识过：
# a,b=1,2
# a,b=b,a
# print(f'{a} {b}')

# 了解引用
# 可以用id()来判断两个变量是不是同一个值的引用，id可以理解为内存的地址标志
a=1
b=a
a=2
print(id(b))
print(id(a))
print(a)
print(b)    #int是不可变类型，改变会有两份地址存储
# 输出结果不同

#列表引用
aa=[10,20]
bb=aa
print(id(aa))
print(id(bb))
aa.append(30)
print(aa)
print(bb)   #列表是可变类型

