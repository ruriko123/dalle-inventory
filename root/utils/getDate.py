from datetime import datetime
import pytz


def getDate():
    my_date = datetime.now(pytz.timezone('Asia/Kathmandu')).strftime('%Y-%m-%d')
    return str(my_date)



def getDateTime():
    my_datetime = datetime.now(pytz.timezone('Asia/Kathmandu')).strftime('%Y-%m-%d %H:%M:%S')
    return str(my_datetime)