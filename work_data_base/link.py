from .tables import Link
from .start_base import session
from sqlalchemy.orm.exc import NoResultFound


class LinkS():
    def __new__(cls, **kwargs):
        obj = LinkS.select(**kwargs)
        if not obj:
            obj = LinkS.add_commit(**kwargs)
        return obj

    def select(name = False, website_id = False):
        try:
            c_o = session.query(Link)

            if name:
                c_o = c_o.filter_by(name = name).one()

                return c_o
            elif website_id:
                return c_o.filter_by(website_id = website_id).all()

        except NoResultFound:
            return False
    def add_commit(name, website_id = None):
        example = Link(name = name, website_id = website_id)
        session.add(example)
        session.commit()
        return example

    def select_all():
        return session.query(Link).all()

    def delete(**kwargs):
        c_o = LinkS.select(**kwargs)
        if c_o:
            session.delete(c_o)
            session.commit()
            print(f'DELETE {kwargs.get("name")} {kwargs.get("website_id")}')
        else:
            print(f'NOT FOUND {kwargs.get("name")} {kwargs.get("website_id")}')

    def update(example):
        session.commit(example)
