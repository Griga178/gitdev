# https://docs.python.org/3/library/sqlite3.html


import sqlite3

#con = sqlite3.connect('example.db')

con = sqlite3.connect("file::memory:?cache=shared", uri=True)

cur = con.cursor()


system_list = ['Компьютер', 'Ноутбук', 'Оперативная память', 'Процессор', 'Видеокарта', 'Материнская плата']
char_list = ['Объем памяти', 'Скорость', 'Форм фактор', 'Размер диагонали']

sys_char_list = [(1, 1), (2, 4), (3, 1), (3, 2), (4, 1), (4, 2), (5, 1), (4, 2), (4, 3), (1, 3)]
sys_elem_list = [(1, 3), (1, 4), (1, 5), (1, 6), (2, 3), (2, 4), (2, 5), (2, 6), (6, 4), (6, 5)]




#PRAGMA foreign_keys=on;

table_system_name = "CREATE TABLE system_names (id integer primary key, system_name text not null)"

table_char = "CREATE TABLE char_names (id integer primary key, char_name text not null)"

table_sys_id_elem_id = '''CREATE TABLE system_elements
                        (system_id integer not null,
                        element_id integer not null,
                        FOREIGN KEY (system_id) REFERENCES system_names(id),
                        FOREIGN KEY (element_id) REFERENCES system_names(id))'''

table_sys_id_char_id = '''CREATE TABLE system_chars
                            (system_id integer not null,
                            char_id integer not null,
                            FOREIGN KEY (system_id) REFERENCES system_names(id),
                            FOREIGN KEY (char_id) REFERENCES char_names(id))'''


# Create table
cur.execute(table_system_name)
cur.execute(table_char)
cur.execute(table_sys_id_elem_id)
cur.execute(table_sys_id_char_id)


for el in system_list:
    cur.execute(f'''INSERT INTO system_names
                    (system_name)
                    VALUES ("{el}");''')

for el in char_list:
    cur.execute(f'''INSERT INTO char_names
                    (char_name)
                    VALUES ("{el}");''')

for el in sys_char_list:
    cur.execute(f'''INSERT INTO system_chars
                    (system_id, char_id)
                    VALUES {el};''')

for el in sys_elem_list:
    cur.execute(f'''INSERT INTO system_elements
                    (system_id, element_id)
                    VALUES {el};''')


con.commit()

select_1 = '''select system_name, char_name from system_names
            inner join system_chars on system_chars.system_id = system_names.id
            inner join char_names on char_names.id = system_chars.char_id;'''

select_2 = '''select system_name, system_name from system_names
            inner join system_elements on system_elements.system_id = system_names.id
            inner join system_names on system_name.id = system_elements.element_id;'''



user_select_0 = '''select * from system_names'''

user_list = []

print(f'Все системы:')
for row in cur.execute(user_select_0):
        print(row)

user_setup = int(input('Введите номер системы: \n'))


user_select_1 = f'''select id, element_id from system_names
                inner join system_elements on system_elements.system_id = system_names.id where id = {user_setup};'''

for row in cur.execute(user_select_1):
        user_list.append(row[1])

user_list.append(user_setup)
a = tuple(user_list)


user_select_2 = f'''select system_name, char_name from system_names
            inner join system_chars on system_chars.system_id = system_names.id
            inner join char_names on char_names.id = system_chars.char_id where system_id in {a};'''

print('Её характеристики и элементы и их характеристики: \n')

for row in cur.execute(user_select_2):
    print(row)

con.close()
