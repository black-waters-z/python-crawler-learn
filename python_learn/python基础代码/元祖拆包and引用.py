def return_num():
    return 100,200

a,b=return_num()
print(a)
print(b)
# ___________________________
dict={'name1':'tom','age':80}
a1,b1=dict
print(a1)
print(b1)
# name1
# age
# ___________________________
print(dict.get(a1))
print(dict.get(b1))
# tom
# 80