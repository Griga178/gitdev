class Offer():
    def __init__(self, **kw):
        self.id = kw['id']
        self.available = kw['available']
        self.url = kw['url']
        self.categoryId = kw['categoryId']
        self.name = kw['name']
        self.price = kw['price'],
        if type(self.price) == tuple:
            self.price = self.price[0]
        self.vendor = kw['vendor']
        self.model = kw['model']
        self.vendorCode = kw['vendorCode']
        self.description = kw['description']
    def __str__(self):
        return f"{self.categoryId}, {self.name}"

    def find_parent_category(self, cat_dict):
        if self.categoryId in cat_dict:
            category_o  = cat_dict[self.categoryId]
            parent_cat_o = category_o.get_parent()

        return parent_cat_o
    def get_list(self):


        r_l = [
            self.id,
            self.available,
            self.url,
            self.categoryId,
            self.name,
            self.price,
            self.vendor,
            # self.id,
            self.vendorCode,
            self.description
        ]
        # print(r_l)
        return r_l


from typing import Dict
import openpyxl
class File_creator():
    def __init__(self, categories: Dict):
        self.categories = categories
        self.parent_categories = {} # {<category>: [<offer>, ...]}

    def add_offer_category(self, offer_object):
        par_cat = offer_object.find_parent_category(self.categories)

        if par_cat not in self.parent_categories:
            self.parent_categories[par_cat] = [offer_object]
        else:
            self.parent_categories[par_cat].append(offer_object)

    def create_files(self):
        for file, offers in self.parent_categories.items():
            print(f"Сохраняем товары в excel файл: {file.name}")
            wb = openpyxl.Workbook()
            sh1 = wb.active
            count = 0
            for offer in offers:
                count += 1
                sh1.append(offer.get_list())
                print(count, end = "\r")
            wb.save(f'C:/Users/G.Tishchenko/Desktop/{file.name}.xlsx')
