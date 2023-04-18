from .tables import Website
from .start_base import session
from sqlalchemy.orm.exc import NoResultFound


class WebsiteS():
    def __new__(cls, **kwargs):
        obj = WebsiteS.select(**kwargs)
        if not obj:
            obj = WebsiteS.add_commit(**kwargs)
        return obj
    def select(domain = False, company_id = False):
        try:
            c_o = session.query(Website)

            if domain:
                 c_o = c_o.filter_by(domain = domain).one()
            elif website_id:
                c_o = c_o.filter_by(company_id = company_id).all()
            return c_o
        except NoResultFound:
            return False
    def add_commit(domain, company_id = None):
        example = Website(domain = domain, company_id = company_id)
        session.add(example)
        session.commit()
        return example

    def select_all():
        return session.query(Website).all()

    def delete(**kwargs):
        c_o = WebsiteS.select(**kwargs)
        if c_o:
            session.delete(c_o)
            session.commit()
            print(f'DELETE {kwargs.get("domain")} {kwargs.get("company_id")}')
        else:
            print(f'NOT FOUND {kwargs.get("domain")} {kwargs.get("company_id")}')

    def update(example):
        session.commit(example)
