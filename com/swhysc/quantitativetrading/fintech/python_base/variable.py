import operator

# strIn = '测试test123'  # input()
# intIn = int(input())
# floatIn = float(input())
#
# print(type(strIn))
# print(type(intIn))
# print(type(floatIn))
# print(type(repr(strIn)))

# tuples = tuple(strIn)
# print(tuple(tuples))

# listIn = list(strIn)
# print(listIn)
#
# print(listIn.append('123')) # None
# print(type(listIn))
# listIn.append(12333)
# print(listIn)

# intIn = 97
# print(chr(intIn))
# print(hex(100))
# print(oct(100))
# print(ord('a'))
# print(unichr(intIn))

# print(2**3)
#
# print(100//3.0)

# # exchange two values
# a, b = 1, 2
# a, b = b, a
# print(a, b)
#
# # and , or , not
# if 1 and 2:
#     print('true')
#
# if 1 and 0:
#     print('true')
# else:
#     print('false')
#
# if 1 or 0:
#     print('true')
#
# if not None:
#     print('true')
# else:
#     print('false')

# abbr = 'ab'
# if abbr == 'a':
#     print(abbr + 'a')
# elif abbr == 'b':
#     print(abbr + 'b')
# elif 'a' in abbr:
#     print('a in ab')
# else:
#     print(abbr + 'ab')

# dict list set
"""
# 1、数组
# 切片规则：左右空，取到头；左要取，右不取
lis = ['小明', 18, 1.70, 'test', '测试123', '18']
print(lis[:])  # ['小明', 18, 1.7, 'test', '测试123']
print(lis[2:])  # [1.7, 'test', '测试123']
print(lis[:3])  # ['小明', 18, 1.7]
print(lis[2:4])  # [1.7, 'test']

lis.clear()
lis.append('18')
print(lis.count('18'))
lis.reverse()

lisIntFloat = [10, 2, 5, 3, 2.45, 0, int('1111111')]
lisIntFloat.sort(reverse=True)  # not supported between instances of 'int' and 'str'
print(lisIntFloat)

lisIntFloat.remove(10)  # 移除元素
# del lisIntFloat[:4]   # 一次性移除多个元素，规则与切片一致
print(lisIntFloat)

print(lisIntFloat.index(2))  # 查询元素在列表中的索引位置

print(lisIntFloat)
print(lisIntFloat.pop(2))  # Remove and return item at index (default last).

tupleIn = (45, 46, 78, 12, 9)
lisIntFloat.extend(tupleIn)  # 从可迭代变量中获取元素并追加到list后面
print(lisIntFloat)

lisIntFloat.insert(4, 888)  # 在指定索引位置插入元素，插入首位则 list.insert(0, '元素值')
list_len = len(lisIntFloat)
lisIntFloat.insert(list_len, '999')  # 插入首位则 list.insert(数组原长度, '元素值')
print(lisIntFloat)

"""

"""
# 2、字典
# 与列表区别： 列表有序，要用偏移量定位；字典无序，便通过唯一的键来取值
# 字典是另一种可变容器模型，且可存储任意类型对象，如字符串、数字、元组等其他容器模型（值不可变）。

score = {"小维": 95, "小红": 90, "小刚": 59}
print(score["小红"])

score["小三"] = 66
del score["小红"]
print(str(score))

keys = ['key1', 'key2', 'key3']
values = [4, 5, 6]
score_1 = score.fromkeys(keys, 'same_value')  # 给keys赋予相同的映射结果：“same_value”
print(score_1)

# print(score. .has_key('小维'))
# score.get("小维", default='不存在的key')

print(type(score.keys()))

# score.setdefault('小微', default=123)  # 和get()类似, 但如果键不已经存在于字典中，将会添加键并将值设为default
print(score)

score_1['小刚'] = 'update_val'
score.update(score_1)  # 把字典dict2的键/值对更新到dict里
print(score)

print(score.items())
for item in score.items():
    break
    print(type(item))  # tuple
score.pop('key1')  # 删除字典元素与其值
print(score.get('小刚'))  # 输出x对应的映射元素

# 字典定义方法
# operator 用于比较两个列表, 数字或字符串等的大小关系的函数，包含 le,lt,ge,gt,ne,eq
a = dict(one=1, two=2, three=3)
b = {'one': 1, 'two': 2, 'three': 3}
c = dict((('one', 1), ('two', 2), ('three', 3)))
d = dict(zip(['one', 'two', 'three'], [1, 2, 3]))
e = dict([('two', 2), ('one', 1), ('three', 3)])
f = dict({'three': 3, 'one': 1, 'two': 2})
print(operator.eq(a, b), operator.eq(a, c), operator.eq(a, d), operator.eq(a, e), operator.eq(a, f))
"""

"""
# 集合方法
total_set = {'one', 'two', 'three'}
sub_set = {'one', 'two', 'four'}
print(sub_set.issubset(total_set))  # s中所有的元素都是t的成员
print(total_set.union(sub_set))  # 合并：total_set或sub_set中的元素
print(total_set.intersection(sub_set))  # 交集:total_set与sub_set中的元素
print(total_set.difference(sub_set))   # 差分操作：在total_set中存在但在sub_set中不存在的元素
print(total_set.symmetric_difference(sub_set))  # 对称差分操作：total_set或sub_set中的元素，而不是两者共有的元素
# 适用于可变集合
total_set.update(sub_set)    # 将sub_set中的元素添加到total_set中
total_set.intersection_update(sub_set)    # 交集修改操作：total_set中仅包含total_set与sub_set共有的元素
total_set.difference_update(sub_set)    # 差修改操作：total_set中仅包括total_set中存在但sub_set中不存在的元素
total_set.symmetric_difference_update(sub_set)    # 对称差分修改操作：total_set中包括仅属于total_set或仅属于sub_set的成员
total_set.discard('one')  # 丢弃操作：将obj从s中删除，如果不存在不抛异常  set.remove(element) 删除元素不存在则抛出异常
print(total_set)
"""






































