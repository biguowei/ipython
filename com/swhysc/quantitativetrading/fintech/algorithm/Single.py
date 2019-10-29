# 方式一
def Single(cls, *args, **kwargs):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@Single
class B:
    pass


# 方式二
class Single:
    def __init__(self):
        print("单例模式实现方式二。。。")


single = Single()
del Single  # 每次调用single就可以了


# 方式三(最常用的方式)
class Single:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
