import easygui as g

msg = '欢迎注册'
title = '注册'
fieldNames = ['*用户名', '*密码', '*重复密码', '真实姓名', '手机号', 'QQ', 'e-mail']
fieldValues = []
fieldValues = g.multenterbox(msg, title, fieldNames)

while 1:
    if fieldValues == None:
        break
    errormsg = ''
    for i in range(len(fieldNames)):
        if '*' in fieldNames[i]:
            if fieldValues[i] == '':
                errormsg += '【%s】不能为空' % fieldNames[i]
                # g.msgbox(errormsg)
                # break
    if errormsg == '':
        break

    fieldValues = g.multenterbox(errormsg, title, fieldNames, fieldValues)

print(str(fieldValues))
