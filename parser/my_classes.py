from datetime import datetime
from my_funcs import *
from random import randint

class Shop():

    shop_count = 0
    amount_of_protos = 0

    def __iinit__(self):
        self.main_page = ''

    # catalog_info = False




main_pages = ["dns.ru", 'ciiti.ru', 'only.ru', 'just.ru']

protos_links = ["dns.ru/1", "https://dns.ru/2", "https://dns.ru/3", 'https://ciiti.ru/1', 'https://only.ru/1',
'https://just.ru/1' 'https://ciiti.ru/2', 'https://only.ru/2', 'https://just.ru/2' 'https://ciiti.ru/3', 'https://only.ru/3', 'https://just.ru/3']


class Link():
    link_counter = 0
    type = 'ссылка магазина или инфосайта'
    status = 'True or False (parsed or not)'
    price_date_screen = {}
    def __init__(self, link, type = False, pars_price = False, screen_path = False):
        self.main_page = define_main_page(link)
        self.link = link
        self.pars_price = pars_price
        self.scr_date = datetime.now()
        self.screen_path = screen_path
        if self.main_page:
            print('Главная стр. - норм, привязываем к магазину')
        else:
            print(f'Что за хрень: {link}?')
    def __str__(self):
        return f"{self.link} \nprice: {self.pars_price}"
    # link_counter += 1
    # Хрень_выводит_кол_во_ссылок = f'Всего ссылок: {link_counter}'
    # не тут считается
example_set = set()
#
# class_list = [Link(link, pars_price = randint(100, 200)) for link in protos_links]
# print(class_list[1].link)
# print(class_list[1].pars_price)
# print(class_list[1].scr_date)
# for link in protos_links:
#     Link(link)
    # print(link.main_page)

for exe in protos_links:
    example_set.add(Link(exe, pars_price = randint(100, 200)))

print(len(example_set))

for el in example_set:
    print(el)

# https://proglib.io/p/vvedenie-v-obektno-orientirovannoe-programmirovanie-oop-na-python-2020-07-23
