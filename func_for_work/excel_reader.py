from settings import desktop_path
from common_funcs import define_links, define_main_page

file_name = desktop_path + 'Нормирование.xlsx'

import openpyxl

def open_excel(excel_file_name, sheet_number = 0):
    """возвращает генератор инф-и из excel """
    work_book = openpyxl.load_workbook(excel_file_name, read_only = True, data_only = True)
    active_sheet = work_book.worksheets[sheet_number]
    rows_generator = active_sheet.iter_rows(min_row = 2)
    return rows_generator

# читаем excel - рабочую таблицу
def read_work_table(excel_file_name):
    ''' Создает:
        словарь компаний,
        список ссылок
        '''
    rows_generator = open_excel(excel_file_name)
    # номера столбцов (-1)
    comp_inn_clm_num = 16
    comp_name_clm_num = 17
    links_clm_num = 18
    link_num_clm_num = 20

    dict_information = {}
    list_links = []

    for string_xlsx_row in rows_generator:

        comp_inn = string_xlsx_row[comp_inn_clm_num].value
        comp_name = string_xlsx_row[comp_name_clm_num].value
        link_num = string_xlsx_row[link_num_clm_num].value
        links_list = define_links(string_xlsx_row[links_clm_num].value)

        main_page_set = set()

        # сощдание словаря компаний
        if links_list:
            for link in links_list:
                main_page = define_main_page(link)
                main_page_set.add(main_page)
        else:
            print(f"№ {link_num} - пропускаем")
            continue

        if "zakupki.gov.ru" in main_page_set:
            # Эти сайты не обрабатываем
            continue

        if comp_inn:
            if comp_inn in dict_information:
                dict_information[comp_inn]["main_pages"] = dict_information[comp_inn]["main_pages"] | main_page_set
                if dict_information[comp_inn]["comp_name"] != comp_name:
                    print(f"Не совпадает {comp_inn}: {comp_name}")

            else:
                dict_information[comp_inn] = {"comp_name": comp_name, "main_pages": main_page_set}

        # Создание списка ссылок
        if len(links_list) > 1:
            cntr = 1
            for link in links_list:
                list_links.append([f"{link_num}_0{cntr}", links_list[0]])
                cntr += 1
        else:
            list_links.append([str(link_num), links_list[0]])

    return dict_information, list_links
