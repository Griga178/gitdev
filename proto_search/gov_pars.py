import sys
import time
import pickle
from selenium import webdriver

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

def table_pars():
    # Создаем список наименований с вложенными словарями
    list_name_char = []
    row_range = 0
    number_g = 0
    row_path = '//*[@id="contract_subjects"]/tbody/tr'
    list_of_rows = driver.find_elements_by_xpath(row_path)
    row_range = len(list_of_rows)
    for row_num in range(1, row_range, 2):
        number_g += 1
        # Создаем словарь Наименование - Характеристика
        char_value = {}
        for cell_num in [2, 3, 4, 5, 6]:
            # Создаем словарь Характеристика - Значение;
            #   список словарей: имя товара характеристики
            x_path = f'//*[@id="contract_subjects"]/tbody/tr[{row_num}]/td[{cell_num}]'
            value = driver.find_element_by_xpath(x_path).text

            if cell_num == 2:
                # Наименование товара (+ страна происхождения Россия: 2 div)
                value_list = value.split("\n")
                # Наименование = ключ к словаре
                goods_name = value_list[0]
                if len(value_list) == 2:
                    # характеристика страны
                    value_country = value_list[1].replace('Страна происхождения: ', '')
                    char_value = char_value | {'Country': value_country}

            elif cell_num == 3:
                # ОКПД2 и КТРУ (ВОЗМОЖНО)
                value_list = value.split("\n")
                if len(value_list) == 3:
                    # характеристика КТРУ
                    ktru_val = value_list[1].replace('(', '').replace(')', '')
                    char_value = char_value | {'KTRU': ktru_val}
                okpd_val = value_list[-1].replace('(', '').replace(')', '')
                char_value = char_value | {'OKPD2': okpd_val}

            elif cell_num == 4:
                # Тип объекта (прим. Товар)
                char_value = char_value | {'Type': value}

            elif cell_num == 5:
                # Количество
                '''
                amount_val = []
                for el in value:
                    if el in {'1', '2', '3', '4', '5', '6', '7', '8','9', '0'}:
                        amount_val.append(el)
                '''
                try:
                    char_value = char_value | {'Amount': string_to_float(value)} #''.join(amount_val)
                except:
                    char_value = char_value | {'Amount': value}
                    print('\n\n', [value], 'ВНИМАНИИЕЕЕ\n\n')

            elif cell_num == 6:
                # Цена за ед
                char_value = char_value | {'Price': float(value.replace(',', '.').replace(' ', ''))}

        # Упаковываем словари в список
        list_name_char.append({goods_name: char_value})
        #print(number_g, goods_name)

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
            list_full_table += table_pars()
            current_page = int(driver.find_element_by_xpath(current_p_path).text)
            if current_page == last_page:
                pars_pages_stat = 1
            else:
                some_list = driver.find_elements_by_xpath(row_page_nambers)
                some_list[-1].click()
                time.sleep(1)
    else:
        list_full_table = table_pars()
    goods_count += len(list_full_table)
    #print(f'Записано товаров: {goods_count}')
    return tuple(list_full_table)

#set_size = sys.getsizeof(my_set) # размер переменной в байтах 1 байт = 8 бит

driver = webdriver.Chrome()
driver.implicitly_wait(100) # ждем столько, если не справился заканчиваем?

current_dict = {}

for gov_number in number_set:
    #print(f'\nПарсим контракт № "{gov_number}"')
    current_link = start_page + gov_number
    driver.get(current_link)
    goods_link = '/html/body/div[2]/div/div[1]/div[3]/div/a[2]'
    driver.find_element_by_xpath(goods_link).click()
    current_dict |= {gov_number: full_page_pars()}

print_table(current_dict)

driver.close()
cur_sec = round((time.time() - start_time), 2)
print(f'Вревмя выполнения: {int(cur_sec // 60)} мин. {cur_sec} сек.)')
