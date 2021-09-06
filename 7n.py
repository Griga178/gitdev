'''
    Создаем папки с названием по компаниям
    Подсчет количества цен (- необходимых скриншотов) по каждой компании (csv)
    Закидываем в эти папки скриншоты (подсчет csv)

    отдельное сохранение скриншотов в ворде

    запись инфы в СЭД
'''
import os
import pandas


exel_file = '../devfiles/reestr 4 ready.xlsx'

sheets_name = 'RT new'

column_name = 'Наименование поставщика'
column_inn = 'ИНН поставщика'
column_price = 'Новая цена 4кв'
column_numer = 'Источник ценовой информации'

dict_main = {}

df = pandas.read_excel(exel_file, sheet_name = sheets_name,
usecols = [column_price, column_numer, column_name, column_inn])

list_name = df[column_name].tolist()
list_numer  = df[column_numer].tolist()
list_inn = df[column_inn].tolist()

#print(df.shape)
#print(df.head)
#print(df[column_name])
#print(df.groupby(column_name).sum())
#print(df[column_name].str[:] + df[column_numer].str[:])
#for el in df[column_name].unique():

list_comp_name = []
list_inn_comp = []
set_otvetov = set()
set_ekran = set()

row = 0
count = 0
o_count = 0
e_count = 0

for el in list_name:
    # el - Название компании
    try:
        str_len = len(list_numer[row])
        if str_len != 33:
            if list_numer[row][:1] == "О":
                o_count += 1
                set_otvetov.add(el)

                #list_comp_name.append(el)
                #list_inn_comp.append(list_inn[row])
            elif list_numer[row][:1] == "Э":
                e_count += 1
                set_ekran.add(el)
            '''
            if el not in list_comp_name:
                list_comp_name.append(el)
                list_inn_comp.append(list_inn[row])
                #print(el)
                print(list_numer[row])
                count += 1
            '''
    except:
        pass
    row += 1


print(o_count,e_count)
print(count)
print(len(set_otvetov))
print(len(set_ekran))
for el in set_ekran:
#print(len(list_comp_name))
