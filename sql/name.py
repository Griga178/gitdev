'''парсинг еис
Контракты:
Санкт-Петербург {'178', '278', '378'}
Ленинградская обл.
2021 год
2020 год
'Исполнение завершено'
'''
import time
from selenium import webdriver
import pickle

page = 'https://zakupki.gov.ru/epz/contract/search/results.html'


driver = webdriver.Chrome()
driver.implicitly_wait(100) # ждем столько, если не справился заканчиваем?

driver.get(page)






all_param = '//*[@id="quickSearchForm_header"]/section[2]/div/div/div[2]/div[2]/div[1]/div/div/a/span[1]'

driver.find_element_by_xpath(all_param).click()


param_click_list = ['//*[@id="contractStageListTag"]/div/div[2]/div[1]/label',
                '//*[@id="contractStageListTag"]/div/div[2]/div[3]/label',
                '//*[@id="contractStageListTag"]/div/div[2]/div[4]/label',
                '//*[@id="searchOptionsEditContainer"]/div/div[7]/div[1]/div']

for link in param_click_list:
    driver.find_element_by_xpath(link).click()
    print(' Щелк! **')

data_path = '//*[@id="contractDateTag"]/div/div/div/div/input'


driver.find_element_by_xpath(data_path).click()
driver.find_element_by_xpath(data_path).send_keys('01.01.2021')
# тут надо кликнуть руками по ячейке
time.sleep(5)
all_right = '//*[@id="searchOptionsEditContainer"]/div/div[15]/div/div[3]/div/button/span'
driver.find_element_by_xpath(all_right).click()

page_set = '//*[@id="quickSearchForm_header"]/section[2]/div/div/div[1]/div[4]/div/div[2]/div/div[2]/div[1]/span'
driver.find_element_by_xpath(page_set).click()
page_set = '//*[@id="_50"]'
driver.find_element_by_xpath(page_set).click()



cells = '//div[@class="registry-entry__header-mid__number"]'
numbers = driver.find_elements_by_xpath(cells)


next0 = '//*[@id="quickSearchForm_header"]/section[2]/div/div/div[1]/div[4]/div/div[1]/ul/a/img'

driver.find_element_by_xpath(next0).click()

next = '//*[@id="quickSearchForm_header"]/section[2]/div/div/div[1]/div[4]/div/div[1]/ul/a[2]/img'
driver.find_element_by_xpath(next).click()

"""
Заходить в расширенные настройки не надо! все на главной странице, решить задачу с вставкой даты
добавить даты из теста и скачать номера всех контрактов
потом пропарсить контракты узнать что за товары и их цены = антирутина
"""



'''
numersss = set()
for el in numbers:
    split_el = str(el.text.split(" ")[1])
    numersss.add(split_el)

try:
    with open('zakup.pkl', 'rb') as f:
        print(pickle.load(f))
except:
    print('no file')

with open('zakup.pkl', 'wb') as f:
    pickle.dump(numersss, f, pickle.HIGHEST_PROTOCOL)
    print(f'Всего: {len(numersss)} номеров')
print(numersss)
'''




time.sleep(10)
