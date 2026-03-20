
p/
├── main.py           # настройки + запуск
├── read_file.py      # чтение старого и нового имени из excel
├── screen_shot.py    # создание нового скрина


*проверка/создание папки(New_jpg_path)

settings:
cheat_file_full_name: str
Old_jpg_folder_path: str
New_jpg_folder_path: str

код меняет нижнюю часть скриншота (время на панели задач) на текущее время
из файла Excel

чтение excel файла -> List[dict, ...]
dict = {'old_name': row[2], 'new_name': row[1]}


edit_screen() - создает копию изображения с измененной нижней частью
(время на панели задач меняется на текущее)
