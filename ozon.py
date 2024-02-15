from selenium import webdriver
from selenium.webdriver.chrome.options import Options

selenium_driver = 'yandexdriver.exe'

options = Options()
options.add_argument('--ignore-certificate-errors')
# options.add_argument('--headless')
# options.add_argument("--incognito")
# options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("--disable-gpu")
options.add_argument('--log-level=3')
DRIVER = webdriver.Chrome(selenium_driver, options = options)

url2 = 'https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html'

url = 'https://www.ozon.ru/product/imice-kovrik-dlya-myshi-bolshoy-kovrik-dlya-myshi-igrovoy-kover-700x300-s-sshitymi-krayami-i-896067985/'
DRIVER.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    }


# a = DRIVER.get(url)
a = DRIVER.get(url2)


print(a)
