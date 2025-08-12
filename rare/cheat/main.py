from read_file import read_file
from screen_shot import *

"""
    редактирование jpg.файла
    Работает, НО ЕСТЬ КУЧА костылей на ошибки если разрешение скриншота не 1920*1080

"""

# settings
# Имя файла
# cheat_file_full_name = 'C:/Users/G.Tishchenko/Desktop/Cheat.xlsx'
cheat_file_full_name = 'C:/Users/G.Tishchenko/Desktop/screenCap/che/Cheat 19.xlsx'
# Имя листа
cheat_file_list_name = 'temp'
# расположение старых фоток
# Old_jpg_folder_path = 'Z:/Тищенко Г.Л/2024_4 Скрины/нормирование/'
Old_jpg_folder_path = 'Z:/Тищенко Г.Л/2024_4 Скрины/19 бытовые приборы/'


# расположение новых фоток
New_jpg_folder_path = 'C:/Users/G.Tishchenko/Desktop/screenCap/che/temp/ok/'
ok_New_jpg_folder_path = 'C:/Users/G.Tishchenko/Desktop/screenCap/che/temp/ok/'
# error_jpg_folder_path = 'C:/Users/G.Tishchenko/Desktop/screenCap/temp/error/'
error_jpg_folder_path = 'C:/Users/G.Tishchenko/Desktop/screenCap/che/temp/error 2/'


# смотрим содержимое файла
jpg_names = read_file(cheat_file_full_name, cheat_file_list_name)
# копируем все нужные фотки с srv
counter = 0
amount = len(jpg_names)
for jpg_name in jpg_names[:]:

    # jpg_name['old_name'] = jpg_name['new_name'] = 330994

    old_image_name = Old_jpg_folder_path + str(jpg_name['old_name']) + '.jpg'
    new_image_name = New_jpg_folder_path + str(jpg_name['new_name']) + '.jpg'
    ok_new_image_name = ok_New_jpg_folder_path + str(jpg_name['new_name']) + '.jpg'
    # ЕСЛИ УЖЕ ОТРЕДАКТИРОВАН - ПРОПУСКАЕМ
    if check(ok_new_image_name):
        continue
    # Просто копия
    copy_image(old_image_name, new_image_name)
    # edit_screen(new_image_name, None)
    try:
        edit_screen(new_image_name, None)

    except Exception as e:
        new_image_name_error = error_jpg_folder_path + str(jpg_name['new_name']) + '.jpg'
        print(e)
        copy_image(new_image_name, new_image_name_error)
        del_image(new_image_name)
    counter += 1
    print(f'{counter}/{amount} шт', str(jpg_name['new_name']))
