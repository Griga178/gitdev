# Решение задачи 
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

def do_mew(i = 0, j = -1, elements = False):
    req = requests.Request('MEW', url)
    prepped = req.prepare()
    send_variables = []
    if elements:
        for index in elements:
            send_variables.append(variables[index])
    else:
        send_variables = variables[i:j]
    prepped.headers = MyDict('x-cat-variable', send_variables)
    resp = s.send(prepped)
    resp = {k.lower(): v for k, v in resp.headers.items()}

    values = resp['x-cat-value'].split(',')
    values = [i.strip() for i in values]
    return values

variables = [sys.stdin.readline().strip() for i in range(4)]
final_values = []


# Запросы + обработка (1: ABC, 2: BCD, 3: ABD)
query_1 = do_mew(0, 3)
if len(set(query_1)) == 1:
    # 1-3 значения одинаковы
    val_1, val_2, val_3 = query_1
    query_2 = do_mew(3, 4)
    val_4 = query_2[0]

elif len(set(query_1)) == 2:
    # 1-3 значения делятся на 2 типа
    query_2 = do_mew(1, 4)
    if len(set(query_2)) == 1:
        val_2 = val_3 =  val_4 = query_2[0]
        val_1 = list(set(query_1) - {val_2})[0]

    elif len(set(query_2)) == 2:
        if set(query_2) != set(query_1):

            val_4 = list(set(query_2) - set(query_1))[0]
            val_3 = val_2 = list(set(query_2) - {val_4})[0]
            query_1.remove(val_3)
            query_1.remove(val_2)
            val_1 = query_1[0]
        else:
            query_3 = do_mew(elements = [0, 1, 3])

            if  len(set(query_3)) == 1:
                val_1 = val_2 = val_4 = list(set(query_3))[0]
                val_3 = list(set(query_1) - {val_2})[0]
            elif query_1 != query_2:
                for el in query_1:
                    if query_1.count(el) == 2:
                        double_in_1 = el
                        break
                for el in query_2:
                    if query_2.count(el) == 2:
                        double_in_2 = el
                        break
                val_1 = double_in_1
                val_4 = double_in_2
                query_3.remove(val_1)
                query_3.remove(val_4)
                val_2 = query_3[0]
                query_1.remove(val_1)
                query_1.remove(val_2)
                val_3 = query_1[0]

            elif query_2 != query_3:
                for el in query_1:
                    if query_1.count(el) == 2:
                        double_in_1 = el
                        break
                for el in query_3:
                    if query_3.count(el) == 2:
                        double_in_3 = el
                        break
                val_3 = double_in_1
                val_4 = double_in_3
                query_2.remove(val_3)
                query_2.remove(val_4)
                val_2 = query_2[0]
                query_1.remove(val_2)
                query_1.remove(val_3)
                val_1 = query_1[0]
            else:
                for el in query_1:
                    if query_1.count(el) == 1:
                        val_unic = el
                        break
                val_2 = val_unic
                val_1 = val_3 = val_4 = list(set(query_1) - {val_2})[0]

    elif len(set(query_2)) == 3:
        val_4 = list(set(query_2) - set(query_1))[0]
        for el in query_1:
            if query_1.count(el) == 2:
                double_in_1 = el
                break
        val_1 = double_in_1
        query_3 = do_mew(1, 2)
        val_2 = query_3[0]
        val_3 = list(set(query_2) - {val_4} - {val_2})[0]

elif len(set(query_1)) == 3:
    # 1,2,3 значения разные --> смотрим на 2,3,4
    query_2 = do_mew(1, 4)
    if len(set(query_2)) == 2:
        # Всего 3 типа значений
        for el in query_2:
            if query_2.count(el) == 2:
                double_in_2 = el
                break
        val_4 = double_in_2
        val_1 = list(set(query_1) - set(query_2))[0]
        query_3 = do_mew(1, 2)
        val_2 = query_3[0]
        query_1.remove(val_1)
        query_1.remove(val_2)
        val_3 = query_1[0]
    else:
        if query_1 == query_2:
            query_3 = do_mew(elements = [0, 1, 3])
            # По логике:  query_1 != query_3
            # ==> query_2 != query_3
            for el in query_3:
                if query_3.count(el) == 2:
                    double_in_3 = el
                    break
            val_4 = double_in_3
            val_3 = list(set(query_1) - set(query_3))[0]
            # в этом случае 1-й == 4-ому
            val_1 = val_4
            val_2 = list(set(query_1) - {val_1} - {val_3})[0]
        else:
            # Всего 4 типа значений
            val_1 = list(set(query_1) - set(query_2))[0]
            val_4 = list(set(query_2) - set(query_1))[0]
            query_3 = do_mew(1, 2)
            val_2 = query_3[0]
            val_3 = list(set(query_1) - {val_2} - {val_1})[0]

final_values = [val_1, val_2, val_3, val_4]

for sval in final_values:
    val = ''.join(sval)
    sys.stdout.write(val + '\n')
