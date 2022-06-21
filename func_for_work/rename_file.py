import os
from os.path import join, isfile
import shutil


old_name = 'C:/Users/G.Tishchenko/Desktop/тест.xlsx'

new_name = 'C:/Users/G.Tishchenko/Desktop/тест2.xlsx'

jpg_folder = 'C:/Users/G.Tishchenko/Desktop/2022 май Нормирование/МФУ'

new_folder = 'C:/Users/G.Tishchenko/Desktop/jpg_mfu'
search_files = {68,70,71,78,79,80,81,85,90,93,91,92,103,
    104,105,43,111,112,114,115,116,118,126,127,128,
    129,130,65,137,140,143,145,149,151,156,159,162,
    164,169,172,173,174,5,2,3,12,7,17,18,19,21,23,
    24,27,28,30,34,35,36,37,38,39,45,46,48,51,56,
    57,58,59,60,61}

# os.rename(old_name, new_name)

content_list = os.listdir(jpg_folder)

for some_file in content_list:

    if isfile(join(jpg_folder, some_file)):

        try:
            cur_file_name = int(some_file.split(".")[0])
        except:
            cur_file_name = ''

        if cur_file_name in search_files:
            new_name = join(new_folder, "м" + str(cur_file_name) + ".jpg")
            old_name = join(jpg_folder, some_file)


            # print(new_name)
            # print(old_name)
            shutil.copyfile(old_name, new_name)
