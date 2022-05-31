import openpyxl
import re
from funcs_parser import define_main_page, define_links

from sqlalchemy.orm import sessionmaker

import sys
sys.path.append('flask_funcs')
from sql_models import *

from flask import json

# Подключаемся к базе
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

excel_file_name = 'C:/Users/G.Tishchenko/Desktop/TEST.xlsx'

def parse_file_links(file_name):
    # ОТКРЫВАЕМ ФАЙЛ
    work_book = openpyxl.load_workbook(excel_file_name, read_only = True, data_only = True)
    # ВЫБИРАЕМ 1 ЛИСТ *
    active_sheet = work_book.worksheets[0]
    # НАХОДИМ СТОЛБЕЦ С СЫЛКАМИ **
    # ---
    # перебор Excel строк
    dict_links = {}
    for string_xlsx_row in active_sheet.rows:
        # находим все ссылки в строке excel
        list_links = define_links(string_xlsx_row[0].value)

        if list_links:
            for link in list_links:
                # проверяем ссылка ли это +...
                main_page = define_main_page(link)
                if main_page:
                    # заполняем словарь.
                    if main_page in dict_links:
                        dict_links[main_page].add(link)
                    else:
                        dict_links[main_page] = {link}
    return dict_links

# dict_links = parse_file_links(excel_file_name)
# counter = 0
# for set_l in dict_links:
    # counter += len(set_l)
# print(len(dict_links), counter)
# СОХРАНЯЕМ (CSV, SQL)

def save_dict_to_sql():
    # загружаем данные
    counter = 0
    for main_page in dict_links:
        counter += 1
        print(counter, main_page)
        # проверяем есть ли в БД искомый магазин
        data_quyrure = session.query(Net_shops).filter_by(name = main_page).all()
        if len(data_quyrure) == 0:
            cur_data = Net_shops(name = main_page)
            session.add(cur_data)
            session.commit()
            data_quyrure = session.query(Net_shops).filter_by(name = main_page).all()
            main_page_id = data_quyrure[0].id
        elif len(data_quyrure) == 1:
            main_page_id = data_quyrure[0].id
        else:
            print('Магазины задублились!')
            main_page_id = None
        for link in dict_links[main_page]:
            print(link, end ='\r')
            cur_data = Net_links(http_link = link, id_main_page = main_page_id)
            session.add(cur_data)
            session.commit()
        print()

def define_links(string_value):
    # возращает список с возможными сылками
    if not string_value  is None:
        re_sult = re.findall(r'[\w:/.\-?=&+%#\[\]]+', string_value)
        return re_sult
    else:
        return False
