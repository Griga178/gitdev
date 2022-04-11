import sys
import os
sys.path.append('../')
from data_loader import save_pkl as save
from data_loader import load_pkl_file as load

def create_subject(cur_dict, sub_name):
    cur_dict[sub_name] = {'id': 0, 'Parent': set(), 'Child': set(), 'Chars': set()}

def recurs_chars_descript(cur_dict, sub_name, space = ''):
    childs = cur_dict[sub_name]['Child']
    chars = cur_dict[sub_name]['Chars']
    print(space, sub_name)
    space += '------'
    for char in chars:
        print(space, char)
    if childs:
        for child in childs:
            recurs_chars_descript(cur_dict, child, space = '---')

def add_sub_parent(cur_dict, sub_name, parent_name):
    cur_dict[sub_name]['Parent'].add(parent_name)
    cur_dict[parent_name]['Child'].add(sub_name)

def add_sub_chars(cur_dict, sub_name, chars_name):
    try:
        cur_dict[sub_name]['Chars'].add(chars_name)
    except:
        cur_dict[sub_name]['Chars'] = {chars_name}

def update_examples(cur_dict):
    for ex_name in cur_dict:
        try:
            cur_dict[ex_name]['Chars']
        except:
            cur_dict[ex_name]['Chars'] = set()


def recurse_interface():
    command = input(str('Вызов подсказок: "9" \nВведите номер команды: '))
    load_set = load('Subjects_dict.pckl')
    if not load_set:
        load_set = dict()
    if command == '0':
        save(load_set, 'Subjects_dict.pckl')
        print('Успешно закрылись')
        quit()
    elif command == '1':
        for el in load_set:
            print(load_set[el]['id'], el)

    elif command == '2':
        create_subject(load_set, input(str('Введите название предмета: ')))
        save(load_set, 'Subjects_dict.pckl')

    elif command == '3':
        for el in load_set:
            recurs_chars_descript(load_set, el)
            print('\n')

    elif command == '4':
        num = 0
        num_list = []
        for el in load_set:
            num_list.append(el)
            print(num, el)
            num += 1
        del_num = input('что удалить? ')
        del_num = int(del_num)
        load_set.pop(num_list[del_num])

        save(load_set, 'Subjects_dict.pckl')

    elif command == '5':
        update_examples(load_set)
        print('Успешно Обновлено')
        save(load_set, 'Subjects_dict.pckl')
    elif command == '6':
        print("Выбери экземпляр\n(для выхода '0')")
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
            print('Добавляем родителя\n Выбрать из списка - "1"\n Создать новый - "2"')
            sec_num_com = str(input("Введите номер: "))
            if sec_num_com == '1':
                sec_num = 0
                sec_num_list = []
                for el in load_set:
                    sec_num_list.append(el)
                    print(sec_num, el)
                    sec_num += 1
                sec_ex_num = int(input('Номер экземпляра: '))
                parent_example = sec_num_list[sec_ex_num]
                # change_example.parent = {parent_example}
                add_sub_parent(load_set, change_example, parent_example)
                save(load_set, 'Subjects_dict.pckl')
            elif sec_num_com == '2':
                print('Ups')
        elif num_com == '3':
            print('Добавляем характеристику')
            chars_name = str(input("Введите название характеристики: "))
            add_sub_chars(load_set, change_example, chars_name)
            save(load_set, 'Subjects_dict.pckl')


    elif command == '9':
        print('''\
        0 - Выход
        1 - Показать все объекты
        2 - Добавить новый экземпляр
        3 - Показать дерево
        4 - Удалить элемент
        5 - Обновить экземпляры
        6 - Добавить данные в класс
        ''')

        # os.system('cls')
    recurse_interface()
recurse_interface()
