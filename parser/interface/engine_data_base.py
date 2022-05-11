from flask import json

import sys
sys.path.append('flask_funcs')

from sql_models import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

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

def check_links_in_db(link):
    ''' Проверка есть ли ссылка в БД'''
    result_dict = {}
    try:
        link_from_bd = session.query(Net_links).filter_by(http_link = link).one()
        result_dict['link_id'] = link_from_bd.id
        result_dict['http_link'] = link_from_bd.http_link
        result_dict['main_page_id'] = link_from_bd.id_main_page
        result_dict['main_page'] = link_from_bd.net_shops.name
        return result_dict
    except NoResultFound:
        return False

def check_main_page_in_db(main_page):
    ''' Проверка есть ли Сайт в БД'''
    result_dict = {}
    try:
        main_page_from_bd = session.query(Net_shops).filter_by(name = main_page).one()
        result_dict['main_page_id'] = main_page_from_bd.id
    except NoResultFound:
        new_main_page = Net_shops(name = main_page)
        session.add(new_main_page)
        session.commit()
        search_result = session.query(Net_shops).filter_by(name = main_page).one()
        result_dict['main_page_id'] = search_result.id
    return result_dict

def add_new_link_to_db(link):
    '''Добавляем ссылку в БД, если нет главной страницы,
    то добавляем и ее - так же связываем'''
    main_page = define_main_page(link)
    result_dict = check_main_page_in_db(main_page)

    link_checker = check_links_in_db(link)
    if not link_checker:
        cur_data = Net_links(
        id_main_page = result_dict['main_page_id'],
        http_link = link)
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
