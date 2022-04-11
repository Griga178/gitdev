import sys
sys.path.append('../')
from data_loader import save_pkl as save
from data_loader import load_pkl_file as load


class Subject_ver_2():
    def __init__(self, name, parent = False, child = False, chars = False):
        self.name = name
        self.parent = parent
        self.child = child
        self.chars = chars

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

class Model(): # Subject_ver_2
    def __init__(self):
        # super(Model, self).__init__()
        self.name = name# Intel Core i7 K-1255
        self.subject_name = subject_name    # Процессор
        self.model_parents = model_parents # {Samsung A 1225}
        self.model_childs = model_childs
        self.model_chars = model_chars # dict


def recurse_interface():
    command = input(str('Вызов подсказок: "9" \nВведите номер команды: '))
    print('\n')
    try:
        load_set = load('Subjects_set')
    except:
        print('Создана новая база!')
        load_set = {}

    if command == '0':
        save(load_set, 'Subjects_set')
        print('Успешно закрылись')
        quit()

    elif command == '1':
        for el in load_set:
            print(el, type(el))

    elif command == '2':
        input_subj = input(str('Введите название предмета: '))
        load_set.add(Subject_ver_2(input_subj))
        save(load_set, 'Subjects_set')

    elif command == '3':
        print('Показать описание:')
        print('Всех предметов 1\nВыбрать предмет 2\nСтарое описание 3 или 4')
        sec_command = input(str('Введите номер команды: '))
        if sec_command == '1':
            for el in load_set:
                el.chars_description(load_set)
        elif sec_command == '2':
            print("Выбери экземпляр")
            num = 0
            num_list = []
            for el in load_set:
                num_list.append(el)
                print(num, el)
                num += 1
            ex_num = int(input('Номер экземпляра: '))
            chosen_example = num_list[ex_num]
            chosen_example.chars_description(load_set)
        elif sec_command == '3':
            for el in load_set:
                print(el.description())
        elif sec_command == '4':
            for el in load_set:
                print(el)
                el.show_child()
                el.show_parent()

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
            # jel = Subject_ver_2(name = el.name, parent = el.parent, child = el.child, chars = False)
            jel = Subject_ver_2(name = el.name, parent = False, child = False, chars = False)
            new_set.add(jel)
        # save(new_set, 'Subjects_set')
        save(load_set, 'Subjects_dict.pckl')
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
        print('Что добавить?\n 1 - Родитель\n 2 - Ребенок\n 3 - Характеристика')
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

    elif command == '9':
        print('''\
        0 - Выход
        1 - Показать все объекты
        2 - Добавить новый экземпляр
        3 - Показать дерево
        4 - Удалить элемент
        5 - Обновить класс
        6 - Добавить данные в класс''')

    recurse_interface()

recurse_interface()
