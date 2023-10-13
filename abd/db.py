from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, create_engine
from sqlalchemy import Column, ForeignKey, Text, Integer, Float, DateTime, Boolean, String

Base = declarative_base()


class Person(Base):
    __tablename__ = "person"
    id = Column(Integer, primary_key = True)
    name = Column(Text)
    second_name = Column(Text)
    phone = Column(Text)
    inn = Column(Text)

    def __repr__(self):
        return f'{self.name}'

class Person(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key = True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)

    def __repr__(self):
        return f'{self.name}'
metadata = MetaData()
DATA_BASE_PATH = 'sqlite:///test.db'
engine = create_engine(f'{DATA_BASE_PATH}?check_same_thread=False')
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind = engine)
session = DBSession()


# insert
# person = Person(name = 'Gri')
# session.add(person)
# session.commit()

# select
# print((session.query(Person).all()))
