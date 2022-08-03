from os.path import isdir
from os import mkdir

def check_create_folder(folder_path_name):
    folder_exist = isdir(folder_path_name)
    if folder_exist:
        print(f'Найдена папка: "{folder_path_name.split("/")[-2]}"')
    else:
        mkdir(folder_path_name)
        print(f'Папка: "{folder_path_name.split("/")[-2]}" успешно создана')
