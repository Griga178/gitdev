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

    def select_spec(self, **kwargs):
        query = self.session.query(Product)
        # query = query.filter(Product.name.contains(kwargs['names']))
        # query = query.filter(Product.name.contains('пианино||аккустич'))
        query = query.filter(Product.name.ilike(f'%{kwargs.get("name")}%')) if kwargs.get("name") else query

        # query = query.filter(Product.name.like(kwargs['names']))
        # query = query.filter(Product.name.match(kwargs['names']))
        # match
        # query = query.filter_by(**kwargs) if kwargs else query

        query = query.filter(Product.okpd_2 == kwargs.get("okpd_2")) if kwargs.get("okpd_2") else query
        query = query.filter(Product.price >= kwargs.get("min_price")) if kwargs.get("min_price") else query
        query = query.filter(Product.price <= kwargs.get("max_price")) if kwargs.get("max_price") else query
        try:
            a = query.one()
            b = set()
            b.add(a)
            return b
        except MultipleResultsFound:
            return set(query.all())
        except NoResultFound:
            return set()

    def insert(self, **kwargs):
        try:
            asset = Product(**kwargs)
            self.session.add(asset)
            self.session.commit()
            # print(f'Добавлен: {asset.name}')
            return asset
        except IntegrityError as e:
            self.session.rollback()
            # print(f'Контракт: {kwargs["number"]} уже есть')
            return None

    def insert_list(self, products):
        for product in products:
            asset = Product(**product)
            self.session.add(asset)
        try:
            self.session.commit()
        except IntegrityError as e:
            self.session.rollback()
            print('ошибка добавления списка')

    def save(self, asset: Product):
        self.session.add(asset)
        self.session.commit()
        print(f"<Product: {asset}> - обновлен")
