""" FILE MANAGER """

import os
import openpyxl

# from settings import desktop_path

# main_folder = desktop_path + 'main/'
# screen_folder = main_folder + 'all_screnshots/'
# word_folder = ''
# current_data_file = main_folder + "current_data.xlsx"

def check_create_folder(folder_path_name):
    folder_exist = os.path.isdir(folder_path_name)
    if folder_exist:
        print(f"Найдена папка: {folder_path_name}")
    else:
        os.mkdir(folder_path_name)
        print(f"Папка: {folder_path_name} успешно создана")
