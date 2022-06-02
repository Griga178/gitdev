import openpyxl
import re
# import sys
# sys.path.append('../../module_data_base')

from flask_funcs.module_data_base.query_for_parser import define_main_page, define_links


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

# задачи:
    # занести новые ккны - в БД
    # занести новые ссылки в БД
    # создать связи ккн - ссылка
    # создать связи файл - ссылка

# заносим файл в бд получаем id
example_d = {"kkn_name": {"link1", "link2"}, "kkn_name2": {"link3", "link4"}}
example_d_2 = {1: {"link1", "link2"}, 2: {"link3", "link4"}}
example_d_3 = {1: {1,2}, 2: {3, 4}}

# получаем id ккн-в
def check_kkn(kkn_list):
    kkn_id = 1
    d_out = {}
    for kkn in kkn_list:
        d_out[kkn] = kkn_id
        # d_out[kkn_id] = kkn
        kkn_id += 1
    return d_out
# меняем ключи в словаре
def raplace_kkn_name_kkn_id(in_dict, kkns_id):
    d_out = {}
    for kkn_name, links in in_dict:
        d_out[kkns_id[kkn_name]] = links



# получили словарь имен с id

# добавить множество ссылок в БД

# добавить ссылку в БД получить id

# добавить связь kkn_id, link_id
