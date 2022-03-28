import requests
from bs4 import BeautifulSoup
from my_funcs import *
from my_classes import Link





#print(my_request.text)

"""Поиск всех ссылок на странице
    **(другая функция определит повторяющиеся ссылки и добавит и в шапку или в др)
    *функция поднятся на страницу вверх

    *Отобразить теги заданного текста

    ПОИСК ОБЪЕКТА - ТЕГА ПО Full_XPath"""


# ПРОВЕРЯЕМ ЕСТЬ ЛИ ЭТОТ САЙТ В БАЗЕ ДАННЫХ
my_site_dict = {'www.citilink.ru':{
'price_tag_class': ['span', 'ProductHeader__price-default_current-price'],
'buy_button_block': ['div', 'ProductHeader__buy-block'],
'buy_button': ['button', 'ProductHeader__buy-button']}
}

# ПРОЦЕСС ПАРСИНГА

# ПАРСЕР ПО ССЫЛКЕ (ДОБАВИТЬ ЧТЕНИЕ ХАРАКТЕРИСТИК) ТОЧЕЧНЫЙ
class Parser():
    # ТЕГИ ДЛЯ ПАРСИНГА
    # ПОДГРУЖАЮТСЯ ИЗ ФАЛА PICKLE
    my_site_tags = {'www.citilink.ru':{
    'price_tag_class': ['span', 'ProductHeader__price-default_current-price'],
    'buy_button_block': ['div', 'ProductHeader__buy-block'],
    'buy_button': ['button', 'ProductHeader__buy-button']}
    }
    parsed_links = {}

    def parse_page(self, page):

        if type(page) == str:
            page = [page]
        for link in page:
            my_request = requests.get(link)
            soup = BeautifulSoup(my_request.text, 'html.parser')
            main_page = define_main_page(link)
            if main_page in my_site_dict:
                # ПОИСК БЛОКА С ЦЕНОЙ ПО ЗНАЧЕНИЮ КЛАССА
                price_tag = soup.find(Parser.my_site_tags[main_page]['price_tag_class'][0], Parser.my_site_tags[main_page]['price_tag_class'][1]).string
                # ПОИСК КНОПКИ КУПИТЬ (проверка на наличие товара)
                # buy_button_block = soup.find(Parser.my_site_tags[main_page]['buy_button_block'][0], Parser.my_site_tags[main_page]['buy_button_block'][1]).contents[0]
                Parser.parsed_links[link] = Link(link, pars_price = clean_number(price_tag))
    def __str__(self):
        parsed_links = Parser.parsed_links
        return f'Отпарсено ссылок: {len(parsed_links)}'
    def all_parsed_links(self):
        parsed_links = Parser.parsed_links
        return parsed_links


exemple_product_link = 'https://www.citilink.ru/product/karta-pamyati-microsdhc-uhs-i-kingston-canvselect-plus-32-gb-100-mb-s-1206983/'
second_product_link = 'https://www.citilink.ru/product/kartrider-vneshnii-buro-bu-cr-110-chernyi-389726/'

# p = Parser()
#
# p.parse_page(exemple_product_link)
#
# for link in p.all_parsed_links():
#     print(link)
#     print(p.all_parsed_links()[link])


# def parser_funcs(link):
#     # ПЕРЕХОД ПО ССЫЛКЕ - ОТВЕТ СЕРВЕРА
#     my_request = requests.get(link)
#     # ПРЕОБРАЗУЕМ HTML-КОД В ЭКЗЕМЛЯР BF4
#     soup = BeautifulSoup(my_request.text, 'html.parser')
#     if main_page in my_site_dict:
#         # ПОИСК БЛОКА С ЦЕНОЙ ПО ЗНАЧЕНИЮ КЛАССА
#         price_tag = soup.find(my_site_dict[main_page]['price_tag_class'][0], my_site_dict[main_page]['price_tag_class'][1]).string
#
#         # ПОИСК КНОПКИ КУПИТЬ (проверка на наличие товара)
#         buy_button_block = soup.find(my_site_dict[main_page]['buy_button_block'][0], my_site_dict[main_page]['buy_button_block'][1]).contents[0]
#         if my_site_dict[main_page]['buy_button'][1] in buy_button_block['class']:
#             print('Товар есть в наличии')
#             print(f'Цена товара: {clean_number(price_tag)}')
#         else:
#             print(buy_button_block['class'])
#             print("Не нашли")
#
#     else:
#         print(f'Нет правил для сайта {main_page}')

# link = second_product_link
# main_page = define_main_page(link)
# parser_funcs(link)

# 1 блок товара:
#     полное название
#     цена / товара нет в наличии
#     Код товара
#     *старая цена
# характеристики товара
# переход по ссылке
# название характеристики
# значение
# статус страницы:
#     слишком много запросов (ввести код, обновить итд)
#     404
# Поиск блока с информацией о товаре:
#     по тегу и классу тега




# НАБОР УПРАВЛЯЮЩИХ ФУНКЦИЙ
# 1 ВЫБОР ИСТОЧНИКА ССЫЛОК (1 ИЗ ФАЙЛА, 2 ИСКАТЬ НА САЙТЕ)
# 2 ИЗУЧЕНИЕ САЙТА (НАХОЖДЕНИЕ КАТАЛОГА, ОСНОВНЫЕ ТЕГИ (ЦЕНА, НАЛИЧИЕ, ЗАГОЛОВКИ))
# 3 ПАРСИНГ ЦЕН, НАЛИЧИЯ, ХАРАКТЕРИСТИК.
# 4 ЗАПИСЬ В БД
# * ЗАПИСЬ МОДЕЛИ И ЕЕ ХАРАКТЕРИСТИК В БД
# * ПАРСИНГ ИНФОРМАЦИОННЫХ САЙТОВ


"""Описание словаря каталога:
    ключ - название сайта = главная стр - http://
    значение - СПИСОК инфы каталога данного сайта
----------------------------------------
        1 ссылка на каталог (корень)
        2 список тегов для определения блока с каталожным наименования
        3 СЛОВАРЬ подкаталогов
----------------------------------------
            ключ - название товара/группы товаров
                если тип значения СПИСОК:
                    значение = [ссылка на группу т., словарь товаров]
                в противном случае
                    значение = СЛОВАРЬ товаров (там такая же схема)
----------------------------------------
                ключ - название товара/группы товаров
                значение - (str, либо если окажется группой: [str, dict])

{"www.citilink.ru":
    ["https://www.citilink.ru/catalog/",
    ['li', 'class', 'CatalogLayout__item-list'],
    {"Смартфоны и гаджеты":['https://www.citilink.ru/catalog/smartfony-i-gadzhety/'
            {"Смартфоны": "https://www.citilink.ru/catalog/smartfony/",
            "Сотовые телефоны": "https://www.citilink.ru/catalog/sotovye-telefony/",
            "Планшеты": "https://www.citilink.ru/catalog/planshety/"}]
    "Бытовая техника для дома и кухни":['https://www.citilink.ru/catalog/bytovaya-tehnika-dlya-doma-i-kuhni/'
            {"Крупная бытовая техника": ["https://www.citilink.ru/catalog/krupnaya-bytovaya-tehnika/"
                                        {'Винные шкафы': "https://www.citilink.ru/catalog/vinnye-shkafy/",
                                        'Холодильники': 'https://www.citilink.ru/catalog/holodilniki/'}],
            "Встраиваемая техника": "https://www.citilink.ru/catalog/vstraivaemaya-tehnika/"}]
    }
    ]
}
"""
catalog_dict = {"www.citilink.ru":["https://www.citilink.ru/catalog/", ['li', 'class', 'CatalogLayout__item-list'],
        {"Смартфоны и гаджеты":['https://www.citilink.ru/catalog/smartfony-i-gadzhety/', {"Смартфоны": "https://www.citilink.ru/catalog/smartfony/",
        "Сотовые телефоны": "https://www.citilink.ru/catalog/sotovye-telefony/", "Планшеты": "https://www.citilink.ru/catalog/planshety/"}],
        "Бытовая техника для дома и кухни":['https://www.citilink.ru/catalog/bytovaya-tehnika-dlya-doma-i-kuhni/',
        {"Крупная бытовая техника": ["https://www.citilink.ru/catalog/krupnaya-bytovaya-tehnika/", {'Винные шкафы': "https://www.citilink.ru/catalog/vinnye-shkafy/",
        'Холодильники': 'https://www.citilink.ru/catalog/holodilniki/'}], "Встраиваемая техника": "https://www.citilink.ru/catalog/vstraivaemaya-tehnika/"}]}]}
