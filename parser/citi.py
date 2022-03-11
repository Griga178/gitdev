
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
    '''Класс для инфромации по сайтам'''
    def __init__(self, link = '', main_page = ''): #, page_type = "unknown"
        self.link = link
        self.main_page = main_page

        '''
        if type(link) = str:
            link_list = link.split('/')
            http_type = link_list[0] # http: or https
            if link_list[1] == '':
                main_page = link_list[2]
        '''
    '''Определение куда ведет ссылка (на главную, на страницу товара
    или в каталог),
    определение главной страницы'''
    def page_info(self):
        return self.link, self.main_page

dns = Just_site(link)

print(dns.page_info())

dns.link = 'new_link'

print(dns.page_info())

dns.main_page = 'https://www.dns-shop.ru'
