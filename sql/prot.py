'''
тут sqlite бд прототипов "процессоров"
- отпарсить кучу сайтов с процессорами - функция + полу/автомат
- вывести уникальные характеристики - функция + полу/автомат
- сделать категорию - функция
- распределить на типы по ценам и другим
 влиятельным характеристикам - функция
- отобразить нужное на сайте
'''

# Построение базы данных

table_prototype_names = '''CREATE TABLE prototypes (
                            id integer primary key,
                            name text not null
                            )'''

table_prototype_chars = '''CREATE TABLE prot_chars (
                            prot_id integer,
                            name text not null,
                            value text not null
                            )'''

list_names = ['AMD A10-9700']
list_chars = [(1, 'Артикул производителя (Part Number)', 'AD970BAGABMPK'),
                (1, 'Частота процессора', '3.5 ГГц'),
                (1, 'Модельный ряд', 'AMD A10-Series'),
                (1, 'Количество ядер', '4'),
                (1, 'Количество потоков', '4')]

import sqlite3
#con = sqlite3.connect("file::memory:?cache=shared", uri=True)
con = sqlite3.connect(":memory:")
cur = con.cursor()

cur.execute(table_prototype_names)
cur.execute(table_prototype_chars)

for el in list_names:
    cur.execute(f'''INSERT INTO prototypes
                    (name)
                    VALUES ("{el}");''')

for el in list_chars:
    cur.execute(f'''INSERT INTO prot_chars
                    (prot_id, name, value)
                    VALUES {el};''')


con.commit()

user_select_0 = '''select * from prot_chars'''

user_select_1 = '''select * from prot_chars'''

for row in cur.execute(user_select_0):
        print(row)

con.close()
