from excel import excel_to_dicts, dicts_to_excel
from database import Data_base_API


def search_products(**kwargs):
    DB_API = Data_base_API()
    return DB_API.products.select_spec(**kwargs)

def read_query_xlsx(file_name, **kw):
    # Смотрим что будем искать в бд

    rows = excel_to_dicts(file_name,
        headers_names = [
            'Наименование ККН',
            'ОКПД2',
            'Средняя цена включая НДС, руб.',
        ],
        headers = False, **kw)

    results = []
    DB_API = Data_base_API()

    for el in rows[:]:
        kkn_name = el['Наименование ККН']
        product_name = " ".join(kkn_name.split(" ")[:-2])
        okpd_2 = el['ОКПД2']
        price = el['Средняя цена включая НДС, руб.']
        per_cent = 0.3
        min_price = price * (1 - per_cent)
        max_price = price * (per_cent + 1)

        products_by_okpd = search_products(
            okpd_2 = okpd_2,
            min_price = min_price,
            max_price = max_price)


        # products_by_okpd = set(products_by_okpd) if products_by_okpd else set()

        products_by_name = search_products(
            name = product_name,
            min_price = min_price,
            max_price = max_price)
        # print([products_by_okpd])
        # print([products_by_name])
        products_by_okpd = products_by_okpd | products_by_name
        print(kkn_name, price)#product_name,
        if products_by_okpd:
            for el in products_by_okpd:
                # print("SQL: ", el, el.okpd_2) #, kkn_name
                contr = DB_API.contrant_cards.select(number = el.contrant_card_id)
                data = {
                    'Наименование ККН': kkn_name,
                    'ОКПД2': okpd_2,
                    'Средняя цена включая НДС, руб.': price,
                    'Наименование закупки': el.name,
                    'Цена закупки': el.price,
                    'Наименование контракта': str(el.contrant_card_id) + contr.date.strftime(" от %d.%m.%Y"),
                    'Ссылка': f'https://zakupki.gov.ru/epz/contract/contractCard/document-info.html?reestrNumber={el.contrant_card_id}'
                }
                # print(data)
                results.append(data)
        print()

    dicts_to_excel(results, kw['fpath'])

def read_work_table(file_name, **kw):
    rows = excel_to_dicts(file_name,
        headers_names = [
            'Наименование ККН',
            'ОКПД2',
            'Средняя цена включая НДС, руб.',
            'Цена 4 квартал 2023 года'
        ],
        headers = False)

    # for el in rows:
    #     print(el) if el['Наименование ККН'] else continue

    results = []
    DB_API = Data_base_API()

    for el in rows[:]:
        if el['Наименование ККН'] == None:
            continue
        kkn_name = el['Наименование ККН']
        product_name = " ".join(kkn_name.split(" ")[:-2])
        okpd_2 = el['ОКПД2']
        # price = el['Средняя цена включая НДС, руб.']
        price = el['Цена 4 квартал 2023 года']
        per_cent = 0.3
        min_price = price * (1 - per_cent)
        max_price = price * (per_cent + 1)

        products_by_okpd = search_products(
            okpd_2 = okpd_2,
            min_price = min_price,
            max_price = max_price)


        # products_by_okpd = set(products_by_okpd) if products_by_okpd else set()

        products_by_name = search_products(
            name = product_name,
            min_price = min_price,
            max_price = max_price)
        # print([products_by_okpd])
        # print([products_by_name])
        products_by_okpd = products_by_okpd | products_by_name
        print(kkn_name, price)#product_name,
        if products_by_okpd:
            for el in products_by_okpd:
                # print("SQL: ", el, el.okpd_2) #, kkn_name
                contr = DB_API.contrant_cards.select(number = el.contrant_card_id)
                data = {
                    'Наименование ККН': kkn_name,
                    'ОКПД2': okpd_2,
                    'Средняя цена включая НДС, руб.': price,
                    'Наименование закупки': el.name,
                    'Цена закупки': el.price,
                    'Наименование контракта': str(el.contrant_card_id) + contr.date.strftime(" от %d.%m.%Y"),
                    'Ссылка': f'https://zakupki.gov.ru/epz/contract/contractCard/document-info.html?reestrNumber={el.contrant_card_id}'
                }
                # print(data)
                results.append(data)
        print()

    dicts_to_excel(results, kw['fpath'])
