from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from engine_parser_addition import clean_number, clean_text, set_current_date
from engine_beauty_parser import html_searcher

def run_selenium_parser(settings):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging']) # не выводит сообщзения в консоль
    options.add_argument('--headless')
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"

    binary_yandex_driver_file = 'yandexdriver.exe'

    headless_mode = settings['headless_mode']

    if not headless_mode:
        options.headless = False

    driver = webdriver.Chrome(binary_yandex_driver_file, desired_capabilities = caps, options = options)
    # driver = webdriver.Chrome(desired_capabilities = caps, options = options)

    dict_output = {}
    for link_id, link in settings['links'].items():
        link_result = {}
        tag_setting = settings['tag_setting']
        try:
            driver.get(link)
            html_page = driver.page_source
            link_result = html_searcher(tag_setting, html_page)
        except:
            dict_output[link_id] = False
            break
        dict_output[link_id] = link_result

    driver.quit()

    return dict_output
