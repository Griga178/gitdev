
def comparison_ais_cmec_dicts(first_dict, second_dict, set_of_names = set()):
    ''' функция сравнивает два словаря
    main_key = Наименование ккн
    child_key = Наименование характеристик

    - 1 Сравнение ключей в о всех словарях
            => общие знач + чего и где нет
    - 2 Сравнение названий характеристик в существующих ккнах
    - 3 Сравнение значений одинаковых характеристик
    '''
    wrong_dict = {}
    first_set = first_dict.keys()
    second_set = second_dict.keys()

    ## -- № 1
    if set_of_names:
        work_set_of_names = first_set & second_set & set_of_names
        first_set_loss = set_of_names - (first_set & set_of_names)
        second_set_loss = set_of_names - (second_set & set_of_names)
    else:
        work_set_of_names = first_set & second_set
        first_set_loss = second_set - (first_set & second_set)
        second_set_loss = first_set - (first_set & second_set)
    if first_set_loss:
        wrong_dict = wrong_dict | {'loss_keys': first_set_loss}
    if second_set_loss:
        wrong_dict = wrong_dict | {'loss_keys_2': second_set_loss}
    if not first_set_loss and not second_set_loss:
        print('Все ккн-ы нашлись\n')

    ## -- № 2
    for kkn_name in work_set_of_names:

        first_char_set = first_dict[kkn_name].keys()
        second_char_set = second_dict[kkn_name].keys()

        comon_char_names = first_char_set & second_char_set
        first_char_loss = second_char_set - comon_char_names
        second_char_loss = first_char_set - comon_char_names
        if first_char_loss or second_char_loss:
            wrong_dict = wrong_dict | {kkn_name: {'loss_char': [first_char_loss, second_char_loss]}}

        ## -- № 3
        for char in comon_char_names:
            adding_char = {}
            first_char_value = first_dict[kkn_name][char]
            second_char_value = second_dict[kkn_name][char]

            if type(first_char_value) == str and type(second_char_value) == str:

                if first_char_value != second_char_value:
                    adding_char = {char: [first_char_value, second_char_value]}

            elif type(first_char_value) == list and type(second_char_value) == list:

                if len(first_char_value) == 3 and len(second_char_value) == 3:
                    # где есть максимальное или минимальное значение

                    if first_char_value[0] != second_char_value[0] or first_char_value[1] != second_char_value[1]:
                        adding_char = {char: [first_char_value[0:1], second_char_value[0:1]]}

                elif type(first_char_value[0]) == str or type(first_char_value[0]) == set:
                    # где ондно значение [str, "ШТ"]
                    # где много значений [{set}, "ШТ"]

                    if first_char_value[0] != second_char_value[0]:
                        adding_char = {char: [first_char_value[0], second_char_value[0]]}
                #else: #можно создать для проверки - должно быть пустым

                if first_char_value[-1] != second_char_value[-1]:
                    if adding_char:
                        adding_char[char].append(first_char_value[-1])
                        adding_char[char].append(second_char_value[-1])
                    else:
                        adding_char = {char: [first_char_value[-1], second_char_value[-1]]}

            if kkn_name in wrong_dict:
                wrong_dict[kkn_name] = wrong_dict[kkn_name] | adding_char
            else:
                wrong_dict = wrong_dict | {kkn_name: adding_char}

    return wrong_dict



first_set = {'a': {'ОКПД2' : '112.112.02'}, 'b': {'ОКПД2' : '112.112.01', 'количество ядер': [{'1','2','3'}, 'ШТ']}, 'c':{'ОКПД2' : '112.112.03', 'Ширина корпуса': ['200', '300', 'ММ']}, 'd':{'ОКПД2' : '112.112.04'}, 'e':{'ОКПД2' : '112.112.05'}, 'f': {'ОКПД2' : '112.112.11'}}
second_set = {'b': {'ОКПД2' : '112.112.01'}, 'c': {'ОКПД2' : '112.112.01', 'Ширина корпуса': ['200', '300', 'ММ']}, 'f': {'ОКПД2' : '112.112.11'}, 'a': {'ОКПД2' : '112.112.02'}}
my_set = {'a', 'b', 'f', 'l'}



#wrong_dict = comparison_ais_cmec_dicts(first_set, second_set, my_set)

#print(wrong_dict)

import openpyxl
import time
import pickle

def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)



name_my_file = 'C:/Users/G.Tishchenko/Desktop/sentember_fresh.xlsx'

def search_set(file_name):
    wb = openpyxl.load_workbook(file_name, read_only = True, data_only = True)
    active_sheet = wb['names']

    search_val = set()

    for row in active_sheet.rows: #
        # чтение ячеейк в строках и добавление в ""список строки"
        for cell in row[:1]:
            #print(cell.value)

            search_val.update({cell.value})
    return search_val

dict1 = load_obj('our_kkn.pkl')
dict2 = load_obj('aic_dict.pkl')


set_of_keys = search_set(name_my_file)

#print(set_of_keys)
wrong_dict_1 = comparison_ais_cmec_dicts(dict1, dict2) #, set_of_keys


count = 0
for el in wrong_dict_1.keys():
    #print(el, wrong_dict_1[el])
    #print('\n\n', el)
    if wrong_dict_1[el] == 'loss_keys_2':
        print(wrong_dict_1[el])
        for char in wrong_dict_1[el]:
            print(char, wrong_dict_1[el][char])



print(count)
