import os
import openpyxl

'''
МЕНЯЕМ НАЗВАНИЕ ФАЙЛОВ ПО СПИСКУ
'''

NAME_EXCEL = 'C:/Users/G.Tishchenko/Desktop/Ответы.xlsx'
NAME_EXCEL_LIST = 'Переименовать'
NAME_FILE_FOLDER = 'C:/Users/G.Tishchenko/Desktop/screens_4_norm/'

list_changing = []

def read_excel(excel_file):
    # ИЗ EXCEL БЕРЕМ СТАРОЕ - НОВОЕ ИМЯ
    wb = openpyxl.load_workbook(excel_file, read_only = True, data_only = True)
    active_sheet = wb[NAME_EXCEL_LIST]

    for row in active_sheet.rows:
        old_name = row[0].value
        new_name = row[1].value

        list_changing.append([str(old_name) + '.jpg', str(new_name) + '.jpg'])

def change_name(names_list):
    # ДОБАВЛЯЕМ ПУТЬ - МЕНЯЕМ
    for name in names_list:
        os.rename(NAME_FILE_FOLDER + name[0], NAME_FILE_FOLDER + name[1])

    print('Вроде, все!')

read_excel(NAME_EXCEL)

print("Кол-во меняемых файлов:", len(list_changing))

change_name(list_changing)
