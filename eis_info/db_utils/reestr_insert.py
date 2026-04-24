
def insert_parsed_data(db, prepared_data: dict):
    """
    Вставляет подготовленные данные в таблицы DuckDB.
    prepared_data - результат функции prepare_search_res_data_to_db.
    """

    # 1. Вставка потребителей (name, eis_id)
    cons_rows = []
    if prepared_data['consumers']:
        cons_rows = db.insert_consumers(prepared_data['consumers'])
    # соответствие consumer_name -> id в словарь для ускорения
    consumer_cache = {}
    for row in cons_rows:
        id, name = row
        consumer_cache[name] = id

    # добавляем consumer_id в order_tuple`s
    order_tuples = []
    for card in prepared_data['cards']:
        (contract_number, contract_type, published_date, submission_deadline, update_date,
         object_name, consumer_name, start_price, order_stage) = card
        consumer_id = consumer_cache[consumer_name]
        order_tuples.append((contract_number, contract_type, published_date, submission_deadline, update_date,
              object_name, consumer_id, start_price, order_stage))

    # 2. Вставка контрактов
    # batch_size = 5000
    # for i in range(0, len(order_tuples), batch_size):
    #     chunk = order_tuples[i:i+batch_size]
    #     db.insert_order_cards(chunk)

    # 2.v2 Вставка контрактов
    db.bulk_insert_order_cards(order_tuples)

    # 3. Вставка данных парсера (parser_data)
    if prepared_data['dates']:
        db.insert_parser_data(prepared_data['dates'])
