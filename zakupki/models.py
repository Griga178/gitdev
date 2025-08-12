# models.py
from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Text
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import datetime
from settings import db_path

Base = declarative_base()

class Ktru(Base):
    __tablename__ = 'ktru'
    id = Column(Integer, primary_key=True)
    number = Column(String, unique=True, nullable=False)
    name = Column(Text)
    unit = Column(String)
    ownCharsIsForbidden = Column(Boolean, default=False)

    versions = relationship("KtruVersion", back_populates="ktru", cascade="all, delete-orphan")


class KtruVersion(Base):
    __tablename__ = 'ktruVersion'
    id = Column(Integer, primary_key=True)
    ktruId = Column(Integer, ForeignKey('ktru.id'), nullable=False)
    versionNumber = Column(Integer, nullable=False)
    dateUpdate = Column(DateTime, default=datetime.datetime.utcnow)

    ktru = relationship("Ktru", back_populates="versions")
    chars = relationship("KtruChars", back_populates="version", cascade="all, delete-orphan")


class KtruChars(Base):
    __tablename__ = 'ktruChars'
    id = Column(Integer, primary_key=True)
    ktruVersionId = Column(Integer, ForeignKey('ktruVersion.id'), nullable=False)
    name = Column(Text)
    values = Column(Text)
    unit = Column(String)

    version = relationship("KtruVersion", back_populates="chars")


class Requests(Base):
    __tablename__ = 'requests'
    id = Column(Integer, primary_key=True)
    requestName= Column(String)
    isSuccess = Column(Boolean, nullable=False)
    ktruNumber = Column(String, index=True)
    ktruVersion = Column(Integer)
    date = Column(DateTime, default=datetime.datetime.utcnow)


def init_db():
    engine = create_engine(db_path)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)
