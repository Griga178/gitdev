
catalog_link = "https://www.citilink.ru/catalog/"

first_link = "https://www.citilink.ru/catalog/noutbuki/"

# Тип сайта "склад - продавец" БД - папки
# парсер страницы
# Пролистыватель страниц
# Переход по каталогу
# Парсер катклога

# БД связь каталог - предметы в нем - ссылки

link = 'https://www.dns-shop.ru/catalog/17a9de8616404e77/igry-dlya-pk/'

class Just_site():
    '''Главный класс для инфромации по сайтам'''
    count_main_pages = 0

    def __init__(self, link = '', main_page = ''): #, page_type = "unknown"
        self.link = link
        self.main_page = main_page

    '''Определение куда ведет ссылка (на главную, на страницу товара
    или в каталог),
    определение главной страницы'''
    def page_info(self):
        return self.link, self.main_page

class Site_info(Just_site):

    count_of_links = 0
    know_main_page = False
    know_catalog_page = False
    catalog_page_content = dict() # 'Ноутбуки':"https://www.citilink.ru/catalog/noutbuki/"
    # Определяем главную страницу
    def func_define(link):
        ''' Определяем главную страницу '''
        temp_list = link.split('/')
        main_page = temp_list[0] + '//' + temp_list[2]
        know_main_page = True
        return main_page
    # Определяем страницу каталога
    # Определяем содержимое каталога


dns = Just_site(link)

print(dns.page_info())

dns.link = 'new_link'

print(dns.page_info())

dns.main_page = 'https://www.dns-shop.ru'
