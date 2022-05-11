from engine_data_base import check_links_in_db, add_new_link_to_db, check_sett_to_parse

from engine_parser import shop_parser

import json

link = 'https://www.citilink.ru/product/ibp-powercom-spider-spd-1000n-1000va-332717/?text=Powercom+SPD-1000N'
# ПАРСИМ 1 ССЫЛКУ
def parse_one_link(link = False, id = False, link_list = False, id_list = False):
    # проверка на безопасность - пропускаем ... define_links from funcs_parser
    # ищем ссылку в БД
    if link:
        link_registration = check_links_in_db(link = link)
    elif id:
        link_registration = check_links_in_db(link_id = id)
    elif link_list:
        pass
    elif id_list:
        pass

    if not link_registration:
        link_registration = add_new_link_to_db(link_registration)
    # Получаем: {'links': {'id': 'http_link'}, 'main_page_id': 'x', 'main_page': 'www.name.ru'}
    # ИЩЕМ ТЕГИ ДЛЯ ПАРСИНГА
    link_info = check_sett_to_parse(link_registration)
    # получаем {"links": {...} "price":{"tag_name":x ...}, "name:..."}
    link_info['request_tool'] = 'py_requests'
    # ПАРСИМ
    parser_result = shop_parser(link_info)
    json_dict = json.dumps(parser_result, skipkeys = True)
    # print(json_dict)
    return parser_result

# print(1)
# parse_one_link(link = link)
# print(2)
# parse_one_link(id = 310)
