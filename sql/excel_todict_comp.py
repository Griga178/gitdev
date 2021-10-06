'''
Код читает эксель файл с информацией по компаниям
создает словарь по ключам ИНН
'''


import openpyxl
import pickle

file_name = 'C:/Users/G.Tishchenko/Desktop/my_table.xlsx'
current_sheet = 'work'

wb = openpyxl.load_workbook(file_name, read_only = True, data_only = True)

active_sheet = wb[current_sheet]

companies_dict = {}

for row in active_sheet.rows:
    # Читаем каждую строку
    row_list = []

    for cell in row:
        # добавляем 12 ячеек строки в "список"
        my_cell = str(cell.value)
        if len(my_cell) != 0:
            row_list.append(my_cell)

    #print(row_list)

    companies_dict |= {row_list[1]:[row_list[0], row_list[2], row_list[3]]}

print(len(companies_dict))

form_set = ['ООО', 'ИП', 'ФБУН', 'ЗАО', 'ОАО', 'АО', 'НАО', 'ФКП']

ip_count = 0
ooo_count = 0
zao_count = 0
ao_count = 0
else_com = 0
oao_count = 0
npk_count = 0
nao_count = 0
fkp_count = 0
fbun_count = 0


for el in companies_dict:
    if form_set[1] + " "  in companies_dict[el][0] or " " + form_set[1] in companies_dict[el][0]:
        ip_count += 1
        companies_dict[el].append(form_set[1])
    elif form_set[0] + " " in companies_dict[el][0] or " " + form_set[0] in companies_dict[el][0]:
        ooo_count += 1
        companies_dict[el].append(form_set[0])
    elif form_set[3] + " "  in companies_dict[el][0] or " " + form_set[3] in companies_dict[el][0]:
        zao_count += 1
        companies_dict[el].append(form_set[3])
    elif form_set[4] + " "  in companies_dict[el][0] or " " + form_set[4] in companies_dict[el][0]:
        oao_count += 1
        companies_dict[el].append(form_set[4])
    elif form_set[5] + " "  in companies_dict[el][0] or " " + form_set[5] in companies_dict[el][0]:
        ao_count += 1
        companies_dict[el].append(form_set[5])
    elif form_set[6] + " "  in companies_dict[el][0] or " " + form_set[6] in companies_dict[el][0]:
        nao_count += 1
        companies_dict[el].append(form_set[6])
    elif form_set[7] + " "  in companies_dict[el][0] or " " + form_set[7] in companies_dict[el][0]:
        fkp_count += 1
        companies_dict[el].append(form_set[7])
    elif form_set[2] + " "  in companies_dict[el][0] or " " + form_set[2] in companies_dict[el][0]:
        fbun_count += 1
        companies_dict[el].append(form_set[2])
    else:
        print([companies_dict[el][0]])

        else_com += 1


print('ИП:', ip_count)
print('ООО: ', ooo_count)
print('ЗАО: ', zao_count)
print('АО: ', ao_count)
print('ОАО: ', oao_count)
print('НАО: ', nao_count)
print('ФКП: ', fkp_count)
print('ФБУН: ', fbun_count)
print('другие: ', else_com)

print('Всего: ', ip_count + ooo_count + zao_count + ao_count + else_com + oao_count + fbun_count + fkp_count + nao_count)



'''
# companies_dict = {'inn': ['comp_name', 'adress', 'phone', 'form']}

for el in companies_dict:
    print(companies_dict[el]) #[2]



with open('comp_info.pkl', 'wb') as f:
    pickle.dump(companies_dict, f, pickle.HIGHEST_PROTOCOL)
'''
