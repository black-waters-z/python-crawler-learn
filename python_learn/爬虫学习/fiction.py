original_list = ["apple", "banana", "apple", "orange"]
unique_list = list(dict.fromkeys(original_list))
print(unique_list)  # 输出: ['apple', 'banana', 'orange']