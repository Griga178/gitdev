from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker
from .setting import DATA_BASE_PATH
from .tables import *

metadata = MetaData()
engine = create_engine(f'{DATA_BASE_PATH}?check_same_thread=False')
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind = engine)
session = DBSession()
