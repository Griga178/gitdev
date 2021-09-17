'''
Делаем скриншоты по ссылкам, обработаным полуручном режиме 4n.py

надо использовать weebbrowser
 - он стандартный открывает все ссылки (в т.ч myshop.ru)
'''

import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import numpy as np
import pyautogui
import imutils
import cv2
start_time = time.time()
csv_file_name = '../devfiles/manual_test3_all.csv'
comon_counter = 0

caps = DesiredCapabilities().CHROME # выбор браузера
caps["pageLoadStrategy"] = "eager" # не ждем полной загрузки
options = Options()
options.add_argument("--start-maximized") # открываем во весь экран
driver = webdriver.Chrome(options = options)
driver.implicitly_wait(3) # ждем столько, если не справился закрываем

try:
    driver.get('https://www.google.com/')
except:
    print('хз что-то произошло')

with open(csv_file_name) as file:
    readers = csv.reader(file, delimiter = ';')
    for row in readers:
        try:
            driver.get(row[2])
        except:
            print('get link error selenium 1')

        # Делаем скириншооот
        name = '../devfiles/scr/' + row[1] + '.jpg'
        print(name)

        time.sleep(1)
        image = pyautogui.screenshot(region=(0, 0, 1920, 1080))
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        cv2.imwrite(name, image)
        comon_counter += 1

driver.quit() # закрываем браузер
cur_sec = round((time.time() - start_time), 2)
print(f'Вревмя выполнения: {int(cur_sec // 60)} мин. или {cur_sec} сек.)')
print("Всего скринов", comon_counter)
