from .start_base import session, Company, Link
from sqlalchemy.orm.exc import NoResultFound

class Common_object():

    def get_by_id(id):
        pass

class Company_object(Common_object):
    def __init__(self, inn = False, name = False):
        if inn:
            self.object = Company_object.get_by_inn(inn)
            # print('no inn')
        elif name:
            self.object = Company_object.get_by_name(name)
            # print('no name')
        else:
            print('НЕТ АРГУМЕНТОВ ДЛЯ СОЗДАНИЯ КОМПАНИИ')
            self.object = False

        if not self.object and inn and name:
            self.object = Company_object.create(inn, name)

    def get_by_inn(inn):
        try:
            c_o = session.query(Company).filter_by(inn = inn).one()
            return c_o
        except NoResultFound:
            return False

    def get_by_name(name):
        try:
            c_o = session.query(Company).filter_by(name = name).one()
            return c_o
        except NoResultFound:
            return False

    def create(inn, name):
        c_o = Company(inn = inn, name = name)
        session.add(c_o)
        session.commit()
        return c_o





class Website_object():
    def __init__(self, inn, name):
        pass

    def connect_website(self, company):
        # company: Company
        self.object.company_id = company.id

class Link_object(Common_object):
    def __init__(self, link):
        self.object = Company_object.get_by_name(link)
        if not self.object:
            self.object = Link_object.create(link)

    def get_by_name(name):
        try:
            l_o = session.query(Link).filter_by(name = name).one()
            return l_o
        except NoResultFound:
            return False

    def create(name):
        l_o = Link(name = name)
        session.add(l_o)
        session.commit()
        return l_o

# class Link_content_object():
#     def __init__(self, inn, name):

# class Parser_setting_object():
#     def __init__(self, inn, name):
