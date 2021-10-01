'''
код для поиска различий между двумя файлами
'''

import pandas

name_ais_file = 'C:/Users/G.Tishchenko/Desktop/ais.xlsx'

name_my_file = 'C:/Users/G.Tishchenko/Desktop/sentember_fresh.xlsx'

ais_sheets1 = 'Sheet0'
ais_sheets2 = 'Sheet1'
#ais_sheets3 = 'Sheet2'

my_sheet_name = 'names'
my_sheet_name_2 = 'kkn'



my_column_name = 'name'


column_list = []
for el in range(12):
    column_list.append(el)

my_data_1 = pandas.read_excel(name_my_file, sheet_name = my_sheet_name, usecols =[0])
#my_data_2 = pandas.read_excel(name_my_file, sheet_name = my_sheet_name_2, usecols = column_list)

my_data_2 = pandas.read_excel(name_ais_file, sheet_name = ais_sheets2, usecols = column_list)
#ais_data_2 = pandas.read_excel(name_ais_file, sheet_name = ais_sheets2, usecols = column_list)


#print(my_data_2.head())

# Список имен, которые надо проверить!
list = my_data_1['name'].tolist()

# список заголовков всех используемых колонок
column_list = my_data_2.columns

list0 = my_data_2[column_list[0]].tolist() # Имя ККН
list1 = my_data_2[column_list[1]].tolist() # Имя ККН
list2 = my_data_2[column_list[2]].tolist()
list3 = my_data_2[column_list[3]].tolist()
list4 = my_data_2[column_list[4]].tolist() # ед.изм
list5 = my_data_2[column_list[5]].tolist() # Имя характеристики
list6 = my_data_2[column_list[6]].tolist()
list7 = my_data_2[column_list[7]].tolist()
list8 = my_data_2[column_list[8]].tolist()
list9 = my_data_2[column_list[9]].tolist()
list10 = my_data_2[column_list[10]].tolist()
list11 = my_data_2[column_list[11]].tolist()

row_num = 0
current_name = 0

new_list0 = []
new_list1 = []
new_list2 = []
new_list3 = []
new_list4 = []
new_list5 = []
new_list6 = []
new_list7 = []
new_list8 = []
new_list9 = []
new_list10 = []
new_list11 = []

super_list = []
for name in list:
    row_num = 0
    for el in list1:
        if type(el) != float:
            current_name = el
        if name == current_name:

            super_list.append([list0[row_num], current_name, list2[row_num], list3[row_num], list4[row_num], list5[row_num], list6[row_num], list7[row_num], list8[row_num], list9[row_num], list10[row_num], list11[row_num]])
            #print(current_name, list2[row_num], list3[row_num], list4[row_num], list5[row_num], list6[row_num], list7[row_num], list8[row_num], list9[row_num], list10[row_num], list11[row_num])
            #print(current_name, list2[row_num])
        row_num += 1

for el in super_list[:10]:
    print(el)

df = pandas.DataFrame(super_list, columns = column_list, dtype = float)

print(df.head)

filename = 'C:/Users/G.Tishchenko/Desktop/excel2.xlsx'
sh_nm = 'Final'

df.to_excel(filename, columns=column_list, index=False)
# нужно "заполучить" все строки где имя есть в файле моем
#print(my_data_2.shape)
