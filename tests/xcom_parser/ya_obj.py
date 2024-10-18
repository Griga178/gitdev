'''
    Да
'''
class Category():
    categories = {}

    def __init__(self, id, name, parent_id = False):
        self.id = id
        self.name = name
        self.parent_id = parent_id

        Category.categories[id] = self
        if parent_id:
            if Category.categories.get(parent_id, False):
                self.parent = Category.categories[parent_id]
            else:
                self.parent = False
        else:
            self.parent = False

    def __str__(self):
        return f"{self.name}"

    def get_parents(self, par_list):
        if self.parent:
            par_list.append(self.parent)
            self.parent.get_parents(par_list)
        return par_list

    def get_list(self):
        par_list = [self]
        par_list = self.get_parents(par_list)
        # x = [x.name for x in reversed(par_list)]
        x = []
        for el in reversed(par_list):
            x.append(el.name)
        x.insert(0, self.id)
        return x

    def check_connections():
        """После сохранения всех категорий запустить, для проверки связей
        Category.check_connections()
        """
        for id, category in Category.categories.items():
            if category.parent_id:
                if type(category.parent) != Category:
                    category.parent = Category.categories[category.parent_id]
    def get_parent(self):
        par_list = [self]
        par_list = self.get_parents(par_list)
        return par_list[-1]
