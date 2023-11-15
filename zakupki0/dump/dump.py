from selenium_setup import get_driver
from convert import string_to_int, string_to_float, string_to_datetime
from database import Data_base_API

DB_API = Data_base_API()


c = DB_API.contrant_cards.select()
# print(c)
# print(len(c))

# def card_to_str(c_obj):
#     row = f'{c_obj.number};{c_obj.date.strftime("%d.%m.%Y")};{c_obj.price};{c_obj.customer}\n'
#
#     return row

# print(card_to_str(c[0]))
# print(c[0].to_file())

temp_file = 'C:/Users/G.Tishchenko/Desktop/myfiles/zakupki.txt'
#
# СОХРАНЯЕМ ТАБЛИЦУ КАРТОЧКИ ТЕКСТОВЫЙ ФАЙЛ
# with open(temp_file, 'w') as tf:
#     for el in c:
#         tf.write(el.to_file())
#         print(el.date)

# СОХРАНЯЕМ ИНФУ ИЗ ФАЙЛА В SQL ТАБЛИЦУ
# txt_dict = {}
# from convert import string_to_int, string_to_float, string_to_datetime
# with open(temp_file, 'r') as tf:
#     for el in tf:
#         elements = el.split(';')
#         da = {
#             'number': string_to_int(elements[0]),
#             'date': string_to_datetime(elements[1]),
#             'price': string_to_float(elements[2]),
#             'customer': elements[3].replace('\n', ''),
#         }
#         txt_dict[string_to_int(elements[0])] = da
        # print(da)
        # DB_API.contrant_cards.insert(**da)

# for key, val in txt_dict.items():
#     if not DB_API.contrant_cards.select(number = key):
#         try:
#             DB_API.contrant_cards.insert(**val)
#             print('=)')
#         except:
#             DB_API.contrant_cards.session.rollback()
#             print('=(')


    # row = tf[0]
    # a = tf.readline()
    # print(a.split(';'))
