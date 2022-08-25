from flask_funcs.module_data_base.sql_tables.tables_web import *

from sqlalchemy import MetaData

metadata = MetaData()

my_base = 'sqlite:///test_base_ver_1.db'

engine = create_engine(f'{my_base}?check_same_thread=False')

Base.metadata.create_all(engine)
