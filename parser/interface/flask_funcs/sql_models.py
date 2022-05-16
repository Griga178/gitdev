# from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, Table
from sqlalchemy.ext.declarative import declarative_base
# для создания отношений между таблицами
from sqlalchemy.orm import relationship # пока не надо
# для настроек
from sqlalchemy import *

Base = declarative_base()
metadata = MetaData()
my_base = 'sqlite:///test_base_ver_1.db'
engine = create_engine(f'{my_base}?check_same_thread=False')

class Net_links(Base):
    """Ссылки на товары"""
    __tablename__ = 'net_links'
    id = Column(Integer, primary_key = True)
    http_link = Column(String(255), nullable = False)
    id_model = Column(Integer, ForeignKey('models.id'))
    id_main_page = Column(Integer, ForeignKey('net_shops.id'))
    net_link = relationship("Parsed_net_links", backref = 'net_links')
    # kkn_id = Column(Integer, ForeignKey('kkns_list.id'))

class Parsed_net_links(Base):
    """Результаты парсинга"""
    __tablename__ = 'parsed_net_links'
    id = Column(Integer, primary_key = True)
    id_http_link = Column(Integer, ForeignKey('net_links.id'), nullable = False)
    current_price = Column(REAL)
    current_date = Column(TEXT)
    current_name = Column(Text)
    product_avaliable = Column(Integer)

class Shops_sett(Base):
    """ Настройки для парсинга """
    __tablename__ = 'shops_setts'
    id = Column(Integer, primary_key = True)
    id_main_page = Column(Integer, ForeignKey('net_shops.id'))
    tag_type = Column(Text)
    tag_name = Column(Text)
    attr_name = Column(Text)
    attr_value = Column(Text)
    sett_active = Column(Integer)

class Net_shops(Base):
    """Интересующие сайты"""
    __tablename__ = 'net_shops'
    id = Column(Integer, primary_key = True)
    name = Column(String(255), nullable = False)
    need_selenium = Column(Integer)
    net_link = relationship("Net_links", backref = 'net_shops')
    net_link_sett = relationship("Shops_sett", backref = 'net_shops')
    shop_type = Column(String)

class KKNs_list(Base):
    """Тут хранятся названия ККН-ов"""
    __tablename__ = 'kkns_list'
    id = Column(Integer, primary_key = True)
    name = Column(String(255), nullable = False)
    links_id = relationship("Net_links", backref = 'kkns_list')


class Models(Base):
    """Модели товаров"""
    __tablename__ = 'models'
    id = Column(Integer, primary_key = True)
    name = Column(String(255), nullable = False)
    information_link = Column(String(255))
    id_subject = Column(Integer, ForeignKey('subjects.id'))
    net_link = relationship("Net_links", backref = 'models')

class Subject(Base):
    """Тут хранятся названия предметов"""
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key = True)
    name = Column(String(255), nullable = False)
    objects = relationship("Models", backref ='subjects')

Base.metadata.create_all(engine)
