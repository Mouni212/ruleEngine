from datetime import datetime, timedelta


def modify_date_time(before_time):
    word_list = before_time.split('_')
    day = word_list[0][:-1]
    hour = word_list[1][:-1]
    minute = word_list[2][:-1]
    second = word_list[3][:-1]
    query_date_time = datetime.today()- timedelta(days = int(day), hours = int(hour), minutes = int(minute), seconds = int(second))
    return query_date_time