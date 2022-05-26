import sys
sys.path.append('module_data_base')
sys.path.append('module_parser')

from query_common import show_list_shops, show_few_links_sql
from query_for_parser import get_links_by_string_to_parser, get_links_by_id_to_parser, save_parsed_result
from query_parser_setting import show_shop_sett_2
from manager_parser import start_parse


import json


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
