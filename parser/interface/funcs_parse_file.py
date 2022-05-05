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

def show_shop_set_ver2(shop_id):
    data = session.query(Net_shops).filter_by(id = shop_id).one() # all
    json_dict = {}
    json_dict['shop_name'] = data.name
    json_dict['shop_id'] = shop_id
    json_dict['price'] = []
    json_dict['name'] = []
    json_dict['chars'] = []
    for settings in data.net_link_sett:
        temp_dict = {
        'tag_type': settings.tag_type,
        'tag_name': settings.tag_name,
        'attr_name': settings.attr_name,
        'attr_val': settings.attr_value,
        'tag_status': settings.sett_active,
        'tag_id': settings.id}
        json_dict[settings.tag_type] = temp_dict
    json_dict = json.dumps(json_dict)
    '''{"shop_name": "citilink",
    "shop_id": 1,
     "price": {}
     "name": {tag_name, attr_name, attr_val, tag_status, tag_id},
     "chars": {}}'''
    return json_dict

def show_settings_by_type(shop_id, tag_type):
    sql_query = session.query(Shops_sett).filter_by(id_main_page = shop_id, tag_type = tag_type).first()
    print(sql_query)
    my_dict = {}
    my_dict[tag_type] = [sql_query.tag_name, sql_query.attr_name, sql_query.attr_value, sql_query.sett_active, sql_query.id]
    json_dict = json.dumps(my_dict)
    # print(json_dict)
    return json_dict
# show_settings_by_type(1,'price')

def show_shop_set(shop_id):
    data = session.query(Net_shops).filter_by(id = shop_id).all()
    json_dict = {}
    for shop_name in data: # [1 магазин]
        main_page = shop_name.name
        sett_dict = {}
        for satts in shop_name.net_link_sett:
            sett_dict[satts.tag_type] = [satts.tag_name, satts.attr_name, satts.attr_value, satts.sett_active, satts.id]
    json_dict[main_page] = sett_dict
    json_dict = json.dumps(json_dict)
    '''{"main_page": {"price": ["div","class","price_tag_vals",False,"1"], "name": [], "chars": []}}'''
    return json_dict

def save_shop_set(shop_id, sett_dict):
    for tags_type in sett_dict:
        sett_list = sett_dict[tags_type]

        cur_data = Shops_sett(id_main_page = shop_id, tag_type = tags_type, tag_name = sett_list[0], attr_name = sett_list[1], attr_value = sett_list[2], sett_active = sett_list[3])
        session.add(cur_data)
        session.commit()

def save_shop_set_ver2(sett_dict):
    if "id" in sett_dict:
        session.query(Shops_sett).filter_by(id = sett_dict['id']).update({
        'id_main_page': sett_dict['id_main_page'],
        'tag_type': sett_dict['tag_type'],
        'tag_name': sett_dict['tag_name'],
        'attr_name': sett_dict['attr_name'],
        'attr_value': sett_dict['attr_value'],
        'sett_active': sett_dict['sett_active']
        })
    else:
        cur_data = Shops_sett(
        id_main_page = sett_dict['id_main_page'],
        tag_type = sett_dict['tag_type'],
        tag_name = sett_dict['tag_name'],
        attr_name = sett_dict['attr_name'],
        attr_value = sett_dict['attr_value'],
        sett_active = sett_dict['sett_active']
        )
        session.add(cur_data)
    session.commit()

def change_shop_set(string_data):
    py_dict_data = json.loads(string_data)
    print(py_dict_data)
    if len(py_dict_data) == 1:
        # в строке должен быть один ключ
        key = [key for key in py_dict_data]
        shop_set_id = key[0]
        shop_set_dict = {}
        shop_set_dict['id_main_page'] = py_dict_data[shop_set_id][4]
        shop_set_dict['tag_type'] = py_dict_data[shop_set_id][5]
        shop_set_dict['tag_name'] = py_dict_data[shop_set_id][0]
        shop_set_dict['attr_name'] = py_dict_data[shop_set_id][1]
        shop_set_dict['attr_value'] = py_dict_data[shop_set_id][2]
        shop_set_dict['sett_active'] = True
        if shop_set_id == "None":
            print("Создаем новую строку настроек")
        else:
            print(f"Перезаписываем строк с  id: {shop_set_id}")
            shop_set_dict['id'] = shop_set_id
        save_shop_set_ver2(shop_set_dict)
        return "succses"

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
