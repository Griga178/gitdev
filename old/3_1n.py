'''
После проверки скринов (удаления без цен и проч.)
удаление строк из excel
'''

import os

# Создание списка, в котором содержаться название скриншотов из папки
dir_for_screen = 'C:/Users/G.Tishchenko/Desktop/screens_2_2022/'
folder_content = os.listdir(dir_for_screen)

#print(len(folder_content))

def list_of_dirs_names(dir_fold):
    ''' Создать список из файлов, имена которых полностью состоят из
        целых чисел
    '''
    list_of_numbers = []
    for full_file_name in dir_fold:

        file_name = full_file_name.split(".")[0]
        if "_" in file_name:
            file_name = full_file_name.split("_")[0] # для тех у кого цена после номера
        #print(file_name)
        try:
            file_name = int(file_name)
            list_of_numbers.append(file_name)
        except:
            pass
            #print("Not Integer")
    return list_of_numbers

def iter_to_csv(iter_name):
    ''' Запись любой последовательности в файл '''
    file_name = dir_for_screen + "scr_names.csv"
    with open(file_name, 'w') as file:
        for row in iter_name:
            file.write(f'{row}\n') # для записи всего

#iter_to_csv(list_of_dirs_names(folder_content))

import openpyxl

def create_dict():
    ''' Создаем словарь из номера и цены '''
    file_with_prices = 'C:/Users/G.Tishchenko/Desktop/prices.xlsx'

    wb = openpyxl.load_workbook(file_with_prices, read_only = True, data_only = True)
    active_sheet = wb['Лист1']

    dict = {}
    for row in active_sheet.rows: #
        # чтение ячеейк в строках и добавление в ""список строки"
        price, number = str(row[0].value), str(row[1].value)
        dict.update({number: price})
        #print(price, number)
    return dict

#print(len(create_dict()))
def rename_screens():
    for number in create_dict():
        #print(number)
        file_oldname = dir_for_screen + number + '.jpg'
        new_name = dir_for_screen + number + f'_{create_dict()[number]}'+ '.jpg'
        os.rename(file_oldname, new_name)

def rename_any(folder):
    ''' Убрать из названия все что за _'''
    names_list = os.listdir(folder)
    for old_name in names_list:
        part_new_name = old_name.split(".")[0]
        part_new_name = part_new_name.split("_")[0]
        new_name = folder + '/' + part_new_name + '.jpg'
        os.rename(folder + '/' + old_name, new_name)
