from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from .tables import Contrant_card


class Contrant_cards():
    def __init__(self, session):
        self.session = session

    def select(self, **kwargs):
        query = self.session.query(Contrant_card)
        query = query.filter_by(**kwargs) if kwargs else query
        try:
            return query.one()
        except MultipleResultsFound:
            return query.all()
        except NoResultFound:
            return None

    def insert(self, **kwargs):
        try:
            asset = Contrant_card(**kwargs)
            self.session.add(asset)
            self.session.commit()
            print(f'Добавлен: {asset.number} от {asset.date}')
            return asset
        except IntegrityError as e:
            self.session.rollback()
            print(f'Контракт: {kwargs["number"]} уже есть')
            return None


    def save(self, asset: Contrant_card):
        self.session.add(asset)
        self.session.commit()
        print(f"<Contrant_card: {asset}> - обновлен")
