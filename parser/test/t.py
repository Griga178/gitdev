from tfuncs import *
from datetime import datetime
import time

class Links():

    def  __init__(self, name, price = False, date = False):
        self.name = name
        price_history = False
        if not date:
            date = datetime.now()
        self.price_history = {}
        if price:
            self.price_history = {date: price}

    def __str__(self):
        '''Надо обработать дату и показывать последнюю цену'''
        cur_price = ''
        if self.price_history:
            cur_price = f' Цена: {self.price_history}'
        answer = f'Ссылка: {self.name}' + cur_price
        return answer

    def add_new_price(self, price, date = datetime.now, scr_folder = False):
        ''' Добавление новой цены '''
        self.price_history[date] = price

# файл с экземлярами класса словарь с именем, либо множество
# pickle_dict_of_examples = set()

# Словарь, ключ - название ссылки, значение - экземпляр
pickle_dict_of_examples = {}

# Инфа из парсера [list]
infa = my_parser()

# преоразование инфы в экземпляр (потом сохранение в pkl - пропуск)
for info in infa:
    # pickle_dict_of_examples.add(Links(info))
    # pickle_dict_of_examples.add(Links(info))
    result = info.split(':')
    if result[0] not in pickle_dict_of_examples:
        pickle_dict_of_examples[result[0]] = Links(result[0], result[1])
        # pars_result_to_example()
    else:
        pickle_dict_of_examples[result[0]].add_new_price(result[1])
        # pars_result_to_example()
    time.sleep(0.1)
    print(info, pickle_dict_of_examples)


# изменение экземпляра
# new_price = {'citi/page1': 400.11}
#
# exa_name = 'citi/page1'
# pickle_dict_of_examples[exa_name].add_new_price(new_price[exa_name], '2022.27.03')

print('\n')
# вывод экземпляров
for example in pickle_dict_of_examples:
    # print(example.name)
    print(pickle_dict_of_examples[example])
    # print(pickle_dict_of_examples[example].price_history)
