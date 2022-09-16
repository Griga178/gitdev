from selenium import webdriver
import time

user_name, user_passw = 'Tishchenko_GL', 'cmec789'
main_page = 'http://srv07/cmec/Login.aspx?ReturnUrl=%2fcmec%2fCA%2fDesktop%2fDefault.aspx%3fwintype%3dwindow_desktops'
binary_yandex_driver_file = '../../yandexdriver.exe'

def start_srv_work(user_name, user_passw):

    driver = webdriver.Chrome(binary_yandex_driver_file)
    driver.implicitly_wait(1000)

    driver.get(main_page)

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

    return driver

def click_by_name(search_text, click_tag = False):
    ''' Аргументы:
            искомый тескст
            кликабельный тег - родитель: [tag, attr, value]'''
    # search_text = 'Вложения'
    if not click_tag:
        # par_clk_elem = "table"
        click_tag = ["table", "class", "WbWidget_Content"]

    btn = driver.find_element_by_xpath(f"//*[contains(text(), '{search_text}')]/ancestor::{click_tag[0]}[@{click_tag[1]}='{click_tag[2]}']")

    '''
    xpath:
        contains(text(), "иском_текст") - ищет * элемент по иском_текст
        элемент/ancestor:: -- Находит всех родителей элемента
    '''
    btn.click()

def search_rows(driver):

    # row_list = driver.find_element_by_xpath('//div[contains(@class ,"treegrid-item-field group")]')
    rows_container = '//div[@class="treegrid-itemsContainer"]/div'
    new_xpath_query = '//div[@class="treegrid-itemsContainer"]/div/div[5]/div/div[3]'
    # row_list = driver.find_element_by_xpath('//div[contains(@class ,"treegrid-item-field group")]/div/div[3]')
    row_list = driver.find_elements_by_xpath(rows_container)

    print('СТРОКИ: ', len(row_list))
    print(row_list)

# driver = start_srv_work(user_name, user_passw)

# click_by_name('На рассмотрении')
#
# search_rows(driver)
#
# time.sleep(2)
#
# driver.quit()
