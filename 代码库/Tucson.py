import datetime
import pytz
import time
# 图森时区
Tucson_tz = pytz.timezone('US/Eastern')
 
# 获取图森当前时间
Tucson_time = datetime.datetime.now(Tucson_tz)
 
print(f"当前图森时间是: {Tucson_time}")
