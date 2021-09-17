'''
Код для добавления значений/файлов в "СЭД"
заходит на сайт, ищет по номеру документ, вставляет его (не проверено, нет обработок ошибок)
'''
import time

import pandas

import os

from selenium import webdriver

page_enter = 'http://srv07/cmec/Login.aspx?ReturnUrl=%2fcmec%2fCA%2fDesktop%2fDefault.aspx%3fwintype%3dwindow_desktops'


def authorization_func(user_name, user_passw):
    global driver
    driver = webdriver.Chrome()
    driver.implicitly_wait(3) # ждем столько, если не справился закрываем

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


def upload_file(file_name): # загрузка файлов с компа
    # Не проверено!! проверять не надо - пока что
    tag = 'input'
    atribute = 'type'
    atr_val = 'file' #file text
    find_element =  driver.find_elements_by_xpath(f"//{tag}[@{atribute}='{atr_val}']")
    ind_element.send_keys(file_name)

    #for el in find_element:
    #    print(el.get_attribute('outerHTML'))

user_name = 'Tishchenko_GL'
user_passw = 'cmec789'


#number_element = '04-5736/21-0-0'#'04-6385/21-0-0'
file_name = "C:/Users/G.Tishchenko/Desktop/myfiles/dev/gitdev/test.txt"

exel_file = 'C:/Users/G.Tishchenko/Desktop/myfiles/dev/devfiles/images/numbers.xlsx'

sheets_name_e = 'Ekranki'
sheets_name_o = 'Otveti'

dir_files = 'C:/Users/G.Tishchenko/Desktop/myfiles/dev/devfiles/images/'

def main_func(sheets_name):
    column_name, column_number = 'name', 'number'
    df = pandas.read_excel(exel_file, sheet_name = sheets_name, usecols = [column_name, column_number])
    list_name = df[column_name].tolist()
    list_number  = df[column_number].tolist()
    # список файлов в папке
    list_docs = os.listdir(dir_files + '/' + sheets_name)

    main_page = 'http://srv07/cmec/CA/Desktop/Default.aspx?wintype=window_desktops#view=desktop_2501'
    num_index = 0
    for number in list_number:
        driver.get(main_page)
        print(f'Следующий номер: {number}')
        find_document_from_main(number)
        print(f'зашли на страницу по номеру {number}')
        #time.sleep(3)
        click_by_name('Вложения')
        print('перешли на вкладку вложения')
        file_name = list_name[num_index].replace('"', '').replace('«', '').replace('»', '') + '.docx'
        #upload_file(file_name)
        print(f'Прикрепили файл {file_name}')

        # штука, что бы контролировать процесс
        # после каждого круга Enter или s = stop
        # добавить запись в csv из 20n.py
        if file_name in list_docs:
            print(dir_files + '/' + file_name)
            num_index += 1
            argument = input('Enter, что бы продолжить\ns, что бы закончить: \n')
            if argument == 's':
                break
    print(num_index - 1)

authorization_func(user_name, user_passw)
print('Авторизовались\n')

main_func(sheets_name_e)
#main_func(sheets_name_o)
driver.quit()

''' # выводит список элементов, по настройкам который загрущзился, что бы дополнить список, надо промотать
list_el = driver.find_elements_by_xpath(f"//{tag}[@{atribute}='{atr_val}']")
count = 0
for el in list_el:
    print(el.text)
    count += 1
print(count)
'''


'''
authorization_func(user_name, user_passw) # тут вход браузери на сайт
find_document(number_element)
click_by_name('Вложения')

# # # #upload_file(file_name) # Не проверено!! проверять не надо - пока что

confirmation = str(input('\n\n\nНажмите Enter для закрытия\n\n\n'))
if confirmation == '':
    driver.quit()
else:
    print('НУ ладно')
    driver.quit()
'''
