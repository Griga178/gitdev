Описание:

./settings - теги для парсинга - старое, использ в 2n.py

./sql - парсинг ЕАИС и поиск по скачанным в sql:

./test_pro - фигня с selenium & СЭД:

./tests - временно:
  чтение xmlx каталога xcom.ru
  прочее

./work_objects - классы для работы:
  Link
  Domain
  Company
  KKN
  Source
  ...

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
