from typing import List
from .search_res_parser import parse_contract_reestr
from .e_fetcher import EisFetcher
from .parser_utils import (
    generate_parse_dates,
    split_query_param
)

def parse_contract_numbers(parse_dates: List):
    """
    отправляем запросы, обрабатываем данные
    INPUT:
        parse_dates = ['dd.mm.yyyy', ... ]

    RETURN:
        list_to_insert = [
        {
            'date':str - дата из фильтра запроса
            'query_param': {} - параметры фильтра текущего запроса
            'amount': int - количество контрактов в запросе (после 1000 - округляется)
            'data': [{}, ...] - инфа по каждому контракту 'contract_number', ...
            'max': float,  'min': float - минимум и максимум в текущем запросе
        },
        {
            # неудачный запрос
            'date':str - дата из фильтра запроса
            'query_param': {} - параметры фильтра текущего запроса
            'query_param' - содержит "resp_status", который удаляется
             и выносится в error_message
        },     ... ]
    """
    e_fetcher = EisFetcher()

    params_for_parser = [{'publishDateFrom': i, 'publishDateTo': i} for i in parse_dates]
    list_to_insert = []
    # содержит инфу для оптимизации запросов. {date:{amount:, min:, max:, ranges: []}}
    unlimited_dates = {}
    while params_for_parser:
        new_params_for_parser = []
        responses = e_fetcher.fetch_all(params_for_parser)

        for param, html in responses:
            query_date = param['publishDateFrom']

            if not html:
                # в этот раз пропускаем даты
                resp_stat = f'resp_status:{param["resp_status"]}'
                param.pop('resp_status')
                list_to_insert.append({
                    'date': query_date,
                    'query_param': param,
                    'error_message' : resp_stat
                })
                continue

            data = parse_contract_reestr(html)
            data['date'] = query_date
            data['query_param'] = param

            """ пример
             data = {'amount': int, 'data': list[], 'max': float, 'min': float}
            """

            if data['amount'] <= 500:
                # отправляем на сохранение
                list_to_insert.append(data)
            elif data['amount'] < 1000:
                # отправляем на сохранение + второй запрос
                list_to_insert.append(data)
                new_qery_param = param.copy()

                if new_qery_param['pageNumber'] == '1':
                    new_qery_param['pageNumber'] = '2' # изменяем параметры запроса
                    new_params_for_parser.append(new_qery_param)

            elif data['amount'] < 2000:
                # отправляем на сохранение + второй запрос
                list_to_insert.append(data)
                new_qery_param = param.copy()

                if new_qery_param['pageNumber'] == '1':
                    new_qery_param['pageNumber'] = '2' # изменяем параметры запроса
                else:
                    new_qery_param['pageNumber'] = '1'
                    # после ограничения по цене amount должно уменьшиться на 1000
                    new_qery_param['priceFromGeneral'] = str(data['max'])
                new_params_for_parser.append(new_qery_param)

            else:
                # результат более 2000
                # отправляем на сохранение 500 шт
                list_to_insert.append(data)

                amount = data['amount']
                min = data['min']
                max = data['max']

                new_qery_param = param.copy()

                # парсим вторую страницу либо с начала, либо с конца
                if new_qery_param['pageNumber'] == '1':
                    new_qery_param['pageNumber'] = '2' # изменяем параметры запроса

                    if query_date not in unlimited_dates:
                        # если это первый проход с начала
                        unlimited_dates[query_date] = {'total_amount':amount, 'step': 1}

                    new_params_for_parser.append(new_qery_param)

                else:
                    # закончили второй проход

                    new_qery_param['pageNumber'] = '1'
                    if unlimited_dates[query_date]['step'] == 1:
                        # прошли с начала -> меняем сортировку
                        unlimited_dates[query_date]['step'] = 2
                        # минимальная цена для разбивки
                        unlimited_dates[query_date]['min'] = max
                        new_qery_param['sortDirection'] = 'false'
                        unlimited_dates[query_date]['query'] = new_qery_param
                        new_params_for_parser.append(new_qery_param)
                    else:
                        # уже отпарсили первую и последнюю тысячу
                        # в надежде, что количество контрактов за 1 день с одной ценой
                        # не превышает 1000 шт, разбиваем запросы по цене и заканчиваем
                        # у новых запросов количество должно быть менее 1000
                        split_min_price = max
                        split_max_price = unlimited_dates[query_date]['min']
                        new_qery_param['sortDirection'] = 'true'
                        amount = unlimited_dates[query_date]['total_amount'] - 2000
                        new_params_for_parser += split_query_param(amount, split_min_price, split_max_price, new_qery_param)

        params_for_parser = new_params_for_parser

    return list_to_insert
