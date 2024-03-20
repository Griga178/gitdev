'''
ДЛЯ ПРЕМИУМ МАГАЗИНОВ
ищем руками
'''
from step_1 import *
my_list = []
# link = 'https://www.ozon.ru/product/adaptirovannyy-videodomofon-commax-cdv-70h2-vz-siniy-906678663/'
# id = 47676
# alt = 'Росси'
# my_list.append((link, id, alt))
# link = 'https://www.ozon.ru/product/gcr-kabel-dvi-d-5m-chernyy-od-8-5mm-28-28-awg-dvi-dvi-25-m-25-m-dvoynoy-ekran-5-metrov-295255981/'
# id = 71453
# alt = '4ПХ'
# my_list.append((link, id, alt))
# link = 'https://www.ozon.ru/product/kommutator-d-link-dgs-1016d-kol-vo-portov-16x1-gbit-s-ustanovka-v-stoyku-dgs-1016d-i2a-475578762/'
# id = 74383
# alt = 'e2e4'
# my_list.append((link, id, alt))
# link = 'https://www.ozon.ru/product/akusticheskiy-royal-wendl-lung-w120bl-chernyy-484580841/'
# id = 44076
# alt = 'Pguards'
# my_list.append((link, id, alt))
# link = 'https://www.ozon.ru/product/saphir-akkordeon-41-120-iv-11-5-chernyy-s-remnyami-i-chehlom-weltmeister-saphir-iv-120-41-bk-432781011/'
# id = 188932
# alt = 'Аврора'
# my_list.append((link, id, alt))

# link = 'https://www.ozon.ru/product/vozduhoduvka-benzinovaya-zimani-br776-rantsevaya-940696852/'
# id = 1068627
# alt = 'Best Seller'
# my_list.append((link, id, alt))


print(len(my_list))

for l, i, a in my_list:
    clear_link = check_link(l)
    print(l, i, a)
    link_obj = db_session.query(Link).filter_by(clear_value = clear_link).one()
    if not link_obj.company_id:

        try:
            company = db_session.query(Company).filter_by(id = i).one()
        except NoResultFound:
            company = Company(id = i, brand = a)
            db_session.add(company)
            db_session.commit()

        link_obj.company_id = company.id

        db_session.add(link_obj)
        db_session.commit()

        print(link)
