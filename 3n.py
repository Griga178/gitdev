'''
удаление ненужных скринов
после проверки отпарсенных значений файла 2n.py
удаляются скрины без цен 
'''
import os
import pandas


exel_file = '../devfiles/manual_test3_all.xlsx'
sheets_name = 'manual_test3_all'

# нужные столбцы
column_price =  'price'
column_numer =  'numer'


file = pandas.read_excel(exel_file, sheet_name = sheets_name, usecols = [column_price, column_numer])

list_price = file[column_price].tolist()
list_numer = file[column_numer].tolist()

count = 0
inde_x = 0
for i in list_price:
    if pandas.isna(i) == True:
        screen_name = '../devfiles/scr/' + str(list_numer[inde_x]) + '.jpg'
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), screen_name)
        try:
            os.remove(path)
            print(f"{screen_name} REMOOVED")
            count += 1
        except:
            print(f"{screen_name} can't remove")

    inde_x += 1
print(count)
