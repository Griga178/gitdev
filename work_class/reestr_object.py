import re

class Links():

    def __init__(self, link_row):
        self.source = False
        self.define_link(link_row)

    def define_link(self, link_row):
        self.links = re.findall(r'[\w:/.\-?=&+%#\[\]]+', link_row)

class Source():
    def __init__(self, source_type_cell, comapany_inn, kkn_part, links: Links):

        self.comapany_inn = comapany_inn
        self.kkn_part = kkn_part
        self.links = links
        self.links.source = self

        self.split_type(source_type_cell)

    def split_type(self, source_type_cell):
        source_parts = source_type_cell.split(" ")

        if source_parts[0] == "Экранная":
            self.type_name = "Экранная копия"
            self.type_date = source_parts[3]
            self.number = source_parts[5]
        elif source_parts[0] == "Ответ":
            self.type_name = "Ответ на запрос"
            self.type_date = source_parts[4]
            self.number = source_parts[6]
        elif source_parts[0].isdigit():
            self.type_name = "Контракт"
            self.type_date = source_parts[2]
            self.number = source_parts[0]
        else:
            """ Не понятный источник """
            self.type_name = False
            self.type_date = False
            self.number = False
