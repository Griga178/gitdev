'''
    Парсим огрн и другую инфу

'''
from o_4 import get_name_ogrn
from step_2 import *

def getOGRN():
    # unparsed Companies
    my_companies = db_session.query(Company).filter_by(ogrn = None).all()

    print(len(my_companies))
    count = 0
    for company in my_companies[:]:
        count += 1
        if company.id == 1:
            print('интернет решения ! id 1')
            continue
        try:
            n, a, og = get_name_ogrn(company.id)
            print(n, a, og)
        except:
            print('-->continue', company.id)
            og = None
            # continue
        if og:
            company.ogrn = og
            db_session.add(company)
            db_session.commit()

            print(count, og)
        else:
            print(count, 'None', company.id)
            print(f'https://www.ozon.ru/seller/{company.id}')
            api_ = f'https://www.ozon.ru/api/entrypoint-api.bx/page/json/v2?url=%2Fmodal%2Fshop-in-shop-info%3Fseller_id%3D{company.id}%26page_changed%3Dtrue'
            print(api_)
