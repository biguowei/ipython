import easygui as g
import random

d = random.randint(0, 10)

while 1:

    g.msgbox("现在开始猜数字小游戏：")
    # num=int(g.enterbox(title='猜我心里在想哪个数字'))

    msg = "我心里在想哪个数字"
    title = '玩游戏'
    num = g.integerbox(msg, title, lowerbound=0, upperbound=99)
    if num == d:
        g.msgbox("牛逼")
        break
    elif num > d:
        g.msgbox('大了')
    else:
        g.msgbox('小了')
