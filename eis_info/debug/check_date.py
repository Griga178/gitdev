"""
Итог:
в БД есть 2 контракта, которые не находятся при повторном парсинге.
на сайте ошибка в адресе местонахождения заказчика, первый раз почему то
прокатило, нашлось по фильтру СПБ. Сейчас по фильтру Ненецкий АО

0372200162026000049 -> Российская Федерация, 191028, Ненецкий АО, Моховая ул, Д.38

у СПБ ГБУ "..." неверный адрес (неточный, м.б. изменился)
код не меняем, данных для анализа достаточно

ДЕЛО ЗАКРЫТО!
"""

if __name__ == "__main__":

    import os
    import sys
    import duckdb
    import datetime
    import requests


    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from parser.e_fetcher import EisFetcher
    from parser.search_res_parser import parse_contract_reestr

    # вывод запроса param для url
    date = datetime.datetime.strptime('2026/04/08', '%Y/%m/%d').date()

    # количество контрактов с этой Датой
    db_path = '../database/analytics.duckdb'
    query = """
            SELECT COUNT(*) FROM order_cards WHERE placement_date = ?
        """
    with duckdb.connect(db_path) as conn:
        resp = conn.execute(query, (date,)).fetchone()[0]

    print("Контрактов в БД 2026.04.08", resp) # 1100 шт

    # запрос для парсера
    fetcher = EisFetcher()
    params = fetcher.prepare_params([{"publishDateFrom":date.strftime('%d.%m.%Y')}])[0]
    req = requests.Request('GET', fetcher.url, params=params)
    prepared = req.prepare()
    print(prepared.url)

    # в первом запросе "более 1000 записей"
    # во втрором запросе с priceFromGeneral=5000000 "99 записей"
    # 2 контракта из первого запроса (с ценой 5000000) попали во второй,
    # общее количество контрактов : 1097 (1000+99-2)

    query = f"SELECT placement_date, contract_number, total_price FROM order_cards WHERE placement_date = ?"
    with duckdb.connect(db_path) as conn:
        resp = conn.execute(query, (date,)).fetchall()

    resp_sorted = sorted(resp, key=lambda x: x[2])

    cnt = 0

    for i in resp_sorted:
        cnt += 1
        # print(cnt, i)

    # lenght = set([i[1] for i in resp])
    # print(len(lenght))
    db_contract_numbers = set([i[1] for i in resp])

    # надо найти 2 "лишних" контракта
    parsed_contract_numbers = set()
    # частично запускаем парсер
    session = requests.Session()

    response = requests.get(fetcher.url, params=params,headers = fetcher.HEADERS)
    data = parse_contract_reestr(response.text)
    for i in data['data']:
        parsed_contract_numbers.add(i['contract_number'])
    print('1', data['amount'], data['max'], data['min'], len(data['data'])) # 500 шт

    params['pageNumber'] = 2
    response = requests.get(fetcher.url, params=params,headers = fetcher.HEADERS)
    data = parse_contract_reestr(response.text)
    for i in data['data']:
        parsed_contract_numbers.add(i['contract_number'])
    print('2', data['amount'], data['max'], data['min'], len(data['data'])) # 500 шт

    params['pageNumber'] = 1
    params['priceFromGeneral'] = data['max']
    response = requests.get(fetcher.url, params=params,headers = fetcher.HEADERS)
    data = parse_contract_reestr(response.text)
    for i in data['data']:
        parsed_contract_numbers.add(i['contract_number'])
    print('3', data['amount'], data['max'], data['min'], len(data['data'])) # 99 шт

    print('отпарсили контрактов', len(parsed_contract_numbers))

    # эти номера есть в БД но не парсятся
    print('лишние номера', db_contract_numbers - parsed_contract_numbers)
    # лишние номера {'0372200162026000049', '0372200193126000018'}
