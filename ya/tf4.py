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
    query_1 = emu_mew(combo, 0, 2)

    if len(set(query_1)) == 1:
        # 1-2 значения одинаковы
        return

    else:
        # 1-2 значения делятся на 2 типа
        query_2 = emu_mew(combo, 1, 4)

        if len(set(query_2)) == 1:
            val_2 = val_3 =  val_4 = query_2[0]
            val_1 = list(set(query_1) - {val_2})[0]
            final_values = [val_1, val_2, val_3, val_4]

        elif len(set(query_2)) == 2:
            if len(set(query_1) | set(query_2)) == 2:
                print(1)
            else:
                return
        else:
            return


    check(combo, final_values)


counter = 0
for combo in combination[:]:
    counter += 1

    main(combo)
