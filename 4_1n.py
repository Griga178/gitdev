import openpyxl
from selenium import webdriver
# Для создания скринов
import time
import numpy as np
import imutils
import cv2
import pyautogui
'''
РУЧНОЙ ПАРСИНГ ССЫЛОК

программа открывает ссылку
человек в консоль вводит цену
если есть цена - запись + создать скрин
(свернуть консоль или в брузер в полный экран)
ДОБАВИТЬ
IF INPUY == 'n':
добавить новую ссылку и цену
elif == 'r'
исправить цену в номере
'''

start_time = time.time()

# ссылки по которым надо пройтись
excel_file_name = 'C:/Users/G.Tishchenko/Desktop/Ручной парсин.xlsx'
sheet_name = 'Лист21'
# Папка для скринов
screens_folder = 'C:/Users/G.Tishchenko/Desktop/screens_2_2022/new_step/'

def links_to_list_from_excel():
    '   Создаем список с [Ссылка, номер скриншота(строки)]'
    work_list = []
    wb = openpyxl.load_workbook(excel_file_name, read_only = True, data_only = True)
    active_sheet = wb[sheet_name]
    for row in active_sheet.rows:
        # чтение ячеейк в строках и добавление в ""список строки"
        link = row[0].value
        screen_name = row[1].value
        work_list.append([link, screen_name])
    return work_list # [['a','1'],['a','2'],...]

def make_screenshoot(screen_name):
    time.sleep(1)
    image = pyautogui.screenshot(region=(0, 0, 1920, 1080))
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    cv2.imwrite(screen_name, image)

def run_manual_parse():
    'В ручную добалвяем цены к ссылке + делаем скрин'
    csv_new_name = 'C:/Users/G.Tishchenko/Desktop/R_manual(three).csv'
    work_list = links_to_list_from_excel()
    #options = webdriver.ChromeOptions()
    #options.add_argument("--ignore-certificate-error")
    #options.add_argument('--ignore-certificate-errors-spki-list')
    #options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome() #options = options
    work_list_with_price = []

    for row in work_list:
        driver.set_window_size(1240, 1080)
        try:
            driver.get(row[0])
        except:
            print(f"ОШИБКА ПЕРЕХОДА НА СТРАНИЦУ: {row[0]}")
        input_price = input(f'{row[1]}. Значение цены: ')

        if input_price == 's':
            print('Стоп машина!')
            with open(csv_new_name, 'w') as file:
                for line in work_list_with_price:
                    file.write(f'{line[0]};{line[1]};{line[2]}\n')
            cur_sec = round((time.time() - start_time), 2)
            print(f'Вревмя выполнения: {int(cur_sec // 60)} мин. {cur_sec} сек.)')
            break
        else:
            try:
                input_price = float(input_price)
            except:
                print('Не получилось создать число!')
                input_price = 0

        if input_price > 0:
            work_list_with_price.append([row[0], row[1], input_price])
            print('Цена =', input_price)
            driver.maximize_window()
            screen_name = screens_folder + str(row[1]) + '.jpg' #row[1] + f'_{str(input_price).replace(".", ",")}'
            print(screen_name)
            make_screenshoot(screen_name)
        elif input_price == 0:
            work_list_with_price.append([row[0], row[1], ''])
            print('Цены нет')
    else:
        with open(csv_new_name, 'w') as file:
            for line in work_list_with_price:
                file.write(f'{line[0]};{line[1]};{line[2]}\n')
        cur_sec = round((time.time() - start_time), 2)
        print(f'Вревмя выполнения: {int(cur_sec // 60)} мин. {cur_sec} сек.)')

        driver.close()
        #return work_list_with_price
    '''
    with open(csv_new_name, 'w') as file:
        for line in work_list_with_price:
            file.write(f'{line[0]};{line[1]};{line[2]}\n')

    cur_sec = round((time.time() - start_time), 2)
    print(f'Вревмя выполнения: {int(cur_sec // 60)} мин. {cur_sec} сек.)')
    '''

run_manual_parse()
