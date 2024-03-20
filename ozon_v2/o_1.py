from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import re
from selenium.common.exceptions import NoSuchElementException
def get_seller_id(link):
    # selenium_driver = 'yandexdriver.exe'

    selenium_driver = '../yandexdriver.exe'
    service = Service(executable_path = selenium_driver)

    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--incognito")
    options.add_argument('--log-level=3')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    cloud_options = {}
    cloud_options["pageLoadStrategy"] = "eager" # eager normal
    options.set_capability('cloud:options', cloud_options)

    sh_i = '//*[@id="layoutPage"]/div[1]/div[5]/div/div/div[2]/a'
    # Попытки найти в другом месте
    sh_i_2 = '//*[@id="layoutPage"]/div[1]/div[6]/div/div[1]/div[2]/div/div/div/div[1]/div/a'
    sh_i_3 = '//*[@data-widget="webCurrentSeller"]//a'

    driver = webdriver.Chrome(service = service, options = options)
    driver.implicitly_wait(5)

    driver.get(link)
    # print(driver.title)
    # import time
    # time.sleep(100)
    try:

        shop_info = driver.find_element("xpath", sh_i)
        print(shop_info)
        str_shop_url = shop_info.get_attribute("href")
        img_tag = shop_info.find_element("xpath", './img')
        str_shop_name = img_tag.get_attribute("alt")

        seller_id = str_shop_url.split('/')[-2]
    except NoSuchElementException:
        seller_id = None
        str_shop_name = None

    title = driver.title
    # print(title)
    try:
        title_v2 = title.split(' купить')[0]
        print(title_v2)
    except:
        title_v2 = None
        print('Title Error', title)

    try:
        price_block = driver.find_element("xpath", '//div[@data-widget="webPrice"]//span').text
        re_price = re.findall('\d+', price_block)
        price = int(''.join(re_price))
        print(price_block)
    except:
        price = None


    driver.close()
    resp_kw = {
        'title': title_v2,
        'company_id': seller_id,
        'brand': str_shop_name,
        'price': price,
    }


    return resp_kw

url = 'https://www.ozon.ru/product/videokarta-afox-geforce-gtx-1050-ti-4-gb-af1050ti-4096d5h2-648951255/'
url_2 = 'https://www.ozon.ru/product/gigabyte-videokarta-geforce-gtx-1050-ti-4-gb-gtx-1050ti-sovershenno-novyy-1442623570/'

# resp_kwa = get_seller_id(url_2)
