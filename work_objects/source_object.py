from .company_object import Company
from .link_object import Link

class Source():
    '''
        строка из excel (рабочей таблицы)
            - тип (экранка/...)
            - компания (имя/инн)
            - ссылка (не закупка)

    '''
    def __init__(self, **kwargs):
        self.company = Company(kwargs['company_inn'], kwargs['company_name'])
        # self.name
        self.split_type(kwargs['source_info'])
        self.links = []
        if kwargs.get('links', False):
            links = Link.define_links(kwargs['links'])
            for link in links:
                li = Link(link)
                self.links.append(li)

    def split_type(self, source_info):
        source_parts = source_info.split(" ")
        if source_parts[0][0] == "Э":
            self.name = "Экранная копия"
        elif source_parts[0][0] == "О":
            self.name = "Ответ на запрос"
        elif source_parts[0].isdigit():
            self.name = "Контракт"
        else:
            """ Не понятный источник """
            self.name = False

    def __str__(self):
        message = f'{self.name}:'
        if self.links:
            domain = self.links[0].domain
            message += f' {domain}'
        if self.company:
            message += f' {self.company}'

        return message
