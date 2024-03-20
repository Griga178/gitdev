from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

binary_yandex_driver_file = 'yandexdriver.exe'

def get_driver():
    options = Options()
    service = Service(executable_path = binary_yandex_driver_file)
    options.add_experimental_option('excludeSwitches', ['enable-logging']) # не выводит сообщзения в консоль
    driver = webdriver.Chrome(service = service, options = options)
    driver.implicitly_wait(1000)

    return driver

def authorization_func(driver, user_name, user_passw):
    page_enter = 'http://srv07/cmec/Login.aspx?ReturnUrl=%2fcmec%2fCA%2fDesktop%2fDefault.aspx%3fwintype%3dwindow_desktops'
    driver.get(page_enter)

    tag = 'input'
    atribute = 'name'
    atr_val = 'ctl00$FasContent$TextLogin'
    atr_val_p = 'ctl00$FasContent$TextPassword'
    atr_val_enter = 'ctl00$FasContent$ButtonLogin'

    login = driver.find_element("xpath", f"//{tag}[@{atribute}='{atr_val}']")
    password = driver.find_element("xpath", f"//{tag}[@{atribute}='{atr_val_p}']")
    button_enter = driver.find_element("xpath", f"//{tag}[@{atribute}='{atr_val_enter}']")

    login.send_keys(user_name)
    password.send_keys(user_passw)
    button_enter.click()

def go_to_upload(driver):
    tag = 'div'
    atribute = 'wbkey'
    atr_val = '12213' # (кнопка) На рассмотрении
    cell = driver.find_element("xpath", f"//{tag}[@{atribute}='{atr_val}']")
    cell.click()  #

def find_document_from_main(driver, number_element):
    '''
        ИНОГДА ТЫКАЕТ НА ПОИСК, НЕ ВСТАВИВ НОРМАЛЬНО ТО ЧТО ИСКАТЬ
    '''
    tag = 'input'
    atribute = 'type'
    atr_val = 'text'
    find_element =  driver.find_element("xpath", f"//{tag}[@{atribute}='{atr_val}']")
    find_element.send_keys(number_element)

    tag = 'div'
    atribute = 'class'
    atr_val_btn = 'WbForm_ButtonIcon buttonSearch searchButtonCtl'
    driver.find_element("xpath", f"//{tag}[@{atribute}='{atr_val_btn}']").click() # поиск в поисковике сайта


def click_by_name(driver, btn_name = 'Вложения'):
    # btn_name = 'Вложения'
    btn = driver.find_element("xpath", f"//div[contains(text(), '{btn_name}')]")#.click()
    btn.click()

def upload_file(driver, file_name):
    # напрямую загружает файл в тег input - Работает
    tag = 'div'
    atribute = 'wbtype'
    atr_val = 'control_upload_button'
    find_element =  driver.find_elements("xpath", f"//{tag}[@{atribute}='{atr_val}']/input")[0]
    find_element.send_keys(file_name)
