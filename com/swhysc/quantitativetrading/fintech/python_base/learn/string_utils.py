import random

我和你 = '我爱你'
print(我和你)
times = 3
secret = random.randint(1, 10)
print('------------------游戏开始------------------')
guess = 0
print("不妨猜一下我现在心里想的是哪个数字：", end=" ")
while (guess != secret) and (times > 0):
    temp = input()
    while not temp.isdigit():
        temp = input("抱歉，您的输入有误，请输入一个整数：")
    guess = int(temp)
    if guess == secret:
        print("你是俺心里的蛔虫吗？！")
        print("哼，猜中了也没有奖励！")
        break
    else:
        if guess > secret:
            print("哥，大了大了~~~")
        else:
            print("嘿，小了，小了~~~")
        times = times - 1  # 用户每输入一次，可用机会就-1
    if times > 0:
        print("再试一次吧：", end=" ")
    else:
        print("机会用光咯T_T")
print("游戏结束，不玩啦^_^")

temp = input('输入需要判断的年份：')
while not temp.isdigit():
    print("您的输入有误，请输入一个数字！")
    temp = input()
year = int(temp)
i = year % 400
j = year % 100
if i == 0 and j == 0:
    print(temp + '是闰年！')
else:
    print(temp + '是平年')
