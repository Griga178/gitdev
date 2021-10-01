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



#file = 'C:/Users/G.Tishchenko/Desktop/Аквариус.msg'

#print(file.split('/')[-1].replace('.msg', ''))

dict1 = {'Кабель-переходник для видеотехники тип 8': [3838, '26.20.40.190', '052', 'ШТ', {'Вид': [None, None, None, 'Переходsник', None], 'количество ячеейк': [0,0,'5',0]}, 'Кабели-переходники для видеотехники'],'Кабель-переходник для видеотехники тип 9': [3848, '26.20.40.190', '052', 'ШТ', {'Вид': [None, None, None, 'Переходник', None], 'количество ячеейк': [0,0,'5',0]}, 'Кабели-переходники для видеотехники']}

dict2 = {'Кабель-переходник для видеотехники тип 8': [3838, '26.20.40.190', '052', 'ШТ', {'Вид': [None, None, None, 'Переходник', None], 'количество ячеейк': [0,0,'5',0]}, 'Кабели-переходники для видеотехники']}

dict3 = {'Кабель-переходник для видеотехники тип 8': [3838, '26.20.40.190', '052', 'ШТ', {'Вид': [None, None, None, 'Переходник', None], 'количество ячеейк': [0,0,'5',0]}, 'Кабели-переходники для видеотехники'],'Кабель-переходник для видеотехники тип 9': [3845, '26.20.40.190', '052', 'ШТ', {'Вид': [None, None, None, 'Переходник', None], 'количество ячеейк': [0,0,'5',0]}, 'Кабели-переходники для видеотехники']}

data_db_keys = set(dict1.keys())

data_db_keys2 = set(dict2.keys())
data_db_keys3 = set(dict3.keys())

my_kkn_name = 'Кабель-переходник для видеотехники тип 8'

for kkn_name in data_db_keys:
    if my_kkn_name in dict1:
        #print(dict1[kkn_name])
        #print(dict3[kkn_name], '\n')
        for all_char_index in range(len(dict1[kkn_name])):
            if type(dict1[kkn_name][all_char_index]) != dict:
                if dict1[kkn_name][all_char_index] != dict3[kkn_name][all_char_index]:
                    print(f'В первом: {dict1[kkn_name][all_char_index]}, во втором: {dict3[kkn_name][all_char_index]}')




import openpyxl


name_my_file = 'C:/Users/G.Tishchenko/Desktop/sentember_fresh.xlsx'

def search_set(file_name):
    wb = openpyxl.load_workbook(file_name, read_only = True, data_only = True)
    active_sheet = wb['kategories']

    search_val = set()

    for row in active_sheet.rows: #
        # чтение ячеейк в строках и добавление в ""список строки"
        for cell in row[:1]:
            #print(cell.value)

            search_val.update({cell.value})
    return search_val

#print(search_set(name_my_file))
