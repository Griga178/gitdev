from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import requests
from bs4 import BeautifulSoup



from datetime import date

from engine_parser_addition import clean_number
# import time
# start_time = time.time()

# ОТПАРСИТЬ ЦЕНУ, НАЗВАНИЕ, ХАРАКТЕРИСТИКИ
''' МОДУЛЬ НА ВХОД ПОЛУЧАЕТ (1 магазин):

    {"links":{1: link, 2: link2},
    "price": {"tag_name": x, "attr_name" y, "attr_value": z},
    "name": {"tag_name": x, "attr_name" y, "attr_value": z},
    "chars": {"tag_name": x, "attr_name" y, "attr_value": z},
    "request_tool": "py_requests"}
    + прочее: "main_page_id":..., "main_page":...

    ВОЗВРАЩАЕТ:

    {1: {"current_price": 10000,
    "current_name": iphone 3gs 32gb white,
    "current_chars": "***Пока не парсим***",
    "current_date": 11/05/2022},
    2: {"current_price": 15000,
    "current_name": iphone 4g 16gb black,
    "current_chars": "***Пока не парсим***"}}
    '''

# options = Options()
# + Строка 115

options = webdriver.ChromeOptions()
binary_yandex_driver_file = 'yandexdriver.exe'


options.add_experimental_option('excludeSwitches', ['enable-logging']) # не выводит сообщзения в консоль
options.add_argument('--headless')

# не ждем полной загрузки JS
caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager"

# link = 'https://www.citilink.ru/product/ibp-powercom-spider-spd-1000n-1000va-332717/?text=Powercom+SPD-1000N'
# link2 = 'https://www.citilink.ru/product/ibp-powercom-raptor-rpt-1000a-euro-1000va-859787/'
# link3 = 'https://www.komus.ru/katalog/produkty-pitaniya/molochnaya-produktsiya/moloko/moloko-ekoniva-ultrapasterizovannoe-3-2-1-l/p/1004358/?from=block-301-1'


# Получаем отрисованную страницу
def take_html_page(link, we_need_selenium = True, driver = False): # py_selenium py_requests
    if we_need_selenium:
        try:
            current_request = requests.get(link)
            html_string = current_request.text
        except:
            print('\npy_requests - html not found')
            html_string = False
    else:
        driver.get(link)
        try:
            html_string = driver.page_source
        except:
            print('\npy_selenium - html not found')
            html_string = False
    return html_string

# ищем инфу по 3 параметрам: tag, attribute, attribute value через BF
def seerch_info_by_param(html_string_page, tag_param):

    try:
        soup = BeautifulSoup(html_string_page, 'html.parser')
        result_info = soup.find(tag_param['tag_name'], attrs = {tag_param['attr_name']: tag_param['attr_val']})
        print(result_info)
        print(result_info.text)
        if not result_info:
            print(result_info)
            return False
        else:
            return result_info.text
    except:
        print("\nОшибка: поиск инфы по тегам")
        print(f"\nТеги: {tag_param}")
        print("\nresult_info")



def shop_parser(input_dict):
    output_dict = {}
    output_dict['new_parse'] = True
    output_dict['main_page_id'] = input_dict['shop_id']
    output_dict['main_page'] = input_dict['shop_name']
    output_dict['http_link'] = input_dict['link']
    output_dict['link_id'] = input_dict['link_id']
    today = date.today()
    current_date = today.strftime("%d/%m/%Y")
    # Что ищем на странице
    tag_types = ["price", "name"] #, "chars"
    # Список ссылок
    # parse_links = input_dict["links"]
    # Каким инструментом достаем html страницу с сервера
    we_need_selenium = input_dict["need_selenium"]
    driver = False
    if we_need_selenium:
        # driver = webdriver.Chrome(desired_capabilities = caps, options = options)
        driver = webdriver.Chrome(binary_yandex_driver_file, desired_capabilities = caps, options = options)

    html_string_page = take_html_page(input_dict["link"], we_need_selenium, driver)

    output_dict["current_date"] = current_date
    if html_string_page:
        for tag_type in tag_types:
            if not input_dict[tag_type]:
                parse_info = "Нет настроек"
                print(f'\n{tag_type} НЕ Парсим {parse_info}')
            else:
                print(f'\nПАрсим   {tag_type}')
                parse_info = seerch_info_by_param(html_string_page, input_dict[tag_type])
                print(parse_info)
                if parse_info:
                    if tag_type == "price":
                        parse_info = clean_number(parse_info)
                        print('Чистим цену', parse_info)
                    elif tag_type == "name":
                        parse_info = " ".join(parse_info.split())
                        print('Чистим имя', parse_info)
                    elif tag_type == "chars":
                        parse_info = "Не готов парсер"
                    output_dict[f'current_{tag_type}'] = parse_info
                    print('\nСЛОВАРЬ', output_dict)
                else:
                    output_dict[f'current_{tag_type}'] = False
    if we_need_selenium:
        driver.quit()
    return output_dict

# example_input_dict = {
#     'link_id': 310, 'link': 'https://www.citilink.ru/product/ibp-powercom-spider-spd-1000n-1000va-332717/?text=Powercom+SPD-1000N',
#     'shop_id': 4, 'shop_name': 'www.citilink.ru', 'current_price': None, 'need_selenium': True,
#     'price': {'tag_id': 13, 'tag_name': 'span', 'attr_name': 'class', 'attr_val': 'ProductHeader__price-default_current-price', 'shop_id': 4, 'tag_type': 'price', 'rus_tag': 'Цена'},
#     'name': {'tag_id': 29, 'tag_name': 'h1', 'attr_name': 'class', 'attr_val': 'ProductHeader__title', 'shop_id': 4, 'tag_type': 'name', 'rus_tag': 'Название'},
#     'chars': {'tag_id': 41, 'tag_name': 'test', 'attr_name': 'test', 'attr_val': 'test2', 'shop_id': 4, 'tag_type': 'chars', 'rus_tag': 'Характеристика'}}
#
# result = shop_parser(example_input_dict)
# print(result)


# cur_sec = round((time.time() - start_time), 2)
# print(f'\nВремя выполнения парсинга: {int(cur_sec // 60)} мин. {cur_sec} сек.\n')
