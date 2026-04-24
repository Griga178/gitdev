import datetime
import time

from db_utils.db_core import DataBase
from db_utils.reestr_utils import prepare_search_res_data_to_db
from db_utils.reestr_insert import insert_parsed_data

from parser.parser_utils import (
    generate_parse_dates,
    generate_parse_dates_repair
)
from parser import parse_contract_numbers

DB_PATH = "database/analytics.duckdb"
# дата для новой БД
START_DATETIME = datetime.datetime.strptime('2023/01/01', '%Y/%m/%d').date()
# 3 минуты на 10 дней -> v1 3тыс/мин -> v2 9 тыс/мин
# 9 мин 30 дней (2 минуты - парсинг) / 60дн- 8 мин (20т стр)/ 122дн (73т стр) -26 vby
# v2 90 дат (40т стр) 4,5 мин (втсавка 50 сек)/ 73т строк 7 мин
# v2 + semaphore 10, fetch_chunk 100: 365дн-165тыс строк 14,4 мин 11 тыс/мин
db = DataBase()
# Начало общего таймера
start_total = time.perf_counter()

# 1 формируем список дат для парсера
# last_parsed_day = db.get_last_parsed_day()
# parse_dates = generate_parse_dates(last_parsed_day, START_DATETIME)

print(f"Подготовка дат: {time.perf_counter() - start_total:.2f} сек")
parsed_days = db.get_parsed_days()
parse_dates = generate_parse_dates_repair(parsed_days, START_DATETIME)
print(f"Ищем {len(parse_dates)} дат:")
print(parse_dates)
# db.show_summary() # для просмотра будущего парсинга
# quit()

# 2 ассинхронный парсинг контрактов по датам
print(f"Парсинг: {time.perf_counter() - start_total:.2f} сек")
list_to_insert = parse_contract_numbers(parse_dates)
# print(list_to_insert)
# quit()
total_c = 0
for i, d in enumerate(list_to_insert):
    cur_c = len(d.get('data', []))
    total_c += cur_c
    # print(f"Запрос {i}: количество элементов = {cur_c}")

print('Количество сделанных запросов', len(list_to_insert))
print(f"Общее количество элементов: {total_c}")


# обработка результатов парсинга для вставки в sql
print(f"Подготовка данных: {time.perf_counter() - start_total:.2f} сек")
insert_data = prepare_search_res_data_to_db(list_to_insert)

# 3 сохраняем результаты в БД
print(f"Загрузка в БД: {time.perf_counter() - start_total:.2f} сек")
insert_parsed_data(db, insert_data)

# просмотр результатов
db.show_summary()

print(f"Общее время выполнения: {time.perf_counter() - start_total:.2f} сек")
