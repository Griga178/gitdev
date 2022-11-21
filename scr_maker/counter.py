from datetime import datetime, timedelta

def counter_gen(some_list, sleep_second):
    start_time = datetime.now()
    print("Начало", start_time.strftime("%H:%M:%S"))

    list_length = len(some_list)
    all_time = timedelta(seconds = sleep_second) * list_length

    counter = 0
    for el in range(list_length):
        counter += 1
        past_time = (datetime.now() - start_time)
        left_time = (all_time - past_time)
        str_past_time = (str(past_time)[2:7]).replace(":", " мин ") + " сек"
        str_left_time = (str(left_time)[2:7]).replace(":", " мин ") + " сек"
        yield f'{counter} / {list_length} Прошло: {str_past_time} / Осталось: {str_left_time}'
