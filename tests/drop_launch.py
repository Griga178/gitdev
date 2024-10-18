'''
    Да
    запуск кода путем перетаскивания
    одного файла на drop_launch.py
'''
import sys
import os

# sys.argv - список, длинна которого не может быть равна 0,
# по умолчанию равна 1

app_name = os.path.basename(sys.argv[0])
drop_files = []

if len(sys.argv) > 1:
    for file in sys.argv[1:]:
        drop_file_name = os.path.basename(file)
        drop_files.append(drop_file_name)
else:
    print('sys.argv !> 1')

print(f'Имя файла с кодом: "{app_name}"')
print(f'еще файлы: {len(drop_files)} шт')
print(drop_files) if drop_files else None

input('\n\n\nPush-Push-Push any button')
