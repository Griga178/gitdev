import time

def go_to_upload(driver):
    tag = 'div'
    atribute = 'wbkey'
    atr_val = '12213' # (кнопка) На рассмотрении
    cell = driver.find_element_by_xpath(f"//{tag}[@{atribute}='{atr_val}']")
    cell.click()  # --> "На рассмотрении" -- не использется

def click_by_name(driver, btn_name = 'Вложения'):

    btn = driver.find_element_by_xpath(f"//div[contains(text(), '{btn_name}')]")#.click()
    btn.click()

def upload_file(driver, file_name, wait_time): # загрузка файлов с компа

    tag = 'div'
    atribute = 'wbtype'
    atr_val = 'control_upload_button'

    find_element =  driver.find_elements_by_xpath(f"//{tag}[@{atribute}='{atr_val}']/input")[0]
    find_element.send_keys(file_name)

    time.sleep(wait_time)

def check_file_sum(driver, current_sum = False):
    """ работает не верно """
    page_title = driver.title
    new_current_sum = page_title[-3]

    if not current_sum:

        return new_current_sum

    else:

        if current_sum + 1 == new_current_sum:
            print('Файл добавлен - проверено')
            return True
        else:
            return False
