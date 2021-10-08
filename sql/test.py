max_days_list = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31] #, 31, 30, 31
mounth_count = 1
year_str = '2021'
days_list = []
for month in max_days_list:
    if len(str(mounth_count)) >= 2:
        monthe = str(mounth_count)
    else:
        monthe = '0' + str(mounth_count)
    mounth_count += 1
    for day in range(month):
        if len(str(day + 1)) >= 2:
            day_str = str(day + 1)
        else:
            day_str = '0' + str(day + 1)
        days_list.append(f'{day_str}.{monthe}.{year_str}')



# Выводит нужные даты если не подходит, то "до" уменьшается на 1 день
first_value = 30
step = first_value

day_index = 0

sum_kontrakts = 0
period = 0

while day_index < len(days_list):

    pre_index = day_index # что бы переписать даты

    day_from = days_list[day_index]
    day_index += step

    if day_index >= len(days_list):
        day_index = len(days_list) - 1

    day_to =  days_list[day_index]
    day_index += 1

    print(day_from, day_to)
    # функция обновления страницы с датами
    # и чтение кол-ва

    some_text = int(input('Значение:   '))

    if some_text > 1000:
        day_index = pre_index
        step -= 1
    else:
        #  парсим - сохраняем
        period = day_index - pre_index
        print(f'Скачали: {some_text} шт. за период {period} дн.')
        sum_kontrakts += some_text
        print(f'Всего скачано: {sum_kontrakts} шт.')

        step = first_value
