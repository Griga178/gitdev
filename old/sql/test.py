'''
Вывод определенной части значений из словаря, с помощью списка
'''


import pickle

file_name = 'comp_info.pkl'

with open(file_name, 'rb') as f:
    pickle_set = pickle.load(f)


def inn_list():
    # создаем список ключей
    key_list = []
    for el in pickle_set:
        key_list.append(el)
    return key_list


# сколько надо вывести ключей
amount = 5

for el in key_list[:amount]:
    for jel in pickle_set[el]:
        print(jel, end = ' ')
