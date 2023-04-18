from work_data_base import CompanyS
from work_objects.link_viewer import Link_viewer
from work_data_base import LinkS
from work_data_base import WebsiteS
# from .link_object import Link


class Source():
    '''
        строка из excel (рабочей таблицы)
            - тип (экранка/...)
            - компания (имя/инн)
            - ссылка (не закупка)

    '''
    linkset = set()
    companyset = set()
    websiteset = set()
    def __init__(self, **kwargs):
        self.company = CompanyS(inn = kwargs['company_inn'], name = kwargs['company_name'])
        
        if self.company:
            company_id = self.company.id
            Source.companyset.add(self.company)
        else:
            company_id = None

        self.split_type(kwargs['source_info'])
        self.links = []
        if kwargs.get('links', False):
            # links = Link_viewer.define_links(kwargs['links'])
            lv = Link_viewer(kwargs['links'])
            domain = WebsiteS(domain = lv.domain, company_id = company_id)
            Source.websiteset.add(domain)

            for link in lv.links:
                li = LinkS(name = link, website_id = domain.id)
                self.links.append(li)
                Source.linkset.add(li)

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
            domain = self.links[0].website.domain
            message += f' {domain}'
        if self.company:
            message += f' {self.company.name}'

        return message
