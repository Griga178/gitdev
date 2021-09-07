'''
    I
    Есть - Создаем папки с названием по компаниям
    Есть - Подсчет количества цен (- необходимых скриншотов) по каждой компании (csv)
    Есть - Закидываем в эти папки скриншоты (подсчет)

    отдельное сохранение скриншотов в ворде

    запись инфы в СЭД
'''

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
list_price = df[column_price].tolist()

list_comp_name = []

set_otvetov = set()
set_ekran = set()

dict_otveti = {}
dict_ekranki = {}

row = 0
count = 0
o_count = 0
e_count = 0

for el in list_name:
    # el - Название компании
    try:
        str_len = len(list_numer[row])
        if str_len != 33:
            count += 1
            if list_numer[row][:1] == "О" and list_price[row] > 0:
                o_count += 1
                new_el = el.replace('"', '')

                set_otvetov.add(new_el)
                list_comp_name.append(new_el)

                if new_el not in dict_otveti:
                    deic_el = {new_el: [row + 2]}
                    dict_otveti.update(deic_el)
                else:
                    dict_otveti[new_el].append(row + 2)
            elif list_numer[row][:1] == "Э" and list_price[row] > 0:
                new_el = el.replace('"', '')

                e_count += 1
                set_ekran.add(new_el)
                list_comp_name.append(new_el)


                if new_el not in dict_ekranki:
                    deic_el = {new_el: [row + 2]}
                    dict_ekranki.update(deic_el)
                else:
                    dict_ekranki[new_el].append(row + 2)
    except:
        pass
    #print(row + 2) # первая 0, вторая - заголовки
    row += 1

#                                                     тут подсчет факт с планом
#for el in dict_ekranki:
    #print(el, len(dict_ekranki[el]))


import os
import shutil

main_dir = '../devfiles/ales_screenes'
otvet_dir = '../devfiles/ales_screenes/Otveti'
ekran_dir = '../devfiles/ales_screenes/Ekranki'

def create_dirs():
    try:
        os.mkdir(main_dir)
        os.mkdir(otvet_dir)
        os.mkdir(ekran_dir)
    except:
        print('\nГлавные папки не создавались\n')

    # СОздание папок для Ответов по компаниям
    for el in set_otvetov:
        dir_name = otvet_dir + '/' + el
        try:
            os.mkdir(dir_name)
        except:
            print(dir_name, '   Не создавалась')
    # СОздание папок для Экранок по компаниям
    for el in set_ekran:
        dir_name = ekran_dir + '/' + el
        try:
            os.mkdir(dir_name)
        except:
            print(dir_name, '   Не создавалась')

# Копируем скриншоты
# испольюзуются: dict_ekranki, dict_otveti

def copy_screen():
    copy_count = 0
    for el in dict_otveti:
        direct_name = otvet_dir + '/' + el + '/'
        #print(direct_name)
        for num in dict_otveti[el]:
            scr_name = str(num) + '.jpg'
            old_screen_name = '../devfiles/scr/first912/' + scr_name
            new_screen_name = direct_name + scr_name
            #print(old_screen_name)
            #print(new_screen_name)
            try:
                shutil.copyfile(old_screen_name, new_screen_name)
                copy_count += 1
            except:
                print("Не удалось скопировать", scr_name)

    print(copy_count, ' Ответов')

    copy_count_ecr = 0
    for el in dict_ekranki:
        direct_name = ekran_dir + '/' + el + '/'
        #print(direct_name)
        for num in dict_ekranki[el]:
            scr_name = str(num) + '.jpg'
            old_screen_name = '../devfiles/scr/first912/' + scr_name
            new_screen_name = direct_name + scr_name
            #print(old_screen_name)
            #print(new_screen_name)
            try:
                shutil.copyfile(old_screen_name, new_screen_name)
                #print(new_screen_name)
                copy_count_ecr += 1
            except:
                print("Не удалось скопировать", scr_name)
    print(copy_count_ecr, ' Экранок')

#create_dirs()
#copy_screen()


# Считаем количество использования источников {Ситилинк ООО; 100}
dict_comp = {el : list_comp_name.count(el) for el in list_comp_name}
sorted_dict = {}
sorted_list = sorted(dict_comp, key = dict_comp.get, reverse = True)
for comp in sorted_list:
    sorted_dict[comp] = dict_comp[comp]
