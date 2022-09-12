''' сравнение скриншотов в папке со списком скриншотов в excel '''
import os


# csv_file_path = 'C:/Users/G.Tishchenko/Desktop/R_manual(19).csv'
# excel_file_name = 'C:/Users/G.Tishchenko/Desktop/26p_4.xlsx'
# screen_folder = 'C:/Users/G.Tishchenko/Desktop/screens_4_26/'

# excel_file_name = 'Z:/Тищенко Е.Ю/screens_4_cat/prices3.xlsx'

# sheet_name = 'main'
# scr_n = 20
# prc_n = 21

        # КАТИНЫ ЧАСТИ
# excel_file_name = 'Z:/Тищенко Е.Ю/ЗАПЧАСТИ/2022/4 кв 2022 ЗАПЧАСТИ/Копия 10. Запасные части для офисного оборудования -4 кв 2022 катина.xlsx'
# screen_folder = 'Z:/Тищенко Е.Ю/screens_4_запч/'
# sheet_name = 'Реестр 3 кв 2022'
# scr_n = 24
# prc_n = 20

excel_file_name = 'Z:/Тищенко Е.Ю/КАРТРИДЖИ/2022/4 кв 2022 КАРТРИДЖИ/Копия 11 часть 3 квартал картирджи катино.xlsx'
screen_folder = 'Z:/Тищенко Е.Ю/screens_4_картр/'
sheet_name = 'Лист1'
scr_n = 25
prc_n = 20


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
        # screen_number = str(row[1].value)
        screen_number = str(row[scr_n].value) # из файла реестра У меня 20 у кати 24/25
        # print(screen_number)

        # price_val = (row[17].value)

        try:
            # price_val = float(row[3].value)
            price_val = float(row[prc_n].value) # из файла реестра У меня 21 у кати 20
            # print(price_val)
        except:
            price_val = None

        if type(price_val) == float and price_val > 0:
            excel_set.add(screen_number)

    return excel_set

            # - - - - - - - - - Чтение содержимого папки - - - - - - - - -

fols_content = os.listdir(screen_folder)

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
    print(f'Не хватает в папке {len(not_in_fol)} шт.\n', not_in_fol)

if not_in_csv:
    print(f'Не хватает в csv/excel {len(not_in_csv)} шт.\n', not_in_csv)

if csv_names == folder_names:
    print('\nВсе ровно')
