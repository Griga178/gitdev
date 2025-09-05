from rbc.controller import RemBrowseControl
from web_parser.parser import parse_html
from web_parser.services.domain import get_domain

rbc = RemBrowseControl(remote_port = 9223, browser='edge')

rbc.run()

urls = [
    'https://www.ozon.ru/product/huawei-smartfon-pura-80-ultra-16-gb-512-gb-chernyy-smart-chasy-watch-gt-5-pro-46-mm-chernyy-2445751960/',
    'https://www.ozon.ru/product/apple-smartfon-iphone-16-pro-esim-only-8-128-gb-belyy-2091983348/?at=6WtZjmgPjsloPyWkhOY0l81uKBNWnqc0gv9xOCJPKAwE']

from web_parser.temp_settings import parse_setting as setts
for url in urls:
    domain = get_domain(url)
    settings = setts[domain]

    tab_id = rbc.new_tab(url)

    content = rbc.get_content(tab_id)


    p_result = parse_html(content, settings)

    print(p_result)
    # rbc.close_tab(tab_id)
# rbc.close()


"""
    есть словарь "d" в python, который является настройками парсинга одного элемента
    все значения ключей, заполня.тся пользователем, по ключу target_point возможна рекурсия
    нужно написать веб страницу с лаконичным дизайном на которой будет блок_1 с формой, где
    пользователь может заполнить словарь "d", блок_2 с окном формирующим словарь для копирования,
    блок_3 для вывода результатов парсинга по текущим настройкам (теги, которые находятся по текущим настройкам)
    кнопка_1 - загружает html документ с пк пользователя (хранится в памяти, по нему в блоке_3 выводится инфа)
    кнопка_2 - формирует словарь "d" по заполненной форме
    пример словаря d = {
    "name": "price", "type": "float","is_expected": True,
    "rules": {
        "search_index": 0,"recursive": True,"expected_amount": None,
        "tag_name": "div","attr_name": "data-widget","attr_value": "webPrice",
        "target_point": {
            "search_index": 0,"recursive": False,"expected_amount": None,
            "tag_name": "div","attr_name": None,"attr_value": None,
            "target_point": {
                "search_index": -1,"recursive": False,"expected_amount": None,
                "tag_name": "div","attr_name": None,"attr_value": None,
                "target_point": {
                    "search_index": 0,"recursive": True,"expected_amount": None,
                    "tag_name": "span","attr_name": None,"attr_value": None,
                    "target_point": True
                    }
                }
            }
        },
    }


"""
