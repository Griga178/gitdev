'''пропарсить каталог с именами, ценами и ссылками
вытащить:
    имя из каталога
    его цену
    ссылку на страницу с описанием
'''
from selenium import webdriver

select_object = 'Компьютер' # то что выбираем в sql системе


source = 'https://www.xcomspb.ru/catalog/kompyutery_i_noytbyki/' #

driver = webdriver.Chrome()

'''Заходит на веб сайт
    выдает список всех найденных элементов
'''
driver.get(source)

tag = 'div'
atribute = 'class'
atr_val = 'name'
#atr_val = 'item border-gray type_337'
#atr_val = 'item border-gray type_8'
atr_val = 'wrap'
atr_val1 = 'name'
atr_val2 = 'new'
lists = driver.find_elements_by_xpath(f"//{tag}[@{atribute}='{atr_val}']")
count = 0

for el in lists:
    print(el) #el.text
    count += 1
print(count)

#driver.quit()
