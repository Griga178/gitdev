from query_for_parser import save_parsed_result
from query_parser_setting import show_shop_sett_2, select_shop_by_id, select_tag_set_by_id

from query_common import select_all_shops_with_tag

cr_res = {1:
            {1:
                {'current_price': 5290.0,
                'current_name': 'ИБП PowerCom Spider SPD-1000N, 1000ВA',
                'current_sold_out': False,
                'current_date': "24/05/2022"},
            2: {'current_price': 27790.0,
                'current_name': 'Монитор игровой Samsung C27G54TQWI 27" черный [lc27g54tqwixci]',
                'current_sold_out': False,
                'current_date': "24/05/2022"}
            }
        }

# save_parsed_result(cr_res)

# ТЕКУЩИЙ РЕЗУЛЬТАТ:
ск = {"new_parse": True,
"main_page_id": 4,
"main_page": "www.citilink.ru",
"http_link": "https://www.citilink.ru/product/udlinitel-yeelight-led-lightstrip-extension-ylot01yl-1434819/",
"link_id": 661,
"current_date": "24/05/2022",
"current_price": 889.0,
"current_name": "\u041b\u0435\u043d\u0442\u0430 \u0441\u0432\u0435\u0442\u043e\u0434\u0438\u043e\u0434\u043d\u0430\u044f YEELIGHT LED Lightstrip Extension [ylot01yl]"}

# test_data = select_all_shops_with_tag(1)
# test_data = select_shop_by_id(1)
# test_data = select_tag_set_by_id(13)
#
# if type(test_data) == list:
#     for el in test_data:
#         print(el)
# else:
#     print(test_data)
from query_parser_setting import insert_to_shops_setts

# my_data = {'shop_id': '1',
#     'tag_type': 'chars',
#     'tag_name': 'test',
#     'attr_name': 'trest',
#     'attr_val': 'test2',
#     'tag_id': False}

my_data = {'id_main_page': '1',
    'tag_type': 'chars',
    'tag_name': 'test3',
    'attr_name': 'test3',
    'attr_value': 'test3',
    'id': False}

my_data2 = {'id_main_page': '1',
    'tag_type': 'chars',
    'tag_name': 'test3',
    'attr_name': 'test3',
    'attr_value': 'test3',
    'id': 78}

a = insert_to_shops_setts(my_data)

print(a.setting_info)
