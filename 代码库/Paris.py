import datetime
import pytz
import time
# 巴黎时区
paris_tz = pytz.timezone('Europe/Paris')
 
# 获取巴黎当前时间
paris_time = datetime.datetime.now(paris_tz)
 
print(f"当前巴黎时间是: {paris_time}")
