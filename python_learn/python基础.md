###元祖拆包and引用
```c
def return_num():
    return 100,200

a,b=return_num()
print(a)
print(b)
```
```c
dict={'name1':'tom','age':80}
a1,b1=dict
print(a1)
print(b1)
```
```c
print(dict.get(a1))
print(dict.get(b1))
```
输出：  
name1  
age  
tom  
80

##数据交换
```c
a,b=1,2
a,b=b,a
print(f'{a} {b}')
```
输出:  
2 1  

#### 了解引用
可以用id()来判断两个变量是不是同一个值的引用，id可以理解为内存的地址标志
```c
a=1
b=a
a=2
print(id(b))
print(id(a))
print(a)
print(b)    
```
####输出：  
int是不可变类型，改变会有两份地址存储  
输出结果不同
1  
2  
int是不可变类型，改变会有两份地址存储  
输出结果不同
```c
aa=[10,20]
bb=aa
print(id(aa))
print(id(bb))
aa.append(30)
print(aa)
print(bb)
```
####输出：
2360072961344  
2360072961344  
[10, 20, 30]  
[10, 20, 30]  
可见，列表是可变类型