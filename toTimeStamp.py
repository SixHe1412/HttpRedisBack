import time


def transToStamp(iTime):

    timeArray = time.strptime(iTime, "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(timeArray)
    base_timeArray = time.strptime("2005-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    base_timestamp = time.mktime(base_timeArray)
    t_stamp =  str(int(timestamp - base_timestamp))

    return t_stamp