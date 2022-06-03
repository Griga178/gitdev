from flask_funcs.module_data_base.sql_start import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from sqlalchemy.sql import exists

DBSession = sessionmaker(bind = engine)
session = DBSession()

# links, main_page_id = False
# .scalar()

def check_kkn_in_db(kkn_list):
    output_dict = {}

    for kkn_name in kkn_list:
        # kkn_id = session.query(KKNs_list).filter_by(name = kkn_name).scalar()

        # kkn_id = session.query(exists().where(KKNs_list.name == kkn_name)).scalar()
        (ret, ), = session.query(exists().where(KKNs_list.name == kkn_name))
        print(ret)
        # if not kkn_id:
        #     print(f'insert {kkn_name}')
        #     sql_kkn = KKNs_list(name = kkn_name)
        #     session.add(sql_kkn)
        #     session.commit()
        #     kkn_id = sql_kkn.id
        #
        # output_dict[kkn_name] = kkn_id
    return output_dict
