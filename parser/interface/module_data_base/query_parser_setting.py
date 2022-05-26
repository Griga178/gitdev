from flask import json
from datetime import date, timedelta

import sys
sys.path.append('flask_funcs')

from sql_models import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

# Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

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

'''ЕСТЬ Ф-Я: get_settings_by_shop_id(shop_id) '''
def show_shop_sett_2(shop_id):
    data = session.query(Net_shops).filter_by(id = shop_id).one()
    output_dict = {}
    output_dict['shop_name'] = data.name
    output_dict['shop_id'] = data.id
    output_dict['need_selenium'] = bool(data.need_selenium)
    output_dict['headless_mode'] = bool(data.headless_mode)
    output_dict['sett_active'] = bool(data.sett_active)
    # output_dict['sett_active'] = True
    # output_dict['headless_mode'] = True

    output_dict['tag_setting'] = {}
    for settings_data in data.net_link_sett:
        output_dict['tag_setting'][settings_data.tag_type] = {'tag_name': settings_data.tag_name,
            'attr_name': settings_data.attr_name,
            'attr_value': settings_data.attr_value,
            'tag_id': settings_data.id
            }
    return json.dumps(output_dict)

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
