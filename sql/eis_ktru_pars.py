'''
Незаконченная функция парсинга КТРУ с еис
'''

import time
from selenium import webdriver
import pickle

page = 'https://zakupki.gov.ru/epz/ktru/start/startPage.html'

driver = webdriver.Chrome()
driver.implicitly_wait(100) # ждем столько сек, если не справился заканчиваем?

driver.get(page)

def some_function():
    # Номера "КТРУ"
    num_ktru = ['26.20.18.000-00000069', '26.20.18.000-00000068', '26.20.17.110-00000037', '26.20.17.110-00000034']
    # Поисковая строка
    search_win = '//*[@id="searchString"]'
    search_btn = '//*[@id="quickSearchForm_header"]/section/div/div/div/div[2]/div/div/button'
    driver.find_element_by_xpath(search_win).send_keys(num_ktru[3])
    driver.find_element_by_xpath(search_btn).click()

    char_btn = '//*[@id="quickSearchForm_header"]/section[2]/div/div/div[2]/div[3]/div/div[2]/div/div[1]/div/div/div/div[1]/span'
    driver.find_element_by_xpath(char_btn).click()

    elem_xpath = '//*[@id="quickSearchForm_header"]/section[2]/div/div/div[2]/div[3]/div/div[2]/div/div[2]/div/div/div/div'
    result = driver.find_elements_by_xpath(elem_xpath)
    char_count = 0
    for el in result:
        char_count += 1
        row = el.text
        row_for_dict_key = row.split(':')[0]
        row_for_dict_char_list = row.split(':')[1].split(',')
        row_for_dict_char_list[-1] = row_for_dict_char_list[-1].replace(' .', '')
        char_set = set()
        list_char = []
        for el in row_for_dict_char_list:
            measure = ''
            el = el.lstrip().rstrip()
            if 'от' in el:
                el = el.replace('от', '≥')
            if 'до' in el:
                el = el.replace('до', '<')
            if '(' in el:
                measure = el.split(' ')[-1]
                el = ' '.join(el.split(' ')[0:-1])
                #el = ' '.join(el.split(' ')[0:-1])
            #char_set.add(el)
            list_char.append(el)
        print(list_char, measure)

    print(char_count)

some_function()

time.sleep(10)
