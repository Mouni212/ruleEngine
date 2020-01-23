from datetime import datetime, timedelta

from common import exceptions


def modify_date_time(before_time):
    word_list = before_time.split('_')
    if len(word_list) is not 4:
        raise exceptions.InvalidException("Invalid data_time format")
    day = word_list[0][:-1]
    hour = word_list[1][:-1]
    minute = word_list[2][:-1]
    second = word_list[3][:-1]
    query_date_time = datetime.today()- timedelta(days = int(day), hours = int(hour), minutes = int(minute), seconds = int(second))
    return query_date_time


def total_seconds(frequency):
    freq_split = frequency.split('_')
    if len(freq_split) is not 4:
        raise exceptions.InvalidException("Invalid Format")
    days = int(freq_split[0][:-1])
    hours = int(freq_split[1][:-1])
    minutes = int(freq_split[2][:-1])
    seconds = int(freq_split[3][:-1])
    total_seconds = seconds + (minutes*60) + (hours*60*60) + (days*24*60*60)
    return total_seconds
