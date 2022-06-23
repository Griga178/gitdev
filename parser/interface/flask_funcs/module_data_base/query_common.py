from flask import json
# from datetime import date, timedelta

from flask_funcs.module_data_base.sql_start import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

''' https://ploshadka.net/sqlalchemy-kak-poluchit-dannye-v-vide-spiska-slovarejj/ '''
# Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# ВЫВОД СПИСКА МАГАЗИНОВ
def select_all_shops_with_tag(shop_id = False):
    if shop_id:
        query_result = session.query(Net_shops).filter_by(id = shop_id).one().full_shop_tags
    else:
        query_result = [shop_row.full_shop_tags for shop_row in session.query(Net_shops).all()]
    return query_result


# показать 3 ссылки
def show_few_links_sql(shop_id):
    sql_query = session.query(Net_links).filter_by(id_main_page = shop_id).limit(3)
    link_dict = {}
    for link in sql_query:
        link_dict[link.id] = link.http_link
    json_dict = json.dumps(link_dict)
    return json_dict
