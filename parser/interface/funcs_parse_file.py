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


# save_dict_to_sql()
#
# data_quyrure = session.query(Net_links).all()
# print(len(data_quyrure))
# for el in data_quyrure:
#     print(el.id, el.net_shops.name)

def show_shop_set(shop_id):
    # запрос всех настроек по id сайта
    data = session.query(Net_shops).filter_by(id = shop_id).all()
    json_dict = {}
    for shop_name in data: # [1 магазин]
        main_page = shop_name.name
        sett_dict = {}
        for satts in shop_name.net_link_sett:
            sett_dict[satts.tag_type] = [satts.tag_name, satts.attr_name, satts.attr_value, satts.sett_active, satts.id]
    json_dict[main_page] = sett_dict
    json_dict = json.dumps(json_dict)
    return json_dict


def save_shop_set(shop_id, sett_dict):
    for tags_type in sett_dict:
        sett_list = sett_dict[tags_type]

        cur_data = Shops_sett(id_main_page = shop_id, tag_type = tags_type, tag_name = sett_list[0], attr_name = sett_list[1], attr_value = sett_list[2], sett_active = sett_list[3])
        session.add(cur_data)
        session.commit()

def del_shop_set(set_id = False):
    if set_id:
        id_of_del = session.query(Shops_sett).filter_by(id = set_id).one()
        session.delete(id_of_del)
        session.commit()
    query_l = session.query(Shops_sett).all()
    for el in query_l:
        print(el.id, el.net_shops.name, el.sett_active)

def show_our_shops():
    main_page_list = session.query(Net_shops).all()
    dict_m_p = {}
    for el in main_page_list:
        dict_m_p[el.id] = el.name
    dict_m_p = json.dumps(dict_m_p)
    return dict_m_p
# save_shop_set(2, {"price": ['div', 'class', 'price', 1]})
# save_shop_set(1, {"name": ['div', 'class', 'name', 0]})
# save_shop_set(1, {"chars": ['div', 'class', 'name', 0]})
# show_shop_set(1)

# del_shop_set()
