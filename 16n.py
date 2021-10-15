'''
Сравнение двух словарей на наличие значений, характеристик и их значений

... Проверка на правильность заполнения аисгз
 --- готовый код в test2

 теперь нужен вывод словарей
'''

import openpyxl
import time
import pickle


def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)


name_my_file = 'C:/Users/G.Tishchenko/Desktop/my_list.xlsx'

def search_set(file_name):
    wb = openpyxl.load_workbook(file_name, read_only = True, data_only = True)
    active_sheet = wb['names']

    search_val = set()

    for row in active_sheet.rows: #
        # чтение ячеейк в строках и добавление в ""список строки"
        for cell in row[:1]:
            #print(cell.value)

            search_val.update({cell.value})
    return search_val


dict2 = load_obj('direct_kkn.pkl')
dict1 = load_obj('our_kkn.pkl')

set_of_keys = search_set(name_my_file)



        if type(ais_value) == list and type(our_value) == list:
            # Тут 3 вида характеристик
            '''
            эта штука менят единицу измерения на set(строк) - на случай нескольких единиц измерения!?!?

            - Надо применить, при выгрузке из excel и убрать пробелы при разделении на set (;)
            '''
            if ais_value[-1] == '-':
                ais_value[-1] = ''
            if our_value[-1] == '-':
                our_value[-1] = ''

            ais_value[-1] = set(ais_value[-1].split(';'))
            our_value[-1] = set(our_value[-1].split(';'))


            if len(ais_value) == 3 and len(our_value) == 3:
                # где есть максимальное или минимальное значение

                if ais_value[0] != our_value[0] or ais_value[1] != our_value[1]:
                    print('- - - - ККН- - - - ККН- - - - ККН- - - - ККН: ', el)
                    print(ais_value, our_value)

            elif len(ais_value) == 2 and type(ais_value[0]) == set:
                # где много значений [{set}, "ШТ"]

                if  ais_value[0] != our_value[0]: # or ais_value[1] != our_value[1]
                    # Проверка множеств на идентичность

                    #print('- - - - ККН- - - - ККН- - - - ККН- - - - ККН: ', el)
                    #print('- - - - ХАР: ', jel)
                    #print(ais_value, our_value)
                    my_count += 1
            elif len(ais_value) == 2 and type(ais_value[0]) == str:
                # где ондно значение str

                pass
            else:
                counter_c += 1
        elif type(ais_value) == str and type(our_value) == str:
            # Тут всегда 4 характеристики (по идее)
            # (ОКПД2, Детализация, Единица измерения, Категория)
            pass
        else:
            # до сюда дойти не должно!
            counter_c += 1


print(counter_k, counter_c)
print(my_count)
'''
Пример словаря:

input = {'Компьютер тип 1': {
                        'ОКПД2' : '112.112.01',                     # 4 постоянные характеристики (ОКПД2, Детализация, Единица измерения, Категория)
                        'Ширина корпуса': ['200', '300', 'ММ'],     # и много переменных хар-к 3-х видов: ['список', 'из 3-х', 'элементов']
                        'количество ядер': [{'1','2','3'}, 'ШТ']    # [{'список', 'тут множество'}, 'из 2-х элементов']
                        'количество потоков': ['>1', 'ШТ']          # [str(список), 'из 2-х элементов']

}}

compared = {'Компьютер тип 1':
                {
                'ОКПД2AI' : '112.112.01',
                'ОКПД2CM' : '112.112.02'},
                'ОКПД2DIF' : '112.112.02'},
                'Имя характеристикиAI': {'Тип интерфейса', ...}
                'Имя характеристикиCM': {'Тип интерфейса монитора', ...}
                }
'''
