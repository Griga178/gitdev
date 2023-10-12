from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates
from sqlalchemy import Column, ForeignKey, Text, Integer, Float, DateTime, Boolean


Base = declarative_base()


class Contrant_card(Base):
    __tablename__ = "contrant_card"
    # id = Column(Integer, primary_key = True)
    number = Column(Integer, primary_key = True)
    date = Column(DateTime)
    price = Column(Float)
    customer = Column(Text)


    def __str__(self):
        return f'{self.number} {self.date}'
