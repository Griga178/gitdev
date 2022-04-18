class Subjects_category():
    def __init__(self, name, other_names = False, subject_names = False, model_names = False):
        self.name = name
        self.other_names = other_names
        self.subject_names = subject_names
        self.model_names = model_names
    def add_other_name(self):
        pass
    def add_subjects(self, subject_name, subjects_example):
        if self.subject_names:
            self.subject_names.add(subject_name)
            subjects_example.categories.add(self.name)

class Model_ver2():
    def __init__(self, name, subject_name = False, model_parents = False, model_childs = False, model_chars = False, categories = False):
        self.name = name# Intel Core i7 K-1255
        self.subject_name = subject_name    # Процессор
        self.model_parents = model_parents # {Samsung A 1225}
        self.model_childs = model_childs
        self.model_chars = model_chars # dict
        self.categories = categories
    def __str__(self):
        return f'{self.name}'
    def add_chars_val(self, chars_name, value, measure = '', subj_set = False):
        if not self.model_chars:
            self.model_chars = {chars_name: [value, measure]}
        else:
            self.model_chars[chars_name] = [value, measure]
        if self.subject_name:
            for subjects_example in subj_set:
                if subjects_example.name == self.subject_name:
                    subjects_example.add_chars(chars_name)
    def description(self, space = ' - - '):
        if self.subject_name:
            print(f'Предмет: {self.subject_name}')
        print(f'Название модели: {self.name}')
        if self.categories:
            for name in self.categories:
                print(space, name)
        if self.model_chars:
            print('Характеристики:')
            for chars_name in self.model_chars:
                print(space, chars_name, self.model_chars[chars_name][0], self.model_chars[chars_name][1])


class Subject_ver_3():
    def __init__(self, name, parent = False, child = False, chars = False, models = False):
        self.name = name
        self.parent = parent
        self.child = child
        self.chars = chars
        self.models = models
        # self.categories = categories

    def __str__(self):
        return f'{self.name}'
    def show_chars(self, space = ' - '):
        if self.chars:
            for char in self.chars:
                print(space, char)
    def show_parent(self):
        if not self.parent:
            print('Родители: -')
        else:
            print(f'Родители: {self.parent}')
    def show_child(self):
        if not self.child:
            print('Предметов внутри: -')
        else:
            print(f'Предметы внутри: {self.child}')
    def show_model(self):
        if not self.models:
            print('Модели внутри: -')
        else:
            print(f'Модели:')
            for mod_name in self.models:
                print(f' - {mod_name}')
    def add_parent(self, parent_name, parent_example):
        if not self.parent:
            self.parent = {parent_name}
        else:
            self.parent.add(parent_name)
        if not parent_example.child:
            parent_example.child = {self.name}
        else:
            parent_example.child.add(self.name)
    def add_child(self, child_name, child_example):
        if not self.child:
            self.child = {child_name}
        else:
            self.child.add(child_name)
        if not child_example.parent:
            child_example.parent = {self.name}
        else:
            child_example.parent.add(self.name)
    def add_chars(self, chars_name):
        if not self.chars:
            self.chars = {chars_name}
        else:
            self.chars.add(chars_name)
    def chars_description(self, examples_set, space = ' - '):
        if space == ' - ':
            print('Характеристики:')
        print(f"{space}{self.name}:")
        space += '- '
        if self.chars:
            for char in self.chars:
                print(f"{space}{char}")
        if self.child:
            for child_name in self.child:
                for example in examples_set:
                    if child_name == example.name:
                        child_example = example
                        break
                child_example.chars_description(examples_set, space = space)

    def chars_description_dict(self, examples_set):
        ex_desc_d = {} # example_description_dict
        ex_desc_d[self.name] = {'chars': False, 'content': False}

        # {"Компьютер":{"Характеристики":[char1, char2],
        #             "Содержимое":[
        #                 "Процессор": {"Характеристики":[char1,char2],
        #                             "Содержимое": False},
        #                 "Видеокарта": {"Характеристики":[char1,char2],
        #                             "Содержимое": False}
        #                                 ]}}

        if self.chars:
            ex_desc_d[self.name]['chars'] = []
            for char in self.chars:
                ex_desc_d[self.name]['chars'].append(char)
        if self.child:
            ex_desc_d[self.name]['content'] = {}
            for child_name in self.child:
                for example in examples_set:
                    if child_name == example.name:
                        child_example = example
                        break
                ex_desc_d[self.name]['content'].update(child_example.chars_description_dict(examples_set))
        else:
            ex_desc_d[self.name]['content'] = False
        return ex_desc_d

    def add_models(self, model_name, model_example):
        if not self.models:
            self.models = {model_name}
        else:
            self.models.add(model_name)
        if not model_example.subject_name:
            model_example.subject_name = self.name
        else:
            print(f'\nМодел принадлежит к {model_example.subject_name}')
            # model_example.subject_name.add(self.name)
        # Так же добавляются все ключи модели в список характеристик
        if model_example.model_chars:
            for chars_name in model_example.model_chars:
                self.add_chars(chars_name)
