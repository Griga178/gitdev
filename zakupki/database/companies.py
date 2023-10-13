from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from .tables import Company


class Companies():
    def __init__(self, session):
        self.session = session

    def select(self, **kwargs):
        query = self.session.query(Company)
        query = query.filter_by(**kwargs) if kwargs else query
        try:
            return query.one()
        except MultipleResultsFound:
            return query.all()
        except NoResultFound:
            return None

    def insert(self, **kwargs):
        try:
            asset = Company(**kwargs)
            self.session.add(asset)
            self.session.commit()
            print(f'Добавлен: {asset.name}')
            return asset
        except IntegrityError as e:
            self.session.rollback()
            print(f'Компания: {kwargs["inn"]} уже есть')
            asset = self.select(inn = kwargs["inn"])
            return asset


    def save(self, asset: Company):
        self.session.add(asset)
        self.session.commit()
        print(f"<Company: {asset}> - обновлен")
