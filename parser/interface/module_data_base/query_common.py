from flask import json
from datetime import date, timedelta

import sys
sys.path.append('flask_funcs')

from sql_models import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

# Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# ВЫВОД СПИСКА МАГАЗИНОВ
def show_list_shops():
    ''' Возвращает:
        {1:{"shop_name":"www.onlinetrade.ru",
            "price":True, "name":True},
        2:{...},...}'''
    main_page_list = session.query(Net_shops).all()
    output_dict = {}
    tags_types = ['price', 'name', 'chars']
    for row in main_page_list:
        output_dict[row.id] = {}
        output_dict[row.id]['shop_name'] = row.name
        settings_rows = row.net_link_sett
        if settings_rows:
            for sett_row in settings_rows:
                if sett_row.tag_type in tags_types:
                    output_dict[row.id][sett_row.tag_type] = True
    json_dict = json.dumps(output_dict)
    return json_dict

# показать 3 ссылки
def show_few_links_sql(shop_id):
    sql_query = session.query(Net_links).filter_by(id_main_page = shop_id).limit(3)
    link_dict = {}
    for link in sql_query:
        link_dict[link.id] = link.http_link
    json_dict = json.dumps(link_dict)
    return json_dict
