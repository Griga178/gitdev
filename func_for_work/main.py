import sys

from settings import main_folder, screen_folder
from settings import companies_info_file, links_table_file

from folder_creator import check_create_folder
from excel_creator import check_companies_info_file, check_links_table_file

from excel_reader import read_work_table, read_links_table
from data_merger import merge_links_tables
from excel_writer import write_links_data
from console_interface import run_console_interface

# Проверка на наличие необходимых файлов, папок - Создание
check_create_folder(main_folder)
check_create_folder(screen_folder)
check_companies_info_file(companies_info_file)
check_links_table_file(links_table_file)

# в случае запуска файла - через перетаскивание реестра
# читается файл, обновляются таблицы компаний/ссылок
if len(sys.argv) > 1:
    print(f'Читаем файл: {(sys.argv[1])}\n')
    work_table_data = read_work_table(sys.argv[1])

    max_number, links_set, links_table_data = read_links_table(links_table_file)

    new_links_table = merge_links_tables(max_number, links_set, links_table_data, work_table_data[1])

    write_links_data(new_links_table, links_table_file)

    print("Записали")

# Запуск панели управления
run_console_interface()

# для добавления через cmd
# desktop_path = 'C:/Users/G.Tishchenko/Desktop/26 Театр.xlsx'
# a = 1
# if a == 1:
    # work_table_data = read_work_table(desktop_path)
