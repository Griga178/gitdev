max_days_list = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31] #, 31, 30, 31

mounth_count = 1

year_str = '2021'

days_list = []

for month in max_days_list:
    if len(str(mounth_count)) >= 2:
        monthe = str(mounth_count)
    else:
        monthe = '0' + str(mounth_count)
    #print(f'\n The end of {monthe}! \n')
    mounth_count += 1

    for day in range(month):

        if len(str(day + 1)) >= 2:
            day_str = str(day + 1)
        else:
            day_str = '0' + str(day + 1)

        #print(day_str, end = '|')
        days_list.append(f'{day_str}.{monthe}.{year_str}')
        #print(f'{day_str}.{monthe}.{year_str}')
'''
step = 3
day_index = 0
print(len(days_list))
for el in days_list[::step]:
    day_from = el
    if day_index < 365 - step:
        day_to = days_list[day_index + step]
        print(day_from, day_to)
        day_index += step

print(day_to, days_list[-1])
'''
some_text = float('1001')


# Выводит нужные даты если не подходит, то "до" уменьшается на 1 день как
first_value = 20
step = first_value
day_index = 0

while day_index < len(days_list) - step:
    pre_index = day_index
    day_from = days_list[day_index]
    day_index += step
    day_to =  days_list[day_index]

    print(day_from, day_to)
    some_text = int(input('Значение:   '))
    if some_text > 1000:
        day_index = pre_index
        step -= 1
    else:
        step = first_value
        
print(day_to, days_list[-1])
