'''
Тут парсятся значения с сайтов
    в будущем
'''
from selenium import webdriver
import time


page_enter = 'https://www.xcomspb.ru/catalog/kompyutery_i_noytbyki/' # для тренировки (испытаний)

page_enter = 'https://convertio.co/ru/'

driver = webdriver.Chrome()

driver.get(page_enter)


'''Эта часть выводит названия 20 ноутбуков с сайта xcom.ru

tag = 'div'
atribute = 'class'
atr_val = 'name'
lists = driver.find_elements_by_xpath(f"//{tag}[@{atribute}='{atr_val}']")
count = 0
for el in lists:
    print(el.text)
    count += 1
print(count)
'''

'''
# Находит по имени элемент и кликает по нему
#find_name = '3M PF14.1'
#driver.find_elements_by_xpath(f"//*[contains(text(), '{find_name}')]")[0].click()
'''


#fileInput = By.cssSelector("input[type=file]");

file_name = "C:/Users/G.Tishchenko/Desktop/myfiles/dev/gitdev/test.txt"

#driver.find_elements_by_xpath("//input[@type='file'").sendKeys(file_adress)

tag = 'input'
atribute = 'type'
atr_val = 'file' #file text
find_element =  driver.find_elements_by_xpath(f"//{tag}[@{atribute}='{atr_val}']")
for el in find_element:
    print(el.get_attribute('outerHTML'))
#find_element.send_keys(file_name)

time.sleep(2)



driver.quit()
