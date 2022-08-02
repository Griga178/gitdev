import sys

from settings import main_folder, screen_folder
from settings import companies_info_file, links_table_file

from folder_creator import check_create_folder
from excel_creator import check_companies_info_file, check_links_table_file

from excel_reader import read_work_table
from console_interface import run_console_interface

# Проверка на наличие необходимых файлов, папок - Создание
check_create_folder(main_folder)
check_create_folder(screen_folder)

check_companies_info_file(companies_info_file)
check_links_table_file(links_table_file)
# в случае запуска файла - реестра
# читается файл, создаются/обновляются раб таблицы
if len(sys.argv) > 1:
    print(sys.argv[1])
    excel_info = read_work_table(sys.argv[1])
    # update_work_table(excel_info)
    print(len(excel_info[0]), len(excel_info[1]))

# Запуск панели управления
run_console_interface()
