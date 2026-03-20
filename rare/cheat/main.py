from read_file import read_file
from screen_shot import *

import os
import shutil


# Имя Excel со старым и новым именем
cheat_file_full_name = 'C:/Users/G.Tishchenko/Desktop/screenCap/ch_scr.xlsx'

# Название листа
cheat_file_list_name = 'Лист1'

# Пути до папок
# со старыми скринами
Old_jpg_folder_path = 'Z:/Тищенко Г.Л/2026_1 Скрины/03. Нормирование/'

# для новых скринов
New_jpg_folder_path = 'C:/Users/G.Tishchenko/Desktop/screenCap/che/'

# для копий старых скриншотов (временно)
PATH_TEMP_COPIES = New_jpg_folder_path + 'copies/'

# папка с изображеними 1920 * 1080
ok_New_jpg_folder_path = New_jpg_folder_path + 'OK/'

# папка с изображеними другого размера (не изменяется)
error_jpg_folder_path = New_jpg_folder_path + 'error/'

# смотрим содержимое файла
jpg_names = read_file(cheat_file_full_name, cheat_file_list_name)

# Создаем необходимые папки
os.makedirs(New_jpg_folder_path, exist_ok=True)
os.makedirs(ok_New_jpg_folder_path, exist_ok=True)
os.makedirs(PATH_TEMP_COPIES, exist_ok=True)
os.makedirs(error_jpg_folder_path, exist_ok=True)

counter = 0
amount = len(jpg_names)
for jpg_name in jpg_names[:]:
    is_succsess = False
    JPG_NEW_NAME = str(jpg_name['new_name']) + '.jpg'

    old_image_name = Old_jpg_folder_path + str(jpg_name['old_name']) + '.jpg'
    temp_img_name = PATH_TEMP_COPIES + JPG_NEW_NAME

    # new_image_name = New_jpg_folder_path + str(jpg_name['new_name']) + '.jpg'
    ok_new_image_name = ok_New_jpg_folder_path + JPG_NEW_NAME
    error_image_name = error_jpg_folder_path + JPG_NEW_NAME

    # избегаем повторное изменение
    if os.path.exists(ok_new_image_name):
        counter += 1
        continue

    # создаем копию скрина
    if not os.path.exists(temp_img_name):
        shutil.copy(old_image_name, temp_img_name)

    try:
        # редактируем скрин
        is_succsess = edit_screen(temp_img_name)

        if is_succsess:
            # перемещаем в новую папку
            shutil.move(temp_img_name, ok_new_image_name)
            counter += 1
        else:
            # перемещаем в папку c ошибками
            shutil.move(temp_img_name, error_image_name)


    except Exception as e:
        shutil.move(temp_img_name, error_image_name)
        print(e)


    print(f'{counter}/{amount} шт', JPG_NEW_NAME)
