from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from .tables import Product


class Products():
    def __init__(self, session):
        self.session = session

    def select(self, **kwargs):
        query = self.session.query(Product)
        query = query.filter_by(**kwargs) if kwargs else query
        try:
            return query.one()
        except MultipleResultsFound:
            return query.all()
        except NoResultFound:
            return None

    def insert(self, **kwargs):
        asset = Product(**kwargs)
        self.session.add(asset)
        self.session.commit()
        print(f'Добавлен: {asset.name}')
        return asset

    def save(self, asset: Product):
        self.session.add(asset)
        self.session.commit()
        print(f"<Product: {asset}> - обновлен")
