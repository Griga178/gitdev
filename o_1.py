from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def get_seller_id(link):
    selenium_driver = 'yandexdriver.exe'
    service = Service(executable_path = selenium_driver)

    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--incognito")
    options.add_argument('--log-level=3')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    sh_i = '//*[@id="layoutPage"]/div[1]/div[5]/div/div/div[2]/a'

    driver = webdriver.Chrome(service = service, options = options)
    driver.implicitly_wait(10)

    driver.get(link)
    shop_info = driver.find_element("xpath", sh_i)
    str_shop_url = shop_info.get_attribute("href")
    img_tag = shop_info.find_element("xpath", './img')
    str_shop_name = img_tag.get_attribute("alt")

    # print([shop_info])
    # print([str_shop_url])
    seller_id = str_shop_url.split('/')[-2]
    # print(seller_id)
    # print(str_shop_name)
    print(driver.title)
    driver.close()


    return seller_id, str_shop_name

url = 'https://www.ozon.ru/product/videokarta-afox-geforce-gtx-1050-ti-4-gb-af1050ti-4096d5h2-648951255/'
url_2 = 'https://www.ozon.ru/product/gigabyte-videokarta-geforce-gtx-1050-ti-4-gb-gtx-1050ti-sovershenno-novyy-1442623570/'
# seller_id, company_name_1 = get_seller_id(url)
# get_seller_id(url_2)
