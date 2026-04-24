import datetime

def generate_parse_dates(db_date = None, default_date:datetime = None) -> list:
    """ Возвращает даты от стартовой до сегоднящней """

    iter_dates = []

    if db_date:
        # пока не обрабатывается
        iter_datetime = db_date
        # последняя успешная дата не парсится -> +day

    else:
        iter_datetime = default_date

    # while iter_datetime < datetime.datetime.now():
    while iter_datetime < datetime.date.today():

        p = (iter_datetime.strftime('%d.%m.%Y'))

        iter_dates.append(p)
        iter_datetime += datetime.timedelta(days=1)

    return iter_dates

def generate_parse_dates_repair(existing_dates_tuples, start_date: datetime.date) -> list[str]:
    """
    Возвращает список дат (строки '%d.%m.%Y'), которых нет в existing_dates_tuples,
    начиная с start_date до сегодняшнего дня.
    existing_dates_tuples: список кортежей, например [(datetime.date(2026,4,23),), ...]
    """
    existing_set = {row[0] for row in existing_dates_tuples} if existing_dates_tuples else set()
    today = datetime.date.today()
    current = start_date
    result = []
    while current <= today:
        if current not in existing_set:
            result.append(current.strftime('%d.%m.%Y'))
        current += datetime.timedelta(days=1)
    return result

def split_query_param(amount, min_price, max_price, param):
    """ разбивает один запрос на множество частей,
     что бы в каждом было не более 1000 шт"""
    if amount <= 0:
        return []
    queries = []

    # Количество интервалов (частей)
    num_parts = amount // 1000 + 3

    step = (max_price - min_price) / num_parts

    for i in range(num_parts):
        lower = min_price + i * step
        upper = min_price + (i + 1) * step

        if i == 0:
            # Первый интервал: нижняя граница открыта
            lower_str = ''
            upper_str = str(int(upper))          # верхняя граница включительно? Округляем вниз
        elif i == num_parts - 1:
            # Последний интервал: верхняя граница открыта
            lower_str = str(int(lower) + 1)      # следующая целая цена после предыдущей границы
            upper_str = ''
        else:
            # Промежуточные интервалы: обе границы указаны
            lower_str = str(int(lower) + 1)
            upper_str = str(int(upper))

        query = param.copy()

        query['priceFromGeneral'] = lower_str
        query['priceToGeneral'] = upper_str

        queries.append(query)

    return queries

if __name__ == "__main__":

    p1 = {'publishDateFrom': '20.04.2026', 'publishDateTo': '20.04.2026', 'default_params': 100}

    print(split_query_param(10000, 100, 100000, p1))
    # print(split_query_param(10000, 100, 100000, p1))
