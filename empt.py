def manual_cicle():
    for el in range(100):
        print(el)
        a = input('Ввод: ')
        if a == 's':
            break
#manual_cicle()

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
#dict1 = load_obj('aic_dict.pkl')

kkn_name = 'Рабочая станция¹ тип 1'

char = 'Суммарное количество встроенных в корпус портов USB 2.0 системного блока'

#print(dict1[kkn_name])
for jey in dict1.keys():
    print(" - - -  - - - - - - - -  - - - - - -", jey)
    for el in dict1[jey]:
        print(el)
        print(dict1[jey][el])
