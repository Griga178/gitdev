from query_for_parser import save_parsed_result
from query_parser_setting import show_shop_sett_2

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

test = show_shop_sett_2(3)
print(test)
