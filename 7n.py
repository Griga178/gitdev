'''
    I
    Есть - Создаем папки с названием по компаниям
    Есть - Подсчет количества цен (- необходимых скриншотов) по каждой компании (csv)
    Есть - Закидываем в эти папки скриншоты (подсчет)

    отдельное сохранение скриншотов в ворде

    запись инфы в СЭД
'''

import pandas


exel_file = '../devfiles/reestr 4 (для скринов + норм вар).xlsx'

sheets_name = 'new+'

column_name = 'Наименование поставщика'
column_inn = 'ИНН поставщика'
column_price = 'Новая цена 4кв'
column_numer = 'Источник ценовой информации'
column_jpg_name = 'jpg_name'

dict_main = {}

df = pandas.read_excel(exel_file, sheet_name = sheets_name,
usecols = [column_price, column_numer, column_name, column_inn, column_jpg_name])

list_name = df[column_name].tolist()
list_numer  = df[column_numer].tolist()
#list_inn = df[column_inn].tolist()
list_price = df[column_price].tolist()
list_jpg_name = df[column_jpg_name].tolist()

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
    # el - Название компании -> new_el
    # row - номер строки = имя скриншота (старое правило) + индекс "всей строки"
    # list_jpg_name[row]
    try:
        str_len = len(list_numer[row])
        if str_len != 33:
            count += 1
            #jpg_name = (str(int(list_jpg_name[row])) + '.jpg')
            jpg_name = (int(list_jpg_name[row]))
            #print(f'Номер строки: {row + 2} jpg_name: {jpg_name}')
            if list_numer[row][:1] == "О" and list_price[row] > 0:
                o_count += 1
                new_el = el.replace('"', '').replace('«', '').replace('»', '')

                set_otvetov.add(new_el)
                list_comp_name.append(new_el)

                if new_el not in dict_otveti:
                    #deic_el = {new_el: [row + 2]}
                    deic_el = {new_el: [jpg_name]}
                    dict_otveti.update(deic_el)
                else:
                    #dict_otveti[new_el].append(row + 2)
                    dict_otveti[new_el].append(jpg_name)
            elif list_numer[row][:1] == "Э" and list_price[row] > 0:
                new_el = el.replace('"', '').replace('«', '').replace('»', '')

                e_count += 1
                set_ekran.add(new_el)
                list_comp_name.append(new_el)


                if new_el not in dict_ekranki:
                    #deic_el = {new_el: [row + 2]}
                    deic_el = {new_el: [jpg_name]}
                    dict_ekranki.update(deic_el)
                else:
                    #dict_ekranki[new_el].append(row + 2)
                    dict_ekranki[new_el].append(jpg_name)
    except:
        pass
    #print(row + 2) # первая 0, вторая - заголовки
    row += 1

#                        тут подсчет количества скриншотов
def count_scr_info():
    print('Количество экранных копий по компаниям')
    cou_ekr = 0
    cou_otv = 0
    for el in dict_ekranki:
        cou_ekr += len(dict_ekranki[el])
        print(el, len(dict_ekranki[el]))
    print(f'\n------Всего экранных: {cou_ekr}\n')
    print('Количество ответов по компаниям')
    for el in dict_otveti:
        cou_otv += len(dict_otveti[el])
        print(el, len(dict_otveti[el]))
    print(f'\n------Всего ответов: {cou_otv}\n')
    print(f'\n------Итого: {cou_otv + cou_ekr}\n')

#count_scr_info()

import os
import shutil

main_dir = '../devfiles/new_ales_screenes'
otvet_dir = main_dir + '/Otveti'
ekran_dir = main_dir + '/Ekranki'

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
where_screens = '../devfiles/scr/new/'

def copy_screen():
    copy_count = 0
    for el in dict_otveti:
        direct_name = otvet_dir + '/' + el + '/'
        #print(direct_name)
        for num in dict_otveti[el]:
            scr_name = str(num) + '.jpg'
            old_screen_name = where_screens + scr_name
            new_screen_name = direct_name + 'new' + scr_name
            #print(old_screen_name)
            #print(new_screen_name)
            try:
                #shutil.copyfile(old_screen_name, new_screen_name)
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
            old_screen_name = where_screens + scr_name
            new_screen_name = direct_name + 'new' +  scr_name
            print(old_screen_name)
            print(new_screen_name)
            try:
                shutil.copyfile(old_screen_name, new_screen_name)
                copy_count_ecr += 1
            except:
                print("Не удалось скопировать", scr_name)
    print(copy_count_ecr, ' Экранок')

#create_dirs()
copy_screen()


# Считаем количество использования источников {Ситилинк ООО; 100}
def count_source_uses():
    count = 0
    dict_comp = {el : list_comp_name.count(el) for el in list_comp_name}
    sorted_dict = {}
    sorted_list = sorted(dict_comp, key = dict_comp.get, reverse = True)
    for comp in sorted_list:
        sorted_dict[comp] = dict_comp[comp]
    for el in sorted_dict:
        count += sorted_dict[el]
        print(el, sorted_dict[el])
    print(f'\n------Итого: {count}\n')

#count_source_uses()
