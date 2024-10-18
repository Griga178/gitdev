from srv_funcs.log_in import log_in
from srv_funcs.find_document import find_document_from_main
from srv_funcs.upload_file import click_by_name, upload_file, check_file_sum
from srv_funcs.excel_reader import get_excel_rows

from selenium import webdriver

import time
'''
ОСНОВНОЙ КОД: 10n.py - НЕ НУЖЕН ВХОДНОЙ ФАЙЛ С НОМЕРАМИ, сами номера в названии скринов
для загрузки файлов в сэд
на основе: ../10n.py
проблема: при загрузке учитывает размер файла, не учитывает торможение самого сайта и проч.
'''


test_number_element = '04-8566/22-0-0'
test_file_name = 'C:/Users/G.Tishchenko/Desktop/test_file_for_sed.txt'

excel_file_name = 'C:/Users/G.Tishchenko/Desktop/Ответы.xlsx'
word_folder = 'C:/Users/G.Tishchenko/Desktop/Word_folder/Ekranki/'

main_page = 'http://srv07/cmec/Login.aspx?ReturnUrl=%2fcmec%2fCA%2fDesktop%2fDefault.aspx%3fwintype%3dwindow_desktops'
user_name, user_passw = 'Tishchenko_GL', 'cmec789'

# -  -  -  *  -  -  - ЗАПУСКАЕМ БРАУЗЕР -  -  -  *  -  -  -
start_time = time.time()
binary_yandex_driver_file = '../yandexdriver.exe'
driver = webdriver.Chrome(binary_yandex_driver_file)
driver.implicitly_wait(1000)
driver.get(main_page)

    # -  -  -  *  -  -  - Логинимся -  -  -  *  -  -  -
log_in(driver, user_name, user_passw)

def upload_current_file_to_document(file_number, file_path): # в цикл по списку
    # -  -  -  *  -  -  - Ищем документ -  -  -  *  -  -  -
    find_document_from_main(driver, file_number)
        # -  -  -  *  -  -  - Добавляем файл -  -  -  *  -  -  -
    click_by_name(driver) # вкладка вложения
    base_file_sum = check_file_sum(driver)
    print(f'Файлов вложено: {base_file_sum}')
    upload_file(driver, file_path) # прикрепили файл

        # -  -  -  *  -  -  - проверяем добавление -  -  -  *  -  -  -
    find_document_from_main(driver, file_number)
    click_by_name(driver) # вкладка вложения
    new_file_sum = check_file_sum(driver)
    print(f'Проверям сколько вложено файлов: {new_file_sum}')

    if new_file_sum > base_file_sum:
        print(f'Файл - добавлен') # запишем в файл
    else:
        print(f'Файл - не добавлен') # запишем в файл (номер - ссылка)

a = get_excel_rows(excel_file_name)

for ex_data in a:

    file_number = ex_data[1]
    file_path = word_folder + ex_data[2] + '.docx'
    print(file_number)
    print(file_path)
    upload_current_file_to_document(file_number, file_path)

time.sleep(1)

driver.quit()
