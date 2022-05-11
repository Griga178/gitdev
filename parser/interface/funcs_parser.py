import re
import requests
from bs4 import BeautifulSoup
from flask import json

import sys
sys.path.append('flask_funcs')
from sql_models import *
from sqlalchemy.orm import sessionmaker

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def check_links_in_db(link):
    ''' Проверка есть ли ссылка в БД'''
    result_dict = {}
    list_of_links = session.query(Net_links).filter_by(http_link = link).all()
    if len(list_of_links) == 1:
        result_dict['link_id'] = list_of_links[0].id
        result_dict['http_link'] = list_of_links[0].http_link
        result_dict['main_page_id'] = list_of_links[0].id_main_page
        result_dict['main_page'] = list_of_links[0].net_shops.name
    elif len(list_of_links) == 0:
        result_dict = add_new_link(link)
    elif len(list_of_links) > 1:
        result = 'Одинаковые ссылки в БД'
    else:
        result = 'Что то не так с запросом'
    return result_dict

def add_new_link(link):
    '''Добавляем ссылку в БД, если нет главной страницы,
    то добавляем и ее - так же связываем'''
    result_dict = {}
    main_page = define_main_page(link)
    list_of_main_page = session.query(Net_shops).filter_by(name = main_page).all()
    if len(list_of_main_page) == 1:
        result_dict['main_page_id'] = list_of_main_page[0].id
    elif len(list_of_main_page) == 0:
        new_main_page = Net_shops(name = main_page)
        session.add(new_main_page)
        session.commit()
        search_result = session.query(Net_shops).filter_by(name = main_page).one()
        # main_page_id = search_result.id
        result_dict['main_page_id'] = search_result.id

    cur_data = Net_links(
    id_main_page = main_page_id,
    http_link = link
    )
    session.add(cur_data)
    session.commit()
    one_link = session.query(Net_links).filter_by(http_link = link).one()
    result_dict['link_id'] = one_link.id
    result_dict['http_link'] = one_link.http_link
    return result_dict

def check_sett_to_parse(result_dict):
    '''dict{link_id, http_link, main_page_id}'''
    sett_query = session.query(Shops_sett).filter_by(id_main_page = result_dict['main_page_id']).all()
    for sett in sett_query:
        result_dict[sett.tag_type] = {'tag_name': sett.tag_name, 'attr_name': sett.attr_name, 'attr_value': sett.attr_value}
    return result_dict

# check_sett_to_parse('https://zakupki.gov.ru/epz/contract/contractCard/document-info.html?reestrNumber=2782543560821000023')

def new_parse(link = False, link_id = False):
    output_dict = {}
    if link_id:
        list_of_links = session.query(Net_links).filter_by(id = link_id).one()
        output_dict['link_id'] = list_of_links.id
        output_dict['http_link'] = list_of_links.http_link
        output_dict['main_page_id'] = list_of_links.id_main_page
        output_dict['main_page'] = list_of_links.net_shops.name
        output_dict = check_sett_to_parse(output_dict)
    else:
        output_dict = check_links_in_db(link)

    # Тут начинается парсинг
    parsing_types = ['price', 'name']
    for type in parsing_types:
        # result_dict[f'current_{type}'] = three_tags_parse(result_dict, type)
        output_dict[f'current_{type}'] = selen_three_tag_parse(output_dict, type)
    return output_dict


def three_tags_parse(link_info, tag_type):
    my_request = requests.get(link_info['http_link'])
    soup = BeautifulSoup(my_request.text, 'html.parser')
    try:
        price_tag = soup.find(link_info[tag_type]['tag_name'], {link_info[tag_type]['attr_name'], link_info[tag_type]['attr_value']}).string

        if tag_type == 'price':
            result = clean_number(price_tag)
        else:
            result = price_tag

        # ТУТ ЗАПИСЬ ВРЕМЕНИ И ЦЕНЫ ПАРСИНГА В БД
    except:
        result = '!!! Не подошли теги'
    return result

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
# options.add_argument("--start-maximized")
# options.add_argument("--window-size=1920x1080")

def selen_three_tag_parse(link_info, tag_type):
    tag, atribute, atr_val = link_info[tag_type]['tag_name'], link_info[tag_type]['attr_name'], link_info[tag_type]['attr_value']
    driver = webdriver.Chrome(options = options)
    driver.implicitly_wait(3) # ждем столько, если не справился закрываем
    driver.get(link_info['http_link'])
    price = driver.find_element_by_xpath(f"//{tag}[@{atribute}='{atr_val}']")
    a = price.get_attribute('outerHTML')
    # result_str = clean_number(a)
    result_str = a
    return result_str

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

# print(new_parse(n_l))
