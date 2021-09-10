# Для поиска файлов
import os
import os.path

file_name = "2у6.jpg" # Имя искомого файла
#cur_dir = os.getcwd() # Текущая директория (C://User.../gitdev  6n.py)

search_in_dir = "C:/Users/G.Tishchenko/Desktop/myfiles/dev/devfiles/ales_screenes/Ekranki" #Ekranki Otveti


content_list = os.listdir(search_in_dir)
count = 0
'''
внутри основной папки (search_in_dir) - папки с файлами, внутри этих папок
ищется файл (file_name)
'''
for dir in content_list:
    search_in = f'{search_in_dir}/{dir}'
    list_in = os.listdir(search_in)
    if file_name in list_in:
        print(f'Файл {file_name} здесь: .../{dir}')
        break
    #print(list_in)
    count += len(list_in)

print(count)
#open_dir = search_in_dir + '/' + file_list[0]

#print(os.listdir(open_dir))

'''
while True:
    file_list = os.listdir(cur_dir) # Список всех файлов в директории
    parent_dir = os.path.dirname(cur_dir) # на папку выше
    if file_name in file_list:
        print("File Exists in: ", cur_dir)
        break
    else:
        if cur_dir == parent_dir: #if dir is root dir
            print("File not found")
            break
        else:
            cur_dir = parent_dir
'''
