from selenium import webdriver
import time
'''
Различные функции для работы с "srv07" (СЭД):

'''
driver = webdriver.Chrome(executable_path = 'C:/Users/G.Tishchenko/Desktop/myfiles/dev/gitdev/chromedriver.exe')

driver.implicitly_wait(1000)

def authorization_func(user_name, user_passw):
    ''' Вход в личный кабинет на сайте '''
    print(f'\nВыполнятеся вход в аккаунт: {user_name[:5]}\n')
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

    #time.sleep(1)
    #print('\n поиск title')
    result = driver.find_element_by_xpath('//title').get_attribute('innerHTML')
    #print('\n Пропущено?!')

    if result == 'Мои документы':
        print('Успешный вход')
    else:
        print('Что еще?')
        print(result)
