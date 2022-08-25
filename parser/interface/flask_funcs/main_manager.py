from flask_funcs.module_data_base.query_common import select_all_shops_with_tag
from flask_funcs.module_data_base.query_for_parser import get_links_by_string_to_parser, get_links_by_id_to_parser, save_parsed_result
from flask_funcs.module_data_base.query_parser_setting import insert_to_tags_settings, delete_set_by_id, update_shop_setting

from flask_funcs.module_parser.manager_parser import start_parse

import json

# НАСТРОЙКИ ПАРСЕРА
# СТАРТ СТРАНИЦЫ
def get_shop_list():
    select_query = select_all_shops_with_tag()
    json_result = json.dumps(select_query)
    return json_result

# НАСТРОЙКИ МАГАЗИНОВ
def get_shop_setting(shop_id):
    select_query = select_all_shops_with_tag(shop_id)
    json_result = json.dumps(select_query)
    return json_result

def save_shop_setting(setting_dict):
    update_shop_setting(setting_dict)

def update_tag_setting(setting_dict):
    # insert + update
    insert_query = insert_to_tags_settings(setting_dict)
    json_result = json.dumps(insert_query)
    return json_result


# ФУНКЦИИ ДЛЯ ПАРСЕРА
def parse_from_input(input_info):
    dict_to_parse = get_links_by_string_to_parser(input_info)
    parse_result = start_parse(dict_to_parse)
    answer_to_html = save_parsed_result(parse_result)
    # ? пока пропустили
    # answer_to_html = get_parsed_result_by_link_id(id_of_parsed_links)
    ''' ! SQL ВОЗВРАЩАЕТ СЛОВАРЬ СТАРОЙ ВЕРСИИ - 1 РЕЗУЛЬТАТ ПАРСИНГА!
                111
                111    '''
    json_answer_to_html = json.dumps(answer_to_html, skipkeys = True)
    return json_answer_to_html

# парсинг ссылок по id
def parse_from_registered_link(list_id):
    dict_to_parse = get_links_by_id_to_parser(list_id)
    parse_result = start_parse(dict_to_parse)
    answer_to_html = save_parsed_result(parse_result)
    # ? пока пропустили
    # answer_to_html = get_parsed_result_by_link_id(id_of_parsed_links)
    ''' ! SQL ВОЗВРАЩАЕТ СЛОВАРЬ СТАРОЙ ВЕРСИИ - 1 РЕЗУЛЬТАТ ПАРСИНГА!
                - надо словарь из
                111
                111    '''
    json_answer_to_html = json.dumps(answer_to_html, skipkeys = True)
    return json_answer_to_html


# парсинг ссылок файла...
def file_recept(file_obj, app):
    import os
    from werkzeug.utils import secure_filename
    from flask_funcs.file_loader.excel_reader import parse_file_links
    filename = secure_filename(file_obj.filename)
    # file_obj.save(os.path.join(app.config['UPLOAD_FOLDER'], file_obj.filename))
    parse_file_links(file_obj)
    # print(type(file_obj), filename)

    return "ok"

from flask_funcs.module_data_base.query_for_db import select_links_table

def get_table_links():
    list_table = select_links_table()

    return json.dumps(list_table)
