from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    ForeignKey,
    Text,
    Integer,
    Float,
    DateTime
    )
import datetime

Base = declarative_base()

class Company(Base):
    __tablename__ = "company"
    id = Column(Integer, primary_key = True)
    name = Column(Text)
    inn = Column(Integer)

    websites = relationship("Website", backref = 'company')

class Website(Base):
    __tablename__ = "website"
    id = Column(Integer, primary_key = True)
    domain = Column(Text)

    company_id = Column(ForeignKey("company.id"))

    links = relationship("Link", backref = 'website')
    parser_settings = relationship("Parser_setting", backref = 'website')

class Link(Base):
    __tablename__ = "link"
    id = Column(Integer, primary_key = True)
    website_id = Column(ForeignKey("website.id"))
    name = Column(Text)

    contents = relationship("Link_content", backref = 'link')

class Link_content(Base):
    __tablename__ = "link_content"
    id = Column(Integer, primary_key = True)
    date = Column(DateTime, default = datetime.datetime.utcnow)
    name = Column(Text)
    price = Column(Float)

    link_id = Column(ForeignKey("link.id"))

class Parser_setting(Base):
    __tablename__ = "parser_setting"
    id = Column(Integer, primary_key = True)
    object = Column(Text)
    settings = Column(Text)

    website_id = Column(ForeignKey("website.id"))
