'''
    Пользовательские запросы
'''

data = [
    'https://www.ozon.ru/product/holodilnik-dvuhkamernyy-bbk-rf-098-belyy-obshchiy-obem-98-l-877254867/',
    'https://www.ozon.ru/product/holodilnik-comfee-rcd115wh1r-belyy-844874232/',
    'https://www.ozon.ru/product/pogruzhnoy-blender-vitek-vt-3425-chernyy-201382792',
    "https://www.ozon.ru/product/ochistitel-vozduha-funai-hap-z200se-zen-belyy-178542125/",
    ]

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from database import *
DBSession = sessionmaker(bind = engine)
db_session = DBSession()
# query = db_session.query(Link).filter(Link.excel_value == data).all()
# print(len(query))


for l in data[:1]:
    l_obj = db_session.query(Link).filter_by(excel_value = l).one()
    print(l_obj)

q = db_session.query(Company).filter(Company.id == 771822).one()

print(q.inn, q.short_name)
# q.ogrn = 1227700808477
# db_session.add(q)
# db_session.commit()
