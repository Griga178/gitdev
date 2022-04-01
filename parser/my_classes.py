from datetime import datetime
from my_funcs import *
from random import randint


class Shop():

    links_data = set()

    def __init__(self, main_page):
        self.name = main_page

    def return_links(category = False):
        # Возвращает все ссылки экземпляра/Объекта
        # Либо ссылки по категориям
        # return Shop.links_data
        pass

class Product():
    def __init__(self, name, id = False, categories_id = False):
        self.id = id
        self.name = name
        self.categories_id = categories_id

class Categories():
    # Загрузка PICKLE инфы
    # послдений id категории
    id_number = 0

    def __init__(self, name, id = False, shop_id = False, parent_id = False, chile_id = False):
        self.name = name
        self.shop_id = shop_id
        self.parent_id = parent_id
        self.chile_id = chile_id
        Categories.examples_id.append(id)
        Categories.id_number += 1
        if not id:
            self.id = Categories.id_number
        else:
            self.id = Categories.id_number
            print(f'Ручной ввод id - не доступен\nНазначен номер: {self.id}')

    def __str__(self):
        return f'{self.id, self.name}'



# cat_list = [['Компы', 1], ['Бытовуха', 3], ['Театр', 26]]
# cat_set = set()
#
# for cat in cat_list:
#     cat_set.add(Categories(cat[0], cat[1]))
# print(Categories.examples_id)
#
# for cat_sets in cat_set:
#     print(cat_sets)


# example_set = set()
#
# class_list = [Link(link, pars_price = randint(100, 200)) for link in protos_links]
# print(class_list[1].link)
# print(class_list[1].pars_price)
# print(class_list[1].scr_date)
# for link in protos_links:
#     Link(link)
    # print(link.main_page)

# for exe in protos_links:
#     example_set.add(Link(exe, pars_price = randint(100, 200)))
#
# print(len(example_set))
#
# for el in example_set:
#     print(el)

# https://proglib.io/p/vvedenie-v-obektno-orientirovannoe-programmirovanie-oop-na-python-2020-07-23
