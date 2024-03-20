from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates
from sqlalchemy import Column, ForeignKey, Text, Integer, Float, DateTime, Boolean
from sqlalchemy import MetaData, create_engine

DATA_BASE_PATH = 'sqlite:///C:/Users/G.Tishchenko/Desktop/ozon.db'
Base = declarative_base()

class Link(Base):
    __tablename__ = "link"
    id = Column(Integer, primary_key = True)
    excel_value = Column(Text)
    clear_value = Column(Text)
    price = Column(Integer)
    title = Column(Text)
    company_id = Column(ForeignKey("company.id"))
    def __str__(self):
        return f'COMP: {self.company_id}; {self.title}: {self.price}'

class Company(Base):
    __tablename__ = "company"
    id = Column(Integer, primary_key = True)
    brand = Column(Text)
    ogrn = Column(Integer)
    egrul_parse = Column(Boolean)
    full_name = Column(Text)
    inn = Column(Integer)
    address = Column(Text)
    short_name = Column(Text)
    kpp = Column(Integer)
    manager = Column(Text)
    date = Column(Text)

    links = relationship("Link", backref = 'company')

metadata = MetaData()
engine = create_engine(f'{DATA_BASE_PATH}?check_same_thread=False')
Base.metadata.create_all(engine)
