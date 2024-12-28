from flask_funcs.module_data_base.sql_start import *
from sqlalchemy.orm import sessionmaker

DBSession = sessionmaker(bind = engine)
session = DBSession()

import datetime

def select_links_table():
    links_query = session.query(Net_links).all()
    output_dict = {'table_header': ['link id', 'Domain', 'link', 'name', 'price', 'parse date']}
    for row in links_query:
        t_link_id = row.id
        t_domain = row.net_shops.name
        t_link = row.http_link
        t_date, t_name, t_price = ' - - -', ' - - -', ' - - -'

        if len(row.net_link) > 0:
            last_t_date = datetime.datetime.strptime('01/01/2000', "%d/%m/%Y")
            for parse_res in row.net_link:
                cur_t_date = datetime.datetime.strptime(parse_res.current_date, "%d/%m/%Y")
                if cur_t_date > last_t_date:
                    result_obj = parse_res
                    last_t_date = cur_t_date
            t_name = result_obj.current_name
            t_date = result_obj.current_date
            t_price = result_obj.current_price

        output_dict[t_link_id] = [t_domain, t_link, t_name, t_price, t_date]

    return output_dict
