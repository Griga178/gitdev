import sys
import time
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from lxml import etree, html

start_time = time.time()

'''
Задача, по списку номеров контрактов пропарсить сайт закупок
вытащить из контракта имя закупаемого товара, цену и ОКПД2

{number: {[okpd, name, price], [okpd, name, price]...}...}
'''


pkl_file_name = '../sql/contra/2021kontr9.pkl'

start_page = 'https://zakupki.gov.ru/epz/contract/contractCard/common-info.html?reestrNumber='

number_set = {'2781404664921000005', '2780610397421000011', '2781930090921000019', '2780210944621000200', '2246503513721000464'}

def pkl_set_reader(file_name):
    with open(file_name, 'rb') as f:
        pickle_set = pickle.load(f)
    return pickle_set

def string_to_float(value):
    float_number = []
    reg_numb = ''
    for el in value:
        if el in {'1', '2', '3', '4', '5', '6', '7', '8','9', '0', ',', '.'}:
            float_number.append(el)
    if float_number:
        reg_numb = (''.join(float_number)).replace(',', '.')
        return float(reg_numb)
    else:
        return value

def print_table(full_dict):
    count = 0
    for number in full_dict:
        print(number)
        list_name_char = full_dict[number]
        count += len(list_name_char)
        for dict_in_list in list_name_char:
            #print(el)
            for dict_key in dict_in_list:
                print(dict_key)
                for char in dict_in_list[dict_key]:
                    print(char, '- - -', dict_in_list[dict_key][char])
    print(f'\n\nВсего товаров {count} шт.\n')

def okpd_ktru_values(content):
    # разделение ячейки ОКПД КТРУ на 2 кода
    first_list = content.split(')')
    if len(first_list) == 3:
        # если в ячейке два кода
        first_string = first_list[0].split('(')
        second_string = first_list[1].split('(')
        first_code = first_string[1].strip()
        second_code = second_string[1].strip()
        content = [first_code, second_code]
    elif len(first_list) == 2:
        first_string = first_list[0].split('(')
        first_code = first_string[1].strip()
        content = [first_code]
    code_dict = {}
    for code in content:
        if '-' in code:
            code_dict = code_dict | {'КТРУ': code}
        else:
            code_dict = code_dict | {'ОКПД2': code}
    return code_dict

def clear_cell(dirty_td):
    content = dirty_td.text_content().strip()
    if '\n' in content:
        content = ' '.join(content.replace('\n', '').split())
    if "\xa0" in content:
        content = content.replace('\xa0', '')
    return content

def table_pars_two():
    # Создаем список наименований с вложенными словарями
    list_name_char = []
    # адрес таблицы
    full_page_path = '//*[@id="contractSubjects"]/div/div/div/div[1]/table/tbody'
    table_pars_code = driver.find_element_by_xpath(full_page_path).get_attribute("outerHTML")
    # все строки таблицы
    rows = html.fromstring(table_pars_code).xpath('//tr/td')
    # Создаем словарь Наименование - Характеристика
    char_value = {}

    count = 0
    for cell in rows:

        count += 1

        if count == 1:
            pass
        elif count == 2:
            name_of_good = clear_cell(cell)
            if 'Страна происхождения' in name_of_good:
                value_list = name_of_good.split('Страна происхождения')
                goods_name = value_list[0].strip()
                country = value_list[1].replace(':', '').strip()
                code_dict = {'Страна происхождения': country}
                char_value = char_value | code_dict
                #print(goods_name)
                #print(code_dict)
            else:
                #print("Наименование:", name_of_good)
                goods_name = name_of_good
        elif count == 3:
            # добавляем в словарь коды ОКПД2 и КТРУ если есть
            content = clear_cell(cell)
            dict_content = okpd_ktru_values(content)
            code_of_good = content.split(')')
            #print(dict_content)
            char_value = char_value | dict_content
        elif count == 4:
            # Добавляем тип Объекта
            content = clear_cell(cell)
            char_value = char_value | {'Тип объекта': content}
            #print({'Тип объекта': content})
        elif count == 5:
            # Добавляем количество и ед изм
            content = clear_cell(cell)
            content = content.split()
            if len(content) == 2:
                measure = content[-1]
                amount = string_to_float(content[0])
                cont_dict = {"Количество": amount, "ЕД. ИЗМ.": measure}
            else:
                cont_dict = {"Количество": float(1), "Количество, ЕД. ИЗМ.": ' '.join(content)}
            #print(cont_dict)
            char_value = char_value | cont_dict
        elif count == 6:
            # Добавляем Цена за единицу
            content = clear_cell(cell)
            cont_dict = {"Цена за единицу": string_to_float(content)}
            char_value = char_value | cont_dict
            #print(cont_dict)
        elif count == 7:
            # Добавляем сумму и ставку НДС
            content = clear_cell(cell)
            content = content.split("Ставка НДС:")
            value_nds = content[-1].strip()
            value_sum = string_to_float(content[0])
            cont_dict = {"Сумма": value_sum, "Ставка НДС": value_nds}
            char_value = char_value | cont_dict
            #print(cont_dict)

        elif count == 8:
            # пустая ячейка
            pass

        elif count == 9:
            #if len(cell):
            content = clear_cell(cell)
            if 'Страна происхождения' in content:
                country = content.split('Страна происхождения')[-1].strip()
                code_dict = {'Страна происхождения': country}
                #print(code_dict)
                char_value = char_value | cont_dict
            count = 0
            list_name_char.append({goods_name: char_value})
            char_value = {}
            #print('\n')

    return list_name_char

def full_page_pars():
    list_full_table = []
    goods_count = 0
    pars_pages_stat = 0
    # адрес количества страниц
    row_page_nambers = '//*[@id="contractSubjectSearchPositionNavigation"]/ul/li'
    # текущая страница
    current_p_path = '//*[@id="contractSubjectSearchPositionNavigation"]/ul/li[@class="page active"]'
    # список номеров страниц, может быть пустым
    some_list = driver.find_elements_by_xpath(row_page_nambers)
    # номер последней страницы
    if len(some_list) > 2:
        # показываем 50 товаров на странице
        count_xpath = '//*[@id="contractSubjects"]/div/div/div/div[2]/div[2]/div/div[2]/div[1]/span'
        numb_xpath = '//*[@id="_50"]'
        driver.find_element_by_xpath(count_xpath).click()
        driver.find_element_by_xpath(numb_xpath).click()
        time.sleep(3)
        some_list = driver.find_elements_by_xpath(row_page_nambers)

    if len(some_list) > 2:
        last_page = int(some_list[-2].text)
        # Если страниц > 1
        while pars_pages_stat == 0:
            list_full_table += table_pars_two()
            current_page = int(driver.find_element_by_xpath(current_p_path).text)
            if current_page == last_page:
                pars_pages_stat = 1
            else:
                some_list = driver.find_elements_by_xpath(row_page_nambers)
                some_list[-1].click()
                time.sleep(1)
    else:
        list_full_table = table_pars_two()
    goods_count += len(list_full_table)
    print(f'Записано товаров: {goods_count}')
    return tuple(list_full_table)

#set_size = sys.getsizeof(my_set) # размер переменной в байтах 1 байт = 8 бит

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options = options)
#driver = webdriver.Firefox()
driver.implicitly_wait(100) # ждем столько, если не справился заканчиваем?

# Слоаварь, который надо сохранить
current_dict = {}
# счетчик контрактов
number_counter = 0
# множество отпарсиных контрактов
parsed_set = set()


for gov_number in number_set:
    #print(f'\nПарсим контракт № "{gov_number}"')
    current_link = start_page + gov_number
    # переходим на страницу контракта
    driver.get(current_link)
    # на страницу товаров
    goods_link = '/html/body/div[2]/div/div[1]/div[3]/div/a[2]'
    driver.find_element_by_xpath(goods_link).click()
    # настраиваем и парсим + добавляем в общий словарь
    current_dict |= {gov_number: full_page_pars()}
    # добавить номер контракта в parsed_set
    # счетчик контрактов если 500 то сохранить в pkl + если ошибка то сохранить в pkl

print_table(current_dict)

driver.close()
cur_sec = round((time.time() - start_time), 2)
print(f'Вревмя выполнения: {int(cur_sec // 60)} мин. {cur_sec} сек.)')
