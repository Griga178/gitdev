'''
Новая версия, на этом этапе отсортированный список кортежей из 1n.py
парсится по порядку
парсится один сайт, затем записываются значения в соседний столбец
в 4 столбце csv записывать цены
'''
import openpyxl
import csv
import pandas
import os
import time

from clear_func import stand_clear

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests
from bs4 import BeautifulSoup

import numpy as np
import pyautogui
import imutils
import cv2

start_time = time.time()

csv_file_name = '../devfiles/test3.csv'
beauty_file_name = 'settings/my_beauty_links.csv'
selenium_file_name = 'settings/my_selenium_links.csv'

finish_list = []
answer = ''

# создание словарей с настройками парсинга
selen_dict = {}
beauty_dict ={}

with open(selenium_file_name) as file:
    for line in file:
        rule = line.split(';')
        dom = rule[0]
        set = [rule[1], rule[2], rule[3]]
        add_i = {dom: set}
        selen_dict.update(add_i)
        #print(f'{dom}, {set1}, {set2}, {set3}')
with open(beauty_file_name) as file:
    for line in file:
        rule = line.split(';')
        dom = rule[0]
        set = [rule[1], rule[2], rule[3]]
        add_i = {dom: set}
        beauty_dict.update(add_i)

#print(selen_dict)
#print(beauty_dict)

# перебираем ссылки из файла
comon_counter = 0
current_counter = 0
current_counter2 = 0
current_counter3 = 0
current_counterz = 0

caps = DesiredCapabilities().CHROME # выбор браузера
caps["pageLoadStrategy"] = "eager" # не ждем полной загрузки
options = Options()
options.add_argument("--start-maximized") # открываем во весь экран
driver = webdriver.Chrome(options = options)

driver.implicitly_wait(3) # ждем столько, если не справился закрываем

def selen_parse(link, name):
    # находим правила
    main_page = link
    name = 0
    # выгрузка тегов для каждого сайта
    tag = selen_dict[main_page][0]
    atribute = selen_dict[main_page][1]
    atr_val = selen_dict[main_page][2]
    # заходим на сайт
    try:
        driver.get(row[2])
    except:
        print('get link error selenium 1')

    # Два варианта парсинга
    a, b = None, None
    try:
        # находит текст внутри тега
        price = driver.find_element_by_xpath(f"//{tag}[@{atribute}='{atr_val}']")
        a = price.get_attribute('outerHTML')
        # находит значение атрибута тега (когда цена не выводится на сайт прямо)
        pricea = driver.find_element_by_xpath(f"//{tag}[@{atribute}='{atr_val}']")
        b = pricea.get_attribute('content')
    except:
        try:
            if main_page == 'www.dns-shop.ru':
                atr_val = 'product-buy__price product-buy__price_active'
                price = driver.find_element_by_xpath(f"//{tag}[@{atribute}='{atr_val}']")
                a = price.get_attribute('outerHTML')
        except:
            b = None
            a = None
    if b == None:
        if a == None:
            answer = 'get link error selenium 2'
        else:
            answer = a
    else:
        answer = b
    '''
    # Делаем скириншооот
    time.sleep(1)
    image = pyautogui.screenshot(region=(0, 0, 1920, 1080))
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    cv2.imwrite(name, image)
    '''
    return stand_clear(answer)

def beauty_pars(name):
    main_page = row[0]
    link = row[2]
    '''
    try:
        driver.get(row[2])
    except:
        print('get link error selenium 1')
    time.sleep(1)
    image = pyautogui.screenshot(region=(0, 0, 1920, 1080))
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    cv2.imwrite(name, image)
    '''
    # подключение
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'lxml')
    # поиск параметров
    price_tag, p_atr, p_atr_val = beauty_dict[main_page]
    # поиск по тегам и их атрибутам
    try:
        quotes = soup.find_all(price_tag, {p_atr: p_atr_val})   # цитаты
    except Exception as e:
        print('BeautifulSoup не справился')
        return 'manual'
    xval = str('')
    for i in quotes:
        xval = i.text

    if xval == '': # поле пустое
        return 'manual'
    else:
        return stand_clear(xval)


#temp_list = [] ###

# открываем браузер  (пытаемся)
try:

    driver.get('https://www.google.com/')

except:
    print('хз что-то произошло')
with open(csv_file_name) as file:
    readers = csv.reader(file, delimiter = ';')

    for row in readers:
        #print('я здесь', row[0])
        if row[0] in selen_dict: ####and comon_counter <= 2000 not in temp_list  and row[0] != 'my-shop.ru'
            answer = selen_parse(row[0], '../devfiles/scr/' + row[1] + '.jpg')

            row.append(answer)
            finish_list.append(row)

            current_counter2 += 1
             ###temp_list.append(row[0])
            print(comon_counter, row[0], answer)


        elif row[0] in beauty_dict: # and row[0] != 'www.citilink.ru'
            answer = beauty_pars('../devfiles/scr/' + row[1] + '.jpg')

            row.append(answer)
            finish_list.append(row)

            current_counter3 += 1
            print(comon_counter, row[0], answer)
             ###temp_list.append(row[0])
        else:
            current_counterz += 1



        comon_counter += 1



#print(len(temp_list), 'len temp list')

driver.quit() # закрываем браузер
print("всего", comon_counter)
print("selen_dict", current_counter2)
print("beauty_dict", current_counter3)

print("not_pars", current_counterz)


new_name = '../devfiles/new_' + csv_file_name.split('/')[-1]
with open(new_name, 'w') as file:
    for line in finish_list:
        file.write(f'{line[0]};{line[1]};{line[2]};{line[3]}\n')

cur_sec = round((time.time() - start_time), 2)
print(f'Вревмя выполнения: {int(cur_sec // 60)} мин. {cur_sec} сек.)')
