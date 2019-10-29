print([[x for x in range(1, 101)][i:i + 3] for i in range(0, 100, 3)])


class Yuan(type):
    def __new__(cls, name, base, attr, *args, **kwargs):
        return type(name, base, attr, *args, **kwargs)


class MyClass(metaclass=Yuan):
    pass


# 一只青蛙一次可以跳上1级台阶，也可以跳上2级。求该青蛙跳上一个n级的台阶总共有多少种跳法。
# 请问用n个2*1的小矩形无重叠地覆盖一个2*n的大矩形，总共有多少种方法？
# 方式一：
fib = lambda n: n if n <= 2 else fib(n - 1) + fib(n - 2)


# 方式二：
def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return b


# 一只青蛙一次可以跳上1级台阶，也可以跳上2级……它也可以跳上n级。求该青蛙跳上一个n级的台阶总共有多少种跳法。
fib = lambda n: n if n < 2 else 2 * fib(n - 1)


# list1 = ['A', 'B', 'C', 'D'] 如何才能得到以list中元素命名的新列表 A=[],B=[],C=[],D=[]呢
list1 = ['A', 'B', 'C', 'D']

# 方法一
for i in list1:
    globals()[i] = []   # 可以用于实现python版反射

# 方法二
for i in list1:
    exec(f'{i} = []')   # exec执行字符串语句