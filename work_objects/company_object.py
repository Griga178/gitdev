from work_data_base import Company_object

class Company():
    def __init__(self, inn, name):
        self.inn = inn
        self.name = name
        self.sites = []
        self.links = []
        
        if inn or name:
            self.object = Company_object(inn, name)
        else:
            self.object = False

    def __str__(self):
        str_row = f'{self.name}'

        if self.object:
            str_row += f'{self.object.object.inn}'

        return str_row
