
Чтение(name.xlsx) --> LIST[DICT(Old_Name, New_Name)]
Найти изображени(Old_Name, Old_Path) --> n.jpg
Создать снимок части экрана(None) --> y.jpg
Сложить (y.jpg, n.jpg) --> New_Name.jpg
Сохранить(New_Name.jpg) --> None

*проверка/создание папки(New_jpg_path)

settings:
cheat_file_full_name: str
Old_jpg_folder_path: str
New_jpg_folder_path: str

##[main.py](./main.py)

код меняет нижнюю часть скриншота (время на панели задач) на текущее время
из файла "cheat_file_full_name" получаем список имен jpg (для изменения)

##[read_file.py](./read_file.py)

чтение excel файла -> List[dict, ...]

dict = {'old_name': row[2], 'new_name': row[1]}

##[screen_shot.py](./screen_shot.py)

edit_screen() - создает копию изображения с измененной нижней частью (время на
  панели задач меняется на текущее)
