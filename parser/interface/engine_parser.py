from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import requests
from bs4 import BeautifulSoup

import re

from datetime import date

# import time
# start_time = time.time()

# ОТПАРСИТЬ ЦЕНУ, НАЗВАНИЕ, ХАРАКТЕРИСТИКИ
''' МОДУЛЬ НА ВХОД ПОЛУЧАЕТ (1 магазин):

    {"links":{1: link, 2: link2},
    "price": {"tag_name": x, "attr_name" y, "attr_value": z},
    "name": {"tag_name": x, "attr_name" y, "attr_value": z},
    "chars": {"tag_name": x, "attr_name" y, "attr_value": z},
    "request_tool": "py_requests"}

    ВОЗВРАЩАЕТ:

    {1: {"current_price": 10000,
    "current_name": iphone 3gs 32gb white,
    "current_chars": "***Пока не парсим***",
    "current_date": 11/05/2022},
    2: {"current_price": 15000,
    "current_name": iphone 4g 16gb black,
    "current_chars": "***Пока не парсим***"}}
    '''

options = Options()

options.add_experimental_option('excludeSwitches', ['enable-logging']) # не выводит сообщзения в консоль
options.add_argument('--headless')

# не ждем полной загрузки JS
caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager"

link = 'https://www.citilink.ru/product/ibp-powercom-spider-spd-1000n-1000va-332717/?text=Powercom+SPD-1000N'
link2 = 'https://www.citilink.ru/product/ibp-powercom-raptor-rpt-1000a-euro-1000va-859787/'


# если на странице нет JS, то просто request, иначе - selenium
input_dict = {
"links":{1: link, 2: link2},
"price": {"tag_name": "span", "attr_name": "class", "attr_value": "ProductHeader__price-default_current-price"},
"name": {"tag_name": "h1", "attr_name": "class", "attr_value": "ProductHeader__title"},
"request_tool": "py_requests"
}

# Получаем отрисованную страницу
def take_html_page(link, request_tool = "py_selenium", driver = False):
    if request_tool == "py_requests":
        try:
            current_request = requests.get(link)
            html_string = current_request.text
        except:
            print('\npy_requests - html not found')
            html_string = False
    elif request_tool == "py_selenium":
        driver.get(link)
        try:
            html_string = driver.page_source
        except:
            print('\npy_selenium - html not found')
            html_string = False
    return html_string

# ищем инфу по 3 параметрам: tag, attribute, attribute value через BF
def seerch_info_by_param(html_string_page, tag_param):
    soup = BeautifulSoup(html_string_page, 'html.parser')
    result_info = soup.find(tag_param['tag_name'], {tag_param['attr_name'], tag_param['attr_value']})
    if not result_info:
        re_sult = "Не удалось найти теги"
    else:
        re_sult = result_info.string
    return re_sult

def clean_number(str_text):
    ''' Выводит только числа из строк с помощью регулярок
        находит числа, в которых "." или "," используется
        только для копеек'''
    result = re.findall(r'\d+\.?\,?', str_text)

    clear_number = ''.join(result)

    if ',' in clear_number:
        clear_number = clear_number.replace(',', '.')
    try:
        clear_number = float(clear_number)
        return clear_number
    except:
        clear_number = f"!Не преобразовать в число:{str_text}"
        return clear_number

def shop_parser(input_dict):
    output_dict = {}
    today = date.today()
    current_date = today.strftime("%d/%m/%Y")
    # Что ищем на странице
    tag_types = ["price", "name", "chars"]
    # Список ссылок
    parse_links = input_dict["links"]
    # Каким инструментом достаем html страницу с сервера
    request_tool = input_dict["request_tool"]
    driver = False
    if request_tool == "py_selenium":
        driver = webdriver.Chrome(desired_capabilities = caps, options = options)

    for link in parse_links:
        # Получаем html страницу
        html_string_page = take_html_page(parse_links[link], request_tool, driver)
        output_dict[link] = {}
        output_dict[link]["current_date"] = current_date
        if html_string_page:
            for tag_type in tag_types:
                if tag_type not in input_dict:
                    parse_info = "Нет настроек"
                else:
                    parse_info = seerch_info_by_param(html_string_page, input_dict[tag_type])

                    if tag_type == "price":
                        parse_info = clean_number(parse_info)
                    elif tag_type == "name":
                        parse_info = " ".join(parse_info.split())
                    elif tag_type == "chars":
                        parse_info = "Не готов парсер"
                    output_dict[link][f'current_{tag_type}'] = parse_info

    if request_tool == "py_selenium":
        driver.quit()
    return output_dict

# result = shop_parser(input_dict)
# print(result)


# cur_sec = round((time.time() - start_time), 2)
# print(f'\nВремя выполнения парсинга: {int(cur_sec // 60)} мин. {cur_sec} сек.\n')
