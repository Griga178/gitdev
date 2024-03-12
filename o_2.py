from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

# from selenium_stealth import stealth

selenium_driver = 'yandexdriver.exe'
service = Service(executable_path = selenium_driver)

options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--incognito")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# driver = webdriver.Chrome(service = service, options = options)
# driver.implicitly_wait(500)


url = 'https://www.ozon.ru/product/imice-kovrik-dlya-myshi-bolshoy-kovrik-dlya-myshi-igrovoy-kover-700x300-s-sshitymi-krayami-i-896067985/'
url = 'https://www.ozon.ru/product/videokarta-afox-geforce-gtx-1050-ti-4-gb-af1050ti-4096d5h2-648951255/'
sh_i = '//*[@id="layoutPage"]/div[1]/div[5]/div/div/div[2]/a'

# driver.get(url)
#
# shop_info = driver.find_element("xpath", sh_i)
# str_shop_url = shop_info.get_attribute("href")
#
# print([str_shop_url])

str_shop_url = 'https://www.ozon.ru/seller/151376/' + '?miniapp=seller_151376'

# driver.get(str_shop_url)


import requests
# cd desktop/myfiles/dev/gitdev

# api_ = 'https://www.ozon.ru/'#api//entrypoint-api.bx/page/json/v2'
# api_ = 'https://www.ozon.ru/api/entrypoint-api.bx/page/json/v2?url=%2Fmodal%2Fshop-in-shop-info%3Fseller_id%3D151376%26page_changed%3Dtrue'
api_ = 'https://www.ozon.ru/api/entrypoint-api.bx/page/json/v2?url=%2Fmodal%2Fshop-in-shop-info%3Fseller_id%3D151376%26page_changed%3Dtrue'
import datetime
import json
# dn = json.dumps({"Date": datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')})
dn = {"Date": datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}

headers_1 = {
    # ':authority': 'www.ozon.ru',
    # ':method': 'GET',
    # ':path': '/api/entrypoint-api.bx/page/json/v2?url=%2Fmodal%2Fshop-in-shop-info%3Fseller_id%3D151376%26page_changed%3Dtrue',
    # ':scheme': 'https',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
    'Cache-Control': 'max-age=0',
    # 'Cookie': '',
    'Sec-Ch-Ua': 'Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122',
    'Sec-Ch-Ua-Mobile':'?0',
    'Sec-Ch-Ua-Platform': "Windows",
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Service-Worker-Navigation-Preload': 'true',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
    }
headers_2 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Sec-Ch-Ua': 'Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122',
    'Sec-Ch-Ua-Mobile':'?0',
    'Sec-Ch-Ua-Platform': "Windows",
    'Service-Worker-Navigation-Preload': 'true',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
}

b = 'https://www.ozon.ru/api/entrypoint-api.bx/page/json/v2?url=%2Fmodal%2Fshop-in-shop-info%3Fseller_id%3D151376%26page_changed%3Dtrue'

# print(headers)
sess = requests.Session()
a = sess.get(b, headers = headers_2)
print(a)
# a = sess.get(api_, headers = headers_1)

print(a.text)
print(a._content)
# print(a._content.encode('utf-8'))
# for k, v in a.__dict__.items():
#     print(k)
#     print(v)
# a = sess.get(api_, headers = headers_1)
# a = sess.get(api_)
# print(a.cookies)
# print(a.headers)
#
# print(a)
# print(a.text)
# import multiprocessing as mp
#
# def get(url):
#     return sess.get(url)
#
# api_usrls = [
#     api_, api_
# ]
# if __name__ == '__main__':
#
#     with mp.Pool(2) as pool:
#         res = pool.map(get, api_usrls)
#         print(res)
