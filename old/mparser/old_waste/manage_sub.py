import sys
sys.path.append('../')
from data_loader import save_pkl as save
from data_loader import load_pkl_file as load

from classes import Subject_ver_3, Subjects_category, Model_ver2

def recurse_interface(command = False, sec_command = False):
    pickle_file_name = 'Models_Subjects_dict'
    try:
        load_dict = load(pickle_file_name)
    except:
        print('Создана новая база!')
        load_dict = {'Subjects': set(), 'Models': set()}
    print(' - - - - - - - - - - - - - - - - - - - - ')
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
                recurse_interface('2')
        elif sec_command == '2':
            input_mod = input(str('Назад - 0\nВведите название модели: '))
            if input_mod == '0':
                recurse_interface('2')
            else:
                load_dict['Models'].add(Model_ver2(input_mod))
                save(load_dict, pickle_file_name)
                print(f'Модель: "{input_mod}" - успешно добавлен')
                recurse_interface('2')
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
            print('Выбрать предмет - 1\nВыбрать модель - 2\nСтарое описание - 3')
            sec_command = input(str('Введите номер команды: '))
        if sec_command == '1':
            # print("Выбери экземпляр")
            chosen_example = chose_example(load_dict['Subjects'])
            chosen_example.chars_description(load_dict['Subjects'])
            chosen_example.show_model()
        elif sec_command == '2':
            chosen_example = chose_example(load_dict['Models'])
            chosen_example.description()
        elif sec_command == '3':
            for el in load_dict['Subjects']:
                print('\n', el)
                el.show_child()
                el.show_parent()
                el.show_model()
                el.show_chars()
        else:
            print("Непонятная команда")
            recurse_interface('2')

    elif command == '4':
        print("Удаление экземпляра")
        if not sec_command:
            sec_command = str(input('Предмета - 1\nМодели - 2\nНазад - 0\nКоманда: '))
        if sec_command == '1':
            sub_example = chose_example(load_dict['Subjects'])
            if sub_example:
                load_dict['Subjects'].remove(sub_example)
                print(f'Предмет: {sub_example} - удален')
                save(load_dict, pickle_file_name)
            else:
                print("Неудача")
        elif sec_command == '2':
            mod_example = chose_example(load_dict['Models'])
            if sub_example:
                load_dict['Models'].remove(mod_example)
                print(f'Предмет: {mod_example} - удален')
                save(load_dict, pickle_file_name)
            else:
                print("Неудача")
        elif sec_command == '0':
            recurse_interface()
        else:
            print("\nНепонятная команда")
            recurse_interface("9")

    elif command == '5':
        if not sec_command:
            print('Обновление классов')
            print('Предметы - 1\nМодели - 2\nКатегории - 3\n')
            sec_command = input(str('Введите номер команды: '))
        if sec_command == '1':
            new_set = set()
            for example in load_dict['Subjects']:
                print(example, 'update')
                jel = Subject_ver_3(name = example.name, parent = example.parent, child = example.child, chars = example.chars, models = example.models)
                new_set.add(jel)
            load_dict['Subjects'] = new_set
            save(load_dict, pickle_file_name)
            print('Предметы успешно Обновлены')
        elif sec_command == '2':
            new_set = set()
            for example in load_dict['Models']:
                print(example, 'update')
                jel = Model_ver2(name = example.name, subject_name = ''.join(list(example.subject_name)) if type(example.subject_name) == set else example.subject_name, model_parents = example.model_parents,
                    model_childs = example.model_childs, model_chars = example.model_chars, categories = False)
            load_dict['Models'] = new_set
            save(load_dict, pickle_file_name)
            print('Предметы успешно Обновлены')
        else:
            recurse_interface()

    elif command == '6':
        print('Работа с экземлярами')
        if not sec_command:
            print('Предмет - 1 - Модель -2')
            sec_command = str(input("Введите номер: "))
        if sec_command == '1':
            print("Выбери экземпляр предмета")
            change_example = chose_example(load_dict['Subjects'])
            print('Что добавить?\n 1 - Родитель\n 2 - Ребенок\n 3 - Характеристика\n 4 - Модель')
            third_command = str(input("Введите номер: "))
            if third_command == '1':
                print(f'Добавляем родителя к {change_example}\n Выбрать из списка - "1"\n Создать новый - "2"')
                sec_num_com = str(input("Введите номер команды: "))
                if sec_num_com == '1':
                    parent_example = chose_example(load_dict['Subjects'])
                    change_example.add_parent(str(parent_example), parent_example)
                    save(load_dict, pickle_file_name)
            elif third_command == '2':
                print(f'Добавляем ребенка к {change_example}\n Выбрать из списка:')
                child_example = chose_example(load_dict['Subjects'])
                change_example.add_child(str(child_example), child_example)
                save(load_dict, pickle_file_name)
            elif third_command == '3':
                print('Добавляем характеристику')
                chars_name = str(input("Введите название характеристики: "))
                change_example.add_chars(chars_name)
                save(load_dict, pickle_file_name)
            elif third_command == '4':
                print('Добавляем модель (существующую) в экземпляр')
                model_example = chose_example(load_dict['Models'])
                change_example.add_models(model_example.name, model_example)
                save(load_dict, pickle_file_name)
        elif sec_command == '2':
            print("Выбери экземпляр предмета")
            model_example = chose_example(load_dict['Models'])
            print('Что добавить?\nПредмет - 1\nХарактеристика - 2')
            what_command = str(input('Введите номер: '))
            if what_command == '1':
                print('Not allowed')
            elif what_command == '2':
                chars_name = str(input('Название характеристики: '))
                chars_value = str(input('Значение: '))
                chars_measure = str(input('Единица измерения: '))
                model_example.add_chars_val(chars_name, chars_value, chars_measure, load_dict['Subjects'])
                save(load_dict, pickle_file_name)

    elif command == '7':
        print('Проверка характеристик')
        for example in load_dict['Subjects']:
            if example.chars:
                for chars_name in example.chars:
                    for example_two in load_dict['Subjects']:
                        if chars_name == example_two.name:
                            print("Совпадение! Не думаю!", chars_name, example.name)

    elif command == '8':
        try:
            exam_with_wrong_char = chose_example(load_dict['Subjects'])
            print(f"Экземпляр с лишними характеристиками: {exam_with_wrong_char}")
            wronng_chars_name = chose_example(exam_with_wrong_char.chars)
            print(f'Лишняя характеристика: {wronng_chars_name}')
            exam_with_wrong_char.chars.remove(wronng_chars_name)
            save(load_dict, pickle_file_name)
            print(f'{wronng_chars_name} - удалено')
            print('Повторить с экземплярами моделей/предметов')
        except:
            recurse_interface()
    # elif command == '10':

    elif command == '9':
        print('''\
        0 - Выход
        1 - Показать все экземпляры
        2 - Добавить новый экземпляр
        3 - Показать описание экземпляров
        4 - Удалить элемент
        5 - Обновить класс
        6 - Добавить данные в экземпляр
        7 - Проверка. Экземляр в характеристиках другого экземляра!
        8 - Изменение характеристик
        (переместить из хар-к модели в отдельную модель)
        х2 - Парсинг страницы характеристики
        х3 - Парсинг каталога''')

    else:
        print("\nНепонятная команда")
        recurse_interface("9")

    recurse_interface()


def chose_example(example_set):
    ex_number = 0
    temp_list = []
    for example in example_set:
        temp_list.append(example)
        print(ex_number, example)
        ex_number += 1
    try:
        command = int(input('Введите номер экземпляра: '))
        # print(temp_list[command])
        return temp_list[command]
    except:
        print('Не удалось выбрать экземпляр')
        return False

def buttons():

    pass
recurse_interface()
