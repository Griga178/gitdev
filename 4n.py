'''
Перебор неизвестных ссылок,
ввод значений (цен) вручную
сохранение цены и строки (скрин отдельно 5n.py)
* сохранение настроек парсинга
'''
import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

start_time = time.time()

#csv_file_name = '../devfiles/test3_all.csv'
csv_file_name = 'C:/Users/G.Tishchenko/Desktop/reestr 4.csv'
beauty_file_name = 'settings/my_beauty_links.csv'
selenium_file_name = 'settings/my_selenium_links.csv'

set_list = []
finish_list = []

with open(selenium_file_name) as file:
    for line in file:
        rule = line.split(';')
        dom = rule[0]
        set_list.append(dom)
with open(beauty_file_name) as file:
    for line in file:
        rule = line.split(';')
        dom = rule[0]
        set_list.append(dom)

comon_counter = 0
current_counter2 = 0

caps = DesiredCapabilities().CHROME # выбор браузера
caps["pageLoadStrategy"] = "eager" # не ждем полной загрузки

driver = webdriver.Chrome()

driver.implicitly_wait(3) # ждем столько, если не справился закрываем
try:
    driver.get('https://www.google.com/')
except:
    print('хз что-то произошло')

with open(csv_file_name) as file:
    readers = csv.reader(file, delimiter = ';')

    for row in readers:
        if row[0] not in set_list and row[0] != 'zakupki.gov.ru':
            comon_counter += 1
            price = 0
            try:
                driver.get(row[2])
            except:
                print('get link error selenium 1')
            #print(row[1], row[0])
            answer = str(input('Что на сайте?: '))
            try:
                price = float(answer)
                if price > 0:
                    row.append(price)
                    finish_list.append(row)
                    print(f'В строку {row[1]}: записана цена {price} (уже записано: {comon_counter})')
                else:
                    current_counter2 += 1
            except:
                print('Не цена')
            if answer == 'stop':
                break


driver.quit() # закрываем браузер

new_name = '../devfiles/manual_' + csv_file_name.split('/')[-1]
with open(new_name, 'w') as file:
    for line in finish_list:
        file.write(f'{line[0]};{line[1]};{line[2]};{line[3]}\n')

cur_sec = round((time.time() - start_time), 2)
print(f'Вревмя выполнения: {int(cur_sec // 60)} мин. {cur_sec} сек.)')
print("Всего записей", comon_counter)
print("Нет товара и проч.", current_counter2)
