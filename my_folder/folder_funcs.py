from os.path import isdir
from os import mkdir

def folder_exists(folder_path):
    return isdir(folder_path)

def create_folder(folder_path):
    folder_name = folder_path.split("/")[-2]
    if folder_exists(folder_path):
        print(f'Папка: "{folder_name}" - уже существует')
    else:
        mkdir(folder_path)
        print(f'Папка: "{folder_name}" - создана')
