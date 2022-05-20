'''
ПАРСЕР ЗАГРУЗИТЬ В ПРОЕКТ, "СОЕДИНИТЬ" С МОДУЛЯМИ
ТУТ ОСТАВИТЬ ФУНКЦИИ ТЕСТА
'''


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import requests
from bs4 import BeautifulSoup

import time

from engine_parser_addition import clean_number, clean_text
from parser_test_examples import *

def load_html_by_selen(defender = False, headless_mode = True, link = False, title = False):

    options = webdriver.ChromeOptions()
    binary_yandex_driver_file = 'yandexdriver.exe'

    options.add_experimental_option('excludeSwitches', ['enable-logging']) # не выводит сообщзения в консоль
    options.add_argument('--headless')

    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"


    if not headless_mode:
        options.headless = False

    driver = webdriver.Chrome(binary_yandex_driver_file, desired_capabilities = caps, options = options)
    # driver = webdriver.Chrome(desired_capabilities = caps, options = options)

    driver.get(link)

    attr_value = title["attr_val"]
    child_xpath = f'//{title["tag"]}[contains(@{title["attr"]}, "{attr_value}")]'
    try:
        # print('попытка парсинга')
        wait_elm = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, child_xpath)))
        html_page = driver.page_source
    except:
        # print('Неудачный парс')
        if defender:
            try:
                attr_value = defender['attr_val']
                def_xpath = f'//{defender["tag"]}[text() = "{attr_value}"]'
                def_wait_elm = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, def_xpath)))
                # ЕСЛИ НЕТ ОШИБКИ, ЗНАЧИТ ЗАПУСТИЛСЯ ЗАЩИТНИК
                # print('Перезапускаем драйвер')
                html_page = load_html_by_selen(headless_mode = False, link = link, title = title)
            except:
                print("Не удалось определить защитник")

    driver.quit()
    # print('Возвращаем странцу')
    return html_page

def pretty_print(dict_output):
        if dict_output['current_name']:
            first_str = dict_output['current_name']
        else:
            first_str = f'Ошибка имени: {dict_output["name_message"]}'

        if dict_output['current_price']:
            second_str = dict_output['current_price']
        else:
            second_str = f'Ошибка цены: {dict_output["price_message"]}'

        print(first_str)
        print(second_str)

def parser(settings):
    dict_output = {}

    if settings['need_selenium']:
        # print('\nзапускаем селениум')
        if settings['defender_message']:
            # print('защитник есть')
            if not settings['headless_mode']:
                html_page = load_html_by_selen(defender = settings['defender_message'], link = settings['http_link'], title = settings['price'], headless_mode = False)
            else:
                html_page = load_html_by_selen(defender = settings['defender_message'], link = settings['http_link'], title = settings['price'])
        else:
            # print('защитника нет')
            html_page = load_html_by_selen( link = settings['http_link'])
    else:
        # достаем страницу из request
        re_t =  requests.get(settings['http_link'])
        html_page = re_t.text

    # на странице есть желаемая инфа?
    desired_info = {'price': clean_number, 'name': clean_text}
    soup = BeautifulSoup(html_page, 'html.parser')

    # проверяем
    for type in desired_info:
        dict_output[f'current_{type}'] = False
        dict_output[f'{type}_message'] = False
        title = settings[type]
        if title:
            # ЖЕЛАЕМЫЙ тип инфы:
            result_info = soup.find(title['tag'], attrs = {title['attr']: title['attr_val']})
            if result_info != None:
                # ИНФА НАЙДЕНА - ЗАПИСЬ
                dict_output[f'current_{type}'] = desired_info[type](result_info.text)
            else:
                # инфы нет
                # проверяем сообщение о наличе товара
                if settings['sold_out_tag'] and settings['sold_out_mes']:
                    title = settings['sold_out_tag']
                    message = settings['sold_out_mes']
                    result_info = soup.find(title['tag'], attrs = {title['attr']: title['attr_val']})
                    if result_info != None:
                        if message in result_info.text:
                            dict_output['price_message'] = False
                            dict_output[f'{type}_message'] = 'Нет в наличии'
                else:
                    dict_output[f'current_{type}'] = False
                    dict_output[f'{type}_message'] = f'Настройки "{type}" не подходят'


        else:
            # В СЛОВАРЕ НЕ УСТАНОВЛЕНЫ НАСТРОЙКИ ЖЕЛАЕМОГО ТИПА
            dict_output[f'{type}_message'] = f'Нет настроек "{type}"'

        # Сообщение "страница не успела загрузиться" - ?
        # ДЕЛАЕМ СКРИНШОТ
        # ЗАПИСЫВАЕМ ССЫЛКУ С ОШИБКОВ В БД
        # Сообщение "страница не найдена" - есть теги

    # return dict_output
    pretty_print(dict_output)


def launch_test():
    num = 0
    start_time = time.time()

    print('# 1')
    parser(settings_dict_1)
    print('# 2')
    parser(settings_dict_2)

    print('# 3')
    parser(settings_dict_3)
    print('# 4')
    parser(settings_dict_4)

    print('# 5')
    parser(settings_dict_5)


    cur_sec = round((time.time() - start_time), 2)
    print(f'\nВревмя выполнения: {int(cur_sec // 60)} мин. {cur_sec} сек.)')

launch_test()
