import re
import requests
from bs4 import BeautifulSoup
from flask import json

def define_main_page(link):
    '''
    Определение главной страницы из строки
    '''
    if type(link) == str:
        split_list = link.split("/")
        h_protocol = split_list[0]
        try:
            main_page = split_list[2]
        except:
            main_page = ''
        if 'http' or 'ftp' in h_protocol:
            return main_page
        else:
            print('ERROR: не похоже на ссылку')
            return False
    else:
        print('ERROR: ссылка не в формате строки')
        return False

def define_links(string_value):
    # возращает список с возможными сылками
    if not string_value  is None:
        re_sult = re.findall(r'[\w:/.\-?=&+%#\[\]]+', string_value)
        return re_sult
    else:
        return False
        
def clean_number(str_text):
    ''' Выводит только числа из строк с помощью регулярок
        находит числа в которых "." или "," используется
        только для копеек'''
    result = re.findall(r'\d+\.?\,?', str_text)

    clear_number = ''.join(result)

    if ',' in clear_number:
        clear_number = clear_number.replace(',', '.')
    try:
        clear_number = float(clear_number)

        return clear_number
    except:
        print(f'Не преобразовать в число: {result, clear_number}')
        return " !Не преобразовать в число"

settings = {"www.citilink.ru": ["span", "class", "ProductHeader__price-default_current-price"],
"www.computermarket.ru":["div", "class", "cnt-price add-tovar cf"]}

def define_tags(main_page, sett_dict = settings):
    if main_page in sett_dict:
        try:
            tag_sett_list = [sett_dict[main_page][0], sett_dict[main_page][1], sett_dict[main_page][2]]
            return tag_sett_list
        except:
            return False
    else:
        return False


def parse_one_link(link, main_page):
    # ПРОВЕРКА НА ПОВТОРНЫЙ ПАРСИНГ
    # ЗНАЕМ ЛИ МЫ ТЕГИ, ГДЕ ИСКАТЬ?
    if main_page in settings:
        my_request = requests.get(link)
        soup = BeautifulSoup(my_request.text, 'html.parser')
        # ПОИСК БЛОКА С ЦЕНОЙ ПО ЗНАЧЕНИЮ КЛАССА
        try:
            price_tag = soup.find(settings[main_page][0], settings[main_page][2]).string
            current_price = clean_number(price_tag)
        except:
            current_price = '!!! Не подошли теги'
    else:
        current_price = '!!! не установлены теги'
    return current_price

def func_parse_link(link):
    main_page = define_main_page(link)
    used_tags = define_tags(main_page)
    if main_page and used_tags:
        current_price = parse_one_link(link, main_page)
        return json.dumps({'main_page': main_page, "price": current_price, "used_tags": used_tags, "link": link})
    else:
        return json.dumps({'main_page': "ПРОВЕРЬ", "price": False, 'used_tags': False})
