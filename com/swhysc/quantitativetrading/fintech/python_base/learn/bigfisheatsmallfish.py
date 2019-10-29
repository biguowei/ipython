import random as r

# from random import choice
# 定义边界
boundary_x = [0, 10]
boundary_y = [0, 10]


# 定义乌龟类
class Tortoise:
    def __init__(self):

        # count=1
        self.physical_power = 100
        self.x = r.randint(boundary_x[0], boundary_x[1])
        self.y = r.randint(boundary_y[0], boundary_y[1])

    def move(self):
        # 随机选择移动速度和移动方向
        new_x = self.x + r.choice([1, 2, -1, -2])
        new_y = self.y + r.choice([1, 2, -1, -2])
        # print("乌龟当前坐标是：",self.x,self.y)
        # print("乌龟当前速度是：",self.speed)
        # 当移动到X轴最大边界时，自动反方向移动
        if new_x > boundary_x[1]:
            self.x = boundary_x[1] - (new_x - boundary_x[1])
        elif new_x < boundary_x[0]:
            self.x = boundary_x[0] - (new_x - boundary_x[0])
        else:
            self.x = new_x

        # 当移动到Y轴最大边界时，自动反方向移动
        if new_y > boundary_y[1]:
            self.x = boundary_y[1] - (new_y - boundary_y[1])
        elif new_y < boundary_y[0]:
            self.y = boundary_y[0] - (new_y - boundary_y[0])
        else:
            self.y = new_y

        # 体力消耗加1
        self.physical_power -= 1

        return (self.x, self.y)

    def eat(self):
        self.physical_power += 20  # 体力增加20
        if self.physical_power > 100:
            self.physical_power = 100


class Fish:
    def __init__(self):

        # count=10
        self.x = r.randint(boundary_x[0], boundary_x[1])
        self.y = r.randint(boundary_y[0], boundary_y[1])
        # 设置移动速度
        # speed = 1

    def move(self):
        # 随机选择移动速度和移动方向
        new_x = self.x + r.choice([1, -1])
        new_y = self.y + r.choice([1, -1])
        # 当移动到X轴最大边界时，自动反方向移动
        if new_x > boundary_x[1]:
            self.x = boundary_x[1] - (new_x - boundary_x[1])
        elif new_x < boundary_x[0]:
            self.x = boundary_x[0] - (new_x - boundary_x[0])
        else:
            self.x = new_x

        # 当移动到Y轴最大边界时，自动反方向移动
        if new_y > boundary_y[1]:
            self.x = boundary_y[1] - (new_y - boundary_y[1])
        elif new_y < boundary_y[0]:
            self.y = boundary_y[0] - (new_y - boundary_y[0])
        else:
            self.y = new_y

        return (self.x, self.y)


fish = []
tor = Tortoise()
for i in range(10):
    new_fish = Fish()
    fish.append(new_fish)

while 1:
    if len(fish) == 0:
        print("鱼儿都被吃光了，游戏结束！")
        break
    if  tor.physical_power == 0:
        print("乌龟体力耗完了，游戏结束！")
        break

    pos = tor.move()
    print("乌龟坐标是：", pos)
    for each_fish in fish[:]:
        f = each_fish.move()
        print("鱼儿坐标是： ", f)
        if f == pos:
            tor.eat()
            fish.remove(each_fish)
            print("------------有一条鱼被吃掉了！----------------")