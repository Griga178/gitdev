
'''ЗАПРОСЫ К БД КАСАЮЩИЕСЯ ПАРСИНГА
    ПРОВЕРИТЬ НАЛИЧИЕ ССЫЛКОК В БД,
    ДОБАВИТЬ ССЫЛКИ,
    ПРОВЕРИТЬ НАЛИЧИЕ Сайта В БД,
    ДОБАВИТЬ Сайт,

    ВЫВОД ССЫЛКОК ПО ID (И НАСТРОЕК),

    ЗАПИСЬ РЕЗУЛЬТАТА ПАРСИНГА
    '''
import re
import sys

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from flask_funcs.module_data_base.sql_start import *

DBSession = sessionmaker(bind = engine)
session = DBSession()

def define_links(string_value):
    # возращает список с возможными сылками
    if not string_value  is None:
        re_sult = re.findall(r'[\w:/.\-?=&+%#\[\]]+', string_value)
        return re_sult
    else:
        return False

def define_main_page(link):
    '''    Определение главной страницы из строки    '''
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

def check_links_in_db(links, main_page_id = False):
    ''' Проверка есть ли ссылка в БД -> id ссыки '''
    output_dict = {}
    for link in links:

        try:
            link_from_bd = session.query(Net_links).filter_by(http_link = link).one()
            output_dict[link_from_bd.id] = link

        except NoResultFound:
            if not main_page_id:
                main_page = define_main_page(link)
                main_page_id = check_main_page_in_db(main_page)

            cur_data = Net_links(id_main_page = main_page_id, http_link = link)
            session.add(cur_data)
            session.commit()
            registred_link = session.query(Net_links).filter_by(http_link = link).one()
            output_dict[registred_link.id] = link

    return output_dict

def check_main_page_in_db(main_page):
    ''' Проверка есть ли Сайт в БД - нет: создать'''
    try:
        main_page_from_bd = session.query(Net_shops).filter_by(name = main_page).one()
        result = main_page_from_bd.id
    except NoResultFound:
        new_main_page = Net_shops(name = main_page) #need_selenium = True
        session.add(new_main_page)
        session.commit()
        search_result = session.query(Net_shops).filter_by(name = main_page).one()
        result = search_result.id
    return result

def sort_links_by_main_page(links_list):
    ''' сортируем ссылки по магазинам '''
    dict_shop_links = {}
    for string_with_links in links_list:
        # на случай, если в строке больше 1 сслыки
        links = define_links(string_with_links)
        if links:
            for link in links:
                # проверяем ссылка ли это +...
                main_page = define_main_page(link)
                if main_page:
                    # заполняем словарь.
                    if main_page in dict_shop_links:
                        dict_shop_links[main_page].add(link)
                    else:
                        dict_shop_links[main_page] = {link}
    return dict_shop_links

def get_settings_by_shop_id(shop_id):
    output_dict = {}
    data = session.query(Net_shops).filter_by(id = shop_id).one()
    output_dict['tag_setting'] = {'price': False, 'name': False, 'sold_out': False}
    output_dict['need_selenium'] = data.need_selenium
    output_dict['headless_mode'] = True
    for settings in data.net_link_sett:
        output_dict['tag_setting'][settings.tag_type] = {
            'tag': settings.tag_name,
            'attr': settings.attr_name,
            'attr_val': settings.attr_value
            }
    return output_dict

def get_links_by_string_to_parser(links_list):
    # из ссылок создаем словарь для парсинга
    # сортируем ссылки по магазинам
    dict_shop_links = sort_links_by_main_page(links_list)

    output_dict = {}
    for shop_name, links in dict_shop_links.items():
        # заменяем 'shop_name': {} на <id_shop_name>: {}
        main_page_id = check_main_page_in_db(shop_name)
        # заменяем 'ссылки' на {id: 'ссылка'}
        output_dict[main_page_id] = {'links': check_links_in_db(links, main_page_id)}
        # добавляем настройки к главной странице
        output_dict[main_page_id].update(get_settings_by_shop_id(main_page_id))

    return output_dict

def get_links_by_id_to_parser(links_id_list):
    data = session.query(Net_links).filter(Net_links.id.in_((links_id_list))).all()
    output_dict = {}
    for links_data in data:
        links = {links_data.id: links_data.http_link}
        main_page_id = links_data.id_main_page
        if main_page_id in output_dict:
            output_dict[main_page_id]['links'].update(links)
        else:
            output_dict[main_page_id] = {}
            output_dict[main_page_id]['links'] = links
    # добавляем настройки к главной странице
    for main_page_id in output_dict:
        output_dict[main_page_id].update(get_settings_by_shop_id(main_page_id))

    return output_dict

def save_parsed_result(parse_result):
    link_id_list = []
    current_dict = {}
    for shop_id, link_id_key in parse_result.items():

        for link_id, parse_data in link_id_key.items():
            if parse_data:
                current_data = Parsed_net_links(
                id_http_link = link_id,
                current_price = parse_data['current_price'],
                current_date = parse_data['current_date'],
                current_name = parse_data['current_name'],
                product_avaliable = (not parse_data['current_sold_out']),
                )
                session.add(current_data)
                # сохраняем экземпляры
                link_id_list.append(current_data)

    session.commit()
    # достаем из экземпляров инфу
    output_dict = {}
    for sql_ex in link_id_list:
        current_dict['current_price'] = sql_ex.current_price
        current_dict['current_name'] = sql_ex.current_name
        current_dict['current_date'] = sql_ex.current_date
        current_dict['current_date'] = sql_ex.current_date
        current_dict['link_id'] = sql_ex.id_http_link

        current_dict['http_link'] = sql_ex.net_links.http_link
        current_dict['main_page_id'] = sql_ex.net_links.id_main_page
        current_dict['main_page'] = sql_ex.net_links.net_shops.name
        current_dict['new_parse'] = True

    # return output_dict
    return current_dict
