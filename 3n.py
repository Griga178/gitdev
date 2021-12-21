'''
удаление ненужных скринов
после проверки отпарсенных значений файла 2n.py
удаляются скрины без цен
'''
import os
import pandas


exel_file = '../devfiles/manual_test3_all.xlsx'
sheets_name = 'manual_test3_all'

check_file_name = 'C:/Users/G.Tishchenko/Desktop/R_screens.csv'
screen_folder = 'C:/Users/G.Tishchenko/Desktop/screens_1_2022/'

# нужные столбцы
column_price =  'price'
column_numer =  'numer'

def delete_empty_screens():

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

def check_empty_screen():
    folder_content = os.listdir(screen_folder)
    list_for_excel = []
    for element in folder_content:
        if element.split('.')[-1] == 'jpg':
            list_for_excel.append(element.split('.')[0])
    with open(check_file_name, 'w') as file:
        for row in list_for_excel:
            file.write(f'{row}\n') # для записи всего
    print(len(list_for_excel))

check_empty_screen()
