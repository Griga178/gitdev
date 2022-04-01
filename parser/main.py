import interface

from my_parser import Parser

parser = Parser()


main_pages = ["dns.ru", 'ciiti.ru', 'only.ru', 'just.ru']

protos_links = ["dns.ru/1", "https://dns.ru/2", "https://dns.ru/3", 'https://ciiti.ru/1', 'https://only.ru/1',
'https://just.ru/1' 'https://ciiti.ru/2', 'https://only.ru/2', 'https://just.ru/2' 'https://ciiti.ru/3', 'https://only.ru/3', 'https://just.ru/3']

example_link = 'https://www.citilink.ru/catalog/karty-pamyati/'
exemple_product_link = 'https://www.citilink.ru/product/karta-pamyati-microsdhc-uhs-i-kingston-canvselect-plus-32-gb-100-mb-s-1206983/'
second_product_link = 'https://www.citilink.ru/product/kartrider-vneshnii-buro-bu-cr-110-chernyi-389726/'

protos_links2 = ['https://www.citilink.ru/product/karta-pamyati-microsdhc-uhs-i-kingston-canvselect-plus-32-gb-100-mb-s-1206983/',
'https://www.citilink.ru/product/kartrider-vneshnii-buro-bu-cr-110-chernyi-389726/'
]


''' парсинг списка ссылок '''
# содает экземпляр ссылки с ценой, датой, *скрином
# parser.parse_page(exemple_product_link)
# parser.parse_page(protos_links2)
#
# # Выводит название предметов (из ссылки) цену и дату
# links_dict = parser.all_parsed_links()
#
# for link in links_dict:
#     print(parser.all_parsed_links()[link])

''' Вывод данных '''


''' парсинг каталога сайта '''

catalog_page = 'https://www.citilink.ru/catalog'
parser.parse_catalog(catalog_page)
