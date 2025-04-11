'''
    2 столба с заголовками:
    A Наименование поставщика
    B Источник ценовой информации
    Лист - первый по счету (не важно какое название)
'''
from srv_funcs.log_in import log_in
from srv_funcs.find_document import find_document_from_main

from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

from srv_funcs.excel_reader import get_excel_rows
import time

test_file_name = 'C:/Users/G.Tishchenko/Desktop/name_for_sed.xlsx'


user_name, user_passw = 'Mustafin_RI', '123123'

binary_yandex_driver_file = '../yandexdriver.exe'
main_page = 'http://srv07/cmec/Login.aspx?ReturnUrl=%2fcmec%2fCA%2fDesktop%2fDefault.aspx%3fwintype%3dwindow_desktops'


    # -  -  -  *  -  -  - ЗАПУСКАЕМ БРАУЗЕР -  -  -  *  -  -  -
service = Service(executable_path = binary_yandex_driver_file)
driver = webdriver.Chrome(service = service)
# driver = webdriver.Chrome(binary_yandex_driver_file)
driver.implicitly_wait(1000)
driver.get(main_page)

start_time = time.time()

# -  -  -  *  -  -  - Логинимся -  -  -  *  -  -  -
log_in(driver, user_name, user_passw)
my_list = get_excel_rows(test_file_name)
for companies_info in my_list:
    print(my_list.index(companies_info), companies_info)
    text_org_type = companies_info[0]
    test_number_element = companies_info[1]
    text_org_name = companies_info[2]

    # -  -  -  *  -  -  - Ищем документ -  -  -  *  -  -  -
    find_document_from_main(driver, test_number_element)

    # -  -  -  *  -  -  - Переход -> "Полная Карточка" -  -  -  *  -  -  -

    qa0 = '//div[@id="btn_Mode_Full"]'
    full_page_btn = driver.find_element("xpath", qa0)
    time.sleep(0.5)
    full_page_btn.click()
    # ПРОВЕРЯЕМ ЗНАЧЕНИЕ ПЕРЕКЛЮЧАТЕЛЯ
    org_btn = '//*[@wbkey="classifier_Where"]/div/table/tbody/tr/td[1]/div'

    # print("Ищем кнопку переключатель")
    if 'Wb_Icon_Organization' not in driver.find_element("xpath", org_btn).get_attribute('class'):
        driver.find_element("xpath", org_btn).click()
        print('Нажали на Переключатель организация/физ. лицо')

    # Вставляем название организации

    input_org_name = '//*[@class="Wb_Input Wb_InputText Wb_InputSelect classifier_FromWhom Wb_EditableField"]/div/input'
    driver.find_element("xpath", input_org_name).clear()
    driver.find_element("xpath", input_org_name).send_keys(text_org_name)

    # Вставляем "Содержание"
    print("Заполняем содержание")

    qa2 = '//div[@class="Wb_Textarea Wb_FormElement_Position1 text_Content Wb_Control Wb_EditableField WbForm_Obligatory"]/div/textarea'
    find_element = driver.find_element("xpath", qa2)
    find_element.clear()
    find_element.send_keys(text_org_type)

    # Сохраняем

    save_btn_path = '//*[@wbkey="btn_saveIncoming"]'
    driver.find_element("xpath", save_btn_path).click()
    print("Сохранили")

    time.sleep(1)

driver.quit()
cur_sec = round((time.time() - start_time), 2)
print(f'Время выполнения: {int(cur_sec // 60)} мин. {cur_sec} сек.)')
