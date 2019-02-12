import time

if __name__ == '__main__':
    timestamp = time.time()
    print('timestamp = ', timestamp)
    localtime = time.localtime(time.time())
    print('localtime = ', localtime)
    print('year = ', localtime.tm_year)  # 年
    print('month = ', localtime.tm_mon)  # 月
    print('day = ', localtime.tm_yday)  # 日
    print('hour = ', localtime.tm_hour)  # 时
    print('minute = ', localtime.tm_min)  # 分
    print('second = ', localtime.tm_sec)  # 秒
    print('wday = ', localtime.tm_wday)  # 星期几，从0开始
    print('format = ',time.strftime("%Y-%m-%d %H:%M:%S", localtime))
