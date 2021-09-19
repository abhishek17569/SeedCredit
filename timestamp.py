from datetime import datetime as dt

def timestamp():
    current_date_time = dt.now()
    time_stamp = current_date_time.strftime("%Y%m%d%H%M%S.%f")
    return time_stamp
# print(timestamp)

def timestamp_readable():
    current_date_time =  dt.now()
    time_stamp = current_date_time.strftime("%Y-%m-%d :: %H:%M:%S")
    return time_stamp

# print(timestamp_readable())

