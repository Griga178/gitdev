
from engine_beauty_parser import run_beautiful_parser
from engine_selenium_parser import run_selenium_parser

def parser_manager(input_dict):
    output_dict = {}
    # ПЕРЕБИРАЕМ ВХОДЯЩИЕ ССЫЛКИ
    for shop_id, shop_settings in input_dict.items():
        parser_result_dict = False
        # ВИБИРАЕМ ТИП ПАРСЕРА
        if shop_settings['need_selenium']:
            # print("Тип парсера: selenium")
            parser_result_dict = run_selenium_parser(shop_settings)
            # pass
        else:
            # pass
            parser_result_dict = run_beautiful_parser(shop_settings)

        if parser_result_dict:
            output_dict[shop_id] = parser_result_dict

    return output_dict
