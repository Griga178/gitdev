## Куча разных функций

## Основные

+ 4_1n.py - создание скриншотов с ручным вводом цены
+ atest.py - создание всех скриншотов по ссылкам файла
  1 пронумеровать ссылки в файле (имя для скриншота INTEGER)
  2 вынести столбцы: "Ссылка", "Номер скрина", "Цена" --> на "Лист2"


./excel_funcs - чтение excel, openpyxl + выбор столбцов, заголовка

./js_project - html + js - есть таблица с пагинацией

./my_folder - функции для управления папками
    ...есть норм, для сохранения повторов: имя(1).txt, имя(2).txt

./parser веб интерфейс парсера - самый первый, не доделан

./scr_maker - создание скриншотов с помощью webbrowser

./tests
  чтение xmlx каталога xcom.ru --> excel
  yandex тесты
  запуск через drop
  math root
  uniq_file

./work_data_base
  SQLAlchemy - ТАБЛИЦЫ - SQL ЗАПРОСЫ
    Link
    Company
    Website

./work_objects - классы для работы:
    Link_viewer - Обработка ссылок
    Source - обработка строки из рабочей таблицы
      сохранение+вывод ссылок доменов компаний



.1n.py - парсим названия цены прямо из рабочей таблицы
.2n.py - настройка доменов для парсинга (пробный парсинг)


.4_1n.py
.8n.py - вставка .jpg --> .word по списку из excel
.9n.py - test 8n
.10n.py - загрузка файлов в СЭД
.11n.py - меняет имена компаний в СЭД
.12n.py - изменение названия файлов по списку (old -> new)
.13n.py - поиск инфы по компании по инн (egrul.nalog.ru)
.14n.py - замена .12n.py
.15n.py - замена .12n.py  и 14.py
.16_comp.py
.16_n.py - СВЕРКА скриншотов в папке и номеров в excel
.16n.py
.20n.py
aexif.py - втсавка/изменение мета инфы в jpg файлах
план:
|-- objects - все классы для работы
|--|-- /sqlalch_tables - хранимые в sql классы

|-- parser - ?
|-- file_manager - ?
|-- screenshots - ?
|-- SED_helper - ?

|-- settings
    место хранения sql
    пароли
    пути к рабочим папке
    драйвер для selenium
