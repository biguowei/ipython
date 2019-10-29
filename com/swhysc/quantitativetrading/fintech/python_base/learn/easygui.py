# 在35-3的基础上进行优化，当用户点击ok按钮的时候，对打开的文件进行检查是否修改。
# 如果修改过，则提示覆盖保存、放弃保存、另存为并实现相应的功能
import easygui as g
import os

msg = '浏览文件并打开'
title = '测试'
default = 'D:\Python练习\*'
fileType = '全部文件'
filePath = g.fileopenbox(msg, title, default, fileType)

with open(filePath) as f:
    title = os.path.basename(filePath)
    msg = '文件%s的内容如下：' % title
    txt = f.read()
    txt_new = g.textbox(title, msg, txt)

if txt != txt_new[:-1]:
    # 检查文件是否修改,因为easygui,txtbox会在返回字符串后面追加一个行结束符（"\n"),因此在比较稳健师傅改变时，需要我们人工忽略这个行结束符
    msg1 = '选择您的操作：'
    title = '检测到文件被修改，请选择是否保存：'
    buttons = ['覆盖保存', '放弃保存', '另存为']
    choice = g.buttonbox(title, msg, buttons)
    # 覆盖保存
    if choice == '覆盖保存':
        with open(filePath, 'w') as f2:
            f2.write(txt_new)
    # 放弃保存
    if choice == '放弃保存':
        pass
    # 另存为。。。
    if choice == '另存为':
        new_path = g.filesavebox(default='txt')
        with open(new_path, 'w') as f3:
            f3.write(txt_new)
