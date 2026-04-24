import duckdb
from datetime import datetime

def test_insert_consumers(db):
    """ тест для insert_consumers """
    # Тестовые данные: список кортежей (name, eis_id)
    test_consumers = [
        ("ООО Тест1", "123456789"),
        ("ИП Тест2", None),
        (None, None),
        ("ЗАО Тест3", "987654321"),
        ("ИП Тест2", "12345"),
        ("ООО Тест1", "111111111"),  # дубликат имени, eis_id будет обновлён только если в БД был NULL
    ]
    print("=== Вставка тестовых потребителей ===")
    inserted = db.insert_consumers(test_consumers)
    print("Результат вставки (id, name):")
    for row in inserted:
        print(row)

    # Проверка, что дубликат имени не создал новую запись, а вернул существующую
    print("\n=== Все записи в таблице consumers после вставки ===")
    with duckdb.connect(db.path) as conn:
        all_consumers = conn.execute("SELECT id, name, eis_id FROM consumers ORDER BY id").fetchall()
        for row in all_consumers:
            print(row)

    # Удаление тестовых записей (по имени или id)
    # Предположим, что тестовые имена начинаются с "ООО Тест", "ИП Тест", "ЗАО Тест"
    delete_query = "DELETE FROM consumers WHERE name LIKE '%Тест%'"
    with duckdb.connect(db.path) as conn:
        conn.execute(delete_query)
        print("\n=== После удаления тестовых записей ===")
        remaining = conn.execute("SELECT id, name, eis_id FROM consumers").fetchall()
        if remaining:
            print("Оставшиеся записи:", remaining)
        else:
            print("Таблица consumers пуста.")

    # "сбрасываем" счетчик id таблицы consumers
    with duckdb.connect(db.path) as conn:
        # Принудительно удаляем последовательность со всеми зависимостями
        conn.execute(f"DROP SEQUENCE IF EXISTS consumer_id_seq CASCADE;")
        max_id = conn.execute("SELECT COALESCE(MAX(id), 0) FROM consumers").fetchone()[0]
        # Создаём последовательность заново, начиная со следующего числа
        conn.execute(f"CREATE SEQUENCE consumer_id_seq START {max_id + 1};")


def test_insert_order_cards(db):
    """ тест для insert_order_cards """
    # Шаг 1: подготовим consumers, чтобы получить id
    test_consumers = [
        ("ООО ТестПоставщик1", "111"),
        ("ИП ТестПоставщик2", None),
        ("ЗАО ТестПоставщик3", "333"),
    ]
    inserted_cons = db.insert_consumers(test_consumers)
    # Словарь для быстрого получения id по имени
    cons_id_by_name = {name: id for id, name in inserted_cons}

    # Шаг 2: подготовим order_tuples
    # Структура кортежа: (contract_number, contract_type, placement_date, end_date, update_date,
    #                    name, consumer_id, total_price, status)
    order_tuples = [
        ("CON001", "Госконтракт", datetime.strptime("31.12.2026", '%d.%m.%Y').date(), "2025-12-31", "2025-01-10",
         "Поставка товаров", cons_id_by_name["ООО ТестПоставщик1"], 1500000.00, "Исполнен"),
        ("CON002", "Договор", "2025-02-15", "2025-06-30", "2025-02-15",
         "Услуги", cons_id_by_name["ИП ТестПоставщик2"], 500000.00, "В работе"),
        ("CON003", "Госконтракт", "2025-03-01", "2025-09-30", "2025-03-01",
         "Оборудование", cons_id_by_name["ЗАО ТестПоставщик3"], 2500000.00, "Новый"),
        ("CON001", "Госконтракт", "2025-01-10", "2025-12-31", "2025-01-10",  # дублируем contract_number
         "Дубликат", cons_id_by_name["ООО ТестПоставщик1"], 0, "Не должен вставиться"),
    ]

    print("\n=== Вставка заказов ===")
    db.insert_order_cards(order_tuples)

    # Проверяем, что вставилось, а дубликат проигнорирован
    with duckdb.connect(db.path) as conn:
        rows = conn.execute("SELECT id, contract_number, placement_date, name, total_price, status FROM order_cards ORDER BY contract_number").fetchall()
        print("\n=== Содержимое order_cards после вставки ===")
        for row in rows:
            print(row)

        # Должно быть 3 уникальных контракта
        assert len(rows) == 3, f"Ожидалось 3 строки, получили {len(rows)}"
        # Проверим, что нет контракта CON001 с дублем
        duplicates = conn.execute("SELECT COUNT(*) FROM order_cards WHERE contract_number = 'CON001'").fetchone()[0]
        assert duplicates == 1, f"Дубликат контракта CON001 вставлен, а должен быть проигнорирован"

    # Шаг 3: очистка – удаляем вставленные заказы
    with duckdb.connect(db.path) as conn:
        conn.execute("DELETE FROM order_cards WHERE contract_number IN ('CON001', 'CON002', 'CON003')")
        # Удаляем тестовых потребителей
        conn.execute("DELETE FROM consumers WHERE name LIKE '%ТестПоставщик%'")
        print("\n=== Очистка выполнена ===")

    # "сбрасываем" счетчик id таблицы consumers
    with duckdb.connect(db.path) as conn:
        # Принудительно удаляем последовательность со всеми зависимостями
        conn.execute(f"DROP SEQUENCE IF EXISTS consumer_id_seq CASCADE;")
        max_id = conn.execute("SELECT COALESCE(MAX(id), 0) FROM consumers").fetchone()[0]
        # Создаём последовательность заново, начиная со следующего числа
        conn.execute(f"CREATE SEQUENCE consumer_id_seq START {max_id + 1};")

    # "сбрасываем" счетчик id таблицы order_cards
    with duckdb.connect(db.path) as conn:
        # Принудительно удаляем последовательность со всеми зависимостями
        conn.execute(f"DROP SEQUENCE IF EXISTS order_cards_id_seq CASCADE;")
        max_id = conn.execute("SELECT COALESCE(MAX(id), 0) FROM order_cards").fetchone()[0]
        # Создаём последовательность заново, начиная со следующего числа
        conn.execute(f"CREATE SEQUENCE order_cards_id_seq START {max_id + 1};")

def test_insert_parser_data(db):
    """ тест для insert_parser_data """
    # Тестовые данные: список кортежей (date, card_amount, card_parsed, queries_params, is_parsed)
    test_data = [
        ("2020-04-01", 100, 50, '[{"param1": "value1"}]', True),
        (datetime.strptime("02.04.2020", '%d.%m.%Y').date(), 200, 150, '[{"param2": "value2"}]', False),
        # ("2020-04-02", 200, 150, '[{"param2": "value2"}]', False),
        ("2020-04-03", 0, 0, '[]', True),
    ]
    print("\n=== Вставка тестовых данных в parser_data ===")
    db.insert_parser_data(test_data)

    with duckdb.connect(db.path) as conn:
        # Проверяем, что записи вставлены
        rows = conn.execute("""
            SELECT date, card_amount, card_parsed, queries_params, is_parsed
            FROM parser_data
            WHERE date IN ('2020-04-01', '2020-04-02', '2020-04-03')
            ORDER BY date
        """).fetchall()
        print("=== Содержимое parser_data после вставки ===")
        for row in rows:
            print(row)

        assert len(rows) == len(test_data), f"Ожидалось {len(test_data)} строк, получено {len(rows)}"

    # Очистка тестовых данных
    with duckdb.connect(db.path) as conn:
        conn.execute("DELETE FROM parser_data WHERE date IN ('2020-04-01', '2020-04-02', '2020-04-03')")
        print("=== Тестовые данные удалены ===")
