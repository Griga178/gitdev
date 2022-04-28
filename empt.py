'''
ХЗ ЧТО ТУТ ДОЛЖНО БЫТЬ ПУСТО!
'''


#global c

'''
# дозаписывает в файл csv значения
# елси файла нет, создает новый
import csv

csv_file_name = 'new_file2.csv'
with open(csv_file_name, mode = "a") as file:
    file_writer = csv.writer(file, delimiter = ";") #, lineterminator="\r"
    for i in range(10):
        file_writer.writerow([i, i*2, i**2])
        print(i)
'''


import pickle


def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)

dict1 = load_obj('our_kkn.pkl')
dict2 = load_obj('direct_kkn.pkl')

kkn_name = 'Принтер тип 1'

char = 'Суммарное количество встроенных в корпус портов USB 2.0 системного блока'

#print(dict1[kkn_name])

def print_kkn_dict(dict_name, search_keys = None):
    '''
    1 Обычный вывод словаря в консоль
    2 вывод определенного ключа или списка
    search_keys = {'множество'}
    '''
    count_kkn = 0
    count_char = 0

    if search_keys:
        work_keys = dict_name.keys() & search_keys
    else:
        work_keys = dict_name.keys()

    for key in work_keys:
        count_kkn += 1
        print(f"\n\n{count_kkn}. Наименование ККН: {key}\n")
        count_char = 0
        for value in dict_name[key]:
            count_char += 1
            if type(dict_name[key][value]) != list:
                pass
                print(f'    {count_char}. {value}: "{dict_name[key][value]}"')
            else:
                row = []
                for el in dict_name[key][value]:
                    if el:
                        row.append(el)
                print(f'    {count_char}. {value}: "{row}"')

se_val = {'Монитор, подключаемый к компьютеру тип 6'}
#print_kkn_dict(dict1, se_val) #, 'Ноутбук¹ тип 2'
#print_kkn_dict(dict2, se_val)
