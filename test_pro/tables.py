import sqlite3

'''База данных SQLite'''

''' Таблица с названиями ККН '''
kkn_names = '''CREATE TABLE kkn_names (
                            id integer primary key,
                            name_kkn text not null,
                            id_measures integer
                            )'''

''' Таблица с сылками на прототипы ККН-ов '''
kkn_proto_links = '''CREATE TABLE kkn_proto_links(
                            id integer primary key,
                            link text not null,
                            id_kkn integer not null,
                            id_comp integer
                            )'''

''' Таблица с данными о компанях '''
proto_salers = '''CREATE TABLE proto_salers(
                            id integer primary key,
                            comp_name text not null,
                            comp_inn text not null
                            )'''

''' Таблица с ценами (только сайты) '''
prices = '''CREATE TABLE prices(
                            price float not null,
                            screen_name text,
                            id_link integer not null,
                            screen_date date,
                            id_source integer
                            )'''

''' Таблица с характеристиками '''
kkn_chars = '''CREATE TABLE chars(
                            id_kkn integer not null,
                            chars text not null
                            )'''

''' Таблица с ед. изм. для ккн '''
measure = '''CREATE TABLE measures(
                            id integer not null,
                            measure text not null
                            )'''

''' Таблица с Источниками цен '''
price_source = '''CREATE table price_source (
                    id integer not null,
                    number text,
                    date date,
                    id_source_type integer,
                    id_company integer
                    )'''

''' Таблица с типами источников цен (О/Э/К) '''
source_type = '''CREATE table source_type (
                    id integer not null,
                    name text not null
                    )'''

kkn_names_list = [[1, "Ноутбук тип 1"], [2, "Ноутбук тип 2"], [3,"Ноутбук тип 3"], [4, "Ноутбук тип 4"]]

link_list = [[1, 1, 'https://www.onlinetrade.ru/catalogue/noutbuki-c9/acer/noutbuk_acer_extensa_15_ex215_32_c07z_nx.egner.007-2869084.html', 1],
            [2, 1, 'https://www.dns-shop.ru/product/8fe562f2fe2fc823/156-noutbuk-digma-c413-seryj/', 2],
            [3, 2, 'https://www.onlinetrade.ru/catalogue/noutbuki-c9/dell/noutbuk_dell_vostro_5301_5301_8372-2412225.html', 1],
            [4, 2, 'https://www.dns-shop.ru/product/a5abdef7a0f52ff1/14-noutbuk-asus-vivobook-s14-s433ea-am304t-cernyj/', 2],
            [5, 3, 'https://www.onlinetrade.ru/catalogue/noutbuki-c9/hp/noutbuk_hp_255_g8_3v5f3ea-2871934.html', 1],
            [6, 3, 'https://www.dns-shop.ru/product/27f93d1b8c4ed760/156-ultrabuk-msi-modern-15-a10m-638xru-seryj/', 2]]

proto_salers_list = [
                    [1, 'ОНЛАЙН ТРЕЙД ООО', '7735092378'],
                    [2, 'ДНС РИТЕЙЛ ООО', '2540167061'],
                    ]

price_list = [
[27300, '1.jpg', 1],
[21999, '2.jpg', 2],
[63900, '3.jpg', 3],
[51799, '4.jpg', 4],
[49500, '5.jpg', 5],
[49999, '6.jpg', 6]
]

con = sqlite3.connect(":memory:")
cur = con.cursor()

cur.execute(kkn_names)
cur.execute(kkn_proto_links)
cur.execute(proto_salers)
cur.execute(prices)
cur.execute(kkn_chars)


'''Функция заполнения таблицы ККН'''
for list in kkn_names_list:
    name = list[1]
    kkn_name_id = list[0]
    cur.execute(f'''INSERT INTO kkn_names
                    (id, name_kkn)
                    VALUES ("{kkn_name_id}", "{name}");''')

'''Функция заполнения таблицы Ссылок'''
for list in link_list:
    link_id = list[0]
    link = list[2]
    name_id = list[1]
    comp_id = list[3]
    cur.execute(f'''INSERT INTO kkn_proto_links
                    (id, id_kkn, link, id_comp)
                    VALUES ("{link_id}", "{name_id}", "{link}", "{comp_id}");''')
'''Функция заполнения таблицы Компаний'''
for list in proto_salers_list:
    id = list[0]
    name = list[1]
    inn = list[2]
    cur.execute(f'''INSERT INTO proto_salers
                    (id, comp_name, comp_inn)
                    VALUES ("{id}", "{name}", "{inn}");''')

'''Функция заполнения таблицы Цены'''
for list in price_list:
    price = list[0]
    screen = list[1]
    link_id = list[2]
    cur.execute(f'''INSERT INTO prices
                    (price, screen_name, id_link)
                    VALUES ("{price}", "{screen}", "{link_id}");''')

con.commit()


def print_sql_table(tables_name, what = '*'):
    str_excecute = f'select {what} from {tables_name}'
    for row in cur.execute(str_excecute):
            print(row)




str_excecute = 'select name_kkn, link from kkn_names join kkn_proto_links on kkn_proto_links.id_kkn = kkn_names.id'

str_excecute_2 = '''select name_kkn, comp_name, comp_inn, price from kkn_names
                    inner join kkn_proto_links on kkn_proto_links.id_kkn = kkn_names.id
                    left outer join proto_salers on kkn_proto_links.id_comp = proto_salers.id
                    inner join prices on prices.id_link = proto_salers.id
                    ''' #inner join proto_salers on kkn_proto_links.id_comp = proto_salers.id; , comp_name, comp_inn
for rows in cur.execute(str_excecute_2):
    print('')
    for el in rows:
        print(el, end = ' ')

#print_sql_table('prices')

con.close()
