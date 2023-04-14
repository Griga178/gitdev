'''
    обновляем рабочую таблицу
    1 - сохранить в бд компании - ссылки
    2 - настроить сайты для парсинга
    3 - запустить парсер
'''
# from work_data_base import
from excel_funcs import excel_to_list
from work_objects import Source
# ПРОЧИТАТЬ ФАЙЛ
work_table_path = 'C:/Users/G.Tishchenko/Desktop/3 кв 23/3 Нормирование.xlsx'
kwargs = {
    'sheet_name': 'Лист1',
    'headers': False,
    'headers_names': ['Источник ценовой информации', 'ИНН поставщика', 'Наименование поставщика', 'Ссылка']
    }

table_rows = excel_to_list(work_table_path, **kwargs)

links = []
for row in table_rows:
    source = Source(
        source_info = row[0],
        company_inn = row[1],
        company_name = row[2],
        links = row[3]
        )

    print(source)


# ВЫДЕЛИТЬ ОБЪЕКТЫ "Источник" (тип, компания, ссылка)

# ВЫДЕЛИТЬ ОБЪЕКТЫ ПРОТОТИПЫ

# ВЫДЕЛИТЬ ОБЪЕКТЫ ССЫЛКИ

# ДОМЕНЫ

# начало парсинга
# for link in links:
    # link.parsed()
