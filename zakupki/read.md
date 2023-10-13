Парсим контракты с сайта zakupki.gov.ru


0 settings.py
  Выбор даты
  Скачать актуальный драйвер

1 app.py
  Скачиваем номера контрактов

2 app2.py
  Скачиваем инфу по закупленным товарам в контракте


Процесс парсинга номеров:
  составления списка дат для поиска
  выставление фильтров на сайте
  проход по страницам пока они не закончатся

Процесс парсинга инф-и из карточки:
  выгрузка контрактов из БД, на которые не ссылаются товары (не парсились)




Настройка миграций Бд

установка:
pip install alembic
инит в папку "migration"

py -m alembic init migration

указываем путь до БД
в alembic.ini
sqlalchemy.url = sqlite:///C:/Users/G.Tishchenko/Desktop/myfiles/zakupki.db

импортируем + подключаем Метаданные от sqlalchemy в migration/env.py
from db import *
target_metadata = Base.metadata

Создаем версию БД
py -m alembic revision --autogenerate -m 'initial'

внесение изменений
1 вносим изменения в модель
2 создаем автоматическую миграцию:
   py -m alembic revision --autogenerate  -m "comment"
3 вноси руками в новый созданый файл в папке versions
4 запуск
  -m alembic upgrade 91123912person add second_name.py
 вносятся изменения в sql таблице

 py -m alembic revision --autogenerate  -m "person add phone"
