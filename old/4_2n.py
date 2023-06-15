import os
import openpyxl
'''
Работа с готовыми скринами
'''
def read_screen_in_dir(dir_name):
    emppte_set = set()
    list = os.listdir(dir_name)
    for el in list:
        emppte_set.add(el)
        # print(el)
    return emppte_set

r_path = r'C:\Users\G.Tishchenko\Desktop\screens_2_2022'

new_s_p = r'C:\Users\G.Tishchenko\Desktop\screens_2_2022\new_step'
new_p = r'C:\Users\G.Tishchenko\Desktop\screens_2_2022\new_prices'

screen_set = read_screen_in_dir(r_path)

'''
Надо выбрать скрины по списку
'''

excel_file_name = 'C:/Users/G.Tishchenko/Desktop/картинки.xlsx'
sheet_name = 'Лист 1'

def read_search_screen():
    emppte_set = set()
    wb = openpyxl.load_workbook(excel_file_name, read_only = True, data_only = True)
    active_sheet = wb[sheet_name]
    for row in active_sheet.rows:
        screen_number = str(row[0].value)
        emppte_set.add(screen_number)
        # print(screen_number)
    return emppte_set


'''
Копирование определенных скринов в новую папку

'''
from shutil import copyfile

#copyfile(src, dst)
def copy_scr():
    set_from_excel = read_search_screen()
    coped_set = set()
    counter = 0
    for old_screen in screen_set:
        name = old_screen.split('.')[0]
        old_screen_name = os.path.join(r_path, old_screen)
        new_scr_name = os.path.join(new_p, old_screen)
        if name in set_from_excel:
            counter += 1
            #coped_set.add(name)
            print(counter, old_screen_name, '\n',new_scr_name)
            copyfile(old_screen_name, new_scr_name)
    #final_set = set_from_excel - coped_set
    #print(final_set)

# copy_scr()
excel_set = read_search_screen()
folder_set = read_screen_in_dir(r_path)
# next_step = read_screen_in_dir(r'C:\Users\G.Tishchenko\Desktop\screens_2_2022\new_step')
print(len(excel_set))
print(len(folder_set))
# print(len(next_step))

# union = folder_set & next_step
union = excel_set - folder_set
print(union)
