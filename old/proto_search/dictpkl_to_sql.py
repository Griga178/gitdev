import sqlite3
import pickle

'''
сохранение словаря из файла pkl в таблицу SQL

SQL БАЗЫ:
ОСНОВНАЯ

SQL ТАБЛИЦЫ:
    КОНТРАКТЫ:
        CONTRACT_NUMBER
        COMPANY_ID
    КОМПАНИИ:
        COMPANY_ID
        ИМЯ
        ИНН
        ПОЧТА
        ...
    ТОВАРЫ:
        PRODUCT_ID
        ИМЯ
        ОКПД2
        КТРУ
        ЦЕНА
        ...
        CONTRACT_NUMBER
'''


#full_dict = {'2780400937321000263': ({'1 Ортодонтические кусачки': {'ОКПД2': '32.50.11.190', 'Цена за единицу': 321.0}},
#{'2 биологические кусачки': {'ОКПД2': '32.50.11.190', 'Цена за единицу': 321.0}})}


def pkl_set_reader(file_name):
    '''Чтение файла .pkl'''
    with open(file_name, 'rb') as f:
        pickle_dict = pickle.load(f)
    return pickle_dict

products_table = '''CREATE TABLE products (
                            product_id integer primary key,
                            product_name text not null,
                            product_country text,
                            okpd_num text not null,
                            ktru_num text,
                            product_type text,
                            product_quantity real,
                            product_type_quantity text,
                            price real not null,
                            product_tax_type text,
                            product_sum real,
                            contract_id text not null
                            )'''
file_name = 'Parsing/contract_union_of_dicts.pkl'
full_dict = pkl_set_reader(file_name)

con = sqlite3.connect('product_base.db')

cur = con.cursor()

#cur.execute(products_table)

def write_to_db():
    # Запись pkl в db ФАЙЛ
    count = 0
    for number in full_dict:
        count += 1
        print(count, number)
        list_name_char = full_dict[number] # содержимое номера (tuple)
        for dict_in_list in list_name_char: # перебор товаров (dict)
            for elem in dict_in_list:
                product_name = elem.replace('"', '')
                try:
                    cur.execute(f'''INSERT INTO products
                            (product_name, product_country, okpd_num, ktru_num, product_type, product_quantity, product_type_quantity, price, product_tax_type, product_sum, contract_id)
                            VALUES ("{product_name}", "{dict_in_list[elem].get('Страна происхождения')}", "{dict_in_list[elem].get('ОКПД2')}", "{dict_in_list[elem].get('КТРУ')}", "{dict_in_list[elem].get('Тип объекта')}",
                                "{dict_in_list[elem].get('Количество')}", "{dict_in_list[elem].get('Количество, ЕД. ИЗМ.')}", "{dict_in_list[elem].get('Цена за единицу')}", "{dict_in_list[elem].get('Ставка НДС:')}", "{dict_in_list[elem].get('Сумма')}", {number});''')
                except:
                    print(' Не удалось')

    con.commit()


#write_to_db()
def print_db():
    user_select_0 = '''select * from products'''
    for row in cur.execute(user_select_0):
        print(row)

print_db()

con.close()
