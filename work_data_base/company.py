from .tables import Company
from .start_base import session
from sqlalchemy.orm.exc import NoResultFound

class CompanyS(Company):
    def __new__(cls, **kwargs):
        obj = CompanyS.select(**kwargs)
        if not obj:
            obj = CompanyS.add_commit(**kwargs)
        return obj

    def select(inn = False, name = False):
        try:
            c_o = session.query(Company)
            c_o = c_o.filter_by(inn = inn) if inn else c_o
            c_o = c_o.filter_by(name = name) if name else c_o
            if not inn and not name:
                return None

            return c_o.one()
        except NoResultFound:
            return False

    def add_commit(inn, name):
        example = Company(inn = inn, name = name)
        session.add(example)
        session.commit()
        return example

    def select_all():
        return session.query(Company).all()

    def delete(**kwargs):
        c_o = CompanyS.select(**kwargs)
        if c_o:
            session.delete(c_o)
            session.commit()
            print(f'DELETE {kwargs.get("inn")} {kwargs.get("name")}')
        else:
            print(f'NOT FOUND {kwargs.get("inn")} {kwargs.get("name")}')

    def update(example):
        session.commit(example)
