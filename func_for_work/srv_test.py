from srv_funcs.log_in import log_in
from srv_funcs.find_document import find_document_from_main
from srv_funcs.upload_file import click_by_name, upload_file, check_file_sum

from selenium import webdriver

import time



test_number_element = '04-8566/22-0-0'

test_file_name = 'C:/Users/G.Tishchenko/Desktop/test_file_for_sed.txt'

user_name, user_passw = 'Tishchenko_GL', 'cmec789'

binary_yandex_driver_file = '../yandexdriver.exe'

main_page = 'http://srv07/cmec/Login.aspx?ReturnUrl=%2fcmec%2fCA%2fDesktop%2fDefault.aspx%3fwintype%3dwindow_desktops'

    # -  -  -  *  -  -  - ЗАПУСКАЕМ БРАУЗЕР -  -  -  *  -  -  -
driver = webdriver.Chrome(binary_yandex_driver_file)
driver.implicitly_wait(1000)
driver.get(main_page)

    # -  -  -  *  -  -  - Логинимся -  -  -  *  -  -  -
log_in(driver, user_name, user_passw)

    # -  -  -  *  -  -  - Ищем документ -  -  -  *  -  -  -
find_document_from_main(driver, test_number_element)

    # -  -  -  *  -  -  - Добавляем файл -  -  -  *  -  -  -
click_by_name(driver) # вкладка вложения
base_file_sum = check_file_sum(driver)
print(f'Файлов вложено: {base_file_sum}')
upload_file(driver, test_file_name, wait_time = 2) # прикрепили файл
print('дальше')
    # -  -  -  *  -  -  - проверяем добавление -  -  -  *  -  -  -
find_document_from_main(driver, test_number_element)
click_by_name(driver) # вкладка вложения
# try:
base_file_sum = int(base_file_sum)
new_file_sum = check_file_sum(driver, base_file_sum)
print(f'Проверям сколько вложено файлов: {new_file_sum}')
# except:
    # print('сумма - не число')


    # -  -  -  *  -  -  - Переименовываем -  -  -  *  -  -  -

    # -  -  -  *  -  -  - проверяем переименование -  -  -  *  -  -  -

# time.sleep(20)

# driver.quit()
