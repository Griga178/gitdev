from excel import excel_to_dicts
from database import Data_base_API


def search_products(**kwargs):
    DB_API = Data_base_API()
    return DB_API.products.select_spec(**kwargs)

def read_query_xlsx(file_name):
    # Смотрим что будем искать в бд

    rows = excel_to_dicts(file_name,
        headers_names = [
            'Наименование ККН',
            'ОКПД2',
            'Средняя цена включая НДС, руб.',
        ],
        headers = False)


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
                print("SQL: ", el, el.okpd_2) #, kkn_name


        print()
