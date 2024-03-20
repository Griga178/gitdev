import time
import re
import os.path

def go_to_upload(driver):
    tag = 'div'
    atribute = 'wbkey'
    atr_val = '12213' # (кнопка) На рассмотрении
    cell = driver.find_element("xpath", f"//{tag}[@{atribute}='{atr_val}']")
    cell.click()  # --> "На рассмотрении" -- не использется

def click_by_name(driver, btn_name = 'Вложения'):
    btn = driver.find_element("xpath", f"//div[contains(text(), '{btn_name}')]")
    btn.click()

def count_upload_time(file_path):
    ''' время загрузки 1 МБ ~ 0,65 сек '''
    byte_size = os.path.getsize(file_path)
    upload_time = round((byte_size / 1000000) * 0.65, 1)
    return upload_time

def upload_file(driver, file_name):
    # загрузка файлов с компа
    wait_time = count_upload_time(file_name)
    print(f'Ожидаем: {wait_time} сек.')
    tag = 'div'
    atribute = 'wbtype'
    atr_val = 'control_upload_button'
    find_element =  driver.find_elements_by_xpath(f"//{tag}[@{atribute}='{atr_val}']/input")[0]
    find_element.send_keys(file_name)
    time.sleep(wait_time)

def check_file_sum(driver):
    ''' Показывает сколько вложено файлов в эл. документе '''
    page_title = driver.title
    # Находим значение между скобок ( ... )
    re_sult = re.findall(r'(?<=\()(.*?)(?=\))', page_title)
    uploaded_file_sum = re_sult[0].replace(' ', '')
    return uploaded_file_sum
