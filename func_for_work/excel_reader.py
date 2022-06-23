from settings import desktop_path
from common_funcs import define_links, define_main_page

file_name = desktop_path + 'Нормирование.xlsx'

import openpyxl

# читаем excel - рабочую таблицу
def read_work_table(excel_file_name):

    work_list = []

    work_book = openpyxl.load_workbook(excel_file_name, read_only = True, data_only = True)

    # active_sheet = wb[sheet_name]
    active_sheet = work_book.worksheets[0]

    # номера столбцов (-1)
    comp_inn_clm_num = 16
    comp_name_clm_num = 17
    links_clm_num = 18
    link_num_clm_num = 20

    information_dict = {}
    file_links = []

    for string_xlsx_row in active_sheet.iter_rows(min_row = 2):

        comp_inn = string_xlsx_row[comp_inn_clm_num].value
        comp_name = string_xlsx_row[comp_name_clm_num].value
        link_num = string_xlsx_row[link_num_clm_num].value
        links_list = define_links(string_xlsx_row[links_clm_num].value)

        main_page_set = set()

        if links_list:
            for link in links_list:
                main_page = define_main_page(link)
                main_page_set.add(main_page)
        else:
            continue

        if "zakupki.gov.ru" in main_page_set:
            # print(link_num, comp_name)
            continue

        if len(links_list) > 1:
            cntr = 1
            for link in links_list:
                file_links.append([f"{link_num}_0{cntr}", links_list[0]])
                cntr += 1
        else:
            file_links.append([str(link_num), links_list[0]])


        if comp_inn:
            if comp_inn in information_dict:
                information_dict[comp_inn]["main_pages"] = information_dict[comp_inn]["main_pages"] | main_page_set
                if information_dict[comp_inn]["comp_name"] != comp_name:
                    print(f"Не совпадает {comp_inn}: {comp_name}")

            else:
                information_dict[comp_inn] = {"comp_name": comp_name, "main_pages": main_page_set}


    return information_dict, file_links

# res_d = read_work_table(file_name)
#
# print(res_d)

'''
Сценарий:
    открытие документа

    перебор каждой строки (инн имя ссылки номер_ссылки)
        перебор ссылок внутри ячейки => список ссылок (от 0 до ...)

        если список ссылок больше 1:
            то для последующих создаем доп номер
            цикл
                [номер, главная страница, ссылка]
        иначе если список не пуст:
            [номер, главная страница, ссылка]

        создать словарь источников


'''
