''' сравнение скриншотов в папке со списком скриншотов в excel '''
import os


# csv_file_path = 'C:/Users/G.Tishchenko/Desktop/R_manual(19).csv'

# excel_file_name = 'C:/Users/G.Tishchenko/Desktop/2 кв 23/3 компьютерное.xlsx'
# screen_folder = 'C:/Users/G.Tishchenko/Desktop/3 компьютеры/'
# excel_file_name = 'C:/Users/G.Tishchenko/Desktop/2 кв 23/19 Бытовые приборы.xlsx'
# screen_folder = 'C:/Users/G.Tishchenko/Desktop/19 Быт/'
excel_file_name = 'C:/Users/G.Tishchenko/Desktop/2 кв 23/26 Оборудование для театрально.xlsx'
screen_folder = 'C:/Users/G.Tishchenko/Desktop/26 Театр/'

# screen_folder = 'Z:/Тищенко Г.Л/4 квартал Скриншоты/'

# excel_file_name = 'Z:/Тищенко Е.Ю/все скрины 4 кв 2022/'

sheet_name = 'Лист1'

scr_n = 21+2 # V столбец - X
prc_n = 22+2 # W столбец - Y
# scr_n = 20
# prc_n = 21 # если есть проверка на 160 тогда +3

        # КАТИНЫ ЧАСТИ
        # из файла реестра У меня 20 у кати 24/25
# excel_file_name = 'Z:/Тищенко Е.Ю/ЗАПЧАСТИ/2023/1 кв 2023/Часть 10. Запасные части для офисного оборудования.xlsx'
# excel_file_name = 'Z:/Тищенко Е.Ю/Часть 10. Запасные части для офисного оборудования.xlsx'
# excel_file_name = 'Z:/Тищенко Е.Ю/КАРТРИДЖИ/2023/Часть 11. Картриджи в реестр 1 кв 2023.xlsx'
# excel_file_name = 'C:/Users/G.Tishchenko/Desktop/Часть 11. Картриджи в реестр 1 кв 2023.xlsx'

# screen_folder = 'Z:/Тищенко Е.Ю/скрины/все скрины 1 кв 2023/запчасти/'
# screen_folder = 'Z:/Тищенко Е.Ю/скрины/все скрины 1 кв 2023/картриджи/'
# sheet_name = 'Реестр 1 кв 2023г'
# sheet_name = 'Лист1'
# sheet_name = 'Картриджи'
# scr_n = 24 # 24 = "Y"
# prc_n = 21 # 21 = "V"

# excel_file_name = 'Z:/Тищенко Е.Ю/КАРТРИДЖИ/2022/4 кв 2022 КАРТРИДЖИ/Копия 11 часть 3 квартал картирджи катино.xlsx'
# excel_file_name = 'C:/Users/G.Tishchenko/Desktop/Общая_K.xlsx'
# screen_folder = 'Z:/Тищенко Е.Ю/все скрины 4 кв 2022/'
# sheet_name = 'Лист1'
# scr_n = 27 #20
# prc_n = 24 # 19


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
