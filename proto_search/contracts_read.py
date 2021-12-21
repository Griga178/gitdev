import os
import pickle

def pkl_set_reader(file_name):
    '''Чтение файла .pkl'''
    with open(file_name, 'rb') as f:
        pickle_dict = pickle.load(f)
    return pickle_dict

def print_table(full_dict):
    '''Вывод всего словаря'''
    count = 0
    for number in full_dict:
        print(number) # Номер контракта - ключ словаря
        list_name_char = full_dict[number] # список со словарями из товаров
        count += len(list_name_char)
        for dict_in_list in list_name_char: # перебор словарей
            for dict_key in dict_in_list: # перебор
                print(dict_key)
                for char in dict_in_list[dict_key]:
                    print(char, '- - -', dict_in_list[dict_key][char])
    print(f'\n\nВсего товаров {count} шт.\n')


file_name = 'Parsing/contract_union_of_dicts.pkl'

my_dict = pkl_set_reader(file_name)

print_table(my_dict)
