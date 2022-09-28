'''поиск адресов и названий по ИНН
'''
import pandas
from selenium import webdriver
import time
import csv

start_time = time.time()

main_page = 'https://egrul.nalog.ru/index.html'

exel_file = 'C:/Users/G.Tishchenko/Desktop/Склейка вер8 +топливо.xlsx'
# exel_file = "Z:/Тищенко Г.Л/Номера 3кв.xlsx"
# exel_file = 'C:/Users/G.Tishchenko/Desktop/comp.csv'
binary_yandex_driver_file = 'yandexdriver.exe'
sheets_name = 'Компании'


column_name = 'Наименование поставщика'
column_inn = 'ИНН'

csv_file_name = 'C:/Users/G.Tishchenko/Desktop/comp.csv'

df = pandas.read_excel(exel_file, sheet_name = sheets_name, usecols = [column_inn]) #column_name

# Вытащили список инн
list_inn = df[column_inn].tolist()

# Список списков для записи в csv
finish_list =[]

driver = webdriver.Chrome(binary_yandex_driver_file)

driver.implicitly_wait(100) # ждем столько, если не справился заканчиваем?

count = 0
try:
    for inn in list_inn:
        count += 1
        driver.get(main_page)

        input_inn = driver.find_element_by_xpath("//input[@placeholder='Укажите ИНН или ОГРН (ОГРНИП) или наименование ЮЛ, ФИО ИП']")
        input_inn.send_keys(inn)

        btn_search = driver.find_element_by_xpath("//button[@id='btnSearch']").click()

        adress = "//div[@class='res-text']"
        t_adress = driver.find_element_by_xpath(adress)

        name = "//div[@class='res-caption']"
        t_name = driver.find_element_by_xpath(name)

        val1 = t_adress.text.split(', ОГРН')[0]

        new_list = [inn, t_name.text, val1]

        finish_list.append(new_list)
        print(f'{count} инн записан')
        time.sleep(1)
except:
    with open(csv_file_name, 'w') as file:
        for line in finish_list:
            file.write(f'{line[0]};{line[1]};{line[2]}\n')

    driver.quit()
    cur_sec = round((time.time() - start_time), 2)
    print(f'Вревмя выполнения: {int(cur_sec // 60)} мин. {cur_sec} сек.)')
    print(f"{count} - всего инн")

with open(csv_file_name, 'w') as file:
    for line in finish_list:
        file.write(f'{line[0]};{line[1]};{line[2]}\n')

driver.quit()
cur_sec = round((time.time() - start_time), 2)
print(f'Вревмя выполнения: {int(cur_sec // 60)} мин. {cur_sec} сек.)')
print(f"{count} - всего инн")
