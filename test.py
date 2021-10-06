# Значения которые мы проверям
set_of_keys = {'яблоко', 'Груша', 'арбуз', 'дыня', 'Апельсин'}

set_of_keys2 = {'яблоко', 'Груша'}
dict1 = {'яблоко':{'вес':5, 'цвет': 'красный', 'Страна производитель': 'Абхазия'}, 'Груша':{'вес': 4, 'Размер': '6см3', 'цвет': 'желтый', 'Страна производитель': 'Абхазия'}, 'Виноград':{'вес': 2,'цвет': 'Фиолетовый'}, 'арбуз':{'вес': 11,'цвет': 'зеленый'}}
dict2 = {'яблоко':{'вес':4, 'цвет': 'красный'}, 'Груша':{'вес': 5,'цвет': 'зеленый', 'Размер': '5см3', 'Страна производитель': {'Абхазия', 'Россия'}},
'арбуз':{'вес': 10,'цвет': 'желтый'}, 'Виноград':{'вес': 2,'цвет': 'Фиолетовый'}}
dict3 = {'яблоко':{'вес':5, 'цвет': 'красный'}, 'Груша':{'вес': 4,'цвет': 'желтый'}, 'Виноград':{'вес': 2,'цвет': 'Фиолетовый'}}

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

#if set_of_keys != dict1.keys():
    #print('No')


'''
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
'''

# Сравнение словарей == множеств (по ключам!): 1 и 2 + 3
# что есть в 1-ом, но хватает во 2-ом
second_value = dict1.keys() - dict2.keys()
#print(second_value, len(second_value))
# что есть в 2-ом, но не хватает во 1-ом
first_value = dict2.keys() - dict1.keys()
#print(first_value, len(first_value))
# Значения, которые есть в обоих словарях
common_value = dict1.keys() & dict2.keys() & dict3.keys()
#print(common_value, len(common_value))
# Значения, которые есть в обоих словарях и в словаре искомых значений
works_value = dict1.keys() & dict2.keys() & set_of_keys
#print(works_value, len(works_value), len(set_of_keys))
# Значения из словаря искомых значений, которые не нашлись в каком то из словарей
lose_value = set_of_keys - works_value
#print(lose_value, len(lose_value))


if works_value == set_of_keys:
    print('Все искомые значения найдены, проверяем на наличие характеристик')
else:
    first_lose_set = set_of_keys - dict1.keys()
    second_lose_set = set_of_keys - dict2.keys()
    # ищем только то, что можем сравнить
    set_of_keys = set_of_keys & dict1.keys() & dict2.keys()
    print(f'В первом словаре не нашлось:\n{first_lose_set} \nВо втором словаре не нашлось:\n{second_lose_set}')
    print(f'Проверяем только по найденым позициям:\n{set_of_keys}')

wrong_kkn = {}
# Работа со значениями, которые есть везде (в сравниваемых словарях и во множестве искомых значений)
for values in set_of_keys:
    # x - текущий словарь
    # y - эталонный словарь
    print('----', values)
    x = dict1[values]
    y = dict2[values]
# Сравнение то, что есть (что можно сравнить):
    set_of_char = y.keys() & x.keys()
    # Записываем то, чего не хватает:
    sum_char = y.keys() | x.keys() # Все характеристики

    wrong_char = sum_char - set_of_char # Характеристики с ошибками

    if wrong_char:
        print(wrong_char)
        wrong_kkn |= {values: wrong_char}

    # сравнение по тем характеристикам, которые есть
    for elements in set_of_char:
        x_elem = x[elements]
        y_elem = y[elements]
        if x_elem != y_elem:
            print('--',elements)
            print(x_elem, y_elem)
    #print(x, y)

print(f'Не хватает искомых ККН: {first_lose_set, second_lose_set}')
print(f'Недостаток характеристик: {wrong_kkn}')
