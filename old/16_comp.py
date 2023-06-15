'''
Сравнение компаний
    из рабочей таблицы
    и
    из файлов со скриншотами
'''
import openpyxl
import os

# work_table_name = 'C:/Users/G.Tishchenko/Desktop/Общая_K.xlsx'
work_table_name = 'C:/Users/G.Tishchenko/Desktop/3 кв 23/3 Нормирование.xlsx'
# screnshot_folder_name = 'C:/Users/G.Tishchenko/Desktop/3 компьютеры/'
screnshot_folder_name = 'Z:/Тищенко Г.Л/3 кв 2023 скрины'

o_excel_companies = set()
e_excel_companies = set()
o_folder_companies = set()
e_folder_companies = set()

def open_excel(excel_file_name, sheet_number = 0):
    """возвращает генератор инф-и из excel """
    work_book = openpyxl.load_workbook(excel_file_name, read_only = True, data_only = True)
    active_sheet = work_book.worksheets[sheet_number]
    rows_generator = active_sheet.iter_rows(min_row = 2)
    return rows_generator

def read_excel(excel_gen):
    comp_name_clm_num = 17 # R столбец
    # price_clm_num = 21 # V столбец
    # price_clm_num = 20 # U столбец
    price_clm_num = 22 # W столбец
    type_of_price = 5 # F столбец
    for ex_row in excel_gen:
        if ex_row[price_clm_num].value:
            company_name = ex_row[comp_name_clm_num].value.replace('"', '').replace('«', '').replace('»', '')
            # print(ex_row[type_of_price].value[0])
            if ex_row[type_of_price].value[0] == 'О':
                o_excel_companies.add(company_name)
            elif ex_row[type_of_price].value[0] == 'Э':
                e_excel_companies.add(company_name)

def read_folder(screnshot_folder_name):
    e_fols_content = os.listdir(screnshot_folder_name + 'Ekranki')
    o_fols_content = os.listdir(screnshot_folder_name + 'Otveti')
    for el in e_fols_content:
        e_folder_companies.add(el)
    for el in o_fols_content:
        o_folder_companies.add(el)



excel_gen = open_excel(work_table_name)

read_excel(excel_gen)

read_folder(screnshot_folder_name)

otveti_diff = o_excel_companies - o_folder_companies
print(f'в папке нет Ответов: {len(otveti_diff)}')
print(otveti_diff)
ekranki_diff = e_excel_companies - e_folder_companies
print(f'в папке нет Экранок: {len(ekranki_diff)}')
print(ekranki_diff)
# print(e_excel_companies)
