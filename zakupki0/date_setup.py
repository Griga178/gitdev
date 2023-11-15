# from settings import START_DATE, END_DATE
from re import findall
from datetime import datetime, timedelta
from convert import string_to_datetime



def get_days(START_DATE, END_DATE = False):
    '''
        Формируем список из дат ОТ START_DATE до END_DATE(now)
    '''
    start_datetime = string_to_datetime(START_DATE)

    if END_DATE:
        end_datetime = string_to_datetime(END_DATE)
    else:
        end_datetime = datetime.now()

    days_list = []

    for i in range((end_datetime - start_datetime).days):
        days_list.append(start_datetime.strftime('%d.%m.%Y'))
        start_datetime = start_datetime + timedelta(days = 1)
    else:
        days_list.append(start_datetime.strftime('%d.%m.%Y'))

    return days_list
