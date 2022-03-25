'''
Помогает изменить имена компаний в номерах СЭДа
'''
import time

import pandas
import csv

import os

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


start_time = time.time()

page_enter = 'http://srv07/cmec/Login.aspx?ReturnUrl=%2fcmec%2fCA%2fDesktop%2fDefault.aspx%3fwintype%3dwindow_desktops'

def authorization_func(user_name, user_passw):

    global driver
    driver = webdriver.Chrome()
    driver.implicitly_wait(1000) # ждем столько, если не справился заканчиваем?

    driver.get(page_enter)

    tag = 'input'
    atribute = 'name'
    atr_val = 'ctl00$FasContent$TextLogin'
    atr_val_p = 'ctl00$FasContent$TextPassword'
    atr_val_enter = 'ctl00$FasContent$ButtonLogin'

    login = driver.find_element_by_xpath(f"//{tag}[@{atribute}='{atr_val}']")
    password = driver.find_element_by_xpath(f"//{tag}[@{atribute}='{atr_val_p}']")
    button_enter = driver.find_element_by_xpath(f"//{tag}[@{atribute}='{atr_val_enter}']")

    login.send_keys(user_name)
    password.send_keys(user_passw)
    button_enter.click()

def find_document_from_main(number_element):
    tag = 'input'
    atribute = 'type'
    atr_val = 'text'
    find_element =  driver.find_element_by_xpath(f"//{tag}[@{atribute}='{atr_val}']")
    find_element.send_keys(number_element)

    tag = 'div'
    atribute = 'class'
    atr_val_btn = 'WbForm_ButtonIcon buttonSearch searchButtonCtl'
    driver.find_element_by_xpath(f"//{tag}[@{atribute}='{atr_val_btn}']").click() # поиск в поисковике сайта

def main_func(sheets_name):
    # Добавляет все экранки по списку excel
    column_name, column_number = 'name', 'number'
    df = pandas.read_excel(exel_file, sheet_name = sheets_name, usecols = [column_name, column_number])
    list_name = df[column_name].tolist()
    list_number  = df[column_number].tolist()

    main_page = 'http://srv07/cmec/CA/Desktop/Default.aspx?wintype=window_desktops#view=desktop_2501'
    num_index = 0
    row = 0
    for number in list_number:

        driver.get(main_page)
        #print(f'Следующий номер: {number}')
        find_document_from_main(number)
        print(f'зашли на {row + 1} страницу по номеру {number}')
        print(list_name[row])
        time.sleep(1)
        #driver.find_element_by_xpath("//html").click()

        ''' Нажать на кнопку "Полная карточка" '''
        qa0 = '//div[@id="btn_Mode_Full"]'
        driver.find_element_by_xpath(qa0).click()


        ''' Вставка текста в "Содержание": "Экранная копия" '''
        qa2 = '//div[@class="Wb_Textarea Wb_FormElement_Position1 text_Content Wb_Control Wb_EditableField WbForm_Obligatory"]/div/textarea'
        text2 = 'Экранная копия'
        print("Пробуем заполнить содержание")
        find_element = driver.find_element_by_xpath(qa2)
        find_element.clear()
        find_element.send_keys(text2)
        #driver.find_element_by_xpath("//html").click()

        ''' Вставка текста в "Откуда": "Сторонняя организация, интернет-магазин" '''
        text3 = 'Сторонняя организация, интернет-магазин'


        print('\n', list_name[row])
        print(text3)
        print(text2)

        # штука, что бы контролировать процесс
        # после каждого круга Enter или s = stop
        # добавить запись в csv из empty.py
        argument = input('\nEnter, что бы продолжить\ns, что бы закончить: \n')
        if argument == 's':
            break
        else:
            print("Продолжаем")
        row += 1




#user_name = #'Tishchenko_GL'
#user_passw = #'cmec789'

user_name = 'Mustafin_RI'
user_passw = '123123'

#exel_file = 'C:/Users/G.Tishchenko/Desktop/myfiles/dev/devfiles/images/numbers.xlsx'
exel_file = 'C:/Users/G.Tishchenko/Desktop/Numbers2_22.xlsx'

sheets_name_e = 'Ekranki'



authorization_func(user_name, user_passw)
print('Авторизовались\n')

main_func(sheets_name_e)


driver.quit()

cur_sec = round((time.time() - start_time), 2)
print(f'Вревмя выполнения: {int(cur_sec // 60)} мин. {cur_sec} сек.)')
