import sys
import pickle
from selenium import webdriver
import time

'''
Задача, по списку номеров контрактов пропарсить сайт закупок
вытащить из контракта имя закупаемого товара, цену и ОКПД2

{number: {[okpd, name, price], [okpd, name, price]...}...}
'''


pkl_file_name = '../sql/contra/2021kontr9.pkl'

search_page = 'https://zakupki.gov.ru/epz/contract/search/results.html'

start_page = 'https://zakupki.gov.ru/epz/contract/contractCard/common-info.html?reestrNumber='

number_example = {'2781404664921000005', '2780610397421000011', '2781930090921000019', '2780210944621000200'}

def pkl_set_reader(file_name):
    with open(file_name, 'rb') as f:
        pickle_set = pickle.load(f)

    return pickle_set

#my_set = pkl_set_reader(pkl_file_name)
#set_size = sys.getsizeof(my_set) # размер переменной в байтах 1 байт = 8 бит

driver = webdriver.Chrome()
driver.implicitly_wait(100) # ждем столько, если не справился заканчиваем?

driver.get(start_page + '2780610397421000011')
traid_obj = '/html/body/div[2]/div/div[1]/div[3]/div/a[2]'
driver.find_element_by_xpath(traid_obj).click()

row_path = '//*[@id="contract_subjects"]/tbody/tr'

rows = driver.find_elements_by_xpath(row_path)
'''
print('\n\n\n')
for el in rows:
    print([el.text])
print('\n\n\n')
time.sleep(10)

1 вариант:
    прочитать таблицу, посмотреть сколько непустых строк
    если строк больше 10, то найти выбор количества строк на странице
    и нажать "50" пролистать все строки

    если в "td[2]" больше 1 инфы, записать страну происхождения
'''

# Наименование товара (+ страна происхождения Россия: 2 div)
a = '//*[@id="contract_subjects"]/tbody/tr[1]/td[2]/div[1]'
# ОКПД2 и характеристики
b = '//*[@id="contract_subjects"]/tbody/tr[1]/td[3]'
# Тип объекта (прим. Товар)
c = '//*[@id="contract_subjects"]/tbody/tr[1]/td[4]'
# Количество
d = '//*[@id="contract_subjects"]/tbody/tr[1]/td[5]'
# Цена за ед
e = '//*[@id="contract_subjects"]/tbody/tr[1]/td[6]'

def row_pars():
    # Создаем словарь наименований с вложенными словарями
    name_char = {}
    for row_num in [1, 3]:
        # Создаем словарь Наименование - Характеристика
        char_value = {}
        for cell_num in [2, 3, 4, 5, 6]:
            # Создаем словарь Характеристика - Значение
            x_path = f'//*[@id="contract_subjects"]/tbody/tr[{row_num}]/td[{cell_num}]'
            value = driver.find_element_by_xpath(x_path).text

            if cell_num == 2:
                value_list = value.split("\n")
                # Наименование = ключ к словаре
                goods_name = value_list[0]
                if len(value_list) == 2:
                    # характеристика страны
                    value_country = value_list[1].replace('Страна происхождения: ', '')
                    char_value = char_value | {'Country': value_country}
            elif cell_num == 3:
                # характеристика страны ОКПД2
                value_list = value.split("\n")
                if len(value_list) == 3:
                    pass
                    # характеристика КТРУ

                okpd_val = value_list[1]
                char_value = char_value | {'OKPD2': [value]}
            elif cell_num == 4:
                char_value = char_value | {'Type': value}
            elif cell_num == 5:
                char_value = char_value | {'AMOUNT': value}
            elif cell_num == 6:
                char_value = char_value | {'PRICE': value}
        name_char = name_char | {goods_name: char_value}

    for el in name_char:
        print(el)
        for jel in name_char[el]:
            print(jel, name_char[el][jel])



row_pars()
