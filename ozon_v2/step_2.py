'''
Парсим id и бренд продавца
# вставка в БД
# создание связи в БД Компания - ссылка

'''
from step_1 import *
from o_1 import get_seller_id


def parse_comp_id():
    # unparsed links
    my_links = db_session.query(Link).filter_by(company_id = None).all()

    # print(len(my_links))
    counter = 0
    for link in my_links[1:]:
        counter +=1
        p_l = link.clear_value + '?oos_search=false'
        # resp_kw = get_seller_id(p_l)

        print(counter, p_l)
        try:
            resp_kw = get_seller_id(p_l)
            print(counter, resp_kw)
            if resp_kw['company_id'] == 'supermarket-25000':
                resp_kw['company_id'] = 1
            elif resp_kw['company_id'] == 'ozon-retail-186820':
                resp_kw['company_id'] = 1
            elif resp_kw['company_id'] == None:
                print( None)
                continue

            print(resp_kw)
            resp_kw['company_id']
            try:
                company = db_session.query(Company).filter_by(id = resp_kw['company_id']).one()
            except NoResultFound:
                company = Company(id = resp_kw['company_id'], brand = resp_kw['brand'])
                db_session.add(company)
                db_session.commit()

            # print(company.id, company.brand)
            link.company_id = company.id
            link.title = resp_kw.get('title')
            link.price = resp_kw.get('price')
            db_session.add(link)
            db_session.commit()
                # print(link)
        except:
            print(counter, 'Не спарсить id:', link.clear_value)
