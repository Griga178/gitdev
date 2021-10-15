'''
для сравнения двух столбцов в excel на одинаковость
'''

import openpyxl

name_my_file = 'C:/Users/G.Tishchenko/Desktop/new_xheck.xlsx'

wb = openpyxl.load_workbook(name_my_file, read_only = True, data_only = True) #, read_only = True
active_sheet = wb['check']

search_val = set()

count_char = 0
wrong_char = 0

row_count = 0

for row in active_sheet.rows: #
    # чтение ячеейк в строках и добавление в ""список строки"
    row_count += 1
    row_set = set()
    row_list = []


    kkn_row_set = set()
    ktru_row_set = set()
    for cell in row[31:34]:
        #print(cell.value)
        row_list.append(cell.value)
        #row_set.add(cell.value)
    if row_list[2] == False:
        kkn_char_list = row_list[0].split(';')
        ktru_chsr_list = row_list[1].split(';')

        for el in kkn_char_list:
            if 'х' in el or 'А' in el:
                el = el.replace('х', 'x')
                el = el.replace('А', 'A')
            if '.' in el:
                el = el.replace('.', ',')
            if '\xa0' in el:
                el = el.replace('\xa0', '')
            kkn_row_set.add(el.replace(' ', ''))

        for el in ktru_chsr_list:
            if 'х' in el or 'А' in el:
                el = el.replace('х', 'x')
                el = el.replace('А', 'A')
            if '.' in el:
                el = el.replace('.', ',')
            if '\xa0' in el:
                el = el.replace('\xa0', '')
            ktru_row_set.add(el.replace(' ', '')) #.lstrip().rstrip()

        comon_set = ktru_row_set & kkn_row_set
        error_st = kkn_row_set - comon_set
        #print(comon_set)
        if comon_set != kkn_row_set and error_st != {'Неустановлено'}:
            some_list = []

            print(f'Это есть {comon_set}')
            print(f'Этого нет в КТРУ: {error_st}')
            print(kkn_row_set, ktru_row_set, '\n')
            for el in error_st:
                some_list.append(el)
            a_str = ";".join(some_list)

            #active_sheet.cell(row = row_count, column = 35).value = a_str

            count_char += 1

#wb.save(name_my_file)

print(count_char)
