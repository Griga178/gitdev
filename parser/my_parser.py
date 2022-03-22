import requests
from bs4 import BeautifulSoup
from my_funcs import *

example_link = 'https://www.citilink.ru/catalog/karty-pamyati/'
exemple_product_link = 'https://www.citilink.ru/product/karta-pamyati-microsdhc-uhs-i-kingston-canvselect-plus-32-gb-100-mb-s-1206983/'
second_product_link = 'https://www.citilink.ru/product/kartrider-vneshnii-buro-bu-cr-110-chernyi-389726/'

my_request = requests.get(second_product_link)

#print(my_request.text)

"""Поиск всех ссылок на странице
    **(другая функция определит повторяющиеся ссылки и добавит и в шапку или в др)
    *функция поднятся на страницу вверх

    *Отобразить теги заданного текста

    ПОИСК ОБЪЕКТА - ТЕГА ПО Full_XPath"""






# 1 ПОЛУЧИЛИ ССЫЛКУ НА ВХОД
# ОПРЕДЕЛЯЕМ ГЛАВНУЮ СТРАНИЦУ
main_page = define_main_page(second_product_link)
print(main_page)

# ПРОВЕРЯЕМ ЕСТЬ ЛИ ЭТОТ САЙТ В БАЗЕ ДАННЫХ
my_site_dict = {'www.citilink.ru':{
'price_tag_class': ['span', 'ProductHeader__price-default_current-price'],
'buy_button_block': ['div', 'ProductHeader__buy-block'],
'buy_button': ['button', 'ProductHeader__buy-button']}}
# ПРЕОБРАЗУЕМ HTML - КОД В ОБЪЕКТЫ BF4
soup = BeautifulSoup(my_request.text, 'html.parser')



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
# product_block = soup.find('div', "ProductCardLayout__product-description")
#
# # Какая инфа присутствует внутри тега?
#     # Какие теги есть в блоке
#     # Что содержиться в блоках
#     # Выбрать теги на которые обращаем внимание
#     #     (старая цена, нет в наличии, цена)
#     # И те которые на которые не обращаем внимание
#     # + все новые теги изучать
#block_content = product_block.contents[0]
#lenght_of_content = len(block_content)

price_area = soup.find('span', 'ProductHeader__price-default_current-price').string
buy_button_block = soup.find('div', 'ProductHeader__buy-block').contents[0]
print(price_area)

if 'ProductHeader__buy-button' in buy_button_block['class']:
    print('Есть в наличии')
else:
    print(buy_button_block['class'])
    print("Не нашли")
