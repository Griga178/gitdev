variables = ['Window','Bird','Food','Human']
# variables = [input() for i in range(4)]
# with open('input.txt') as f:
#     variables = f.read().split('\n')[:-1]

# with open('answer.txt') as f:
#     values = f.read().split('\n')[:-1]
# with open('output.txt', 'w') as f:
#     for val in values:
#         f.write(val.strip() + '\n')

# for val in values:
#     print(val.strip())

import requests
import sys

class MyDict(dict):
    def __init__(self, key, variables):
        self.my_key = key
        self.variables = variables

    def copy(self):
        return self

    def items(self):
        return ((self.my_key, var) for var in self.variables)

url = 'http://127.0.0.1:7777/'
s = requests.Session()

def do_mew(i = 0, j = -1):
    req = requests.Request('MEW', url)
    prepped = req.prepare()
    prepped.headers = MyDict('x-cat-variable', variables[i:j])
    resp = s.send(prepped)
    resp = {k.lower(): v for k, v in resp.headers.items()}

    values = resp['x-cat-value'].split(',')
    values = [i.strip() for i in values]
    return values

# variables = [sys.stdin.readline().strip() for i in range(4)]
final_values = []


# 1-й Запрос к 1-3 позициям
query_1 = do_mew(0, 3)
if len(set(query_1)) == 1:
    # 1-3 значения одинаковы
    final_values = query_1
    query_2 = do_mew(3, 4)
    final_values.append(query_2[0])

elif len(set(query_1)) == 2:
    # 1-3 значения делятся на 2 типа
    # находим значение 1 элемента
    query_2 = do_mew(0, 1)
    val_1 = query_2[0]

    if query_1.count(val_1) == 1:
        # 2 и 3 значения - одинаковы
        val_2_and_3 = list(set(query_1) - set(val_1))[0]
        # находим 4 значение
        query_3 = do_mew(3, 4)
        val_4 = query_3[0]
        final_values = [val_1, val_2_and_3, val_2_and_3, val_4]
    else:
        # 2 и 3 значения - разные --> смотрим 3-й и 4-й
        # одно из них = значению 1-ого элемента
        query_3 = do_mew(2, 4)
        if len(set(query_3)) == 1:
            # 3 и 4 значения - одинаковы
            val_3_and_4 = list(set(query_3))[0]
            ''' !!!!!!!!!! - ? '''
            val_2 = list(set(query_1) - set(val_1))[0]
            final_values = [val_1, val_2, val_3_and_4, val_3_and_4]
        else:
            # 3 и 4 - разные
            ''' !!!!!!!!!! '''
            val_3 = list(set(query_3) & set(query_1))[0]
            val_4 = list(set(query_3) - set(val_3))[0]
            val_2 = list(set(query_1) - set(val_3))[0]
            final_values = [val_1, val_2, val_3, val_4]


elif len(set(query_1)) == 3:
    # 1,2,3 значения разные --> смотрим на 2,3,4
    query_2 = do_mew(1, 4)
    if len(set(query_2)) == 2:
        # знаем значение 1-ого элемента
        val_1 = list(set(query_1) - set(query_2))[0]
        # смотрим значение 2 элемента
        query_3 = do_mew(1, 4)
        val_2 = query_3[0]
        if query_3.count(val_2) == 1:
            # 3 и 4 значения - одинаковы
            val_3_and_4 = list(set(query_2) - set(val_2))[0]
            final_values = [val_1, val_2, val_3_and_4, val_3_and_4]
        else:
            # 2 и 4 значения - одинаковы
            val_4 = query_3[0]
            val_3 = list(set(query_2) - set(val_2))[0]
            final_values = [val_1, val_2, val_3, val_4]

    else:
        # знаем 1 и 4 значения
        val_1 = list(set(query_1) - set(query_2))[0]
        val_4 = list(set(query_2) - set(query_1))[0]
        # находим 2 значение
        query_3 = do_mew(1, 2)
        val_2 = query_3[0]
        val_3 = list((set(query_2) & set(query_1) - set(query_3)))[0]
        final_values = [val_1, val_2, val_3, val_4]


for sval in final_values:
    val = ''.join(sval)
    sys.stdout.write(val + '\n')
