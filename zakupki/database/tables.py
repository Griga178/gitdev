from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates
from sqlalchemy import Column, ForeignKey, Text, Integer, Float, DateTime, Boolean
from sqlalchemy import MetaData, create_engine
from settings import DATA_BASE_PATH

Base = declarative_base()

class Contrant_card(Base):
    __tablename__ = "contrant_card"

    number = Column(Integer, primary_key = True)
    date = Column(DateTime)
    price = Column(Float)
    customer = Column(Text)
    update_date = Column(DateTime)

    provider_id = Column(ForeignKey("company.inn"))

    products = relationship("Product", backref = 'contrant_card', lazy='subquery', viewonly=True)

    def __str__(self):
        return f'{self.number} {self.date}'

    def to_file(self):
        return f'{self.number};{self.date.strftime("%d.%m.%Y")};{self.price};{self.customer}\n'

class Company(Base):
    __tablename__ = "company"

    inn = Column(Integer, primary_key = True)
    name = Column(Text)
    phone = Column(Text)
    e_mail = Column(Text)

    addres = Column(Text)

    contrants = relationship("Contrant_card", backref = 'company')

    def __str__(self):
        return f'{self.name}'

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key = True)
    name = Column(Text)
    country_producer = Column(Text)
    ktru = Column(Text)
    okpd_2 = Column(Text)
    type = Column(Text)
    measure = Column(Text)
    quantity = Column(Float)
    price = Column(Float)
    cost = Column(Float)
    tax = Column(Text)

    contrant_card_id = Column(ForeignKey("contrant_card.number"))

    def __str__(self):
        return f'{self.name}: {self.price}'

metadata = MetaData()
engine = create_engine(f'{DATA_BASE_PATH}?check_same_thread=False')
Base.metadata.create_all(engine)
