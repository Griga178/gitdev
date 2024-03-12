from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By

def get_name_ogrn(seller_id):

    selenium_driver = 'yandexdriver.exe'
    service = Service(executable_path = selenium_driver)

    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--incognito")
    options.add_argument('--log-level=3')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)


    api_ = f'https://www.ozon.ru/api/entrypoint-api.bx/page/json/v2?url=%2Fmodal%2Fshop-in-shop-info%3Fseller_id%3D{seller_id}%26page_changed%3Dtrue'

    driver = webdriver.Chrome(service = service, options = options)
    driver.implicitly_wait(10)

    driver.get(api_)

    time.sleep(2)

    # content = driver.find_element_by_tag_name('body')
    content = driver.find_element(By.TAG_NAME, 'pre')

    # content = driver.page_source

    # print(content.text)

    import json

    y = json.loads(content.text)

    # print(y)
    # for key,val in y.items():
    #     print(key,val)

    # print((y['textAtom']))
    widgetStates = y['widgetStates']

    comp_name = False
    for key, val in widgetStates.items():
        if 'textBlock' in key:
            # print(key)
            # print([val])
            z = json.loads(val)
            z_type = z['body'][0]['type']
            z_cont = z['body'][0][z_type]
            z_str = z_cont['text']
            if z_str != 'О магазине':
                split_content = z_str.split('<br>')
                if len(split_content) == 1:
                    comp_name = split_content[0]
                elif len(split_content) == 2:
                    comp_name = split_content[0]
                    if len(split_content[1]) == 13:
                        c_ogrn = split_content[1]
                        c_address = None
                    else:
                        c_ogrn = None
                        c_address = split_content[1]


                elif len(split_content) == 3:
                    comp_name = split_content[0]
                    if len(split_content[1]) == 13:
                        c_ogrn = split_content[1]
                        c_address = split_content[2]
                    else:
                        c_ogrn = split_content[2]
                        c_address = split_content[1]
                else:
                    comp_name = z_str
                    c_address = 'error'
                    c_ogrn = 'error'
    if comp_name:
        # print(comp_name, c_address, c_ogrn)
        # print(widgetStates = y['widgetStates'])
        return comp_name, c_address, c_ogrn
    else:
        print(widgetStates = y['widgetStates'])
        return None, None, None


# get_name_ogrn('1826')
# get_name_ogrn('1387675')
# get_name_ogrn('1338131')
