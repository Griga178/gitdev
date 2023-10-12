from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

from .tables import Base

from .contract_cards import Contrant_cards

class Data_base_API():
    def __init__(self, DATA_BASE_PATH):
        metadata = MetaData()
        engine = create_engine(f'{DATA_BASE_PATH}?check_same_thread=False')
        Base.metadata.create_all(engine)
        DBSession = sessionmaker(bind = engine)

        self.session = DBSession()

        self.contrant_cards = Contrant_cards(self.session)
