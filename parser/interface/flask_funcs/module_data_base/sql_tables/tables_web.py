from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Net_links(Base):
    """Ссылки на товары"""
    __tablename__ = 'net_links'
    id = Column(Integer, primary_key = True)
    http_link = Column(String(255), nullable = False)
    id_model = Column(Integer, ForeignKey('models.id'))
    id_main_page = Column(Integer, ForeignKey('net_shops.id'))
    kkn_id = Column(Integer, ForeignKey('kkns_list.id'))
    net_link = relationship("Parsed_net_links", backref = 'net_links')
    # files = relationship("File_Link", back_populates = "net_links")

class Loaded_files(Base):
    __tablename__ = 'loaded_files'
    id = Column(Integer, primary_key = True)
    name = Column(String(255), nullable = False)

    # links = relationship("File_Link", back_populates = "loaded_files")


class File_Link(Base):
    __tablename__ = 'file_link'
    id = Column(Integer, primary_key = True)
    files_id = Column(Integer, ForeignKey("loaded_files.id"), nullable = False)
    link_id = Column(Integer, ForeignKey("net_links.id"), nullable = False)

    # link = relationship("Net_links", back_populates = "loaded_files")
    # file = relationship("Loaded_files", back_populates = "net_links")

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

    @property
    def order_by_type(self):
        return {self.tag_type: {
            'tag_id': self.id,
            'tag_name': self.tag_name,
            'attr_name': self.attr_name,
            'attr_value': self.attr_value,
            }}

    @property
    def setting_info(self):
        output_dict = {
            'tag_id': self.id,
            'tag_type': self.tag_type,
            'tag_name': self.tag_name,
            'attr_name': self.attr_name,
            'attr_value': self.attr_value,
            }
        return output_dict

class Net_shops(Base):
    """Интересующие сайты"""
    __tablename__ = 'net_shops'
    id = Column(Integer, primary_key = True)
    name = Column(String(255), nullable = False)
    need_selenium = Column(Integer)
    headless_mode = Column(Integer)
    sett_active = Column(Integer)
    shop_type = Column(String)
    net_link = relationship("Net_links", backref = 'net_shops')
    net_link_sett = relationship("Shops_sett", backref = 'net_shops')

    @property
    def full_shop_tags(self):
        tag_setting = {}
        [tag_setting.update(row.order_by_type) for row in self.net_link_sett]
        output_dict = {
            'shop_id': self.id,
            'shop_name': self.name,
            'need_selenium': bool(self.need_selenium),
            'headless_mode': bool(self.headless_mode),
            'sett_active': bool(self.sett_active),
            'tag_setting': tag_setting
            }
        return output_dict

    @property
    def shop_info(self):
        output_dict = {
            'shop_id': self.id,
            'shop_name': self.name,
            'need_selenium': bool(self.need_selenium),
            'headless_mode': bool(self.headless_mode),
            'sett_active': bool(self.sett_active),
            }
        return output_dict

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
