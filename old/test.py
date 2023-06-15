str_a = 'Тип подключения клавиатуры'
str_b = 'Тип подключения'


def levenshtein(s1, s2):
    '''
        расстояние редактирования между двумя строками
        почти = from difflib import SequenceMatcher
    '''
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    cicle_a = 0
    cicle_b = 0
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        cicle_a += 1
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            cicle_b += 1
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


#print(levenshtein(set_a, set_b))

from difflib import SequenceMatcher

#ratio_a = SequenceMatcher(None, set_a, set_b).ratio()

#print(ratio_a)

set_a = {'Тип матрицы монитора',
                'Угол обзора монитора по вертикали, градус',
                'Угол обзора монитора по горизонтали, градус',
                'Тип клавиатуры', 'Размер диагонали монитора',
                'Длина кабеля мыши',
                'Максимальная частота обновления (смена кадров) монитора',
                'Тип подключения мыши', 'Наличие встроенных динамиков монитора',
                'Наличие боковых кнопок мыши', 'Тип сенсора мыши',
                'Интерфейс подключения клавиатуры',
                'Разрешение сенсора мыши, точек/дюйм', 'Интерфейс подключения мыши',
                'Интерфейс подключения монитора',
                'Наличие дополнительных клавиш клавиатуры',
                'Тип подключения клавиатуры',
                'Разрешение экрана монитора',
                'Яркость монитора, кд/м2'}

set_b = {'Наличие боковых кнопок',
            'Максимальная частота обновления (смена кадров)',
            'Тип сенсора',
            'Тип подключения',
            'Разрешение сенсора, точек/дюйм',
            'Тип матрицы',
            'Разрешение экрана',
            'Длина кабеля',
            'Размер диагонали',
            'Угол обзора по вертикали, градус',
            'Интерфейс подключения',
            'Яркость, кд/м2',
            'Наличие дополнительных клавиш',
            'Наличие встроенных динамиков',
            'Угол обзора по горизонтали, градус',
            'Тип'}


def compearing_set (set_a, set_b, set_print = False):
    '''
    '''
    cicle_run_count = 0
    used_keys = {'a'}
    compeared_set = set()
    # Создали set в котором хранятся все значения "коэф одинаковости" (а - удалится)
    while len(used_keys) != 0:
        # пока все значения не будут соотнесены
        cicle_run_count += 1
        if set_print:
            print(f'Запуск цикла № {cicle_run_count}')
            print(f'нет пар для {len(set_a)} значений')
            print(f'количество пар {len(set_b)} шт\n')

        # множество tuple, содержащие пары значений
        test_dict = {}
        if set_print:
            print(f'    Подбираем наиболее "подходимые" значения')

        for first_string in set_a:
            # Подбираем максимально подходящие строки из множества б к множ. а
            second_element = str()
            max_ratio_a = 0
            for second_string in set_b:
                # перебираем их "схожесть"
                cur_ratio_a = SequenceMatcher(None, first_string, second_string).ratio()
                if cur_ratio_a > max_ratio_a:
                    # выбираем максимальную
                    max_ratio_a = cur_ratio_a
                    second_element = second_string
            # записываем в словарь максимально похожие строки
            test_dict.update({round(max_ratio_a, 3): (first_string, second_element)})                   #### ПЕРВАЯ ПОДБОРКА
        # сортируем по убыванию значение "похожести"
        sorted_list = sorted(test_dict, key = float, reverse = True)
        sorted_dict = {}
        for el in sorted_list:
            # создаем отсортированый словарь
            sorted_dict[el] = test_dict[el]

        if set_print:
            print(f'    Отсортированный список готов!\n')

        #used_keys = sorted_dict.keys()
        used_keys = set()
        for el in sorted_dict:
            used_keys.add(sorted_dict[el][0])
        # добавляем ключи "подходимости" отсортированного словаря!

        test_set_a = set()
        test_set_b = set()
        test_set_keys = set()

        for key in sorted_dict:                         #### ВТОРАЯ ПОДБОРКА
            # первая строка с масимальной схожестью
            first_string = sorted_dict[key][0]
            #first_string = key
            if set_print:
                print(f'Первая строка:   {first_string}')
                second_prob_string = sorted_dict[key][1]
                print(f'Подходящий вариант:   {second_prob_string} __ {key}')

            max_ratio_b = 0
            # Соединяем максимально похожие строки
            # Использованные значения "удаляем"
            if first_string in test_set_a or second_string in test_set_b:
                if len(set_b) == 0:
                    second_element = 'Значения закончились'
                if set_print:
                    print(f'- - - - - -пропускаем цикл с {first_string}- -\n')

            else:
                if set_print:
                    print('- -Перебираем значения- -')

                if len(set_b) == 0:
                    second_element = 'Значения закончились'
                else:
                    for second_string in set_b:
                        # выбор максимально подходящей из имеющихся
                        cur_ratio_a = SequenceMatcher(None, first_string, second_string).ratio()
                        if cur_ratio_a > max_ratio_b:
                            max_ratio_b = cur_ratio_a
                            second_element = second_string
                    if set_print:
                        print(f'Подобрали:   "{second_element}" -- {round(max_ratio_b, 3)}')
                    test_set_b.add(second_element)
                    test_set_keys.add(first_string)
                    set_a.discard(first_string)

                # Записываем все значения, совпадения которых уже использовались
                for el in sorted_dict:
                    if sorted_dict[el][1] == second_element:
                        test_set_a.add(first_string)
                        #test_set_a.add(el)
                        if set_print:
                            print(f'Это больше не сравниваем:   {first_string}')
                if set_print:
                    print('\n')

                # Записали ключи значений которые найдены
                #test_set_keys.add(sorted_dict[el][0])
                # Удаляем, что бы не использовать в следующем кругу
                set_b.discard(second_element)
                current_taple = (first_string, second_element, max_ratio_a)
                compeared_set.add(current_taple)
        if set_print:
            print(f'Длинна первого списка: {len(set_a)}')
            print(f'Длинна второго списка: {len(set_b)}\n')

                    #print(current_taple)


        used_keys = used_keys - test_set_keys
        print(len(used_keys))
        print(len(test_set_b))





    print(set_b - test_set_b)




    return compeared_set


co_set = compearing_set(set_a, set_b, True)

print('\n')
for el in co_set:
    print(el)
