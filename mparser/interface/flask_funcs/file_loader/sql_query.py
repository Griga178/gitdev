from flask_funcs.module_data_base.sql_start import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from sqlalchemy.sql import exists

from flask_funcs.module_data_base.query_for_parser import check_links_in_db

DBSession = sessionmaker(bind = engine)
session = DBSession()

# links, main_page_id = False
# .scalar()

def replace_kkn_name_kkn_id(kkn_dict):
    output_dict = {}

    for kkn_name in kkn_dict:
        kkn_id = session.query(KKNs_list.id).filter_by(name = kkn_name).scalar()

        if not kkn_id:
            sql_kkn = KKNs_list(name = kkn_name)
            session.add(sql_kkn)
            session.commit()
            kkn_id = sql_kkn.id

        output_dict[kkn_id] = kkn_dict[kkn_name]
    return output_dict

def replace_link_name_link_id(inp_dict):

    for kkn_id, link_name_set in inp_dict.items():
        link_id_set = set()

        # for link_name in link_name_set:
        #
        #     link_id = session.query(Net_links.id).filter_by(http_link = link_name).scalar()
        #
        #     if not link_id:
        #
        #         sql_link = Net_links(http_link = link_name)
        #         session.add(sql_link)
        #         session.commit()
        #         link_id = sql_link.id
        #
        #     link_id_set.add(link_id)

        [link_id_set.add(link_id) for link_id in check_links_in_db(link_name_set)]
        # inp_dict[kkn_id] = link_id_set
        inp_dict[kkn_id] = link_id_set

    return inp_dict
