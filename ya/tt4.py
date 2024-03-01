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


def emu_mew(combo, i = 0, j = -1):
    query = my_keys[i:j]
    variables = []
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
        final_values = query_1
        query_2 = emu_mew(combo, 3, 4)
        final_values.append(query_2[0])

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
            # elif set(query_2) != set(query_1):
            else:
                if query_1 == query_2:
                    # print('ТУТ', combo)
                    # for el in query_1:
                    #     if query_1.count(el) == 2:
                    #         double_1 = el
                    # for el in query_2:
                    #     if query_2.count(el) == 2:
                    #         double_2 = el
                    # val_1 = double_1
                    # val_4 = double_2
                    #
                    # query_3 = emu_mew(combo, 1, 2)
                    # val_2 = query_3[0]
                    # query_1.remove(val_1)
                    # query_1.remove(val_2)
                    # val_3 = query_1[0]
                     query_3 = emu_mew(combo, 0, 2)
                     if len(set(query_3)) == 1:
                         val_1 = val_2 = list(set(query_3))[0]
                         val_3 = list(set(query_1) - {val_1})[0]
                         query_2.remove(val_3)
                         query_2.remove(val_2)
                         val_4 = query_2[0]
                     else:
                        for el in query_1:
                            if query_1.count(el) == 2:
                                double_1 = el

                        val_3 = double_1
                        val_1 = 5
                        val_2 = 5
                        val_4 = 5
                else:
                    '''     !!!!         '''
                    return

        elif len(set(query_2)) == 3:
            if len(set(query_1) | set(query_2)) == 2:
                for el in query_1:
                    if query_1.count(el) == 2:
                        val_1 = el
                val_4 = list(set(query_2) - set(query_1))[0]
                query_3 = emu_mew(combo, 1, 2)
                val_2 = query_3[0]
                query_2.remove(val_4)
                query_2.remove(val_2)
                val_3 = query_2[0]

            elif len(set(query_1) | set(query_2)) == 3:
                '''     !!!!         '''
                return
            else:
                '''     !!!!         '''
                return

        final_values = [val_1, val_2, val_3, val_4]
    else:
        return

    if True:
        pass
    elif len(set(query_1)) == 3:
        # 1,2,3 значения разные --> смотрим на 2,3,4
        query_2 = emu_mew(combo, 1, 4)
        if len(set(query_2)) == 2:
            # знаем значение 1-ого элемента
            val_1 = list(set(query_1) - set(query_2))[0]
            # смотрим значение 2 элемента
            query_3 = emu_mew(combo, 1, 4)
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
            query_3 = emu_mew(combo, 1, 2)
            val_2 = query_3[0]
            val_3 = list((set(query_2) & set(query_1) - set(query_3)))[0]
            final_values = [val_1, val_2, val_3, val_4]


    check(combo, final_values)

counter = 0
for combo in combination[:]:
    counter += 1

    main(combo)
