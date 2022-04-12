import sys
sys.path.append('../')
from data_loader import save_pkl as save
from data_loader import load_pkl_file as load


class Subject_ver_3():
    def __init__(self, name, parent = False, child = False, chars = False, models = False):
        self.name = name
        self.parent = parent
        self.child = child
        self.chars = chars
        self.models = models

    def __str__(self):
        return f'{self.name}'
    def description(self):
        ''' не актуально, переделать во что либо'''
        return f'{self.name}\n Входит в состав: {[str(element) for element in self.parent] if self.parent else self.parent}\n Предметы внутри: {self.child}\n Характеристики: {self.chars}'
    def show_parent(self):
        print(f'Находится внутри: {self.parent}')
        if not self.parent:
            print('Родители: -')
        else:
            print(f'Родители: {self.parent}')
    def show_child(self):
        if not self.child:
            print('Предметов внутри: -')
        else:
            print(f'Предметы внутри: {self.child}')
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
    def chars_description(self, examples_set, space = ''):
        print(f'{space} {self.name}')
        space += '--'
        if self.chars:
            for char in self.chars:
                print(space, char)
        if self.child:
            for child_name in self.child:
                for example in examples_set:
                    if child_name == example.name:
                        child_example = example
                        break
                child_example.chars_description(examples_set, space = space)
    def add_models(self, model_name, model_example):
        if not self.models:
            self.models = {model_name}
        else:
            self.models.add(model_name)
        if not model_example.subject_name:
            model_example.subject_name = {self.name}
        else:
            model_example.subject_name.add(self.name)



class Model():
    def __init__(self, name, subject_name = False, model_parents = False, model_childs = False, model_chars = False):
        self.name = name# Intel Core i7 K-1255
        self.subject_name = subject_name    # Процессор
        self.model_parents = model_parents # {Samsung A 1225}
        self.model_childs = model_childs
        self.model_chars = model_chars # dict
    def __str__(self):
        return f'{self.name}'

def recurse_interface(command = False, sec_command = False):
    pickle_file_name = 'Models_Subjects_dict'
    try:
        load_dict = load(pickle_file_name)
        print('Загружена база!')

    except:
        print('Создана новая база!')
        load_dict = {'Subjects': set(), 'Models': set()}
    print('\n - - - - - - - - - - - - - - - - - - - - ')
    if not command:
        command = input(str('Вызов подсказок: "9" \nВведите номер команды: '))

    if command == '0':
        save(load_dict, pickle_file_name)
        print('Успешно закрылись')
        quit()

    elif command == '1':
        for class_types in load_dict:
            print('\n', class_types, len(load_dict[class_types]))
            try:
                for example in load_dict[class_types]:
                    print(example)
            except:
                pass

    elif command == '2':
        print('Добавление экземпляров')
        if not sec_command:
            sec_command = str(input('Предмет - 1\nМодель - 2\nНазад - 0\nВыход 00:\n'))
        if sec_command == '1':
            input_subj = input(str('Назад - 0\nВведите название предмета: '))
            if input_subj == '0':
                recurse_interface('2')
            else:
                load_dict['Subjects'].add(Subject_ver_3(input_subj))
                save(load_dict, pickle_file_name)
                print(f'Предмет: "{input_subj}" - успешно добавлен')
                recurse_interface('2', '1')
        elif sec_command == '2':
            input_mod = input(str('Назад - 0\nВведите название модели: '))
            if input_mod == '0':
                recurse_interface('2')
            else:
                load_dict['Models'].add(Model(input_mod))
                save(load_dict, pickle_file_name)
                print(f'Модель: "{input_mod}" - успешно добавлен')
                recurse_interface('2', '2')
        elif sec_command == '0':
            recurse_interface()
        elif sec_command == '00':
            recurse_interface('0')
        else:
            print("Непонятная команда")
            recurse_interface('2')

    elif command == '3':
        if not sec_command:
            print('Показать описание:')
            print('Выбрать предмет - 1\nСтарое описание - 2 или 3\n')
            sec_command = input(str('Введите номер команды: '))
        if sec_command == '1':
            print("Выбери экземпляр")
            num = 0
            num_list = []
            for el in load_dict['Subjects']:
                num_list.append(el)
                print(num, el)
                num += 1
            ex_num = int(input('Номер экземпляра: '))
            chosen_example = num_list[ex_num]
            chosen_example.chars_description(load_dict['Subjects'])
        elif sec_command == '2':
            for el in load_dict['Subjects']:
                print(el.description())
        elif sec_command == '3':
            for el in load_dict['Subjects']:
                print(el)
                el.show_child()
                el.show_parent()
        else:
            print("Непонятная команда")
            recurse_interface('2')

    elif command == '4':
        num = 0
        num_list = []
        for el in load_set:
            num_list.append(el)
            print(num, el)
            num += 1
        del_num = input('что удалить? ')
        del_num = int(del_num)
        load_set.remove(num_list[del_num])
        save(load_set, 'Subjects_set')

    elif command == '5':
        new_set = set()
        for el in load_set:
            if type(el) == 'Subject_ver_3':
                print(el, 'update')
                jel = Subject_ver_3(name = el.name, parent = el.parent, child = el.child, chars = el.chars, models = False)
                new_set.add(jel)
        save(new_set, 'Subjects_set')
        print('Успешно Обновлено')

    elif command == '6':
        print("Выбери экземпляр")
        num = 0
        num_list = []
        for el in load_set:
            num_list.append(el)
            print(num, el)
            num += 1
        ex_num = int(input('Номер экземпляра: '))
        change_example = num_list[ex_num]
        print('Что добавить?\n 1 - Родитель\n 2 - Ребенок\n 3 - Характеристика\n 4 - Модель')
        num_com = str(input("Введите номер: "))

        if num_com == '1':
            print(f'Добавляем родителя к {change_example}\n Выбрать из списка - "1"\n Создать новый - "2"')
            sec_num_com = str(input("Введите номер команды: "))
            if sec_num_com == '1':
                sec_num = 0
                sec_num_list = []
                for el in load_set:
                    sec_num_list.append(el)
                    print(sec_num, el)
                    sec_num += 1
                sec_ex_num = int(input('Номер экземпляра: '))
                parent_example = sec_num_list[sec_ex_num]
                # print(parent_example)
                change_example.add_parent(str(parent_example), parent_example)
                save(load_set, 'Subjects_set')
        elif num_com == '2':
            print(f'Добавляем ребенка к {change_example}\n Выбрать из списка:')
            sec_num = 0
            sec_num_list = []
            for el in load_set:
                sec_num_list.append(el)
                print(sec_num, el)
                sec_num += 1
            sec_ex_num = int(input('Номер экземпляра: '))
            child_example = sec_num_list[sec_ex_num]
            change_example.add_child(str(child_example), child_example)
            save(load_set, 'Subjects_set')
        elif num_com == '3':
            print('Добавляем характеристику')
            chars_name = str(input("Введите название характеристики: "))
            change_example.add_chars(chars_name)
            save(load_set, 'Subjects_set')
        elif num_com == '4':
            print('Добавляем модель (существующую) в экземпляр')
            sec_num = 0
            sec_num_list = []
            for el in load_set:
                sec_num_list.append(el)
                print(sec_num, el)
                sec_num += 1
            sec_ex_num = int(input('Номер экземпляра: '))
            change_example = sec_num_list[sec_ex_num]
            sec_num = 0
            sec_num_list = []
            # выбор модели
            for el in load_set:
                sec_num_list.append(el)
                print(sec_num, el)
                sec_num += 1
            model_name_num = int(input('Номер модели: '))
            model_example = sec_num_list[model_name_num]
            change_example.add_models(model_example.name, model_example)
            save(load_set, 'Subjects_set')

    elif command == '9':
        print('''\
        0 - Выход
        1 - Показать все объекты
        2 - Добавить новый экземпляр
        3 - Показать дерево Предметов
        4 - Удалить элемент
        5 - Обновить класс
        6 - Добавить данные в класс''')
    else:
        print("\nНепонятная команда")
        recurse_interface("9")

    recurse_interface()

recurse_interface()
