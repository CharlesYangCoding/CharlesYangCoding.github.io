import datetime
import pytz
 
# 设置时区为北京时间
bj_timezone = pytz.timezone('Asia/Shanghai')
 
# 获取当前日期时间
bj_time = datetime.datetime.now(tz=bj_timezone)
 
print(bj_time)
