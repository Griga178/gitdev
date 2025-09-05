# models.py
from sqlalchemy import (
    create_engine, Column, Integer, DateTime, ForeignKey, Text, JSON
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import datetime
from web_parser.settings import db_path

Base = declarative_base()

class SiteInfo(Base):
    __tablename__ = 'site_info'
    id = Column(Integer, primary_key=True)
    name = Column(Text) # домен сайта "github.com"
    settings = Column(JSON) # настройки в формате json

    parsed_data = relationship("ParseResult", back_populates="webPage")


class ParseResult(Base):
    __tablename__ = 'parsedData'
    id = Column(Integer, primary_key=True)
    url = Column(Text) # ссылка
    date =  = Column(DateTime, default=datetime.datetime.now)
    screenshot = Column(Text) # id скриншота
    data = Column(JSON) # результат парсинга в формате json

    site_info_id = Column(Integer, ForeignKey('site_info.id'), nullable=False)


def init_db():
    engine = create_engine(db_path)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)
