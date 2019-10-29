from datetime import datetime, timedelta
import time
import locale
import re
import enum

# time.struct_time(tm_year=2019, tm_mon=10, tm_mday=25, tm_hour=16, tm_min=27, tm_sec=3, tm_wday=4, tm_yday=298,
# tm_isdst=0)
localtime = time.localtime(time.time())
print(localtime)

# 日期转换为字符串
print(datetime.now())  # 2019-10-25 16:33:02.818177
print(datetime.now().date())
print(datetime.now().time())
print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))
print(str(datetime.now())[:19])

print(time.strftime('%Y-%m-%d %H:%M:%S'))
print(time.strftime("%Y-%m-%d", time.localtime()))
print()

# 字符串转换为日期
time_str = "2013-05-21 09:50:35"
time_inst = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
date_inst = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S").date()

print(time_inst)
print(date_inst)
print()

# 日期操作
# datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
today = datetime.today().date()
yesterday = today + timedelta(days=-1)
tomorrow = today + timedelta(days=1)
print(today, yesterday, tomorrow)
print((yesterday - tomorrow).days)
print((yesterday - tomorrow).total_seconds())
