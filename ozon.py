'''
https://codeby.net/threads/metody-obxoda-zaschity-ot-avtomatizirovannogo-po-v-brauzere-chrome-pod-upravleniem-selenium-v-python.81358/

pip install undetected-chromedriver

pip install selenium selenium-stealth
'''
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium_stealth import stealth

links = [
    'https://www.ozon.ru/product/kovrik-dlya-myshi-bmg-battlegrounds-bayk-h8-kv60-raznotsvetnyy-610072082/',
    'https://www.ozon.ru/product/onkron-potolochno-nastennyy-kronshteyn-dlya-proektora-belyy-k5a-148044023/',
    'https://www.ozon.ru/product/kronshteyn-dlya-proektora-holder-pr-103-b-chernyy-nagruzka-20-kg-potolochnyy-povorot-i-naklon-298763-823827163/',
    'https://www.ozon.ru/product/kronshteyn-dlya-proektora-wize-wpb-s-serebristyy-nagruzka-12-kg-potolochnyy-povorot-i-naklon-1515273-823826930/',
    'https://www.ozon.ru/product/kreplenie-dlya-proektora-nastennoe-potolochnoe-naklonno-povorotnoe-uniteki-pm2102b-1074657667/',
    'https://www.ozon.ru/product/videokarta-sinotex-geforce-gtx-750-ti-2-gb-nh75ti025f-rev-1-0-268920858/',
    'https://www.ozon.ru/product/videokarta-afox-geforce-gtx-1050-ti-4-gb-af1050ti-4096d5h2-648951255/',
    'https://www.ozon.ru/product/videokarta-geforce-rtx-2070-8-gb-nvidia-geforce-rtx-2070-lhr-1080444698/',
]

selenium_driver = 'yandexdriver.exe'
service = Service(executable_path = selenium_driver)

options = Options()
options.add_argument('--ignore-certificate-errors')
# options.add_argument('--headless')
# options.add_argument("--incognito")
# options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
# options.add_argument("--disable-gpu")
options.add_argument('--log-level=3')

driver = webdriver.Chrome(service = service, options = options)

# driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#     'source': '''
#         delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
#         delete window.cdc_adoQpoasnfa76pfcZLmcfl_JSON
#         delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object
#         delete window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy
#         delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
#         delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
#   '''
# })



# stealth(driver=driver,
#         user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
#                    'Chrome/83.0.4103.53 Safari/537.36',
#         languages=["ru-RU", "ru"],
#         vendor="Google Inc.",
#         platform="Win32",
#         webgl_vendor="Intel Inc.",
#         renderer="Intel Iris OpenGL Engine",
#         fix_hairline=True,
#         run_on_insecure_origins=True,
#         )



url = 'https://www.ozon.ru/product/imice-kovrik-dlya-myshi-bolshoy-kovrik-dlya-myshi-igrovoy-kover-700x300-s-sshitymi-krayami-i-896067985/'
# driver.headers = {
#     'User-Agent': 'Mozilla/6.0 (Windows NT 10.0; Win64; x64)',
#     }


# a = DRIVER.get(url)
import time
for el in links[:2]:
    driver.get(el)
    time.sleep(4)

# print(a)
