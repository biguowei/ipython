import re
import urllib.request
import time
import easygui as g

# 输入地址
g.msgbox("利用Python3 编写爬虫，从笔趣阁抓个小说下载到手机查看")
msg = "输入小说地址，例如http://www.biquge.com.tw/0_213/"
title = '爬虫'
root = g.enterbox(msg, title)

# 伪造浏览器
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) ' \
                         'AppleWebKit/537.36 (KHTML, like Gecko)' \
                         ' Chrome/62.0.3202.62 Safari/537.36'}

req = urllib.request.Request(url=root, headers=headers)

with urllib.request.urlopen(req, timeout=1) as response:
    # 大部分的涉及小说的网页都有charset='gbk'，所以使用gbk编码
    htmls = response.read().decode('gbk')

# 匹配所有目录http://www.biquge.com.tw/0_213/"
story_id = root.lstrip("http://www.biquge.com.tw/")

dir_req = re.compile(r'<a href="/%s(\d+?.html)">' % story_id)
dirs = dir_req.findall(htmls)

# 创建文件流，将各个章节读入内存
with open('E:\一念永恒.txt', 'w') as f:
    for dir in dirs:
        # 组合链接地址，即各个章节的地址
        url = root + dir
        # 有的时候访问某个网页会一直得不到响应，程序就会卡到那里，我让他0.6秒后自动超时而抛出异常
        while True:
            try:
                request = urllib.request.Request(url=url, headers=headers)
                with urllib.request.urlopen(request, timeout=0.6) as response:
                    html = response.read().decode('gbk')
                    break
            except:
                # 对于抓取到的异常，让程序停止1.1秒，再循环重新访问这个链接，访问成功时退出循环
                time.sleep(1.1)

        # 匹配文章标题
        title_req = re.compile(r'<h1>(.+?)</h1>')
        # 匹配文章内容，内容中有换行，所以使flags=re.S
        content_req = re.compile(r'<div id="content">(.+?)</div>', re.S, )
        # 获取标题
        title = title_req.findall(html)[0]
        # 获取内容
        content_test = content_req.findall(html)[0]
        # 筛除不需要的的html元素
        strc = content_test.replace('&nbsp;', ' ')
        content = strc.replace('<br />', '\n')
        print('抓取章节>' + title)
        f.write(title + '\n')
        f.write(content + '\n\n')
