# from sqlalchemy import MetaData
from main_import import metadata

from sql_models import *

my_base = 'sqlite:///test_base_ver_1.db'

# metadata = MetaData()

engine = create_engine(f'{my_base}?check_same_thread=False')

Base.metadata.create_all(engine)
