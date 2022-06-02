# from flask_funcs.module_data_base.sql_tables.tables_file import *
from flask_funcs.module_data_base.sql_tables.tables_web import *

from sqlalchemy import MetaData

metadata = MetaData()

my_base = 'sqlite:///test_base_ver_1.db'

engine = create_engine(f'{my_base}?check_same_thread=False')

Base.metadata.create_all(engine)

'''
Таблицы:
    Ссылки
    Парсинг ссылки
    Настройки сайта
    Сайты
    ККН-ы
    Модели предметов
    Предметы

    Загруженные файлы
    файл-ссылка

Эталон:
    1 файл:        tables_subject
        Предметы
        Названия предметов (синонимы) - Предмет
        Модели                  -Предмет

    2 файл:        tables_chars
        Названия характеристик
        Единицы измерения

    3 файл:        tables_companies
        Компании
        **Инфа компании

    4 файл:        tables_web
        Сайты
        * Типы сайтов
        Настройки магазинов     -Сайт
        * Типы настроек
        Ссылки                  -Сайт, Модель
        * Типы ссылок
        Парсинг ссылки          -Ссылка

    5 файл:        tables_CMEC
        ККН-ы                   -Часть, КТРУ, ОКПД (+ детализация)
        КТРУ
        Характеристики КТРУ
        Части
        ОКПД
        Характеристики ККН-а    -ККН


    6 файл:        tables_zakupki
        Закупки                 -Компания, Ссылка
        (M to M)
        Закупки     - Модель - Цена - ОКПД - КТРУ

    *файл:        tables_file
        Loaded_files

    связи(Many to Many):
    7 файл:        tables_connections
        Файл    -   ссылка
        ККН     -   ссылка

        Компания    - сайт
        Компания    - модель

        Предмет     - характеристика
        Модель      - характеристика - значение
        Предмет(id) - Предмет (child_id)



'''
