from step_3 import *

from o_5 import *

import time

def egrul_parse():
    my_companies = db_session.query(Company).filter(Company.ogrn != None, Company.egrul_parse == None).all()


    print(len(my_companies))
    count = 0
    for company in my_companies[:]:
        count += 1

        if company.id == 1 or company.id == 72545:
            print('интернет решения ! id 1')
            continue
        try:
            time.sleep(1)
            egrul_kw = get_info(company.ogrn)


            company.egrul_parse = True
            company.full_name = egrul_kw['full_name']
            company.inn = egrul_kw['inn']
            company.address = egrul_kw['address']
            company.short_name = egrul_kw['name']
            company.kpp = egrul_kw['kpp']
            company.manager = egrul_kw['manager']
            company.date = egrul_kw['date']
            db_session.add(company)
            db_session.commit()

            print(company.id, '--> OK')
        except:
            print('-->continue', company.id, company.ogrn)
            break
