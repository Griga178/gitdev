'''
Код для добавления значений/файлов в "СЭД"
заходит на сайт, ищет по номеру документ, вставляет его (нет обработок ошибок)
полуавтомат, не дожидается полной загрузки файла, идет на след стр
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


def go_to_upload():
    tag = 'div'
    atribute = 'wbkey'
    atr_val = '12213' # (кнопка) На рассмотрении
    cell = driver.find_element_by_xpath(f"//{tag}[@{atribute}='{atr_val}']")
    cell.click()  # --> "На рассмотрении" -- не использется


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


def click_by_name(btn_name):
    btn_name = 'Вложения'
    btn = driver.find_element_by_xpath(f"//div[contains(text(), '{btn_name}')]")#.click()
    btn.click()
    #print(btn.get_attribute('outerHTML')) # Открытие ссылки по тексту (1 работает)

reestr_list = []
def upload_file(file_name): # загрузка файлов с компа
    # напрямую загружает файл в тег input - Работает
    tag = 'div'
    atribute = 'wbtype'
    atr_val = 'control_upload_button'
    find_element =  driver.find_elements_by_xpath(f"//{tag}[@{atribute}='{atr_val}']/input")[0]
    find_element.send_keys(file_name)
    '''
    попытки подождать загрузку

    short_name = file_name.split('/')[-1]
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.text_to_be_present_in_element((By.XPATH, f"//*[contains(text(), '{short_name}')]"), f"{short_name}"))
    reestr_list.append(short_name.replace('.docx', ''))
    print('Элемент найден')
    #find_uploaded_doc = driver.find_elements_by_xpath(f"//*[contains(text(), '{short_name}')]")[0]
    #try:

    #except:
    #    print(f'- - -[ulpoad_file] - - - - - - - Не получилось добавить в:    {short_name}\n')
    '''

user_name = 'Tishchenko_GL'
user_passw = 'cmec789'
#user_name = 'Mustafin_RI'
#user_passw = '123123'

#exel_file = 'C:/Users/G.Tishchenko/Desktop/myfiles/dev/devfiles/images/numbers.xlsx'
exel_file = 'C:/Users/G.Tishchenko/Desktop/Numbers3_22.xlsx'

sheets_name_e = 'Ekranki'
sheets_name_o = 'Otveti'

#dir_files = 'C:/Users/G.Tishchenko/Desktop/myfiles/dev/devfiles/images/'
dir_files = 'C:/Users/G.Tishchenko/Desktop/Word_folder/'



def main_func(sheets_name):
    # Добавляет все экранки по списку excel
    column_name, column_number = 'name', 'number'
    df = pandas.read_excel(exel_file, sheet_name = sheets_name, usecols = [column_name, column_number])
    list_name = df[column_name].tolist()
    list_number  = df[column_number].tolist()
    # список файлов в папке
    cur_dir = dir_files + sheets_name + '/'
    list_docs = os.listdir(cur_dir)

    main_page = 'http://srv07/cmec/CA/Desktop/Default.aspx?wintype=window_desktops#view=desktop_2501'
    num_index = 0

    for number in list_number:

        driver.get(main_page)
        #print(f'Следующий номер: {number}')
        find_document_from_main(number)
        print(f'зашли на страницу по номеру {number} -- {list_name[num_index]}')
        time.sleep(1)
        click_by_name('Вложения')
        #print('перешли на вкладку вложения')
        file_name = list_name[num_index].replace('"', '').replace('«', '').replace('»', '') + '.docx'
        time.sleep(1)
        #print(f'Прикрепили файл {file_name}\n')

        # штука, что бы контролировать процесс
        # после каждого круга Enter или s = stop
        # добавить запись в csv из empty.py
        if file_name in list_docs:
            #print(cur_dir + file_name) #+ '/'
            upload_file(cur_dir + file_name)
            reestr_list.append(number)
            #time.sleep(1)

            num_index += 1
        else:
            print(f'Не нашел файл: {file_name}\nв папке {cur_dir}')
            num_index += 1
        argument = input('Enter, что бы продолжить\ns, что бы закончить: \n')
        if argument == 's':
            break


    print(f'Добавлено: {num_index} файлов')

def one_append(file, number):
    main_page = 'http://srv07/cmec/CA/Desktop/Default.aspx?wintype=window_desktops#view=desktop_2501'
    driver.get(main_page)
    find_document_from_main(number)
    time.sleep(1)
    click_by_name('Вложения')
    time.sleep(1)
    upload_file(file)
    time.sleep(5)


authorization_func(user_name, user_passw)
print('Авторизовались\n')

# main_func(sheets_name_e)
main_func(sheets_name_o)


#file = 'C:/Users/G.Tishchenko/Desktop/Аквариус.msg'
#number = '04-6401/21-0-0'
#one_append(file, number)

driver.quit()

cur_sec = round((time.time() - start_time), 2)
print(f'Вревмя выполнения: {int(cur_sec // 60)} мин. {cur_sec} сек.)')


csv_file_name = 'added_file.csv'
with open(csv_file_name, mode = "a") as file:
    file_writer = csv.writer(file) #, lineterminator="\r" , delimiter = ";"
    for el in reestr_list:
        file_writer.writerow([el])
    file_writer.writerow([f'Вревмя выполнения: {int(cur_sec // 60)} мин. {cur_sec} сек.)'])
