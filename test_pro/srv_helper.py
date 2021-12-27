from selenium import webdriver
import time
'''
Различные функции для работы с "srv07" (СЭД):
https://www.guru99.com/xpath-selenium.html#6 статья по xpath запросам

'''
driver = webdriver.Chrome(executable_path = 'C:/Users/G.Tishchenko/Desktop/myfiles/dev/gitdev/chromedriver.exe')

driver.implicitly_wait(1000)

page_enter = 'http://srv07/cmec/Login.aspx?ReturnUrl=%2fcmec%2fCA%2fDesktop%2fDefault.aspx%3fwintype%3dwindow_desktops'
main_page = 'http://srv07/cmec/CA/Desktop/'

def authorization_func(user_name, user_passw):
    ''' Вход в личный кабинет на сайте '''
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
        print(f'Успешный вход в аккаунт: {user_name[:5]}')
        return True
    else:
        print('Что еще? проверить title или пароли')
        print(result)
        return False

#text = 'На рассмотрении' # considering
#t = '//*[contains(@wbtitle, "На рассмотрении")]'

def link_by_wbtitle (search_text):
    xpath_rules = f'//*[contains(@wbtitle, "{search_text}")]'
    search_t = driver.find_element_by_xpath(xpath_rules)
    search_t.click()

def find_document_by_number(number):
    text = 'Быстрый поиск документов'
    searc_btn = f'//*[contains(@placeholder, "{text}")]'
    find_element = driver.find_element_by_xpath(searc_btn)
    find_element.send_keys(number)
    start_search_btn = "//div[@class='WbForm_ButtonIcon buttonSearch searchButtonCtl']"
    driver.find_element_by_xpath(start_search_btn).click()
    print('put btn')
    # находим div по началу текста "Вх. №"
    path = '//div[starts-with(@wbtitle, "Вх. №")]'
    result = driver.find_element_by_xpath(path).text#.get_attribute('innerHTML')
    if number in result:
        print("Нашли:", result)
    else:
        print("Не нашли, что искали")
    time.sleep(10)
