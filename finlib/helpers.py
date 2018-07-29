import time

def totimestamp(dt):
    return int(time.mktime(dt.timetuple()))

