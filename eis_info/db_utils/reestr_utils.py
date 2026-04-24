import json
from datetime import datetime

def prepare_search_res_data_to_db(parser_data):

    """
    INPUT LIST [
        Dict{
        'date':str - дата из фильтра запроса -> меняем тип в date
        'query_param': {} - словарь параметров get запроса -> в строку json
        'data': contracts, - сортируем, содержание см.ниже
        'amount': int - количество контрактов в запросе (после 1000 - округляется)
        ...,
        other_data,...},
        {
            # неудачный запрос - нет ключа "data"
            'date':str - дата из фильтра запроса
            'query_param': {} - параметры фильтра текущего запроса
            'resp_status' - статус ответа сервера (не 200)
        }, ...
    ]

    contracts = list[dict]: список контрактов, каждый с полями:
        - contract_type: тип закупки
        - contract_number: номер закупки
        - object: объект закупки
        - customer: заказчик
        - customer_id: id в системе eis
        - start_price: начальная цена (число или строка)
        - published_date: дата размещения
        - updated_date: дата обновления
        - submission_deadline: окончание подачи заявок
        - order_stage: Этап закупки


    RETURN
        данные для вставки в таблицы
        {
        dates: (
            date:datetime,
            card_amount:int,        # кол-во из response
            card_parsed:int,        # фактическое кол-во
            is_parsed:bool,         # false если не все отпарсилось
            queries_params:str,     # Список простых словарей
            ),
        cards: (
            contract_number:str,
            contract_type:str,
            published_date:datetime,
            submission_deadline:datetime,
            updated_date:datetime,
            object:str,
            consumer_name:str,      # замена на consumer_id
            start_price:float,
            order_stage:str
        ),
        consumers: (
            name:str,
            eis_id:str,
        ),
        }

    порядок вставки в БД:
        1 вставить всех consumers получить id
        2 вставить все контракты с consumer_id
        3 вставить все даты
    """
    def parse_date(date_str):
        if not date_str:
            return None
        try:
            # ожидаем формат dd.mm.yyyy
            return datetime.strptime(date_str, '%d.%m.%Y').date()
        except:
            return None

    dates = {}
    cards = set()
    consumers = set()

    for pd in parser_data:
        date = parse_date(pd['date'])

        if date not in dates:
            dates[date] = {
                'card_amount': pd.get('amount', 0),
                'card_parsed': 0,
                'queries_params': [],
                'is_parsed': True
            }
        dates[date]['queries_params'].append(pd['query_param'])

        if pd.get('amount', 0) > dates[date]['card_amount']:
            # результаты могут быть не попорядку
            # если были доп запросы с фильтрами,
            # то кол-во заявок в эти даты меньше
            dates[date]['card_amount'] = pd['amount']

        if pd.get('resp_status'):
            # неудачный запрос
            dates[date]['is_parsed'] = False
        else:

            for card in pd['data']:
                # Заказчики
                consumers.add((card['customer'], card['customer_id']))

                # Карточка заявки
                card_tuple = (
                    card['contract_number'],
                    card['contract_type'],
                    parse_date(card['published_date']),
                    parse_date(card['submission_deadline']),
                    parse_date(card['updated_date']),
                    card['object'],
                    card['customer'], # замена на consumer_id
                    # market_id - не в этот раз
                    # products_count - не в этот раз
                    card['start_price'],
                    card['order_stage']
                )
                cards.add(card_tuple)

                # результат парсинга
                dates[date]['card_parsed'] += 1


    date_tuples = set()

    for key, val in dates.items():
        val['queries_params'] = json.dumps(val['queries_params'], ensure_ascii=False)
        date_tuples.add((
            key,
            val['card_amount'],
            val['card_parsed'],
            val['queries_params'],
            val['is_parsed'],
        ))

    return {'dates': date_tuples,'consumers': consumers, 'cards': cards}
