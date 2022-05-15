from flask import json

import sys
sys.path.append('flask_funcs')

from sql_models import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# ВЫВОД СПИСКА МАГАЗИНОВ
def show_list_shops():
    ''' Возвращает:
        {1:{"shop_name":"www.onlinetrade.ru",
            "price":True, "name":True},
        2:{...},...}'''
    main_page_list = session.query(Net_shops).all()
    output_dict = {}
    tags_types = ['price', 'name', 'chars']
    for row in main_page_list:
        output_dict[row.id] = {}
        output_dict[row.id]['shop_name'] = row.name
        settings_rows = row.net_link_sett
        if settings_rows:
            for sett_row in settings_rows:
                if sett_row.tag_type in tags_types:
                    output_dict[row.id][sett_row.tag_type] = True
    json_dict = json.dumps(output_dict)
    return json_dict

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

        result_dict['link_id'] = link_from_bd.id
        result_dict['link'] = link_from_bd.http_link
        result_dict['shop_id'] = link_from_bd.id_main_page
        result_dict['shop_name'] = link_from_bd.net_shops.name
        # result_dict['current_price'] = link_from_bd.current_price
        # result_dict['current_name'] = link_from_bd.current_name
        # result_dict['current_date'] = link_from_bd.current_date
        result_dict['need_selenium'] = True #link_from_bd.net_shops.need_selenium

        return result_dict
    except NoResultFound:
        return False

def check_main_page_in_db(main_page):
    ''' Проверка есть ли Сайт в БД - нет: создать'''
    try:
        main_page_from_bd = session.query(Net_shops).filter_by(name = main_page).one()
        result = main_page_from_bd.id
    except NoResultFound:
        new_main_page = Net_shops(name = main_page) #need_selenium = True
        session.add(new_main_page)
        session.commit()
        search_result = session.query(Net_shops).filter_by(name = main_page).one()
        result = search_result.id
    return result

def add_new_link_to_db(link):
    '''Добавляем ссылку в БД, если нет главной страницы,
    то добавляем и ее - так же связываем'''
    main_page = define_main_page(link)
    main_page_id = check_main_page_in_db(main_page)
    cur_data = Net_links(id_main_page = main_page_id, http_link = link)
    session.add(cur_data)
    session.commit()
    registred_link = session.query(Net_links).filter_by(http_link = link).one()
    link_id = registred_link.id
    return link_id

def check_sett_to_parse(result_dict):

    '''dict{link_id, http_link, main_page_id1, main_page_id2}'''
    sett_query = session.query(Shops_sett).filter_by(id_main_page = result_dict['main_page_id']).all()
    for sett in sett_query:
        result_dict[sett.tag_type] = {'tag_name': sett.tag_name, 'attr_name': sett.attr_name, 'attr_value': sett.attr_value}
    return result_dict

# СМОТРИМ НАСТРОЙКИ ТЕГОВ
def show_shop_sett(shop_id):
    data = session.query(Net_shops).filter_by(id = shop_id).one()
    json_dict = {}
    json_dict['shop_name'] = data.name
    # json_dict['shop_id'] = shop_id
    json_dict['price'] = {'tag_type': "price", 'rus_tag': "Цена", 'shop_id': shop_id, 'tag_id': False, 'tag_name': "", 'attr_name': "", 'attr_val': ""}
    json_dict['name'] = {'tag_type': "name", 'rus_tag': "Название", 'shop_id': shop_id, 'tag_id': False, 'tag_name': "", 'attr_name': "", 'attr_val': ""}
    json_dict['chars'] = {'tag_type': "chars", 'rus_tag': "Характеристика", 'shop_id': shop_id, 'tag_id': False, 'tag_name': "", 'attr_name': "", 'attr_val': ""}
    json_dict['use_selenium'] = True #data.selenium_used
    for settings in data.net_link_sett:
        json_dict[settings.tag_type] = show_settings_by_type(shop_id, settings.tag_type)
    json_dict = json.dumps(json_dict)
    return json_dict

# ВЫВОДИ НАСТРОЙКИ ТЕГОВ ПО ТИПУ
def show_settings_by_type(shop_id, tag_type):
    tags_types = {"price": "Цена", "name": "Название", "chars": "Характеристика"}
    try:
        sql_query = session.query(Shops_sett).filter_by(id_main_page = shop_id, tag_type = tag_type).one()
        my_dict = {}
        my_dict['tag_id'] = sql_query.id
        my_dict['tag_name'] = sql_query.tag_name
        my_dict['attr_name'] = sql_query.attr_name
        my_dict['attr_val'] = sql_query.attr_value
        my_dict['shop_id'] = sql_query.id_main_page
        my_dict['tag_type'] = sql_query.tag_type
        my_dict['tag_status']: sql_query.sett_active
        my_dict['rus_tag'] = tags_types[sql_query.tag_type]
        return my_dict
    except NoResultFound:
        return False


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

# Меняем текущие настройки
def take_post_message(string_data):
    py_dict_data = json.loads(string_data)
    if py_dict_data["tag_id"]:
        # Меняем старые настройки
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
    json_answer = json.dumps(answer)
    return json_answer

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
    json_answer = json.dumps(answer)
    return json_answer
