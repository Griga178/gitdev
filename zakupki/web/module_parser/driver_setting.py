from settings import selenium_driver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_driver():

    options = Options()
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--headless')
    options.add_argument("--disable-gpu")
    options.add_argument('--log-level=3')
    DRIVER = webdriver.Chrome(selenium_driver, options = options)
    DRIVER.implicitly_wait(100)

    DRIVER.get('https://zakupki.gov.ru/epz/contract/search/results.html')

    return DRIVER
