''' сравнение скриншотов в папке со списком скриншотов в excel '''
import os
import sys


FILE_PATH = 'C:/Users/G.Tishchenko/Desktop/4 кв 2025/'
# SCREEN_PATH = 'Z:/Тищенко Г.Л/2025_4 Скрины/'
SCREEN_PATH = 'C:/Users/G.Tishchenko/Desktop/screenCap/'
scr_n, prc_n  = 24, 25

# еще поменять номера столбов строка: 29 --> 24 И 25

# part = '03. Оборудование '
# part = '26. Оборудование'
# part = '19. Бытовые'
part = '03. Нормирование'
split_part = part.split(" ")
part = " ".join(split_part[:2])

part_dict = {
    '3': "3 компьютерное",
    '26': '26 Оборудование для театрально',
    '19': '19 бытовые приборы',
    "n": "Нормирование"
}


if len(sys.argv) == 2:
    path_key = sys.argv[1]

    if path_key in part_dict:
        # print(part_dict[path_key])
        part = part_dict[path_key]

    else:
        print(f'ERROR PATH KEY (str19): {path_key}')
        quit()


FILE_NAME = f'{part}.xlsx'
SCREEN_FOLDER = part


excel_file_name = FILE_PATH + FILE_NAME
screen_folder = SCREEN_PATH + SCREEN_FOLDER

sheet_name = 'Лист1'

'''Номер скрина'''
# scr_n = 21+2 # V столбец - X
# scr_n = 20 # столбец - U
# scr_n = 24 # столбец - Y

'''Новая цена'''
# prc_n = 21  # столбец - V
# prc_n = 24  # столбец - Y
# prc_n = 25  # столбец - Z


folder_names = set()

            # - - - - - - - - - Чтение файлов - - - - - - - - -
def read_csv(csv_file_path):
    import csv
    csv_names = set()
    with open(csv_file_path) as file:
        data_reader = csv.reader(file, delimiter = ";")

        for line in data_reader:
            # print (line)
            if line[2] != '':
                csv_names.add(line[1])
    return csv_names

def read_excel(file_name):
    ''' Возвращает множество set() имен скринов с ценами из excel файла '''
    excel_set = set()
    import openpyxl

    wb = openpyxl.load_workbook(file_name, read_only = True, data_only = True)
    active_sheet = wb[sheet_name]

    for row in active_sheet.rows:

        screen_number = str(row[scr_n].value)
        # print(screen_number)
        try:
            # price_val = float(row[3].value)
            # print(price_val)
            price_val = float(row[prc_n].value)
        except:
            price_val = None

        if type(price_val) == float and price_val > 0:
            excel_set.add(screen_number)

    return excel_set

            # - - - - - - - - - Чтение содержимого папки - - - - - - - - -

fols_content = os.listdir(screen_folder)
# fols_content = os.listdir(screen_folder_2)

for fol_file in fols_content:
    if ".jpg" in fol_file:
        folder_names.add(fol_file.replace('.jpg', ''))

            # - - - - - - - - - Вывод результата - - - - - - - - -

# csv_names = read_csv(csv_file_path)
csv_names = read_excel(excel_file_name)

print(f'Количество в CSV/EXCEL: {len(csv_names)} шт.')
print(f'Количество в Папке: {len(folder_names)} шт.\n')

not_in_fol = csv_names - folder_names
not_in_csv = folder_names - csv_names

if not_in_fol:
    print(f'Не хватает в папке {len(not_in_fol)} шт.(м.б. лишние в excel)\n', not_in_fol)

if not_in_csv:
    print(f'Не хватает в csv/excel {len(not_in_csv)} шт.\n', not_in_csv)

if csv_names == folder_names:
    print('\nВсе ровно')
