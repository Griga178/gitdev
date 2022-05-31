import openpyxl
import re
# import sys
# sys.path.append('../../module_data_base')

# from query_for_parser import define_main_page, define_links
def define_main_page():
    pass
def define_links():
    pass

def parse_file_links(file_name):
    # ОТКРЫВАЕМ ФАЙЛ
    work_book = openpyxl.load_workbook(file_name, read_only = True, data_only = True)
    # ВЫБИРАЕМ 1 ЛИСТ *
    active_sheet = work_book.worksheets[0]
    # НАХОДИМ СТОЛБЕЦ С СЫЛКАМИ **
    # ---
    # перебор Excel строк
    links_column_number = 19 - 1
    kkn_name_column_number = 3 - 1
    output_dict = {}
    for string_xlsx_row in active_sheet.iter_rows(min_row = 2):
        # находим все ссылки в строке excel
        list_links = define_links(string_xlsx_row[links_column_number].value)
        kkn_name = string_xlsx_row[kkn_name_column_number].value

        if kkn_name:
            current_kkn = kkn_name
            # ДЛЯ ККН-ов без ссылок
            output_dict[current_kkn] = set()



        if list_links:
            for link in list_links:
                # проверяем ссылка ли это +...
                main_page = define_main_page(link)
                if main_page:
                    # заполняем словарь.
                    if current_kkn in output_dict:
                        output_dict[current_kkn].add(link)
                    else:
                        output_dict[current_kkn] = {link}
    # # return dict_links
    for kkn in output_dict:
        print(kkn)
        print(output_dict[kkn])
    print(len(output_dict))

# вывод
# test_file_name = 'C:/Users/G.Tishchenko/Desktop/26 Театр.xlsx'

# parse_file_links(test_file_name)
