from mparser import catalog_parse

catalog_url = 'https://www.kns.ru/catalog/proektory/'

rules = {
    'curent_count': {
        'tag_name': 'span',
        'tag_val': {'id': "CurentGoodsCount"},
    },

    'total_count': {
        'tag_name': 'span',
        'tag_val': {'id': "TotalGoodsCount"},
    },
    'iter_by_url': True,
    'url_start_part' : "page",
    'url_end_part' : "",

    "short_card_info": [
        {'link': ''},
        {'title': ''},
        {'description': ''},
        {'price': ''},
    ]

}

cards = catalog_parse(catalog_url, rules)

import requests

class Algo():

    self.page_count = None
    self.catalog_url = None
    self.catalog = [] # :List[Dict, ...]
    self.current_page = None

    def get_catalog_page(self):
        page = requests.get(self.catalog_url)
        if page.status_code != 200:
            quit()
        return page

    def parse_catalog_page(self):
        pass

    def run(self):
        page = self.get_catalog_page()

        # Парсинг стартовой страницы
        self.parse_catalog_page(page)
        # -> Инфа с 1-ой страницы
        # -> кол-во страниц в каталоге {self.page_count}
        if self.page_count:

            self.parse_catalog_page(page, page_count)
