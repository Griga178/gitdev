import sys
import time
import pickle
from selenium import webdriver


#page = 'https://zakupki.gov.ru/epz/contract/contractCard/payment-info-and-target-of-order.html?reestrNumber=2781930090921000019&contractInfoId=66596577'
page = 'https://zakupki.gov.ru/epz/contract/contractCard/payment-info-and-target-of-order.html?reestrNumber=2780610397421000011&contractInfoId=64745227'

driver = webdriver.Chrome()
driver.implicitly_wait(100) # ждем столько, если не справился заканчиваем?
driver.get(page)

goods_link = '/html/body/div[2]/div/div[1]/div[3]/div/a[2]'
#driver.find_element_by_xpath(goods_link).click()

full_page_path = '//*[@id="contractSubjects"]/div/div'
str_full_page = driver.find_element_by_xpath(full_page_path).text
full_list = str_full_page.split('\n')

'''
Дан сплошной блок текста, разделенный '\n'
первые 3 = 6 заголовков 1 название общей таблицы

строка заканчивается наличием "Ставка НДС"
4 индекс ИМЯ

'''
counter = 0
for el in full_list[3:]:
    # НАЗВАНИЕ ТОВАРА
    if counter == 0:
        print(f'Наименование:\n {el}')
    elif "Страна происхождения: " in el:
        print(f'Страна:\n   {el.replace("Страна происхождения: ", "")}')
        counter = 1
    elif counter == 2:
        print(f'Пошло КТРУ:\n   {el.replace("Страна происхождения: ", "")}')
    elif "Ставка НДС" in el:
        counter = 0
    elif counter == 8:
        print('\n')
    else:
        print(f'\n\nНЕ УЧТЕНО {el}\n\n')
    counter += 1
    # Конец строки





driver.close()
