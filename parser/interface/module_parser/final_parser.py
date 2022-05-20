
'''
переходят в engine_parser.py
run_beautiful_parser
run_selenium_parser

parser_manager() переходит в back end_manager.py
'''
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import requests
from bs4 import BeautifulSoup

from engine_parser_addition import clean_number, clean_text, set_current_date

from parser_test_examples import final_result_output_dict

def parser_manager(input_dict):
    output_dict = {}
    # ПЕРЕБИРАЕМ ВХОДЯЩИЕ ССЫЛКИ
    for shop_id, shop_settings in input_dict.items():

        # print("Key:", shop_id)
        # print("Shop_name:", shop_settings["shop_name"])

        # ВИБИРАЕМ ТИП ПАРСЕРА
        if shop_settings['need_selenium']:
            print("Тип парсера: selenium")
            # parser_result_dict = run_selenium_parser(shop_settings)

        # if not shop_settings['need_selenium']:
        else:
            # parser_result_dict = 'BeautifulSoup - OFF'
            parser_result_dict = run_beautiful_parser(shop_settings)
        output_dict[shop_id] = parser_result_dict
    return output_dict

def run_beautiful_parser(settings):
    dict_output = {}
    for link_id, link in settings['links'].items():
        link_result = {}
        link_result['current_date'] = set_current_date()
        html_page =  requests.get(link)
        soup = BeautifulSoup(html_page.text, 'html.parser')

        for type in ["price", "name"]:
            # ищем настройки ЦЕНЫ и ИМЕНИ
            title = settings[type]
            if title:
                result_info = html_checker(type, title, soup)
                if result_info:
                    # НАШЛИ, ТО ЧТО ИСКАЛИ
                    link_result[f'current_{type}'] = result_info
                    link_result[f'{type}_message'] = False
                else:
                    # ПОПРОБУЕМ ПОСМОТРЕТЬ СТАТУС ЦЕНЫ
                    # ДЛЯ ИМЕНИ - НЕПРАВИЛЬНЫЙ ТЕГ
                    title = settings['sold_out_tag']
                    message = settings['sold_out_mes']

                    if title:
                        result_info = html_checker('name', title, soup)
                        if result_info:
                            if message in result_info:
                                link_result[f'current_{type}'] = False
                                link_result[f'{type}_message'] = 'Нет в наличии'
                            else:
                                link_result[f'current_{type}'] = False
                                link_result[f'{type}_message'] = False
                                print('Сообщение не нашлось в блоке')
                        else:
                            print('Теги для поиска сообщения не подошли')
                    else:
                        print('Возможно:\n  Товар распродан- нет тегов\n Страница не доступна\n    ДЛЯ ИМЕНИ - НЕПРАВИЛЬНЫЙ ТЕГ')
        dict_output[link_id] = link_result
    return dict_output



def html_checker(type, type_setting, text_html_page):
    desired_info = {'price': clean_number, 'name': clean_text}
    result_info = text_html_page.find(type_setting['tag'], attrs = {type_setting['attr']: type_setting['attr_val']})
    if result_info != None:
        # Нашли что то по установленным настройкам
        return desired_info[type](result_info.text)
    else:
        return False

d = parser_manager(final_result_output_dict)

print(d)
