'''
замена 14n.py (И 12n.py)
функция преобразующая excel файл с ккнами и его характеристиками в словарь
сохраняет его в формате pkl
Таблица содержит 11 столбцов
'''



import openpyxl
import time
import pickle


start_time = time.time()

def import_dicts_from_excel(file_name, listofsheets = None):
    # Переменная "listofsheets" содержит список существующих листов Excel по умолчанию
    # либо принимает ['Название  Листа']

    counter_kkn = 0
    counter_char = 0
    # Открываем файл только на чтение - по быстрому
    wb = openpyxl.load_workbook(file_name, read_only = True, data_only = True)

    if not listofsheets:
        listofsheets = wb.sheetnames


    pre_name = str()
    kkn_dict = {}

    name_okpd2 = 'ОКПД2'
    name_detalisation = 'Детализация'
    name_measure = 'Единица измерения'
    name_category = 'Категория'

    for current_sheet in listofsheets:
        # Перебираем листы по очереди
        active_sheet = wb[current_sheet]

        for row in active_sheet.rows:
            # Читаем каждую строку
            row_list = []

            for cell in row[:12]:
                # добавляем 12 ячеек строки в "список"
                my_cell = cell.value
                if my_cell == None:
                    my_cell = str('')

                row_list.append(my_cell)

            if len(str(row_list[1])) != 0:
                # Первое создание ключа и значений из этой же строки
                # Название ККН, которое распространяется на следующие строки
                pre_name = str(row_list[1]) # - ключ для будущего словаря! (ККН)

                # создается словарь для ккн-а
                # характеристики из первой строки
                permanent_char_dict = {name_okpd2: str(row_list[2]), name_detalisation: str(row_list[3]), name_measure: str(row_list[4]), name_category: str(row_list[11]).lstrip().rstrip()}
                kkn = {str(row_list[1]): permanent_char_dict}

                kkn_dict = kkn_dict | kkn
                counter_char += 1
                counter_kkn += 1

            if row_list[10] == '-':
                row_list[10] = ''

            if len(str(row_list[6])) != 0 or len(str(row_list[7])) != 0:
                # Если характеристика имеет максимальное или минимальное значение
                char_dict = {str(row_list[5]).lstrip().rstrip(): [str(row_list[6]), str(row_list[7]), str(row_list[10])]}
                kkn_dict[pre_name] = kkn_dict[pre_name] | char_dict
                counter_char += 1

            elif len(str(row_list[8])) != 0:
                # Если в характеристике есть изменяемые значения
                temp_list = str(row_list[8]).split(';')

                for i in range(len(temp_list)):
                    # Удаляем пробелы из элементов
                    temp_list[i] = str(temp_list[i]).lstrip().rstrip()
                value_set = set(temp_list)

                char_dict = {str(row_list[5]).lstrip().rstrip(): [value_set, row_list[10]]}
                kkn_dict[pre_name] = kkn_dict[pre_name] | char_dict
                counter_char += 1
            elif len(str(row_list[9])) != 0:
                # Характеристика определена одним значением
                temp_list = str(row_list[9]).lstrip().rstrip()

                char_dict = {str(row_list[5]).lstrip().rstrip(): [temp_list, row_list[10]]}
                kkn_dict[pre_name] = kkn_dict[pre_name] | char_dict
                counter_char += 1

    print(f'Колво ккн-в:  {counter_kkn}, Колво характ-к (строк):  {counter_char - counter_kkn}')
    # без первых строк
    try:
        del kkn_dict['Наименование ККН']
    except:
        print('Наименование ККН не нашлось')
    try:
        del kkn_dict['Название товара']
    except:
        print('Название товара не нашлось')
    try:
        del kkn_dict['2']
    except:
        print('2 не нашлось')

    return kkn_dict


test_ais = 'C:/Users/G.Tishchenko/Desktop/ditrctory.xlsx'
test_ais2 = 'C:/Users/G.Tishchenko/Desktop/check_dir.xlsx'
exel_name_ais = 'C:/Users/G.Tishchenko/Desktop/ais.xlsx'
exel_name_kkn = 'C:/Users/G.Tishchenko/Desktop/49_kkn.xlsx'

#ais_dict = import_dicts_from_excel(exel_name_ais)
#current_dict = import_dicts_from_excel(exel_name_kkn)
#current_dict = import_dicts_from_excel(test_ais)
#current_dict = import_dicts_from_excel(test_ais2, ['check_dir'])


def save_obj(object, file_name):
    with open(file_name + '.pkl', 'wb') as f:
        pickle.dump(object, f, pickle.HIGHEST_PROTOCOL)

#save_obj(current_dict, 'direct_kkn')
#save_obj(current_dict, 'our_kkn')

#dict1 = import_dicts_from_excel(exel_name_ais)
'''
for jey in dict1.keys():
    print(" - - -  - - - - - - - -  - - - - - -", jey)
    for el in dict1[jey]:
        print(el)
        print(dict1[jey][el])
'''
cur_sec = round((time.time() - start_time), 2)
print(f'Вревмя выполнения: {int(cur_sec // 60)} мин. {cur_sec} сек.)')
