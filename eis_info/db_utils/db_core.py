import duckdb
import os
import csv
import tempfile

# Определяем абсолютный путь к папке, где лежит этот файл
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class DataBase:

    def __init__(self, db_path=None, schema_path=None):

        if db_path is None:
            self.path = os.path.join(BASE_DIR, "..", "database", "analytics.duckdb")
        else:
            self.path = db_path

        # Путь к create.sql: ../sql/create.sql
        if schema_path is None:
            create_query_script = os.path.join(BASE_DIR, "..", "sql", "create.sql")
        else:
            create_query_script = schema_path

        # create_query_script = "../sql/create.sql"
        # self.path = PATH
        # 1. проверка есть ли папка "db_files" - создаем
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

        with duckdb.connect(self.path) as conn:

            with open(create_query_script, 'r', encoding='utf-8') as f:
                query = f.read()

            conn.execute(query)

    def get_info(self):
        """ выводит описание созданных таблиц sql """

        with duckdb.connect(self.path) as conn:
            tables = conn.execute("SHOW TABLES").fetchall()
            if not tables:
                print("Нет таблиц в базе данных")
            else:
                for table_row in tables:
                    table_name = table_row[0]
                    print(f"\nТаблица: {table_name}")
                    # описание столбцов
                    desc = conn.execute(f"DESCRIBE {table_name}").fetchall()
                    for col in desc:
                        col_name, col_type, nullable, key, default, extra = col
                        print(f"  {col_name}: {col_type} (nullable={nullable})")

    def get_last_parsed_day(self):
        """ возвращает последнюю успешную дату парсинга """
        query = """
            SELECT date FROM parser_data
            WHERE is_parsed=TRUE
            ORDER BY date DESC
            LIMIT 1;
            """
        with duckdb.connect(self.path) as conn:
            date = conn.execute(query).fetchone()

        return date[0] if date else None

    def get_parsed_days(self):
        """ возвращает все успешные дату парсинга """
        query = """
            SELECT date FROM parser_data
            WHERE is_parsed=TRUE
            ORDER BY date DESC
            """
        with duckdb.connect(self.path) as conn:
            return conn.execute(query).fetchall()


        return date[0] if date else None
    def insert_consumers(self, consumers_d):
        """
            consumers_d - кортежи (name:str, eis_id:[str,None])
        """
        # удаляем (None, ...)
        consumers = [item for item in consumers_d if not item[0] is None]
        query = """
            INSERT INTO consumers (name, eis_id) VALUES (?, ?)
            ON CONFLICT (name) DO UPDATE
            SET eis_id = EXCLUDED.eis_id
            WHERE consumers.eis_id IS NULL
            """

        with duckdb.connect(self.path) as conn:
            conn.executemany(query, consumers)

            names = [c[0] for c in consumers]

            query = "SELECT id, name FROM consumers WHERE name = ANY(?)"
            rows = conn.execute(query, (names,)).fetchall()
            return rows

    def insert_order_cards(self, order_tuples):
        query = """
            INSERT INTO order_cards (
                contract_number, contract_type, placement_date, end_date, update_date,
                name, consumer_id, total_price, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT (contract_number) DO NOTHING
            """

        with duckdb.connect(self.path) as conn:
            conn.executemany(query, order_tuples)

    def insert_parser_data(self, dates):
        query = """
            INSERT INTO parser_data (date, card_amount, card_parsed, queries_params, is_parsed)
            VALUES (?, ?, ?, ?, ?)
            """

        with duckdb.connect(self.path) as conn:
            conn.executemany(query, dates)

    def show_summary(self, limit=1):
        """
        Выводит для каждой таблицы:
        - количество строк
        - последние 5 строк (с сортировкой по убыванию первичного ключа или даты)
        """
        with duckdb.connect(self.path) as conn:
            # Получение списка таблиц (без системных)
            tables = conn.execute("SHOW TABLES").fetchall()
            if not tables:
                print("Нет таблиц в базе данных")
                return

            for (table_name,) in tables:
                print(f"\n=== Таблица: {table_name} ===")
                # Количество строк
                cnt = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
                print(f"Количество строк: {cnt}")

                if cnt == 0:
                    print("(нет данных)")
                    continue

                # Пытаемся определить подходящий столбец для сортировки
                # Получим список столбцов и их типы
                columns = conn.execute(f"DESCRIBE {table_name}").fetchall()
                col_names = [col[0] for col in columns]

                # Определим порядок:
                # 1) если есть 'id' -> ORDER BY id DESC
                # 2) если есть 'date' (например, в parser_data) -> ORDER BY date DESC
                # 3) если есть 'placement_date' (в order_cards) -> ORDER BY placement_date DESC
                # 4) иначе просто ORDER BY 1 (первый столбец)
                order_col = None
                if 'id' in col_names:
                    order_col = 'id DESC'
                elif 'date' in col_names:
                    order_col = 'date DESC'
                elif 'placement_date' in col_names:
                    order_col = 'placement_date DESC'
                else:
                    order_col = '1 DESC'  # первый столбец

                query = f"SELECT * FROM {table_name} ORDER BY {order_col} LIMIT {limit}"
                try:
                    rows = conn.execute(query).fetchall()
                    print("Последние 5 строк (от новых к старым):")
                    for row in rows:
                        # Формируем строку для печати
                        row_str = ', '.join(str(v) for v in row)
                        print(f"  {row_str}")
                except Exception as e:
                    print(f"Не удалось получить последние строки: {e}")

    def _write_csv(self, data, columns, temp_file):
        """Записывает список кортежей в CSV-файл (временный)."""
        with open(temp_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(columns)   # заголовок
            writer.writerows(data)

    def bulk_insert_order_cards(self, order_tuples):
        """
        Вставка данных order_cards.
        Загружаем во временную таблицу, затем INSERT ... ON CONFLICT.
        """
        if not order_tuples:
            return

        columns = ['contract_number', 'contract_type', 'placement_date', 'end_date',
                   'update_date', 'name', 'consumer_id', 'total_price', 'status']

        # Временный CSV
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='', encoding='utf-8') as tmp:
            self._write_csv(order_tuples, columns, tmp.name)
            tmp_path = tmp.name

        try:
            with duckdb.connect(self.path) as conn:
                # Создаём временную таблицу без ограничений
                conn.execute("CREATE TEMP TABLE tmp_order_cards AS SELECT * FROM read_csv('{}', HEADER=TRUE)".format(tmp_path))
                # Вставляем, игнорируя дубликаты по contract_number
                conn.execute("""
                    INSERT INTO order_cards (contract_number, contract_type, placement_date, end_date,
                                             update_date, name, consumer_id, total_price, status)
                    SELECT contract_number, contract_type, placement_date, end_date,
                           update_date, name, consumer_id, total_price, status
                    FROM tmp_order_cards
                    ON CONFLICT (contract_number) DO NOTHING
                """)
                # Временная таблица удалится автоматически после выхода из контекста
        finally:
            os.unlink(tmp_path)



if __name__ == "__main__":
    from tests import (
        test_insert_consumers,
        test_insert_order_cards,
        test_insert_parser_data
        )
    # Инициализация базы данных (создаст таблицы, если их нет)
    db = DataBase()

    # test_insert_consumers(db)
    # test_insert_order_cards(db)
    # test_insert_parser_data(db)
