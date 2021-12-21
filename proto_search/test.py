
'''
Объединение пропарсенных множество
и множеств с ошибками
Объединение пропарсенных словарей


Не запускать сохраняет словари!!!


'''
import os
import pickle

def pkl_set_reader(file_name):
    with open(file_name, 'rb') as f:
        pickle_set = pickle.load(f)
    return pickle_set

def pkl_saver(file_name, variable_name):
    with open(file_name, 'wb') as f:
        pickle.dump(variable_name, f, pickle.HIGHEST_PROTOCOL)


union_of_parsed_sets = set()
error_union_of_sets = set()
contract_union_dict = {}

search_in = 'Parsing'
list_in = os.listdir(search_in)


for el in list_in:
    file_name = el.split('_')
    if file_name[-1] == 'parsed.pkl':
        temp_set = pkl_set_reader('Parsing/' + el)
        union_of_parsed_sets |= temp_set
        os.remove('Parsing/' + el)
    elif file_name[-1] == 'errors.pkl':
        temp_set = pkl_set_reader('Parsing/' + el)
        error_union_of_sets |= temp_set
        os.remove('Parsing/' + el)
    elif file_name[-1] == 'dict.pkl':
        #temp_dict = pkl_set_reader('Parsing/dicts/' + el)
        temp_dict = pkl_set_reader('Parsing/' + el)
        contract_union_dict |= temp_dict
try:
    old_set_errors = pkl_set_reader('Parsing/error_comon_set.pkl')
except:
    print('Не было old errors_set')
old_set_parsed = pkl_set_reader('Parsing/parsed_comon_set.pkl')
old_dict_parsed = pkl_set_reader('Parsing/contract_union_of_dicts.pkl')

union_of_parsed_sets |= old_set_parsed
error_union_of_sets |= old_set_errors
contract_union_dict |= old_dict_parsed

# Сохранение общего файла пропарсенных множеств
pkl_saver('Parsing/parsed_comon_set.pkl', union_of_parsed_sets)
print(len(union_of_parsed_sets))

# СОхранение общего файла множеств номеров, вызвавшшых ошибку
pkl_saver('Parsing/error_comon_set.pkl', error_union_of_sets)
print(len(error_union_of_sets))

pkl_saver('Parsing/contract_union_of_dicts.pkl', contract_union_dict)
print(len(contract_union_dict))

#for el in contract_union_dict:
    #union_of_parsed_sets.add(el)
#pkl_saver('Parsing/parsed_comon_set.pkl', union_of_parsed_sets)
