set_of_keys = {'яблоко', 'Груша', 'арбуз', 'дыня', 'Апельсин'}
set_of_keys2 = {'яблоко', 'Груша'}
dict1 = {'яблоко':{'вес':5, 'цвет': 'красный'},                      'Груша':{'вес': 4,'цвет': 'желтый'}}
dict2 = {'яблоко':{'вес':4, 'цвет': 'синий'},                      'Груша':{'вес': 5,'цвет': 'зеленый'},
'арбуз':{'вес': 10,'цвет': 'желтый'},
'Виноград':{'вес': 2,'цвет': 'Фиолетовый'}}
dict3 = {'яблоко':{'вес':5, 'цвет': 'красный'},                      'Груша':{'вес': 4,'цвет': 'желтый'}}

'''
print(f'Искомые значения: {set_of_keys}')
search_in_dict1 = dict1.keys() & set_of_keys
search_in_dict2 = dict2.keys() & set_of_keys
print(f'То что есть в первом словаре: {search_in_dict1}')
print(f'То что есть во втором словаре: {search_in_dict2}')
#print(dict.keys() & set_of_keys)
#print(dict2.keys() & set_of_keys)

#for key in set_of_keys:
print('В первом словаре из искомого нашлось ... элементов')
print('Во втором словаре из искомого нашлось ... элементов')
print('В обоих словарях из искомого нашлись все элементы')
'''

if set_of_keys != dict1.keys():
    print('No')


# Тема для сохранения данных в файл сразу в словарь
import pickle


def save_obj(obj, name ):
    with open('test_dick' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)



def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)

save_obj(dict2, 'dict')
x = load_obj('test_dickdict.pkl')
print(type(x), x)
