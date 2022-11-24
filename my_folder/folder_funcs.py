from os.path import isdir, isfile, splitext, exists
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

def file_exists(file_path):
    return isfile(file_path)

def uniquify_file_name(path):
    # https://translated.turbopages.org/proxy_u/en-ru.ru.c271bd91-637f2872-629353bc-74722d776562/https/stackoverflow.com/questions/13852700/create-file-but-if-name-exists-add-number
    filename, extension = splitext(path)
    counter = 0
    while exists(path):
        path = filename + "(" + str(counter) + ")" + extension
        counter += 1
    return path

def check_file_name(file_path):
    if file_exists(file_path):
        file_path = uniquify_file_name(file_path)
        return file_path
    else:
        return file_path
