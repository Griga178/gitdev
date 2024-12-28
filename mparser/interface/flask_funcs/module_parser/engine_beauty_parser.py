import requests
from bs4 import BeautifulSoup
# import flask_funcs.module_parser.engine_parser_addition
'''


ПРОБЛЕМА 1 ФУНКЦИЯ НЕ ДОБАВЛЯЕТСЯ !!!!!!


'''
from flask_funcs.module_parser.engine_parser_addition import clean_number, clean_text #, change_to_true #

def change_to_true(usless_t):
    # ЕСЛИ НАХОДИТ ЭТОТ ТЕГ, ЗНАЧИТ ТОВАРА НЕТ В НАЛИЧИИ
    a = True
    return a

def run_beautiful_parser(settings):
    dict_output = {}
    for link_id, link in settings['links'].items():
        tag_setting = settings['tag_setting']
        try:
            html_page =  requests.get(link).text
            link_result = html_searcher(tag_setting, html_page)
        except:
            dict_output[link_id] = False
            print('Нет настроек')
            break
        dict_output[link_id] = link_result
    return dict_output



def html_searcher(tag_setting, for_soup):
    # ИСПОЛЬЗУЕТСЯ В run_selenium_parser
    dict_output = {}
    html_page = BeautifulSoup(for_soup, 'html.parser')

    desired_info = {'price': clean_number, 'name': clean_text, 'sold_out': change_to_true}

    for type in desired_info:
        type_setting = tag_setting[type]

        if type_setting:
            result_info = html_page.find(type_setting['tag'], attrs = {type_setting['attr']: type_setting['attr_val']})
            # print(result_info)
            if result_info != None:
                # Нашли что то по установленным настройкам
                dict_output[f'current_{type}'] = desired_info[type](result_info.text)
                # print(desired_info[type](result_info.text))

            else:
                dict_output[f'current_{type}'] = False
        else:
            dict_output[f'current_{type}'] = False

    result_true = False
    for result in dict_output:
        result_true += bool(dict_output[result])
    if result_true:
        return dict_output
    else:
        return False
