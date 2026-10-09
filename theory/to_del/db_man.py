from data_d1 import db

def select(find_raw, data_base):
    tags = find_raw.split('_')
    # print(tags)
    # шаг 1 - ищем полное совпадение
    res_0 = data_base.get(find_raw)
    # шаг 2
    if type(res_0) == list:
        print(' '.join(tags))
        for rel_text in res_0:
            # res_1 = data_base.get(find_raw + '_' + rel_text)
            res_1 = data_base.get(rel_text)
            st = rel_text.split('_')[-1]
            print(f'- - - {st}:', res_1)
    else:

        print(' '.join(tags), res_0) if res_0 else None


# select("теорема_пифагора_формула", db)
# select("теорема_пифагора", db)
select("закономерность", db)
