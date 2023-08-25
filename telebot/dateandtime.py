from datetime import datetime

def find_time():
    tim = datetime.now()
    format = tim.strftime("%H:%M:%S")
    return format

def find_date():
    date = datetime.now()
    year = date.strftime("%Y")
    month = date.strftime("%m")
    day = date.strftime("%d")
    out=day+"-"+month+"-"+year
    return out