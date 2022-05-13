from engine_data_base import check_links_in_db, add_new_link_to_db, check_sett_to_parse, show_settings_by_type

from engine_parser import shop_parser

import json


# ПАРСИМ 1 ССЫЛКУ
def parse_one_link(input_link = False, input_id = False):
    # проверка на безопасность - пропускаем ... define_links from

    # ИЩЕМ ССЫЛКИ В БД
    if input_link:
        link_registration = check_links_in_db(link = input_link)
    elif input_id:
        link_registration = check_links_in_db(link_id = input_id)

    # ЕСЛИ ССЫЛОК НЕ БЫЛО, РЕГИСТРИРУЕМ
    if not link_registration:
        new_link_id = add_new_link_to_db(input_link)
        link_registration = check_links_in_db(link_id = new_link_id)


    # ЕСЛИ ССЫЛКА УЖЕ БЫЛА ПРОПАРСЕНА (НА ЭТОЙ НЕДЕЛЕ) - НЕ ПАРСИМ
        # если есть цена temp_setting
        # return parser_result

    # ИЩЕМ ТЕГИ ДЛЯ ПАРСИНГА
    tags_types = ['price', 'name', 'chars']
    start_parse = False
    for type in tags_types:
        link_registration[type] = show_settings_by_type(link_registration['shop_id'], type)
        start_parse += bool(link_registration[type])

    # ПАРСИМ
    # Если есть хоть одна настройка: парсим

    if start_parse:
        # print(link_registration)
        parser_result = shop_parser(link_registration)
        json_dict = json.dumps(parser_result, skipkeys = True)
        # print(json_dict)
        return json_dict
    else:
        return False

# ЗАПИСЬ В БД

# {"main_page_id": 4, "main_page": "www.citilink.ru", 
# "current_date": "13/05/2022", "current_price": 5790.0,
# "current_name": "\u0418\u0411\u041f PowerCom Spider SPD-1000N, 1000\u0412A"}

# print(1)
link = 'https://www.citilink.ru/product/ibp-powercom-spider-spd-1000n-1000va-332717/?text=Powercom+SPD-1000N'
link2 = 'https://online.metro-cc.ru/category/molochnye-prodkuty-syry-i-yayca/syry/lamber-v-bochonke-1kg-bzmzh'
link3 = 'https://spb.x-m.su/moped-delta-s-moto-lifan'
link4 = 'https://zakupki.gov.ru/epz/contract/contractCard/document-info.html?reestrNumber=2782543560821000023'
print(parse_one_link(link))
# parse_one_link(link3)
# parse_one_link(link3)
# print(2)
# parse_one_link(id = 310)
