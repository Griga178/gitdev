""" FILE MANAGER """

import os
import openpyxl

from settings import desktop_path

main_folder = desktop_path + 'main/'
screen_folder = main_folder + 'all_screnshots/'
word_folder = ''
current_data_file = main_folder + "current_data.xlsx"

def create_folder(folder_path_name):
    folder_exist = os.path.isdir(folder_path_name)
    if folder_exist:
        print(f"Папка: {folder_path_name} уже создана")
    else:
        os.mkdir(folder_path_name)
        print(f"Новая папка: {folder_path_name} успешно создана")

def open_current_setting_file(file_path):
    file_exists = os.path.isfile(file_path)
    if file_exists:
        print("файл существует")
    else:
        wb = openpyxl.Workbook()
        current_sheet = wb.active
        current_sheet.title = "Компании"
        wb.save(file_path)



# open_current_setting_file(current_data_file)

def run_manager():
    create_folder(main_folder)
    create_folder(screen_folder)
    # open_current_setting_file(current_data_file)
