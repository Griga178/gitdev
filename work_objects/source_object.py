from .company_object import Company

class Source():
    def __init__(self, source_type_cell, company_inn, company_name, domain_obj):

        self.company = Company(company_inn, company_name)
        self.domain = domain_obj
        self.split_type(source_type_cell)

    def split_type(self, source_type_cell):
        source_parts = source_type_cell.split(" ")

        if source_parts[0] == "Экранная":
            self.name = "Экранная копия"
            self.date = source_parts[3]
            self.number = source_parts[5]
        elif source_parts[0] == "Ответ":
            self.name = "Ответ на запрос"
            self.date = source_parts[4]
            self.number = source_parts[6]
        elif source_parts[0].isdigit():
            self.name = "Контракт"
            self.date = source_parts[2]
            self.number = source_parts[0]
        else:
            """ Не понятный источник """
            self.name = False
            self.date = False
            self.number = False
