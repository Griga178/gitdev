# Тест 4 задачи
my_keys = ['A', 'B', 'C', 'D']

combination = []

for a in range(1, 5):
    for b in range(1, 5):
        for c in range(1, 5):
            for d in range(1, 5):
                srv_dict = {
                    "A": a,
                    "B": b,
                    "C": c,
                    "D": d,
                }
                combination.append(srv_dict)


def emu_mew(combo, i = 0, j = -1, elements = False):
    variables = []
    if elements:
        for ie in elements:
            key = my_keys[ie]
            variables.append(combo[key])
    else:
        query = my_keys[i:j]
        for el in query:
            variables.append(combo[el])

    values = sorted(variables)
    return values

def check(combo, answer):
    i = 0
    wrong = False
    for k, v in combo.items():
        # print(k, v, answer[i])
        if v != answer[i]:
            wrong = True
        i += 1
    print('Error:', combo, answer) if wrong else None

def main(combo):
    query_1 = emu_mew(combo, 0, 3)
    if len(set(query_1)) == 1:
        # 1-3 значения одинаковы
        val_1, val_2, val_3 = query_1
        query_2 = emu_mew(combo, 3, 4)
        val_4 = query_2[0]

    elif len(set(query_1)) == 2:
        # 1-3 значения делятся на 2 типа
        query_2 = emu_mew(combo, 1, 4)
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
                query_3 = emu_mew(combo, elements = [0, 1, 3])

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
            query_3 = emu_mew(combo, 1, 2)
            val_2 = query_3[0]
            val_3 = list(set(query_2) - {val_4} - {val_2})[0]

    elif len(set(query_1)) == 3:
        # 1,2,3 значения разные --> смотрим на 2,3,4
        query_2 = emu_mew(combo, 1, 4)
        if len(set(query_2)) == 2:
            # Всего 3 типа значений
            for el in query_2:
                if query_2.count(el) == 2:
                    double_in_2 = el
                    break
            val_4 = double_in_2
            val_1 = list(set(query_1) - set(query_2))[0]
            query_3 = emu_mew(combo, 1, 2)
            val_2 = query_3[0]
            query_1.remove(val_1)
            query_1.remove(val_2)
            val_3 = query_1[0]
        else:
            if query_1 == query_2:
                query_3 = emu_mew(combo, elements = [0, 1, 3])
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
                query_3 = emu_mew(combo, 1, 2)
                val_2 = query_3[0]
                val_3 = list(set(query_1) - {val_2} - {val_1})[0]

    final_values = [val_1, val_2, val_3, val_4]
    check(combo, final_values)

counter = 0
for combo in combination[:]:
    counter += 1

    main(combo)
