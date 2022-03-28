
import requests
from bs4 import BeautifulSoup

catalog_link = "https://www.citilink.ru/catalog/"

first_link = "https://www.citilink.ru/catalog/noutbuki/"

# Тип сайта "склад - продавец" БД - папки
# парсер страницы
# Пролистыватель страниц
# Переход по каталогу
# Парсер катклога

def catalog_parser(catalog_page):
    my_request = requests.get(catalog_page)
    soup = BeautifulSoup(my_request.text, 'html.parser')
    block_info = ['ul', 'class', 'CatalogLayout__item']
    child_block_info = ['li', 'class', 'CatalogLayout__children-item']
    answer = soup.findAll(block_info[0], block_info[2])
    # answer = soup.findAll(child_block_info[0], child_block_info[2])
    # print(answer)
    return answer


# page = catalog_parser(catalog_link)
# # print(page)
#
#
# for el in page:
#     # print(el.li('div', "CatalogLayout__item-title-wrapper")[0].div.h4.a.text)
#     # Тоже самое
#     print(el.a.string)
#     print(el.a['href'])
# print(len(page))
