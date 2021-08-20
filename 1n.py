'''
Новая версия, на этом этапе формируется список ссылок в алфавитном порядке
с сохранением места ссылки в файле excel (список кортежей с 3 парам.).

из Excel в sorted_tuples

'''
import pandas

exel_file = '../devfiles/reestr 4.xlsx'
sheets_name = 'RT new'

# нужные столбцы
column_links =  'Ссылка'

csv_file_name = '../devfiles/test3.csv'

first_num = 2 # Номер первой строки, в которой ссылка



file = pandas.read_excel(exel_file, sheet_name = sheets_name, usecols = [column_links])

list_num = []
list_link = file[column_links].tolist()

for num in range(len(list_link)):
    list_num.append(num + first_num)

list_tuples_links = []
inde_x = 0

if len(list_num) == len(list_link):
    for val in list_link:
        print(list_num[inde_x])

        # вырезаем главную стр из ссылки для сортировки
        try:
            if '\n' in val and type(val) == str:
                val = val.split("\n")[0] # убираем места с двумя ссылками
            main_page = (val.split("/")[2])
            list_tuples_links.append((main_page, list_num[inde_x], val))
        except:
            #return
            print('trouble with main_page')

        inde_x += 1

sorted_tuples = sorted(list_tuples_links)

with open(csv_file_name, 'w') as file:
    for line in sorted_tuples:
        file.write(f'{line[0]};{line[1]};{line[2]}\n')
        #print(f'{line[0]};{line[1]};{line[2]}')
