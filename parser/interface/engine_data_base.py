from flask import json

import sys
sys.path.append('flask_funcs')

from sql_models import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def define_main_page(link):
    '''
    Определение главной страницы из строки
    '''
    if type(link) == str:
        split_list = link.split("/")
        h_protocol = split_list[0]
        try:
            main_page = split_list[2]
        except:
            main_page = ''
        if 'http' or 'ftp' in h_protocol:
            return main_page
        else:
            print('ERROR: не похоже на ссылку')
            return False
    else:
        print('ERROR: ссылка не в формате строки')
        return False

def check_links_in_db(link = False, link_id = False):
    ''' Проверка есть ли ссылка в БД'''
    result_dict = {}
    try:
        if link:
            link_from_bd = session.query(Net_links).filter_by(http_link = link).one()
        elif link_id:
            link_from_bd = session.query(Net_links).filter_by(id = link_id).one()
        result_dict['links'] = {}
        result_dict['links'][link_from_bd.id] = link_from_bd.http_link
        result_dict['main_page_id'] = link_from_bd.id_main_page
        result_dict['main_page'] = link_from_bd.net_shops.name
        return result_dict
    except NoResultFound:
        return False

def check_main_page_in_db(main_page):
    ''' Проверка есть ли Сайт в БД'''
    result_dict = {}
    try:
        main_page_from_bd = session.query(Net_shops).filter_by(name = main_page).one()
        result_dict['main_page_id'] = main_page_from_bd.id
    except NoResultFound:
        new_main_page = Net_shops(name = main_page)
        session.add(new_main_page)
        session.commit()
        search_result = session.query(Net_shops).filter_by(name = main_page).one()
        result_dict['main_page_id'] = search_result.id
    return result_dict

def add_new_link_to_db(link):
    '''Добавляем ссылку в БД, если нет главной страницы,
    то добавляем и ее - так же связываем'''
    main_page = define_main_page(link)
    result_dict = check_main_page_in_db(main_page)

    link_checker = check_links_in_db(link)
    if not link_checker:
        cur_data = Net_links(
        id_main_page = result_dict['main_page_id'],
        http_link = link)
        session.add(cur_data)
        session.commit()

    one_link = session.query(Net_links).filter_by(http_link = link).one()
    result_dict['links'] = {}
    result_dict['links'][one_link.id] = one_link.http_link

    return result_dict

def check_sett_to_parse(result_dict):

    '''dict{link_id, http_link, main_page_id}'''
    sett_query = session.query(Shops_sett).filter_by(id_main_page = result_dict['main_page_id']).all()
    for sett in sett_query:
        result_dict[sett.tag_type] = {'tag_name': sett.tag_name, 'attr_name': sett.attr_name, 'attr_value': sett.attr_value}
    return result_dict

# СМОТРИМ НАСТРОЙКИ ТЕГОВ
tags_types = {"price": "Цена", "name": "Название", "chars": "Характеристика"}
def show_shop_set_ver2(shop_id):
    data = session.query(Net_shops).filter_by(id = shop_id).one()
    json_dict = {}
    json_dict['shop_name'] = data.name
    # json_dict['shop_id'] = shop_id
    json_dict['price'] = {'tag_type': "price", 'rus_tag': "Цена", 'shop_id': shop_id, 'tag_id': False, 'tag_name': "", 'attr_name': "", 'attr_val': ""}
    json_dict['name'] = {'tag_type': "name", 'rus_tag': "Название", 'shop_id': shop_id, 'tag_id': False, 'tag_name': "", 'attr_name': "", 'attr_val': ""}
    json_dict['chars'] = {'tag_type': "chars", 'rus_tag': "Характеристика", 'shop_id': shop_id, 'tag_id': False, 'tag_name': "", 'attr_name': "", 'attr_val': ""}
    for settings in data.net_link_sett:
        temp_dict = {
        'rus_tag': tags_types[settings.tag_type],
        'tag_type': settings.tag_type,
        'shop_id': shop_id,
        'tag_name': settings.tag_name,
        'attr_name': settings.attr_name,
        'attr_val': settings.attr_value,
        'tag_status': settings.sett_active,
        'tag_id': settings.id}
        json_dict[settings.tag_type] = temp_dict
    json_dict = json.dumps(json_dict)
    return json_dict
# СМОТРИМ НАСТРОЙКИ ТЕГОВ
def show_settings_by_type(shop_id, tag_type):
    sql_query = session.query(Shops_sett).filter_by(id_main_page = shop_id, tag_type = tag_type).first()
    my_dict = {}
    my_dict['tag_id'] = sql_query.id
    my_dict['tag_name'] = sql_query.tag_name
    my_dict['attr_name'] = sql_query.attr_name
    my_dict['attr_val'] = sql_query.attr_value
    my_dict['shop_id'] = sql_query.id_main_page
    my_dict['tag_type'] = sql_query.tag_type
    my_dict['rus_tag'] = tags_types[sql_query.tag_type]
    json_dict = json.dumps(my_dict)
    return json_dict
# показать 3 ссылки
def show_few_links_sql(shop_id):
    sql_query = session.query(Net_links).filter_by(id_main_page = shop_id).limit(3)
    link_dict = {}
    for link in sql_query:
        link_dict[link.id] = link.http_link
    json_dict = json.dumps(link_dict)
    return json_dict
# Удалить настройки
def delete_setting(string_data):
    py_dict_data = json.loads(string_data)
    id_of_del = session.query(Shops_sett).filter_by(id = py_dict_data["tag_id"]).one()
    session.delete(id_of_del)
    session.commit()
    py_dict_data['tag_name'] = ''
    py_dict_data['attr_name'] = ''
    py_dict_data['attr_val'] = ''
    py_dict_data['tag_id'] = False
    answer = json.dumps(py_dict_data)
    return answer
# Показать все магазины
def show_our_shops():
    main_page_list = session.query(Net_shops).all()
    dict_m_p = {}
    for el in main_page_list:
        dict_m_p[el.id] = el.name
    dict_m_p = json.dumps(dict_m_p)
    return dict_m_p
# Изменяем текущие настройки
def take_post_message(string_data):
    py_dict_data = json.loads(string_data)
    if py_dict_data["tag_id"]:
        # Изменяем старые настройки
        answer = change_current_settings(py_dict_data)
    else:
        # Создаем новые настройки
        answer = create_settings(py_dict_data)
    return answer

def change_current_settings(js_dict):
    session.query(Shops_sett).filter_by(id = js_dict['tag_id']).update({
    'tag_name': js_dict['tag_name'],
    'attr_name': js_dict['attr_name'],
    'attr_value': js_dict['attr_val'],
    'sett_active': js_dict['tag_status']
    })
    session.commit()
    answer = show_settings_by_type(js_dict['shop_id'], js_dict['tag_type'])
    return answer

def create_settings(js_dict):
    cur_data = Shops_sett(
    id_main_page = js_dict['shop_id'],
    tag_type = js_dict['tag_type'],
    tag_name = js_dict['tag_name'],
    attr_name = js_dict['attr_name'],
    attr_value = js_dict['attr_val'],
    sett_active = js_dict['tag_status']
    )
    session.add(cur_data)
    session.commit()

    answer = show_settings_by_type(js_dict['shop_id'], js_dict['tag_type'])
    return answer
